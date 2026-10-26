"""Frappe adapter: Sales Invoice -> Moadian payload. Sending: erpnext_iran.moadian.sender."""

from zoneinfo import ZoneInfo

import frappe
from frappe import _
from frappe.model.naming import getseries
from frappe.utils import get_datetime, get_system_timezone

from erpnext_iran.moadian.payload import build_payload, compute_invoice_lines, validate_payload
from erpnext_iran.moadian.taxid import generate_tax_id
from erpnext_iran.utils.settings import get_settings


def invoice_timestamp(doc):
	dt = get_datetime(f"{doc.posting_date} {doc.posting_time or '00:00:00'}")
	return dt.replace(tzinfo=ZoneInfo(get_system_timezone())).timestamp()


def get_memory_id(company):
	return frappe.db.get_value("Company", company, "ir_moadian_memory_id") or get_settings().moadian_memory_id


def assign_tax_id(doc, timestamp=None):
	"""A new tax ID for doc, dated by the invoice (or by timestamp, e.g. for its cancellation)."""
	memory_id = get_memory_id(doc.company)
	if not memory_id:
		frappe.throw(_("Set the Fiscal Memory ID on Company {0} or in Iran Localization Settings").format(doc.company))
	serial = int(getseries(f"IRTAX-{memory_id.upper()}-", 10))
	return generate_tax_id(memory_id, timestamp or invoice_timestamp(doc), serial)


def get_invoice_lines(doc):
	lines = compute_invoice_lines(doc, get_settings().vat_rate)
	unit_codes = {}
	for line, row in zip(lines, doc.items):
		if row.uom not in unit_codes:
			unit_codes[row.uom] = frappe.db.get_value("UOM", row.uom, "ir_moadian_unit_code")
		line["unit_code"] = unit_codes[row.uom]
	return lines


def _party(doctype, name):
	values = frappe.db.get_value(
		doctype, name, ["ir_person_type", "ir_national_id", "ir_economic_code"], as_dict=True
	) or {}
	return {
		"person_type": values.get("ir_person_type"),
		"national_id": values.get("ir_national_id"),
		"economic_code": values.get("ir_economic_code"),
	}


SUBJECT_ORIGINAL, SUBJECT_CORRECTION, SUBJECT_CANCELLATION, SUBJECT_RETURN = 1, 2, 3, 4


def invoice_subject(doc):
	"""(subject, reference tax ID) of a Sales Invoice being submitted.

	A return of an invoice is a return (4) of its tax ID. An amendment of an invoice whose
	Moadian cancellation has not been sent yet is a correction (2) of it instead; any other
	invoice is an original (1)."""
	if doc.is_return and doc.return_against:
		return SUBJECT_RETURN, frappe.db.get_value("Sales Invoice", doc.return_against, "ir_tax_id")
	if doc.amended_from:
		tax_id, status = frappe.db.get_value(
			"Sales Invoice", doc.amended_from, ["ir_tax_id", "ir_moadian_status"]
		) or (None, None)
		if tax_id and status in ("Cancellation Pending", "Cancellation Rejected"):
			return SUBJECT_CORRECTION, tax_id
	return SUBJECT_ORIGINAL, None


def make_payload(doc, cancellation=False):
	"""The invoice's Moadian payload; cancellation=True gives its cancellation (subject 3) instead."""
	seller = _party("Company", doc.company)
	seller["tax_code"] = seller["economic_code"] or seller["national_id"]
	buyer = _party("Customer", doc.customer)
	if doc.customer_address:
		buyer["postal_code"] = frappe.db.get_value("Address", doc.customer_address, "pincode")

	if cancellation:
		subject, tax_id, reference = SUBJECT_CANCELLATION, doc.get("ir_cancel_tax_id"), doc.ir_tax_id
	else:
		subject, tax_id, reference = int(doc.get("ir_invoice_subject") or 1), doc.ir_tax_id, doc.get("ir_reference_tax_id")
		if doc.is_return:  # invoices submitted before subjects were set on submit
			subject = SUBJECT_RETURN
			reference = reference or frappe.db.get_value("Sales Invoice", doc.return_against, "ir_tax_id")

	invoice = {"subject": subject, "paid_amount": abs(doc.base_paid_amount or 0) if doc.is_pos else 0}
	return build_payload(
		invoice,
		seller,
		buyer,
		get_invoice_lines(doc),
		tax_id,
		int(invoice_timestamp(doc) * 1000),
		invoice_type=get_settings().moadian_invoice_type or 1,
		reference_tax_id=reference,
	)


@frappe.whitelist()
def get_moadian_payload(sales_invoice):
	doc = frappe.get_doc("Sales Invoice", sales_invoice)
	doc.check_permission("read")
	payload = make_payload(doc, cancellation=doc.docstatus == 2 and bool(doc.get("ir_cancel_tax_id")))
	return {"payload": payload, "problems": validate_payload(payload)}


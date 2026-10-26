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


def assign_tax_id(doc):
	memory_id = get_memory_id(doc.company)
	if not memory_id:
		frappe.throw(_("Set the Fiscal Memory ID on Company {0} or in Iran Localization Settings").format(doc.company))
	serial = int(getseries(f"IRTAX-{memory_id.upper()}-", 10))
	return generate_tax_id(memory_id, invoice_timestamp(doc), serial)


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


def make_payload(doc):
	seller = _party("Company", doc.company)
	seller["tax_code"] = seller["economic_code"] or seller["national_id"]
	buyer = _party("Customer", doc.customer)
	if doc.customer_address:
		buyer["postal_code"] = frappe.db.get_value("Address", doc.customer_address, "pincode")

	subject = int(doc.get("ir_invoice_subject") or 1)
	reference = None
	if doc.is_return:
		subject = 4
	if doc.is_return and doc.return_against:
		reference = frappe.db.get_value("Sales Invoice", doc.return_against, "ir_tax_id")

	invoice = {"subject": subject, "paid_amount": abs(doc.base_paid_amount or 0) if doc.is_pos else 0}
	return build_payload(
		invoice,
		seller,
		buyer,
		get_invoice_lines(doc),
		doc.ir_tax_id,
		int(invoice_timestamp(doc) * 1000),
		invoice_type=get_settings().moadian_invoice_type or 1,
		reference_tax_id=reference,
	)


@frappe.whitelist()
def get_moadian_payload(sales_invoice):
	doc = frappe.get_doc("Sales Invoice", sales_invoice)
	doc.check_permission("read")
	payload = make_payload(doc)
	return {"payload": payload, "problems": validate_payload(payload)}


"""Send Sales Invoices (and their cancellations) to Moadian and follow their status.

Status on the invoice (ir_moadian_status):
- Pending (has a tax ID, not sent) -> Sent (the organization gave a reference number) ->
  Accepted or Rejected (from the inquiry). A correction or return waits until the invoice it
  refers to is accepted.
- An accepted invoice that is cancelled: Cancellation Pending -> Cancellation Sent -> Cancelled
  or Cancellation Rejected. If it is amended before its cancellation is sent, the amendment goes
  as a correction instead and the invoice becomes Corrected.
Messages from the organization, or why something could not be sent, go to ir_moadian_error.
"""

import frappe
from frappe import _
from frappe.utils import add_to_date, now_datetime

from erpnext_iran.moadian.api import get_memory_id, make_payload
from erpnext_iran.moadian.client import PRODUCTION_URL, MoadianClient, inquiry_outcome
from erpnext_iran.moadian.payload import validate_payload
from erpnext_iran.utils.settings import get_settings

SENDABLE = ("Pending", "Rejected")
CANCEL_SENDABLE = ("Cancellation Pending", "Cancellation Rejected")
# statuses of an invoice that Moadian accepted at some point: corrections and returns can refer to it
WAS_ACCEPTED = ("Accepted", "Corrected", "Cancellation Pending", "Cancellation Sent", "Cancelled", "Cancellation Rejected")
CANCELLATION_GRACE_MINUTES = 30  # time to amend (send a correction) before a cancellation goes out
BATCH = 50


def _read(path, label):
	if not path:
		frappe.throw(_("Set the {0} in Iran Localization Settings").format(_(label)))
	try:
		with open(path) as f:
			return f.read()
	except OSError as e:
		frappe.throw(_("Cannot read the {0} at {1}: {2}").format(_(label), path, e.strerror))


def get_client(company, session=None):
	settings = get_settings()
	memory_id = get_memory_id(company)
	if not memory_id:
		frappe.throw(_("Set the Fiscal Memory ID on Company {0} or in Iran Localization Settings").format(company))
	return MoadianClient(
		memory_id,
		_read(settings.moadian_private_key_path, "Private Key File"),
		_read(settings.moadian_certificate_path, "Certificate File"),
		base_url=settings.moadian_api_url or PRODUCTION_URL,
		session=session,
	)


def _set(name, status=None, error=None, **values):
	values["ir_moadian_error"] = error or ""
	if status:
		values["ir_moadian_status"] = status
	frappe.db.set_value("Sales Invoice", name, values, update_modified=False)


def _packet(doc):
	"""("invoice" | "cancellation", payload), or (None, reason it cannot be sent now)."""
	if doc.docstatus == 2 and doc.ir_moadian_status in CANCEL_SENDABLE and doc.get("ir_cancel_tax_id"):
		return "cancellation", make_payload(doc, cancellation=True)
	if doc.docstatus == 1 and doc.ir_moadian_status in SENDABLE and doc.ir_tax_id:
		payload = make_payload(doc)
		reference = payload["header"].get("irtaxid")
		if reference:
			referenced = frappe.db.get_value("Sales Invoice", {"ir_tax_id": reference}, "ir_moadian_status")
			if referenced not in WAS_ACCEPTED:
				return None, _("Waiting until Moadian accepts the invoice with tax ID {0}").format(reference)
		return "invoice", payload
	return None, None


def send_invoices(names, session=None):
	"""Send the given invoices, or the cancellations of cancelled ones; returns {name: status}."""
	by_company, statuses = {}, {}
	for name in names:
		doc = frappe.get_doc("Sales Invoice", name)
		kind, payload = _packet(doc)
		if not kind:
			if payload:  # a reason
				_set(doc.name, error=payload)
			statuses[doc.name] = doc.ir_moadian_status
			continue
		problems = validate_payload(payload)
		if problems:
			_set(doc.name, error=_("Not sent: {0}").format("; ".join(problems)))
			statuses[doc.name] = doc.ir_moadian_status
			continue
		by_company.setdefault(doc.company, []).append((doc, kind, payload))

	for company, ready in by_company.items():
		try:
			results = get_client(company, session).send_invoices([payload for _doc, _kind, payload in ready])
		except Exception as e:
			frappe.log_error(title=_("Moadian sending failed"), message=frappe.get_traceback())
			for doc, _kind, _payload in ready:
				_set(doc.name, error=_("Not sent: {0}").format(e))
				statuses[doc.name] = doc.ir_moadian_status
			continue
		for (doc, kind, _payload), result in zip(ready, results):
			reference = result.get("referenceNumber")
			if not reference:
				_set(doc.name, error=_("Not sent: {0}").format(frappe.as_json(result.get("data") or result)))
				statuses[doc.name] = doc.ir_moadian_status
			elif kind == "cancellation":
				_set(doc.name, "Cancellation Sent", ir_cancel_reference=reference)
				statuses[doc.name] = "Cancellation Sent"
			else:
				_set(doc.name, "Sent", ir_moadian_reference=reference)
				statuses[doc.name] = "Sent"
	return statuses


def check_status(names=None, session=None):
	"""Ask the organization about sent invoices and cancellations; returns {name: status}."""
	sent = {"docstatus": 1, "ir_moadian_status": "Sent", "ir_moadian_reference": ["is", "set"]}
	cancelling = {"docstatus": 2, "ir_moadian_status": "Cancellation Sent", "ir_cancel_reference": ["is", "set"]}
	if names is not None:
		sent["name"] = cancelling["name"] = ["in", names]
	fields = ["name", "company", "ir_moadian_reference", "ir_cancel_reference"]
	waiting = {}  # company -> {reference: (name, is cancellation)}
	for row in frappe.get_all("Sales Invoice", filters=sent, fields=fields):
		waiting.setdefault(row.company, {})[row.ir_moadian_reference] = (row.name, False)
	for row in frappe.get_all("Sales Invoice", filters=cancelling, fields=fields):
		waiting.setdefault(row.company, {})[row.ir_cancel_reference] = (row.name, True)

	statuses = {}
	for company, by_reference in waiting.items():
		try:
			client = get_client(company, session)
			references = list(by_reference)
			results = []
			for start in range(0, len(references), 10):
				results += client.inquiry_by_reference_ids(references[start : start + 10])
		except Exception:
			frappe.log_error(title=_("Moadian inquiry failed"), message=frappe.get_traceback())
			continue
		for result in results:
			name, is_cancellation = by_reference.get(result.get("referenceNumber"), (None, False))
			if not name:
				continue
			status, message = inquiry_outcome(result)
			if status == "Sent":
				statuses[name] = "Cancellation Sent" if is_cancellation else "Sent"
				continue
			if is_cancellation:
				status = "Cancelled" if status == "Accepted" else "Cancellation Rejected"
			_set(name, status, error=message)
			statuses[name] = status
	return statuses


def process_queue():
	"""Scheduler: send pending invoices and due cancellations, check sent ones, when automatic
	sending is on. A cancellation waits CANCELLATION_GRACE_MINUTES and while a draft amendment of
	the invoice exists, so that the amendment can go as a correction instead."""
	settings = get_settings()
	if not (settings.moadian_enabled and settings.moadian_auto_send):
		return
	pending = frappe.get_all(
		"Sales Invoice",
		filters={"docstatus": 1, "ir_moadian_status": "Pending", "ir_tax_id": ["is", "set"]},
		pluck="name",
		order_by="posting_date, name",
		limit=BATCH,
	)
	cancellations = [
		name
		for name in frappe.get_all(
			"Sales Invoice",
			filters={
				"docstatus": 2,
				"ir_moadian_status": "Cancellation Pending",
				"modified": ["<", add_to_date(now_datetime(), minutes=-CANCELLATION_GRACE_MINUTES)],
			},
			pluck="name",
			limit=BATCH,
		)
		if not frappe.db.exists("Sales Invoice", {"amended_from": name, "docstatus": 0})
	]
	if pending or cancellations:
		send_invoices(pending + cancellations)
	check_status()


@frappe.whitelist()
def send_to_moadian(sales_invoice):
	doc = frappe.get_doc("Sales Invoice", sales_invoice)
	doc.check_permission("cancel" if doc.docstatus == 2 else "submit")
	if doc.ir_moadian_status not in SENDABLE + CANCEL_SENDABLE:
		frappe.throw(_("Nothing to send to Moadian for this invoice"))
	send_invoices([doc.name])
	return frappe.db.get_value("Sales Invoice", doc.name, ["ir_moadian_status", "ir_moadian_error"], as_dict=True)


@frappe.whitelist()
def check_moadian_status(sales_invoice):
	frappe.get_doc("Sales Invoice", sales_invoice).check_permission("read")
	check_status([sales_invoice])
	return frappe.db.get_value("Sales Invoice", sales_invoice, ["ir_moadian_status", "ir_moadian_error"], as_dict=True)


@frappe.whitelist()
def test_connection(company=None):
	"""Get a token and the fiscal information of the memory ID: checks keys, certificate and ID."""
	frappe.only_for(("System Manager", "Accounts Manager"))
	company = company or frappe.defaults.get_user_default("Company")
	return get_client(company).fiscal_information()

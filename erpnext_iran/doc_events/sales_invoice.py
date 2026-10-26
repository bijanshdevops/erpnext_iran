import frappe
from frappe import _

from erpnext_iran.utils.jalali import format_jalali
from erpnext_iran.utils.settings import get_settings


def validate(doc, method=None):
	if doc.posting_date:
		doc.ir_jalali_posting_date = format_jalali(doc.posting_date)
	if doc.is_new() and not doc.get("ir_is_export") and is_foreign_address(doc.customer_address):
		doc.ir_is_export = 1
	if doc.get("ir_is_export") and charges_vat(doc):
		frappe.msgprint(
			_("This is an export sale but it charges VAT. Exports are zero-rated: remove the VAT row if it does not apply."),
			indicator="orange",
			alert=True,
		)


def charges_vat(doc):
	from erpnext_iran.setup.chart_of_accounts import get_account
	from erpnext_iran.setup.taxes import VAT_OUTPUT_ACCOUNT_NUMBER

	vat_account = get_account(doc.company, VAT_OUTPUT_ACCOUNT_NUMBER)
	return any(row.account_head == vat_account and row.tax_amount for row in doc.get("taxes") or [])


def is_foreign_address(address):
	if not address:
		return False
	country = frappe.db.get_value("Address", address, "country")
	return bool(country) and country != frappe.db.get_value("Country", {"code": "ir"}, "name")


def on_submit(doc, method=None):
	if not get_settings().moadian_enabled:
		return
	if doc.get("ir_tax_id") and not copied_tax_id(doc):
		return
	from erpnext_iran.moadian.api import SUBJECT_CORRECTION, assign_tax_id, invoice_subject

	subject, reference = invoice_subject(doc)
	doc.db_set(
		{
			"ir_tax_id": assign_tax_id(doc),
			"ir_moadian_status": "Pending",
			"ir_invoice_subject": str(subject),
			"ir_reference_tax_id": reference,
			# fields a server-side copy may have carried over from the amended invoice
			"ir_moadian_reference": None,
			"ir_moadian_error": "",
			"ir_cancel_tax_id": None,
			"ir_cancel_reference": None,
		}
	)
	if subject == SUBJECT_CORRECTION:
		# the correction replaces the cancellation the amended invoice was waiting to send
		frappe.db.set_value(
			"Sales Invoice",
			doc.amended_from,
			{"ir_moadian_status": "Corrected", "ir_moadian_error": _("Corrected by {0}").format(doc.name)},
			update_modified=False,
		)


def copied_tax_id(doc):
	"""An amendment copied server-side (frappe.copy_doc copies no_copy fields) carries the tax ID of
	the invoice it amends; it needs its own."""
	return bool(doc.amended_from) and doc.ir_tax_id == frappe.db.get_value("Sales Invoice", doc.amended_from, "ir_tax_id")


def before_cancel(doc, method=None):
	if doc.get("ir_moadian_status") in ("Sent", "Cancellation Sent"):
		frappe.throw(
			_("This invoice was sent to Moadian and its answer is not in yet. Use Check Moadian Status, then cancel.")
		)


def on_cancel(doc, method=None):
	"""An accepted invoice needs a Moadian cancellation (or a correction, if it is amended);
	one Moadian never accepted needs nothing."""
	status = doc.get("ir_moadian_status")
	if status == "Accepted":
		from erpnext_iran.moadian.api import assign_tax_id

		doc.db_set(
			{
				"ir_cancel_tax_id": assign_tax_id(doc, timestamp=frappe.utils.now_datetime().timestamp()),
				"ir_moadian_status": "Cancellation Pending",
				"ir_moadian_error": "",
			}
		)
	elif status in ("Pending", "Rejected"):
		doc.db_set(
			{"ir_moadian_status": "", "ir_moadian_error": _("Cancelled before Moadian accepted it: nothing to send.")}
		)

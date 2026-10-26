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
	if not get_settings().moadian_enabled or doc.get("ir_tax_id"):
		return
	from erpnext_iran.moadian.api import assign_tax_id

	doc.db_set({"ir_tax_id": assign_tax_id(doc), "ir_moadian_status": "Pending"})

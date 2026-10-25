import frappe
from frappe import _
from frappe.utils import flt

from erpnext_iran.setup.chart_of_accounts import get_account

VAT_OUTPUT_ACCOUNT_NUMBER = "210201"
VAT_INPUT_ACCOUNT_NUMBER = "110401"


def create_vat_templates(company, rate, output_account=None, input_account=None):
	"""Sales/Purchase VAT templates plus an exempt Item Tax Template for the company."""
	rate = flt(rate)
	output_account = output_account or get_account(company, VAT_OUTPUT_ACCOUNT_NUMBER)
	input_account = input_account or get_account(company, VAT_INPUT_ACCOUNT_NUMBER)
	if not output_account or not input_account:
		frappe.throw(_("Select the VAT output and input accounts for {0}").format(company))

	description = _("VAT and Levy {0}%").format(f"{rate:g}")
	title = _("VAT {0}%").format(f"{rate:g}")
	created = []

	if not frappe.db.exists("Sales Taxes and Charges Template", {"company": company, "title": title}):
		frappe.get_doc(
			{
				"doctype": "Sales Taxes and Charges Template",
				"title": title,
				"company": company,
				"is_default": 1,
				"taxes": [
					{
						"charge_type": "On Net Total",
						"account_head": output_account,
						"description": description,
						"rate": rate,
					}
				],
			}
		).insert(ignore_permissions=True)
		created.append("Sales Taxes and Charges Template")

	if not frappe.db.exists("Purchase Taxes and Charges Template", {"company": company, "title": title}):
		frappe.get_doc(
			{
				"doctype": "Purchase Taxes and Charges Template",
				"title": title,
				"company": company,
				"is_default": 1,
				"taxes": [
					{
						"category": "Total",
						"add_deduct_tax": "Add",
						"charge_type": "On Net Total",
						"account_head": input_account,
						"description": description,
						"rate": rate,
					}
				],
			}
		).insert(ignore_permissions=True)
		created.append("Purchase Taxes and Charges Template")

	exempt_title = _("VAT Exempt")
	if not frappe.db.exists("Item Tax Template", {"company": company, "title": exempt_title}):
		frappe.get_doc(
			{
				"doctype": "Item Tax Template",
				"title": exempt_title,
				"company": company,
				"taxes": [
					{"tax_type": output_account, "tax_rate": 0},
					{"tax_type": input_account, "tax_rate": 0},
				],
			}
		).insert(ignore_permissions=True)
		created.append("Item Tax Template")

	return created

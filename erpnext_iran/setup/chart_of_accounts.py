import json
import os

import frappe
from frappe import _

CHART_PATH = os.path.join(os.path.dirname(__file__), "data", "ir_chart_of_accounts.json")

# Company default field -> account number in ir_chart_of_accounts.json
COMPANY_DEFAULTS = {
	"default_receivable_account": "110301",
	"default_payable_account": "210101",
	"default_cash_account": "110101",
	"default_bank_account": "110103",
	"default_income_account": "4101",
	"default_expense_account": "5101",
	"default_inventory_account": "110501",
	"stock_received_but_not_billed": "210207",
	"stock_adjustment_account": "5102",
	"expenses_included_in_valuation": "5103",
	"round_off_account": "5213",
	"write_off_account": "5215",
	"exchange_gain_loss_account": "4203",
	"unrealized_exchange_gain_loss_account": "4203",
	"accumulated_depreciation_account": "120202",
	"depreciation_expense_account": "5209",
	"disposal_account": "4202",
	"capital_work_in_progress_account": "120107",
	"asset_received_but_not_billed": "210208",
	"default_advance_received_account": "210301",
	"default_advance_paid_account": "110601",
}


def load_chart():
	with open(CHART_PATH, encoding="utf-8") as f:
		return json.load(f)


def get_account(company, account_number):
	return frappe.db.get_value(
		"Account", {"company": company, "account_number": account_number, "is_group": 0}, "name"
	)


def apply_chart(company):
	"""Replace the company's chart with the Iranian chart. Only allowed before any transaction."""
	if frappe.db.exists("GL Entry", {"company": company}):
		frappe.throw(_("Company {0} already has accounting entries; its chart cannot be replaced").format(company))

	from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts
	from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
		unset_existing_data,
	)

	frappe.local.flags.ignore_root_company_validation = True
	frappe.db.sql("update `tabWarehouse` set account = NULL where company = %s", company)
	unset_existing_data(company)
	# standard chart-file format (names are keys), so not the importer's from_coa_importer mode
	create_charts(company, custom_chart=load_chart()["tree"])
	set_company_defaults(company)


def set_company_defaults(company):
	doc = frappe.get_doc("Company", company)
	for fieldname, account_number in COMPANY_DEFAULTS.items():
		if doc.meta.has_field(fieldname):
			account = get_account(company, account_number)
			if account:
				doc.set(fieldname, account)
	doc.flags.ignore_permissions = True
	doc.save()

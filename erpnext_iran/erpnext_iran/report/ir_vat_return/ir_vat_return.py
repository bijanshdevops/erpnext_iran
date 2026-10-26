"""Seasonal VAT return: sales and purchases of a Jalali season split into taxable and exempt,
the output and input VAT on them, the VAT payable, and a check against the VAT ledger accounts.
The "by party" views list each customer or supplier with their tax IDs, as needed for the
seasonal transactions list."""

from collections import defaultdict

import frappe
from frappe import _
from frappe.utils import flt

from erpnext_iran.setup.chart_of_accounts import get_account
from erpnext_iran.setup.taxes import VAT_INPUT_ACCOUNT_NUMBER, VAT_OUTPUT_ACCOUNT_NUMBER
from erpnext_iran.utils.jalali import format_jalali, jalali_year_range
from erpnext_iran.utils.jalali_periods import season_range
from erpnext_iran.utils.vat import split_invoice

SEASONS = {"Spring": 1, "Summer": 2, "Autumn": 3, "Winter": 4}

SIDES = {
	"Sales": {
		"doctype": "Sales Invoice",
		"party_type": "Customer",
		"party_field": "customer",
		"name_field": "customer_name",
		"item_table": "Sales Invoice Item",
		"tax_table": "Sales Taxes and Charges",
	},
	"Purchases": {
		"doctype": "Purchase Invoice",
		"party_type": "Supplier",
		"party_field": "supplier",
		"name_field": "supplier_name",
		"item_table": "Purchase Invoice Item",
		"tax_table": "Purchase Taxes and Charges",
	},
}


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.company:
		frappe.throw(_("Company is required"))
	from_date, to_date = get_date_range(filters)
	currency = frappe.get_cached_value("Company", filters.company, "default_currency")
	accounts = {
		"Sales": filters.vat_output_account or get_account(filters.company, VAT_OUTPUT_ACCOUNT_NUMBER),
		"Purchases": filters.vat_input_account or get_account(filters.company, VAT_INPUT_ACCOUNT_NUMBER),
	}
	for side, account in accounts.items():
		if not account:
			message = (
				_("{0} has no VAT output account (210201). Select it in the report filters.")
				if side == "Sales"
				else _("{0} has no VAT input account (110401). Select it in the report filters.")
			)
			frappe.throw(message.format(filters.company))

	invoices = {
		side: get_invoices(SIDES[side], filters.company, from_date, to_date, accounts[side])
		for side in SIDES
	}

	view = filters.view or "Summary"
	if view == "Summary":
		ledger = get_ledger_vat(filters.company, from_date, to_date, accounts)
		columns, data = summary_columns(), summary_rows(invoices, ledger, currency)
		message = _("{0} to {1}").format(format_jalali(from_date), format_jalali(to_date))
		return columns, data, message, None, report_summary(invoices, currency)

	side = "Sales" if view == "Sales by Party" else "Purchases"
	return party_columns(SIDES[side]), party_rows(SIDES[side], invoices[side], currency)


def get_date_range(filters):
	jy = int(filters.jalali_year or 0)
	if not jy:
		frappe.throw(_("Jalali Year is required"))
	if filters.season in SEASONS:
		return season_range(jy, SEASONS[filters.season])
	return jalali_year_range(jy)


def get_invoices(side, company, from_date, to_date, vat_account):
	doctype = side["doctype"]
	invoices = frappe.get_all(
		doctype,
		filters={"company": company, "docstatus": 1, "posting_date": ["between", [from_date, to_date]]},
		fields=["name", f"{side['party_field']} as party", "base_net_total"],
		order_by="posting_date, name",
	)
	if not invoices:
		return []
	names = [inv.name for inv in invoices]

	vat = defaultdict(float)
	tax_fields = ["parent", "base_tax_amount_after_discount_amount as amount"]
	if doctype == "Purchase Invoice":
		tax_fields.append("add_deduct_tax")
	for row in frappe.get_all(
		side["tax_table"],
		filters={"parenttype": doctype, "parent": ["in", names], "account_head": vat_account},
		fields=tax_fields,
	):
		sign = -1 if row.get("add_deduct_tax") == "Deduct" else 1
		vat[row.parent] += sign * flt(row.amount)

	lines = defaultdict(list)
	for row in frappe.get_all(
		side["item_table"],
		filters={"parenttype": doctype, "parent": ["in", names]},
		fields=["parent", "base_net_amount", "item_tax_rate"],
	):
		lines[row.parent].append((flt(row.base_net_amount), row.item_tax_rate))

	for inv in invoices:
		inv.vat = vat[inv.name]
		inv.taxable, inv.exempt = split_invoice(
			flt(inv.base_net_total), inv.vat, lines[inv.name], vat_account
		)
	return invoices


def get_ledger_vat(company, from_date, to_date, accounts):
	"""VAT booked on the ledger accounts in the period, from any voucher (journal entries too)."""
	ledger = {}
	for side, account in accounts.items():
		debit, credit = frappe.db.get_value(
			"GL Entry",
			{
				"company": company,
				"account": account,
				"is_cancelled": 0,
				"posting_date": ["between", [from_date, to_date]],
			},
			["sum(debit)", "sum(credit)"],
		) or (0, 0)
		ledger[side] = flt(credit) - flt(debit) if side == "Sales" else flt(debit) - flt(credit)
	return ledger


def totals(invoices):
	return {
		key: sum(inv[key] for inv in invoices)
		for key in ("taxable", "exempt", "vat")
	}


def summary_columns():
	return [
		{"fieldname": "description", "label": _("Description"), "fieldtype": "Data", "width": 320},
		{"fieldname": "base_amount", "label": _("Amount"), "fieldtype": "Currency", "options": "currency", "width": 180},
		{"fieldname": "vat_amount", "label": _("VAT and Levy"), "fieldtype": "Currency", "options": "currency", "width": 180},
		{"fieldname": "currency", "label": _("Currency"), "fieldtype": "Link", "options": "Currency", "hidden": 1},
	]


def summary_rows(invoices, ledger, currency):
	sales, purchases = totals(invoices["Sales"]), totals(invoices["Purchases"])

	def row(description, base=None, vat=None, indent=0, bold=0):
		return {
			"description": description,
			"base_amount": base,
			"vat_amount": vat,
			"currency": currency,
			"indent": indent,
			"bold": bold,
		}

	payable = sales["vat"] - purchases["vat"]
	ledger_payable = ledger["Sales"] - ledger["Purchases"]
	return [
		row(_("Sales"), bold=1),
		row(_("Taxable Sales"), sales["taxable"], sales["vat"], indent=1),
		row(_("Exempt and Zero-Rated Sales"), sales["exempt"], 0, indent=1),
		row(_("Total Sales"), sales["taxable"] + sales["exempt"], sales["vat"], indent=1, bold=1),
		row(_("Purchases"), bold=1),
		row(_("Taxable Purchases"), purchases["taxable"], purchases["vat"], indent=1),
		row(_("Exempt Purchases"), purchases["exempt"], 0, indent=1),
		row(_("Total Purchases"), purchases["taxable"] + purchases["exempt"], purchases["vat"], indent=1, bold=1),
		row(_("VAT Payable") if payable >= 0 else _("VAT Credit Carried Forward"), vat=abs(payable), bold=1),
		row(_("Check Against the Ledger"), bold=1),
		row(_("Output VAT per Ledger"), vat=ledger["Sales"], indent=1),
		row(_("Input VAT per Ledger"), vat=ledger["Purchases"], indent=1),
		row(_("Difference From Invoices"), vat=ledger_payable - payable, indent=1),
	]


def report_summary(invoices, currency):
	output_vat = totals(invoices["Sales"])["vat"]
	input_vat = totals(invoices["Purchases"])["vat"]
	payable = output_vat - input_vat
	return [
		{"label": _("Output VAT"), "value": output_vat, "datatype": "Currency", "currency": currency},
		{"label": _("Input VAT"), "value": input_vat, "datatype": "Currency", "currency": currency},
		{
			"label": _("VAT Payable") if payable >= 0 else _("VAT Credit Carried Forward"),
			"value": abs(payable),
			"datatype": "Currency",
			"currency": currency,
			"indicator": "Red" if payable > 0 else "Green",
		},
	]


def party_columns(side):
	return [
		{"fieldname": "party", "label": _(side["party_type"]), "fieldtype": "Link", "options": side["party_type"], "width": 160},
		{"fieldname": "party_name", "label": _("Name"), "fieldtype": "Data", "width": 200},
		{"fieldname": "ir_person_type", "label": _("Person Type"), "fieldtype": "Data", "width": 110},
		{"fieldname": "ir_national_id", "label": _("National ID"), "fieldtype": "Data", "width": 120},
		{"fieldname": "ir_economic_code", "label": _("Economic Code"), "fieldtype": "Data", "width": 130},
		{"fieldname": "invoices", "label": _("Invoices"), "fieldtype": "Int", "width": 80},
		{"fieldname": "taxable", "label": _("Taxable Amount"), "fieldtype": "Currency", "options": "currency", "width": 150},
		{"fieldname": "exempt", "label": _("Exempt Amount"), "fieldtype": "Currency", "options": "currency", "width": 150},
		{"fieldname": "vat", "label": _("VAT and Levy"), "fieldtype": "Currency", "options": "currency", "width": 140},
		{"fieldname": "grand_total", "label": _("Total With VAT"), "fieldtype": "Currency", "options": "currency", "width": 150},
		{"fieldname": "currency", "label": _("Currency"), "fieldtype": "Link", "options": "Currency", "hidden": 1},
	]


def party_rows(side, invoices, currency):
	by_party = {}
	for inv in invoices:
		row = by_party.setdefault(
			inv.party,
			{"party": inv.party, "invoices": 0, "taxable": 0.0, "exempt": 0.0, "vat": 0.0, "currency": currency},
		)
		row["invoices"] += 1
		for key in ("taxable", "exempt", "vat"):
			row[key] += inv[key]
	if not by_party:
		return []

	fields = ["name", f"{side['name_field']} as party_name", "ir_person_type", "ir_national_id", "ir_economic_code"]
	for party in frappe.get_all(side["party_type"], filters={"name": ["in", list(by_party)]}, fields=fields):
		row = by_party[party.name]
		row.update(
			party_name=party.party_name,
			ir_person_type=_(party.ir_person_type) if party.ir_person_type else "",
			ir_national_id=party.ir_national_id,
			ir_economic_code=party.ir_economic_code,
		)

	rows = sorted(by_party.values(), key=lambda r: -(r["taxable"] + r["exempt"]))
	for row in rows:
		row["grand_total"] = row["taxable"] + row["exempt"] + row["vat"]
	return rows


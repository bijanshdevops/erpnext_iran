"""Statutory journal and general ledger of a company for a Jalali period, from GL Entry."""

import frappe
from frappe import _
from frappe.query_builder.functions import Sum
from frappe.utils import add_days, getdate

from erpnext_iran.books.core import build_journal, build_ledger, level_map
from erpnext_iran.utils.jalali import format_jalali
from erpnext_iran.utils.jalali_periods import period_range

# depth below the root group: 2 is the general account (کل), None every posting account (معین)
LEVELS = {"General": 2, "Subsidiary": None}


def get_period(filters):
	if not filters.get("company"):
		frappe.throw(_("Company is required"))
	if not filters.get("jalali_year"):
		frappe.throw(_("Jalali Year is required"))
	return period_range(int(filters["jalali_year"]), filters.get("period") or "Whole Year")


def get_accounts(company):
	return frappe.get_all(
		"Account",
		filters={"company": company},
		fields=["name", "parent_account", "account_number", "account_name", "root_type", "lft"],
		order_by="lft",
	)


def fiscal_year_start(company, date):
	from erpnext.accounts.utils import get_fiscal_year

	try:
		return getdate(get_fiscal_year(date, company=company)[1])
	except Exception:  # no fiscal year covers the date: number vouchers from the period start
		return getdate(date)


def voucher_descriptions(entries):
	"""One description per voucher: its type and number, then its remarks."""
	remarks = {}
	for e in entries:
		key = (e.voucher_type, e.voucher_no)
		text = (e.remarks or "").strip()
		if key not in remarks or (not remarks[key] and text):
			remarks[key] = "" if text in ("", "No Remarks", _("No Remarks")) else text

	# ERPNext v16 no longer copies a Journal Entry's user remark into its GL Entries
	missing = [no for (kind, no), text in remarks.items() if kind == "Journal Entry" and not text]
	if missing:
		for je in frappe.get_all(
			"Journal Entry", filters={"name": ["in", missing]}, fields=["name", "user_remark", "remark"]
		):
			remarks[("Journal Entry", je.name)] = (je.user_remark or je.remark or "").strip()
	return {
		key: f"{_(key[0])} {key[1]}" + (f" - {text}" if text else "")
		for key, text in remarks.items()
	}


def get_journal(filters):
	"""(rows, accounts by name, from_date, to_date) of the statutory journal."""
	company = filters["company"]
	from_date, to_date = get_period(filters)
	accounts = get_accounts(company)
	level_of = level_map(accounts, LEVELS[filters.get("level") or "General"])

	# number vouchers from the start of the fiscal year, so a month's book continues the year's
	start = min(fiscal_year_start(company, from_date), from_date)
	entries = frappe.get_all(
		"GL Entry",
		filters={"company": company, "is_cancelled": 0, "posting_date": ["between", [start, to_date]]},
		fields=["posting_date", "voucher_type", "voucher_no", "account", "debit", "credit", "remarks"],
		order_by="posting_date, creation, voucher_no, name",
	)
	descriptions = voucher_descriptions(entries)
	for e in entries:
		e.description = descriptions[(e.voucher_type, e.voucher_no)]

	rows = [r for r in build_journal(entries, level_of) if getdate(r["posting_date"]) >= getdate(from_date)]
	by_name = {a.name: a for a in accounts}
	for row in rows:
		account = by_name.get(row["account"]) or frappe._dict()
		row.update(
			jalali_date=format_jalali(row["posting_date"]),
			account_number=account.account_number or "",
			account_name=account.account_name or row["account"],
		)
	return rows, by_name, from_date, to_date


def get_openings(company, accounts, level_of, from_date):
	"""Balance (debit positive) of each reported account before from_date. Income and expense
	accounts start from zero at the beginning of the fiscal year."""
	fy_start = fiscal_year_start(company, from_date)
	by_name = {a.name: a for a in accounts}
	day_before = add_days(from_date, -1)
	openings = {}
	for root_types, since in ((("Asset", "Liability", "Equity"), None), (("Income", "Expense"), fy_start)):
		names = [a.name for a in accounts if a.root_type in root_types]
		if not names or (since and since >= getdate(from_date)):
			continue
		gle = frappe.qb.DocType("GL Entry")
		query = (
			frappe.qb.from_(gle)
			.select(gle.account, Sum(gle.debit).as_("debit"), Sum(gle.credit).as_("credit"))
			.where(
				(gle.company == company)
				& (gle.is_cancelled == 0)
				& gle.account.isin(names)
				& (gle.posting_date <= day_before)
			)
			.groupby(gle.account)
		)
		if since:
			query = query.where(gle.posting_date >= since)
		for row in query.run(as_dict=True):
			target = level_of.get(row.account, row.account)
			openings[target] = openings.get(target, 0) + (row.debit or 0) - (row.credit or 0)
	return {name: value for name, value in openings.items() if name in by_name}


def get_ledger(filters):
	"""(ledger, accounts by name, from_date, to_date) of the statutory general ledger."""
	journal, by_name, from_date, to_date = get_journal(filters)
	accounts = list(by_name.values())
	level_of = level_map(accounts, LEVELS[filters.get("level") or "General"])
	openings = get_openings(filters["company"], accounts, level_of, from_date)
	order = [a.name for a in accounts]  # chart order (lft)
	if filters.get("account"):
		order = [name for name in order if name == level_of.get(filters["account"], filters["account"])]
	ledger = build_ledger(journal, openings, order)
	for account, book in ledger.items():
		for row in book["rows"]:
			if row.get("opening"):
				row["description"] = _("Balance Brought Forward")
	return ledger, by_name, from_date, to_date


def account_label(account):
	return f"{account.account_number} {account.account_name}" if account.account_number else account.account_name

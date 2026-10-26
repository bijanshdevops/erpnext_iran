"""Statutory general ledger (دفتر کل): for each general (or subsidiary) account its balance brought
forward and its movements with the journal number and running balance."""

from frappe import _

from erpnext_iran.books.data import account_label, get_ledger


def dr_cr(balance):
	if not round(balance, 6):
		return ""
	return _("Dr") if balance > 0 else _("Cr")


def execute(filters=None):
	ledger, accounts, _from, _to = get_ledger(filters or {})
	data = []
	for account, book in ledger.items():
		data.append(
			{
				"description": account_label(accounts[account]),
				"debit": None,
				"credit": None,
				"balance": None,
				"account": account,
				"bold": 1,
				"indent": 0,
			}
		)
		for row in book["rows"]:
			data.append(
				{
					"jalali_date": row.get("jalali_date", ""),
					"voucher_number": row.get("voucher_number"),
					"description": row["description"],
					"debit": row["debit"] or None,
					"credit": row["credit"] or None,
					"dr_cr": dr_cr(row["balance"]),
					"balance": abs(row["balance"]),
					"voucher_type": row.get("voucher_type"),
					"voucher_no": row.get("voucher_no"),
					"account": account,
					"indent": 1,
				}
			)
		data.append(
			{
				"description": _("Total and Balance"),
				"debit": book["debit"] or None,
				"credit": book["credit"] or None,
				"dr_cr": dr_cr(book["balance"]),
				"balance": abs(book["balance"]),
				"account": account,
				"bold": 1,
				"indent": 1,
			}
		)
	return columns(), data


def columns():
	return [
		{"fieldname": "jalali_date", "label": _("Date"), "fieldtype": "Data", "width": 100},
		{"fieldname": "voucher_number", "label": _("Journal No."), "fieldtype": "Data", "width": 90},
		{"fieldname": "description", "label": _("Description"), "fieldtype": "Data", "width": 320},
		{"fieldname": "debit", "label": _("Debit"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "credit", "label": _("Credit"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "dr_cr", "label": _("Dr / Cr"), "fieldtype": "Data", "width": 80},
		{"fieldname": "balance", "label": _("Balance"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "voucher_type", "label": _("Voucher Type"), "fieldtype": "Data", "hidden": 1},
		{"fieldname": "voucher_no", "label": _("Voucher No"), "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 170},
		{"fieldname": "account", "label": _("Account"), "fieldtype": "Link", "options": "Account", "hidden": 1},
	]

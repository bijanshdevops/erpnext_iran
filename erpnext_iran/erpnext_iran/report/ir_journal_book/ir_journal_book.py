"""Statutory journal (دفتر روزنامه): every voucher of the period in date order, numbered from the
start of the fiscal year, its lines netted per general (or subsidiary) account."""

from frappe import _

from erpnext_iran.books.data import get_journal


def execute(filters=None):
	rows, _accounts, _from, _to = get_journal(filters or {})
	data = [
		{
			"voucher_number": row["voucher_number"],
			"jalali_date": row["jalali_date"] if row["first"] else "",
			"account_number": row["account_number"],
			"account_name": row["account_name"],
			"description": row["description"] if row["first"] else "",
			"debit": row["debit"] or None,
			"credit": row["credit"] or None,
			"voucher_type": row["voucher_type"],
			"voucher_no": row["voucher_no"],
		}
		for row in rows
	]
	if data:
		data.append(
			{
				"account_name": _("Total"),
				"debit": sum(r["debit"] for r in rows),
				"credit": sum(r["credit"] for r in rows),
				"bold": 1,
			}
		)
	return columns(), data


def columns():
	return [
		{"fieldname": "voucher_number", "label": _("Journal No."), "fieldtype": "Data", "width": 90},
		{"fieldname": "jalali_date", "label": _("Date"), "fieldtype": "Data", "width": 100},
		{"fieldname": "account_number", "label": _("Account Code"), "fieldtype": "Data", "width": 100},
		{"fieldname": "account_name", "label": _("Account"), "fieldtype": "Data", "width": 220},
		{"fieldname": "description", "label": _("Description"), "fieldtype": "Data", "width": 300},
		{"fieldname": "debit", "label": _("Debit"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "credit", "label": _("Credit"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "voucher_type", "label": _("Voucher Type"), "fieldtype": "Data", "hidden": 1},
		{"fieldname": "voucher_no", "label": _("Voucher No"), "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 170},
	]

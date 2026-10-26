"""Cheques by due date: what falls due, what bounced, and the total in each status."""

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate

from erpnext_iran.utils.jalali import format_jalali

OPEN_STATUSES = ("Received", "Deposited", "Issued")


def execute(filters=None):
	filters = frappe._dict(filters or {})
	conditions = {"docstatus": 1}
	for field in ("company", "cheque_type", "party_type", "party"):
		if filters.get(field):
			conditions[field] = filters[field]
	if filters.status == "Open":
		conditions["status"] = ["in", OPEN_STATUSES]
	elif filters.status:
		conditions["status"] = filters.status
	if filters.from_date and filters.to_date:
		conditions["due_date"] = ["between", [filters.from_date, filters.to_date]]
	elif filters.from_date:
		conditions["due_date"] = [">=", filters.from_date]
	elif filters.to_date:
		conditions["due_date"] = ["<=", filters.to_date]

	cheques = frappe.get_all(
		"IR Cheque",
		filters=conditions,
		fields=["name", "cheque_type", "sayad_id", "serial", "party_type", "party", "party_name", "bank",
				"due_date", "amount", "status", "endorsed_to"],  # fmt: skip
		order_by="due_date, name",
	)
	today = getdate()
	for cheque in cheques:
		cheque.jalali_due_date = format_jalali(cheque.due_date)
		cheque.days_to_due = date_diff(cheque.due_date, today) if cheque.status in OPEN_STATUSES else None
		cheque.cheque_type_label = _(cheque.cheque_type)
		cheque.status_label = _(cheque.status)
	return columns(), cheques, None, None, summary(cheques)


def summary(cheques):
	totals = {}
	for cheque in cheques:
		key = (cheque.cheque_type, cheque.status)
		totals[key] = totals.get(key, 0) + flt(cheque.amount)
	indicators = {"Cleared": "Green", "Bounced": "Red", "Deposited": "Orange"}
	return [
		{
			"label": f"{_(cheque_type)} - {_(status)}",
			"value": amount,
			"datatype": "Currency",
			"indicator": indicators.get(status, "Blue"),
		}
		for (cheque_type, status), amount in sorted(totals.items())
	]


def columns():
	return [
		{"fieldname": "name", "label": _("Cheque"), "fieldtype": "Link", "options": "IR Cheque", "width": 120},
		{"fieldname": "cheque_type_label", "label": _("Cheque Type"), "fieldtype": "Data", "width": 90},
		{"fieldname": "jalali_due_date", "label": _("Due Date"), "fieldtype": "Data", "width": 100},
		{"fieldname": "days_to_due", "label": _("Days to Due"), "fieldtype": "Int", "width": 90},
		{"fieldname": "party_name", "label": _("Party"), "fieldtype": "Data", "width": 180},
		{"fieldname": "sayad_id", "label": _("Sayad ID"), "fieldtype": "Data", "width": 150},
		{"fieldname": "serial", "label": _("Cheque Serial"), "fieldtype": "Data", "width": 90},
		{"fieldname": "bank", "label": _("Bank"), "fieldtype": "Link", "options": "Bank", "width": 120},
		{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "status_label", "label": _("Status"), "fieldtype": "Data", "width": 100},
		{"fieldname": "endorsed_to", "label": _("Endorsed To"), "fieldtype": "Link", "options": "Supplier", "width": 140},
	]

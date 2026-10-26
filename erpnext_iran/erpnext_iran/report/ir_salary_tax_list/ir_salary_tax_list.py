"""Monthly salary tax list (لیست مالیات حقوق): pay, exempt part, taxable income and tax."""

from frappe import _

from erpnext_iran.payroll.lists import get_slips, total_row

AMOUNTS = ["gross_pay", "exempt_insurance", "ir_taxable_income", "ir_salary_tax"]


def execute(filters=None):
	rows = get_slips(filters)
	data = [dict(r) for r in rows]
	if data:
		data.append(total_row(rows, _("Total"), AMOUNTS))
	return columns(), data


def columns():
	money = lambda fieldname, label: {"fieldname": fieldname, "label": label, "fieldtype": "Currency", "width": 150}  # noqa: E731
	return [
		{"fieldname": "employee", "label": _("Employee"), "fieldtype": "Link", "options": "Employee", "width": 120},
		{"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 170},
		{"fieldname": "ir_national_id", "label": _("National ID"), "fieldtype": "Data", "width": 110},
		money("gross_pay", _("Gross Pay")),
		money("exempt_insurance", _("Exempt Part of Insurance")),
		money("ir_taxable_income", _("Taxable Income")),
		money("ir_salary_tax", _("Salary Tax")),
		{"fieldname": "name", "label": _("Salary Slip"), "fieldtype": "Link", "options": "Salary Slip", "width": 160},
	]

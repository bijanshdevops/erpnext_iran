"""Monthly social security list (لیست بیمه): days, wage, insurable benefits and both shares."""

from frappe import _

from erpnext_iran.payroll.lists import get_slips, total_row

AMOUNTS = ["monthly_wage", "insurable_benefits", "ir_insurable_wage", "ir_employee_insurance",
		   "ir_employer_insurance", "total_insurance"]  # fmt: skip


def execute(filters=None):
	rows = get_slips(filters)
	data = [dict(r) for r in rows]
	if data:
		data.append(total_row(rows, _("Total"), AMOUNTS + ["payment_days"]))
	return columns(), data


def columns():
	money = lambda fieldname, label: {"fieldname": fieldname, "label": label, "fieldtype": "Currency", "width": 140}  # noqa: E731
	return [
		{"fieldname": "employee", "label": _("Employee"), "fieldtype": "Link", "options": "Employee", "width": 120},
		{"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 170},
		{"fieldname": "ir_national_id", "label": _("National ID"), "fieldtype": "Data", "width": 110},
		{"fieldname": "ir_insurance_number", "label": _("Social Security Number"), "fieldtype": "Data", "width": 120},
		{"fieldname": "payment_days", "label": _("Days Worked"), "fieldtype": "Float", "width": 80},
		money("daily_wage", _("Daily Wage")),
		money("monthly_wage", _("Monthly Wage")),
		money("insurable_benefits", _("Insurable Benefits")),
		money("ir_insurable_wage", _("Insurable Wage")),
		money("ir_employee_insurance", _("Employee Share")),
		money("ir_employer_insurance", _("Employer Share")),
		money("total_insurance", _("Total Premium")),
		{"fieldname": "name", "label": _("Salary Slip"), "fieldtype": "Link", "options": "Salary Slip", "width": 160},
	]

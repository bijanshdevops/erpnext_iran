"""Rows for the monthly social security and salary tax lists, from submitted Salary Slips."""

import frappe
from frappe import _
from frappe.utils import flt

from erpnext_iran.utils.jalali_periods import period_range


def get_slips(filters):
	filters = frappe._dict(filters or {})
	if not filters.company or not filters.jalali_year or not filters.month:
		frappe.throw(_("Company, Jalali Year and Month are required"))
	if "hrms" not in frappe.get_installed_apps():
		frappe.throw(_("Install the Frappe HR (hrms) app first"))
	from_date, to_date = period_range(int(filters.jalali_year), str(filters.month))
	docstatus = ["in", [0, 1]] if filters.include_drafts else 1
	slips = frappe.get_all(
		"Salary Slip",
		filters={"company": filters.company, "docstatus": docstatus, "start_date": ["between", [from_date, to_date]]},
		fields=["name", "employee", "employee_name", "payment_days", "gross_pay", "ir_insurable_wage",
				"ir_employee_insurance", "ir_employer_insurance", "ir_taxable_income", "ir_salary_tax"],  # fmt: skip
		order_by="employee_name",
	)
	if not slips:
		return []
	employees = {
		e.name: e
		for e in frappe.get_all(
			"Employee",
			filters={"name": ["in", [s.employee for s in slips]]},
			fields=["name", "ir_national_id", "ir_insurance_number"],
		)
	}
	base_wage = {
		row.parent: flt(row.amount)
		for row in frappe.get_all(
			"Salary Detail",
			filters={"parenttype": "Salary Slip", "parent": ["in", [s.name for s in slips]], "abbr": "IR_B"},
			fields=["parent", "amount"],
		)
	}
	for slip in slips:
		employee = employees.get(slip.employee) or frappe._dict()
		slip.ir_national_id = employee.ir_national_id
		slip.ir_insurance_number = employee.ir_insurance_number
		slip.monthly_wage = base_wage.get(slip.name, 0)
		slip.daily_wage = slip.monthly_wage / flt(slip.payment_days) if slip.payment_days else 0
		slip.insurable_benefits = flt(slip.ir_insurable_wage) - slip.monthly_wage
		slip.total_insurance = flt(slip.ir_employee_insurance) + flt(slip.ir_employer_insurance)
		slip.exempt_insurance = flt(slip.gross_pay) - flt(slip.ir_taxable_income)
	return slips


def total_row(rows, label, fields):
	row = {field: sum(flt(r.get(field)) for r in rows) for field in fields}
	row.update(employee_name=label, bold=1)
	return row

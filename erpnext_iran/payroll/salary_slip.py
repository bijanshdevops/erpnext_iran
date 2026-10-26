"""Salary Slip hooks for Iranian payroll (HRMS).

before_validate puts the year's wage parameters (IR Payroll Year of the slip's Jalali year) and
the employee's children and years of service on the slip, where the salary structure's formulas
read them. validate runs after HRMS has calculated the slip and sets the social security and
salary tax deductions, which need a ceiling and progressive brackets no formula can express.
"""

import frappe
from frappe.utils import cint, date_diff, flt, getdate

from erpnext_iran.payroll.core import insurance, rial, salary_tax, taxable_income, years_of_service
from erpnext_iran.utils.jalali import to_jalali


def payroll_year(date):
	name = str(to_jalali(getdate(date))[0])
	return frappe.get_cached_doc("IR Payroll Year", name) if frappe.db.exists("IR Payroll Year", name) else None


def before_validate(doc, method=None):
	year = payroll_year(doc.start_date)
	if not year:
		return
	employee = frappe.get_cached_doc("Employee", doc.employee)
	doc.ir_payroll_year = year.name
	doc.ir_children = cint(employee.get("ir_children"))
	doc.ir_seniority_years = years_of_service(employee.date_of_joining, getdate(doc.start_date))
	doc.ir_overtime_premium = flt(year.overtime_premium)
	doc.ir_housing = flt(year.housing_allowance)
	doc.ir_food = flt(year.food_allowance)
	doc.ir_marital_allowance = flt(year.marital_allowance) if employee.marital_status == "Married" else 0
	doc.ir_child_allowance = rial(flt(year.child_allowance_days) * flt(year.daily_minimum_wage))
	doc.ir_seniority_monthly = flt(year.seniority_monthly)


def component_settings():
	return {
		row.name: row
		for row in frappe.get_all(
			"Salary Component",
			fields=["name", "salary_component_abbr", "ir_payroll_role", "ir_insurable", "ir_taxable"],
		)
	}


def validate(doc, method=None):
	year = payroll_year(doc.start_date)
	if not year:
		return
	settings = component_settings()

	def total(flag):
		return sum(flt(row.amount) for row in doc.earnings if settings.get(row.salary_component, {}).get(flag))

	days = date_diff(doc.end_date, doc.start_date) + 1
	ceiling = flt(year.insurance_ceiling_days) * flt(year.daily_minimum_wage) * days
	base, employee_share, employer_share = insurance(
		total("ir_insurable"), ceiling, year.employee_insurance_rate, year.employer_insurance_rate
	)
	taxable = taxable_income(total("ir_taxable"), employee_share, year.exempt_insurance_fraction)
	tax = salary_tax(taxable, [(row.from_amount, row.rate) for row in year.tax_brackets])

	amounts = {"Employee Insurance": employee_share, "Salary Tax": tax}
	for row in doc.deductions:
		role = settings.get(row.salary_component, {}).get("ir_payroll_role")
		if role in amounts:
			row.amount = row.default_amount = amounts.pop(role)
	for role, amount in amounts.items():  # a structure without the row: add it
		component = next((c for c in settings.values() if c.ir_payroll_role == role), None)
		if component and amount:
			doc.append("deductions", {"salary_component": component.name, "abbr": component.salary_component_abbr,
									  "amount": amount, "default_amount": amount, "depends_on_payment_days": 0})  # fmt: skip

	doc.ir_insurable_wage = base
	doc.ir_employee_insurance = employee_share
	doc.ir_employer_insurance = employer_share
	doc.ir_taxable_income = taxable
	doc.ir_salary_tax = tax

	# totals and year/month-to-date figures were computed before these amounts were set
	doc.set_net_pay()
	doc.compute_year_to_date()
	doc.compute_month_to_date()
	doc.compute_component_wise_year_to_date()

"""Iranian payroll setup: the years' wage parameters and a ready salary structure (HRMS)."""

import frappe
from frappe import _

from erpnext_iran.setup.chart_of_accounts import get_account

# Supreme Labour Council decree of 24 Esfand 1404 (minimum wage and allowances) and the 1405
# budget law (salary tax), as published; check them against the official circulars.
PAYROLL_YEARS = {
	1405: {
		"daily_minimum_wage": 5_541_850,
		"housing_allowance": 30_000_000,
		"food_allowance": 22_000_000,
		"marital_allowance": 5_000_000,
		"child_allowance_days": 3,
		"seniority_monthly": 5_000_000,
		"overtime_premium": 40,
		"employee_insurance_rate": 7,
		"employer_insurance_rate": 23,
		"insurance_ceiling_days": 7,
		"exempt_insurance_fraction": 2 / 7,
		"tax_brackets": [(0, 0), (400_000_000, 10), (800_000_000, 15), (1_000_000_000, 20),
						 (1_200_000_000, 25), (1_400_000_000, 30)],  # fmt: skip
		"source": "مصوبه شورای عالی کار ۱۴۰۴/۱۲/۲۴ (حداقل مزد و مزایا) و قانون بودجه ۱۴۰۵ (مالیات حقوق)، به نقل از منابع منتشرشده؛ با بخشنامه‌های رسمی تطبیق دهید.",
	}
}

# name, abbreviation, type, role, insurable, taxable, formula. Insurance and tax have formula "0"
# (HRMS drops structure rows with a zero fixed amount); erpnext_iran sets their amounts.
COMPONENTS = [
	("حقوق پایه", "IR_B", "Earning", "Base Wage", 1, 1, "base * payment_days"),
	("حق مسکن", "IR_H", "Earning", "Housing", 1, 1, "ir_housing * payment_days / total_working_days"),
	("بن خواربار", "IR_F", "Earning", "Food", 1, 1, "ir_food * payment_days / total_working_days"),
	("حق تأهل", "IR_M", "Earning", "Marital", 1, 1, "ir_marital_allowance * payment_days / total_working_days"),
	("حق اولاد", "IR_C", "Earning", "Child", 0, 1, "ir_children * ir_child_allowance * payment_days / total_working_days"),
	("پایه سنوات", "IR_S", "Earning", "Seniority", 1, 1, "ir_seniority_years * ir_seniority_monthly * payment_days / total_working_days"),
	("اضافه‌کار", "IR_OT", "Earning", "Overtime", 1, 1, "ir_overtime_hours * base / 7.33 * (1 + ir_overtime_premium / 100)"),
	("حق بیمه سهم کارگر", "IR_SS", "Deduction", "Employee Insurance", 0, 0, "0"),
	("مالیات حقوق", "IR_TAX", "Deduction", "Salary Tax", 0, 0, "0"),
]
# account number per component type in the Iranian chart
ACCOUNTS = {"Earning": "5201", "Employee Insurance": "210204", "Salary Tax": "210202"}


def ensure_payroll_years():
	for jalali_year, values in PAYROLL_YEARS.items():
		if frappe.db.exists("IR Payroll Year", str(jalali_year)):
			continue
		values = dict(values)
		brackets = values.pop("tax_brackets")
		doc = frappe.get_doc({"doctype": "IR Payroll Year", "jalali_year": jalali_year, **values})
		for start, rate in brackets:
			doc.append("tax_brackets", {"from_amount": start, "rate": rate})
		doc.insert(ignore_permissions=True)


def ensure_components(company):
	for name, abbr, kind, role, insurable, taxable, formula in COMPONENTS:
		doc = frappe.get_doc("Salary Component", name) if frappe.db.exists("Salary Component", name) else frappe.new_doc("Salary Component")
		doc.update(
			{
				"salary_component": name,
				"salary_component_abbr": abbr,
				"type": kind,
				"ir_payroll_role": role,
				"ir_insurable": insurable,
				"ir_taxable": taxable,
				"depends_on_payment_days": 0,  # the formulas prorate themselves
				"round_to_the_nearest_integer": 1,
				"amount_based_on_formula": 1,
				"formula": formula,
				"is_tax_applicable": 0,
			}
		)
		account = get_account(company, ACCOUNTS[kind] if kind == "Earning" else ACCOUNTS[role])
		if account and company not in [row.company for row in doc.get("accounts") or []]:
			doc.append("accounts", {"company": company, "account": account})
		doc.save(ignore_permissions=True)


def create_salary_structure(company):
	name = _("Iran Standard Salary - {0}").format(frappe.get_cached_value("Company", company, "abbr"))
	if frappe.db.exists("Salary Structure", name):
		return name
	doc = frappe.get_doc(
		{
			"doctype": "Salary Structure",
			"name": name,
			"company": company,
			"currency": frappe.get_cached_value("Company", company, "default_currency"),
			"payroll_frequency": "Monthly",
			"is_active": "Yes",
		}
	)
	for component, abbr, kind, _role, _ins, _tax, formula in COMPONENTS:
		doc.append(
			"earnings" if kind == "Earning" else "deductions",
			{
				"salary_component": component,
				"abbr": abbr,
				"amount_based_on_formula": 1,
				"formula": formula,
				"depends_on_payment_days": 0,
			},
		)
	doc.insert(ignore_permissions=True)
	doc.submit()
	return name


@frappe.whitelist()
def setup_iran_payroll(company):
	"""Components, a submitted 'Iran Standard Salary' structure and payroll settings for company."""
	frappe.only_for(("HR Manager", "System Manager"))
	if "hrms" not in frappe.get_installed_apps():
		frappe.throw(_("Install the Frappe HR (hrms) app first"))
	ensure_payroll_years()
	ensure_components(company)
	settings = frappe.get_single("Payroll Settings")
	settings.include_holidays_in_total_working_days = 1  # monthly wages count every day of the month
	settings.save(ignore_permissions=True)
	holiday_list = frappe.db.get_value("Company", company, "default_holiday_list")
	if holiday_list:
		from erpnext_iran.setup.iran_calendar import assign_to_company

		assign_to_company(company, holiday_list)
	payable = get_account(company, "210205")
	if payable and frappe.get_meta("Company").has_field("default_payroll_payable_account"):
		if not frappe.db.get_value("Company", company, "default_payroll_payable_account"):
			frappe.db.set_value("Company", company, "default_payroll_payable_account", payable)
	return create_salary_structure(company)

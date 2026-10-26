"""Custom fields for Iranian payroll. Salary Slip / Salary Component fields only exist with HRMS."""

ROLES = [
	"Base Wage",
	"Housing",
	"Food",
	"Marital",
	"Child",
	"Seniority",
	"Overtime",
	"Employee Insurance",
	"Salary Tax",
]


def _currency(fieldname, label, insert_after):
	return {"fieldname": fieldname, "label": label, "fieldtype": "Currency", "options": "currency",
			"read_only": 1, "insert_after": insert_after}  # fmt: skip


def employee_fields():
	return [
		{"fieldname": "ir_payroll_section", "label": "Iran Payroll", "fieldtype": "Section Break",
		 "insert_after": "marital_status", "collapsible": 1},
		{"fieldname": "ir_national_id", "label": "National ID", "fieldtype": "Data", "length": 10,
		 "insert_after": "ir_payroll_section"},
		{"fieldname": "ir_insurance_number", "label": "Social Security Number", "fieldtype": "Data",
		 "insert_after": "ir_national_id"},
		{"fieldname": "ir_payroll_column", "fieldtype": "Column Break", "insert_after": "ir_insurance_number"},
		{"fieldname": "ir_children", "label": "Children for Child Allowance", "fieldtype": "Int",
		 "insert_after": "ir_payroll_column"},
	]  # fmt: skip


def hrms_fields():
	slip = [
		{"fieldname": "ir_section", "label": "Iran Payroll", "fieldtype": "Section Break",
		 "insert_after": "deductions", "collapsible": 1},
		{"fieldname": "ir_overtime_hours", "label": "Overtime Hours", "fieldtype": "Float",
		 "insert_after": "ir_section"},
		{"fieldname": "ir_payroll_year", "label": "Payroll Year", "fieldtype": "Link",
		 "options": "IR Payroll Year", "read_only": 1, "insert_after": "ir_overtime_hours"},
		{"fieldname": "ir_children", "label": "Children for Child Allowance", "fieldtype": "Int",
		 "read_only": 1, "insert_after": "ir_payroll_year"},
		{"fieldname": "ir_seniority_years", "label": "Years of Service", "fieldtype": "Int",
		 "read_only": 1, "insert_after": "ir_children"},
		{"fieldname": "ir_overtime_premium", "label": "Overtime Premium", "fieldtype": "Percent",
		 "read_only": 1, "insert_after": "ir_seniority_years"},
		_currency("ir_housing", "Housing Allowance", "ir_overtime_premium"),
		_currency("ir_food", "Food Allowance (Consumer Goods)", "ir_housing"),
		_currency("ir_marital_allowance", "Marital Allowance", "ir_food"),
		_currency("ir_child_allowance", "Child Allowance per Child", "ir_marital_allowance"),
		_currency("ir_seniority_monthly", "Seniority Increment per Year of Service", "ir_child_allowance"),
		{"fieldname": "ir_column", "fieldtype": "Column Break", "insert_after": "ir_seniority_monthly"},
		_currency("ir_insurable_wage", "Insurable Wage", "ir_column"),
		_currency("ir_employee_insurance", "Employee Insurance", "ir_insurable_wage"),
		_currency("ir_employer_insurance", "Employer Insurance", "ir_employee_insurance"),
		_currency("ir_taxable_income", "Taxable Income", "ir_employer_insurance"),
		_currency("ir_salary_tax", "Salary Tax", "ir_taxable_income"),
	]  # fmt: skip
	component = [
		{"fieldname": "ir_payroll_role", "label": "Iranian Payroll Role", "fieldtype": "Select",
		 "options": "\n" + "\n".join(ROLES), "insert_after": "type",
		 "description": "Employee Insurance and Salary Tax amounts are calculated by erpnext_iran"},
		{"fieldname": "ir_insurable", "label": "Subject to Social Security", "fieldtype": "Check",
		 "insert_after": "ir_payroll_role"},
		{"fieldname": "ir_taxable", "label": "Subject to Salary Tax", "fieldtype": "Check",
		 "insert_after": "ir_insurable"},
	]  # fmt: skip
	return {"Salary Slip": slip, "Salary Component": component}

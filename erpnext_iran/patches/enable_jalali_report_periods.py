import frappe


def execute():
	"""Sites that saved Iran Localization Settings before the field existed read it as 0."""
	frappe.db.set_single_value("Iran Localization Settings", "jalali_report_periods", 1)

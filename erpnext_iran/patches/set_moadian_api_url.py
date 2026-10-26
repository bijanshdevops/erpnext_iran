import frappe

from erpnext_iran.moadian.client import PRODUCTION_URL


def execute():
	# the field's default only applies to new settings
	if not frappe.db.get_single_value("Iran Localization Settings", "moadian_api_url"):
		frappe.db.set_single_value("Iran Localization Settings", "moadian_api_url", PRODUCTION_URL)

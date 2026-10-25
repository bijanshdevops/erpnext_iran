"""Persian names for a company's default warehouses and Iranian system-wide defaults."""

import frappe
from frappe import _

# ERPNext's Company.create_default_warehouses names (created in English on most sites)
DEFAULT_WAREHOUSES_FA = {
	"All Warehouses": "همه انبارها",
	"Stores": "انبار اصلی",
	"Work In Progress": "کالای در جریان ساخت",
	"Finished Goods": "انبار محصول",
	"Goods In Transit": "کالای در راه",
}

SYSTEM_DEFAULTS = {
	"country": "Iran",
	"time_zone": "Asia/Tehran",
	"currency": "IRR",
	"date_format": "yyyy-mm-dd",
	"first_day_of_the_week": "Saturday",
	# amounts use each currency's own format (Rial: #,### without decimals)
	"use_number_format_from_currency": 1,
}


def rename_default_warehouses(company):
	"""Rename the company's default warehouses to Persian; links follow the rename."""
	abbr = frappe.get_cached_value("Company", company, "abbr")
	renamed = []
	for english, persian in DEFAULT_WAREHOUSES_FA.items():
		old = frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": english})
		new = f"{persian} - {abbr}"
		if not old or frappe.db.exists("Warehouse", new):
			continue
		frappe.rename_doc("Warehouse", old, new, force=True, show_alert=False)
		# rename_doc changes the ID only; the display name is a separate field
		frappe.db.set_value("Warehouse", new, "warehouse_name", persian)
		renamed.append(new)
	return renamed


def apply_system_defaults():
	"""Time zone, currency, date format and week start for an Iranian company."""
	settings = frappe.get_doc("System Settings")
	for fieldname, value in SYSTEM_DEFAULTS.items():
		if settings.meta.has_field(fieldname):
			settings.set(fieldname, value)
	settings.flags.ignore_mandatory = True
	settings.save(ignore_permissions=True)
	# System Settings.set_defaults copies only changed fields into the site defaults, and the
	# System Settings form (and frappe.boot.sysdefaults) read those copies: a value that was
	# already set in the record but not in the defaults (e.g. time_zone set directly) would
	# keep showing the old one. Write them all.
	for fieldname, value in SYSTEM_DEFAULTS.items():
		if settings.meta.has_field(fieldname):
			frappe.db.set_default(fieldname, value)

	if frappe.db.exists("Currency", "IRR"):
		frappe.db.set_single_value("Global Defaults", "default_currency", "IRR")
		frappe.db.set_single_value("Global Defaults", "country", "Iran")
	frappe.clear_cache()
	return _("Iranian system defaults")

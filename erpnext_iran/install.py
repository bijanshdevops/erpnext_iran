import frappe

from erpnext_iran.setup.custom_fields import delete_custom_fields, setup_custom_fields


def after_install():
	setup_custom_fields()
	setup_currency()


def after_migrate():
	setup_custom_fields()


def before_uninstall():
	delete_custom_fields()


def setup_currency():
	"""Rial has no fractional unit in practice; show it as 1,234,567."""
	if not frappe.db.exists("Currency", "IRR"):
		return
	frappe.db.set_value(
		"Currency",
		"IRR",
		{
			"enabled": 1,
			"fraction": "",
			"fraction_units": 0,
			"smallest_currency_fraction_value": 0,
			"number_format": "#,###",
			"symbol_on_right": 1,
		},
	)

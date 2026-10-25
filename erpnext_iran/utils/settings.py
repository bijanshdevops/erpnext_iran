import frappe

SETTINGS_DOCTYPE = "Iran Localization Settings"

DEFAULTS = {
	"jalali_display": "Jalali and Gregorian",
	"persian_digits": 0,
	"persian_digits_everywhere": 1,
	"validate_national_id": 1,
	"validate_iban": 1,
	"validate_postal_code": 1,
	"normalize_arabic_letters": 1,
	"vat_rate": 10,
	"moadian_enabled": 0,
	"moadian_memory_id": "",
	"moadian_invoice_type": "1",
	"show_partner_logo": 1,
	"partner_logo": "",
}


def get_settings():
	"""Settings as a dict; falls back to DEFAULTS before the doctype is installed."""
	try:
		doc = frappe.get_cached_doc(SETTINGS_DOCTYPE)
	except Exception:
		return frappe._dict(DEFAULTS)
	values = frappe._dict(DEFAULTS)
	for key in DEFAULTS:
		value = doc.get(key)
		if value is not None:
			values[key] = value
	return values

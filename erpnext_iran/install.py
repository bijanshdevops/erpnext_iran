import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from erpnext_iran.setup.custom_fields import delete_custom_fields, setup_custom_fields

# Persian names for the Rial and the currencies Iranian businesses deal in most. Stored in the
# Currency custom field ir_local_name, which currency pickers search and show under the code.
CURRENCY_NAMES_FA = {
	"IRR": "ریال ایران",
	"USD": "دلار آمریکا",
	"EUR": "یورو",
	"GBP": "پوند انگلیس",
	"AED": "درهم امارات",
	"CNY": "یوان چین",
	"TRY": "لیر ترکیه",
	"IQD": "دینار عراق",
	"AFN": "افغانی افغانستان",
	"RUB": "روبل روسیه",
	"INR": "روپیه هند",
	"PKR": "روپیه پاکستان",
	"JPY": "ین ژاپن",
	"KRW": "وون کره جنوبی",
	"CHF": "فرانک سوئیس",
	"CAD": "دلار کانادا",
	"AUD": "دلار استرالیا",
	"SAR": "ریال عربستان",
	"QAR": "ریال قطر",
	"OMR": "ریال عمان",
	"KWD": "دینار کویت",
	"BHD": "دینار بحرین",
	"AMD": "درام ارمنستان",
	"AZN": "منات آذربایجان",
	"TMT": "منات ترکمنستان",
	"MYR": "رینگیت مالزی",
}


def after_install():
	setup_custom_fields()
	setup_currency()
	setup_currency_names()


def after_migrate():
	setup_custom_fields()
	setup_currency_names()


def before_uninstall():
	frappe.db.delete("Property Setter", {"doc_type": "Currency", "property": "search_fields", "value": "ir_local_name"})
	delete_custom_fields()


def setup_currency():
	"""Rial has no fractional unit in practice; show it as 1,234,567. Install time only, so a
	format the user changes later is kept."""
	if not frappe.db.exists("Currency", "IRR"):
		frappe.get_doc(
			{"doctype": "Currency", "currency_name": "IRR", "symbol": "﷼", "enabled": 1}
		).insert(ignore_permissions=True)
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


def setup_currency_names():
	"""Keep the Rial enabled, fill empty Persian names and let currency pickers search them."""
	if frappe.db.exists("Currency", "IRR"):
		frappe.db.set_value("Currency", "IRR", "enabled", 1)
	for code, name in CURRENCY_NAMES_FA.items():
		if frappe.db.exists("Currency", code) and not frappe.db.get_value("Currency", code, "ir_local_name"):
			frappe.db.set_value("Currency", code, "ir_local_name", name, update_modified=False)
	make_property_setter("Currency", None, "search_fields", "ir_local_name", "Data", for_doctype=True)
	frappe.clear_cache(doctype="Currency")

app_name = "erpnext_iran"
app_title = "ERPNext Iran"
app_publisher = "ERPNext Iran Contributors"
app_description = "Iranian localization for ERPNext"
app_email = "info@example.com"
app_license = "GPL-3.0"
required_apps = ["erpnext"]

app_include_js = "erpnext_iran.bundle.js"
app_include_css = "erpnext_iran.bundle.css"

doctype_js = {
	"Company": "public/js/company.js",
	"Holiday List": "public/js/holiday_list.js",
	"Sales Invoice": "public/js/sales_invoice.js",
}

after_install = "erpnext_iran.install.after_install"
after_migrate = "erpnext_iran.install.after_migrate"
before_uninstall = "erpnext_iran.install.before_uninstall"

boot_session = "erpnext_iran.boot.boot_session"
update_website_context = "erpnext_iran.boot.update_website_context"

doc_events = {
	"Customer": {
		"before_insert": "erpnext_iran.doc_events.party.normalize_names",
		"validate": "erpnext_iran.doc_events.party.validate_party",
	},
	"Supplier": {
		"before_insert": "erpnext_iran.doc_events.party.normalize_names",
		"validate": "erpnext_iran.doc_events.party.validate_party",
	},
	"Company": {
		"before_insert": "erpnext_iran.doc_events.party.normalize_names",
		"validate": "erpnext_iran.doc_events.party.validate_party",
	},
	"Item": {"validate": "erpnext_iran.doc_events.item.validate_item"},
	"Bank Account": {"validate": "erpnext_iran.doc_events.bank.validate_bank_account"},
	"Address": {"validate": "erpnext_iran.doc_events.address.validate_address"},
	"Sales Invoice": {
		"validate": "erpnext_iran.doc_events.sales_invoice.validate",
		"on_submit": "erpnext_iran.doc_events.sales_invoice.on_submit",
	},
}

jinja = {
	"methods": [
		"erpnext_iran.utils.jinja.jalali_date",
		"erpnext_iran.utils.jinja.persian_digits",
		"erpnext_iran.utils.jinja.amount_in_words_fa",
		"erpnext_iran.utils.jinja.ir_invoice_lines",
		"erpnext_iran.utils.jinja.ir_invoice_totals",
	],
	"filters": [
		"erpnext_iran.utils.jinja.jalali_date",
		"erpnext_iran.utils.jinja.persian_digits",
	],
}

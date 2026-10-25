from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

PERSON_TYPES = "\nNatural Person\nLegal Entity\nCivil Partnership\nForeign National"


def _party_fields(insert_after):
	return [
		{
			"fieldname": "ir_section",
			"label": "Iran Tax Details",
			"fieldtype": "Section Break",
			"insert_after": insert_after,
			"collapsible": 1,
		},
		{
			"fieldname": "ir_person_type",
			"label": "Person Type",
			"fieldtype": "Select",
			"options": PERSON_TYPES,
			"insert_after": "ir_section",
		},
		{
			"fieldname": "ir_national_id",
			"label": "National ID",
			"fieldtype": "Data",
			"length": 12,
			"description": "National code (10 digits) or legal national ID (11 digits)",
			"insert_after": "ir_person_type",
		},
		{
			"fieldname": "ir_column_break",
			"fieldtype": "Column Break",
			"insert_after": "ir_national_id",
		},
		{
			"fieldname": "ir_economic_code",
			"label": "Economic Code",
			"fieldtype": "Data",
			"length": 14,
			"insert_after": "ir_column_break",
		},
		{
			"fieldname": "ir_registration_number",
			"label": "Registration Number",
			"fieldtype": "Data",
			"insert_after": "ir_economic_code",
		},
	]


def get_custom_fields():
	company_fields = _party_fields("tax_id") + [
		{
			"fieldname": "ir_moadian_memory_id",
			"label": "Fiscal Memory ID",
			"fieldtype": "Data",
			"length": 6,
			"description": "Moadian unique fiscal memory ID (overrides Iran Localization Settings)",
			"insert_after": "ir_registration_number",
		}
	]
	return {
		"Customer": _party_fields("tax_id"),
		"Supplier": _party_fields("tax_id"),
		"Company": company_fields,
		"Item": [
			{
				"fieldname": "ir_stuff_id",
				"label": "Moadian Goods/Service ID",
				"fieldtype": "Data",
				"length": 13,
				"description": "13 digit goods/service ID from the Tax Organization catalogue",
				"insert_after": "item_group",
			}
		],
		"UOM": [
			{
				"fieldname": "ir_moadian_unit_code",
				"label": "Moadian Unit Code",
				"fieldtype": "Data",
				"insert_after": "uom_name",
			}
		],
		"Sales Invoice Item": [
			{
				"fieldname": "ir_stuff_id",
				"label": "Moadian Goods/Service ID",
				"fieldtype": "Data",
				"fetch_from": "item_code.ir_stuff_id",
				"fetch_if_empty": 1,
				"insert_after": "item_name",
				"print_hide": 1,
			}
		],
		"Sales Invoice": [
			{
				"fieldname": "ir_section",
				"label": "Iran / Moadian",
				"fieldtype": "Section Break",
				"insert_after": "remarks",
				"collapsible": 1,
			},
			{
				"fieldname": "ir_jalali_posting_date",
				"label": "Jalali Posting Date",
				"fieldtype": "Data",
				"read_only": 1,
				"insert_after": "ir_section",
			},
			{
				"fieldname": "ir_invoice_subject",
				"label": "Invoice Subject",
				"fieldtype": "Select",
				"options": "1\n2\n3\n4",
				"default": "1",
				"description": "1 Original, 2 Correction, 3 Cancellation, 4 Return",
				"insert_after": "ir_jalali_posting_date",
			},
			{
				"fieldname": "ir_column_break",
				"fieldtype": "Column Break",
				"insert_after": "ir_invoice_subject",
			},
			{
				"fieldname": "ir_tax_id",
				"label": "Tax ID",
				"fieldtype": "Data",
				"length": 22,
				"read_only": 1,
				"no_copy": 1,
				"allow_on_submit": 1,
				"insert_after": "ir_column_break",
			},
			{
				"fieldname": "ir_moadian_status",
				"label": "Moadian Status",
				"fieldtype": "Select",
				"options": "\nPending\nSent\nAccepted\nRejected",
				"read_only": 1,
				"no_copy": 1,
				"allow_on_submit": 1,
				"insert_after": "ir_tax_id",
			},
			{
				"fieldname": "ir_moadian_reference",
				"label": "Moadian Reference",
				"fieldtype": "Data",
				"read_only": 1,
				"no_copy": 1,
				"allow_on_submit": 1,
				"insert_after": "ir_moadian_status",
			},
		],
	}


def setup_custom_fields():
	create_custom_fields(get_custom_fields(), ignore_validate=True, update=True)


def delete_custom_fields():
	import frappe

	for doctype, fields in get_custom_fields().items():
		for field in fields:
			frappe.db.delete("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]})
		frappe.clear_cache(doctype=doctype)

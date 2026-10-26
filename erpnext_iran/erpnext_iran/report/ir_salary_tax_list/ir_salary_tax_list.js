frappe.query_reports["IR Salary Tax List"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "jalali_year",
			label: __("Jalali Year"),
			fieldtype: "Int",
			default: erpnext_iran.jalali.fromISO(frappe.datetime.get_today()).jy,
			reqd: 1,
		},
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: erpnext_iran.jalali.MONTH_NAMES.map((name, i) => ({ value: String(i + 1), label: name })),
			default: String(erpnext_iran.jalali.fromISO(frappe.datetime.get_today()).jm),
			reqd: 1,
		},
		{ fieldname: "include_drafts", label: __("Include Draft Slips"), fieldtype: "Check" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		return data && data.bold ? `<b>${value}</b>` : value;
	},
};

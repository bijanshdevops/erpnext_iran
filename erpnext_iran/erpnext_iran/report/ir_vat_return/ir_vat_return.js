// Seasonal VAT return; dates are picked as a Jalali year and season.
(function () {
	const today = erpnext_iran.jalali.fromISO(frappe.datetime.get_today());
	const seasons = ["Spring", "Summer", "Autumn", "Winter"];

	frappe.query_reports["IR VAT Return"] = {
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
				default: today.jy,
				reqd: 1,
			},
			{
				fieldname: "season",
				label: __("Season"),
				fieldtype: "Select",
				options: [
					...seasons.map((s) => ({ value: s, label: __(s) })),
					{ value: "Whole Year", label: __("Whole Year") },
				],
				default: seasons[Math.ceil(today.jm / 3) - 1],
				reqd: 1,
			},
			{
				fieldname: "view",
				label: __("View"),
				fieldtype: "Select",
				options: [
					{ value: "Summary", label: __("Summary") },
					{ value: "Sales by Party", label: __("Sales by Party") },
					{ value: "Purchases by Party", label: __("Purchases by Party") },
				],
				default: "Summary",
			},
			{
				fieldname: "vat_output_account",
				label: __("VAT Output Account"),
				fieldtype: "Link",
				options: "Account",
				get_query: () => ({
					filters: { company: frappe.query_report.get_filter_value("company"), is_group: 0 },
				}),
			},
			{
				fieldname: "vat_input_account",
				label: __("VAT Input Account"),
				fieldtype: "Link",
				options: "Account",
				get_query: () => ({
					filters: { company: frappe.query_report.get_filter_value("company"), is_group: 0 },
				}),
			},
		],
		formatter(value, row, column, data, default_formatter) {
			value = default_formatter(value, row, column, data);
			return data && data.bold ? `<b>${value}</b>` : value;
		},
	};
})();

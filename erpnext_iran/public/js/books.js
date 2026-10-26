// Shared filters and the "Print Legal Book" button of the IR Journal Book and IR General
// Ledger Book reports.
frappe.provide("erpnext_iran.books");

erpnext_iran.books.filters = function (extra = []) {
	const today = erpnext_iran.jalali.fromISO(frappe.datetime.get_today());
	const periods = [
		{ value: "Whole Year", label: __("Whole Year") },
		...["Spring", "Summer", "Autumn", "Winter"].map((s) => ({ value: s, label: __(s) })),
		...erpnext_iran.jalali.MONTH_NAMES.map((name, i) => ({ value: String(i + 1), label: name })),
	];
	return [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{ fieldname: "jalali_year", label: __("Jalali Year"), fieldtype: "Int", default: today.jy, reqd: 1 },
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: periods,
			default: String(today.jm),
			reqd: 1,
		},
		{
			fieldname: "level",
			label: __("Account Level"),
			fieldtype: "Select",
			options: [
				{ value: "General", label: __("General Account") },
				{ value: "Subsidiary", label: __("Subsidiary Account") },
			],
			default: "General",
			reqd: 1,
		},
		...extra,
	];
};

erpnext_iran.books.setup = function (book) {
	return {
		onload(report) {
			report.page.add_inner_button(__("Print Legal Book"), () => {
				const params = new URLSearchParams({
					book,
					filters: JSON.stringify(report.get_filter_values(true)),
				});
				window.open(frappe.urllib.get_full_url(`/api/method/erpnext_iran.books.api.download_pdf?${params}`));
			});
		},
		formatter(value, row, column, data, default_formatter) {
			value = default_formatter(value, row, column, data);
			return data && data.bold ? `<b>${value}</b>` : value;
		},
	};
};

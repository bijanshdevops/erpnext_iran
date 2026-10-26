frappe.query_reports["IR General Ledger Book"] = {
	filters: erpnext_iran.books.filters([
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "Link",
			options: "Account",
			get_query: () => ({ filters: { company: frappe.query_report.get_filter_value("company") } }),
		},
	]),
	...erpnext_iran.books.setup("ledger"),
};

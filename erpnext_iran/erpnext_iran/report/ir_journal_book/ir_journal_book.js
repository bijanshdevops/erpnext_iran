frappe.query_reports["IR Journal Book"] = {
	filters: erpnext_iran.books.filters(),
	...erpnext_iran.books.setup("journal"),
};

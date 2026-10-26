frappe.query_reports["IR Cheque Register"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "cheque_type",
			label: __("Cheque Type"),
			fieldtype: "Select",
			options: [
				{ value: "", label: "" },
				{ value: "Received", label: __("Received") },
				{ value: "Issued", label: __("Issued") },
			],
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: ["", "Open", "Received", "Deposited", "Cleared", "Bounced", "Endorsed", "Issued"].map((s) => ({
				value: s,
				label: s ? __(s === "Open" ? "Open Cheques" : s) : "",
			})),
			default: "Open",
		},
		{ fieldname: "from_date", label: __("Due From"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("Due To"), fieldtype: "Date" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "days_to_due" && data && data.days_to_due !== null && data.days_to_due < 0) {
			return `<span style="color: var(--red-500)">${value}</span>`;
		}
		if (column.fieldname === "status_label" && data && data.status === "Bounced") {
			return `<span style="color: var(--red-500)">${value}</span>`;
		}
		return value;
	},
};

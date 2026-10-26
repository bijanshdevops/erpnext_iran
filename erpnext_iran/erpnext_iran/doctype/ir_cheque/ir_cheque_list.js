frappe.listview_settings["IR Cheque"] = {
	add_fields: ["status", "cheque_type", "due_date"],
	get_indicator(doc) {
		const colors = {
			Draft: "gray",
			Received: "blue",
			Deposited: "orange",
			Cleared: "green",
			Bounced: "red",
			Endorsed: "purple",
			Issued: "blue",
			Cancelled: "gray",
		};
		return [__(doc.status), colors[doc.status] || "gray", `status,=,${doc.status}`];
	},
};

frappe.ui.form.on("Iran Localization Settings", {
	refresh(frm) {
		// URL and file paths read left to right in the RTL desk
		for (const field of ["moadian_api_url", "moadian_private_key_path", "moadian_certificate_path"]) {
			frm.fields_dict[field].$input.attr("dir", "ltr");
		}
		if (!frm.doc.moadian_enabled) return;
		frm.add_custom_button(__("Test Moadian Connection"), async () => {
			const { message } = await frappe.call({
				method: "erpnext_iran.moadian.sender.test_connection",
				freeze: true,
				freeze_message: __("Connecting to Moadian..."),
			});
			frappe.msgprint({
				title: __("Connected to Moadian"),
				indicator: "green",
				message: `<pre dir="ltr" style="text-align:left">${frappe.utils.escape_html(
					JSON.stringify(message, null, 2)
				)}</pre>`,
			});
		});
	},
	after_save() {
		frappe.show_alert({ message: __("Reload the page to apply display changes"), indicator: "blue" });
	},
});

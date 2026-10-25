frappe.ui.form.on("Iran Localization Settings", {
	after_save() {
		frappe.show_alert({ message: __("Reload the page to apply display changes"), indicator: "blue" });
	},
});

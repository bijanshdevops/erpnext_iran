frappe.ui.form.on("Company", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Iran Setup"), () => erpnext_iran.company_setup_dialog(frm), __("Manage"));
	},
});

erpnext_iran.company_setup_dialog = function (frm) {
	const today = erpnext_iran.jalali.fromISO(frappe.datetime.get_today());
	const company_filter = () => ({ filters: { company: frm.doc.name, is_group: 0, account_type: "Tax" } });

	const dialog = new frappe.ui.Dialog({
		title: __("Iran Setup for {0}", [frm.doc.name]),
		fields: [
			{
				fieldname: "apply_chart",
				fieldtype: "Check",
				label: __("Replace chart of accounts with the Iranian standard chart"),
				description: __(
					"Deletes the current accounts and tax templates. Only possible before any transaction."
				),
			},
			{ fieldtype: "Section Break", label: __("Value Added Tax") },
			{ fieldname: "create_taxes", fieldtype: "Check", label: __("Create VAT templates"), default: 1 },
			{ fieldname: "vat_rate", fieldtype: "Percent", label: __("VAT Rate"), depends_on: "create_taxes" },
			{
				fieldname: "vat_output_account",
				fieldtype: "Link",
				options: "Account",
				label: __("VAT Output Account"),
				description: __("Leave empty when using the Iranian chart"),
				depends_on: "eval:doc.create_taxes && !doc.apply_chart",
				get_query: company_filter,
			},
			{
				fieldname: "vat_input_account",
				fieldtype: "Link",
				options: "Account",
				label: __("VAT Input Account"),
				depends_on: "eval:doc.create_taxes && !doc.apply_chart",
				get_query: company_filter,
			},
			{ fieldtype: "Section Break", label: __("Calendar") },
			{
				fieldname: "jalali_year",
				fieldtype: "Int",
				label: __("Jalali Fiscal Year"),
				default: today ? today.jy : null,
				description: __("Creates Fiscal Year from 1 Farvardin to the end of Esfand"),
			},
			{
				fieldname: "create_holiday_list",
				fieldtype: "Check",
				label: __("Create Holiday List (Fridays and official solar holidays)"),
				default: 1,
				depends_on: "jalali_year",
			},
			{
				fieldname: "include_thursday",
				fieldtype: "Check",
				label: __("Thursday is also a weekly holiday"),
				depends_on: "create_holiday_list",
			},
		],
		primary_action_label: __("Run"),
		primary_action(values) {
			const run = () =>
				frappe
					.call({
						method: "erpnext_iran.setup.api.setup_company",
						args: Object.assign({ company: frm.doc.name }, values),
						freeze: true,
						freeze_message: __("Setting up..."),
					})
					.then((r) => {
						dialog.hide();
						frappe.msgprint({
							title: __("Done"),
							indicator: "green",
							message: (r.message || []).join("<br>"),
						});
						frm.reload_doc();
					});

			if (values.apply_chart) {
				frappe.confirm(__("All existing accounts of {0} will be deleted. Continue?", [frm.doc.name]), run);
			} else {
				run();
			}
		},
	});
	dialog.show();
};

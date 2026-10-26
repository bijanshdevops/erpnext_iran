frappe.ui.form.on("IR Payroll Year", {
	refresh(frm) {
		frm.add_custom_button(__("Set Up Iranian Payroll"), () => {
			frappe.prompt(
				[
					{
						fieldname: "company",
						label: __("Company"),
						fieldtype: "Link",
						options: "Company",
						reqd: 1,
						default: frappe.defaults.get_user_default("Company"),
					},
				],
				async ({ company }) => {
					const { message: structure } = await frappe.call({
						method: "erpnext_iran.payroll.setup.setup_iran_payroll",
						args: { company },
						freeze: true,
					});
					frappe.msgprint({
						title: __("Iranian Payroll"),
						indicator: "green",
						message: __(
							"Salary components and the salary structure {0} are ready. Assign it to employees with their daily wage as the base.",
							[`<a href="/app/salary-structure/${encodeURIComponent(structure)}">${frappe.utils.escape_html(structure)}</a>`]
						),
					});
				},
				__("Set Up Iranian Payroll")
			);
		});
	},
});

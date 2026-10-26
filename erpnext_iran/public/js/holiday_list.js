frappe.ui.form.on("Holiday List", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Add Iranian Holidays"), () => {
			const start = erpnext_iran.jalali.fromISO(frm.doc.from_date);
			frappe.prompt(
				[
					{
						fieldname: "jalali_year",
						fieldtype: "Int",
						label: __("Jalali Year"),
						default: start ? start.jy : null,
						reqd: 1,
					},
					{
						fieldname: "include_thursday",
						fieldtype: "Check",
						label: __("Thursday is also a weekly holiday"),
					},
				],
				(values) => {
					frappe
						.call({
							method: "erpnext_iran.setup.api.add_iran_holidays",
							args: Object.assign({ holiday_list: frm.doc.name }, values),
							freeze: true,
						})
						.then((r) => {
							const { added, lunar_estimated } = r.message;
							if (lunar_estimated) {
								frappe.msgprint({
									title: __("Lunar holidays are estimated"),
									message: __(
										"{0} holidays added. The official calendar of {1} is not in the system yet, so the lunar holidays (marked «پیش‌بینی») are estimated and can be a day off. Check them against the official calendar once it is published.",
										[added, values.jalali_year]
									),
									indicator: "orange",
								});
							} else {
								frappe.show_alert({
									message: __("{0} holidays added, lunar holidays from the official calendar.", [added]),
									indicator: "green",
								});
							}
							frm.reload_doc();
						});
				},
				__("Add Iranian Holidays")
			);
		});
	},
});

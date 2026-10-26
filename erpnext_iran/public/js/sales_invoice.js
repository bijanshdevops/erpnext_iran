frappe.ui.form.on("Sales Invoice", {
	refresh(frm) {
		if (frm.doc.docstatus !== 1 || !frm.doc.ir_tax_id) return;
		const status = frm.doc.ir_moadian_status;
		const run = (method, label) =>
			frm.add_custom_button(
				__(label),
				async () => {
					const { message } = await frappe.call({
						method: `erpnext_iran.moadian.sender.${method}`,
						args: { sales_invoice: frm.doc.name },
						freeze: true,
					});
					frappe.show_alert({
						message: __("Moadian Status: {0}", [__(message.ir_moadian_status || "")]),
						indicator: { Accepted: "green", Rejected: "red", Sent: "blue" }[message.ir_moadian_status] || "orange",
					});
					frm.reload_doc();
				},
				__("Moadian")
			);
		if (["Pending", "Rejected"].includes(status)) run("send_to_moadian", "Send to Moadian");
		if (status === "Sent") run("check_moadian_status", "Check Moadian Status");
		frm.add_custom_button(__("Moadian Payload"), () => {
			frappe
				.call({
					method: "erpnext_iran.moadian.api.get_moadian_payload",
					args: { sales_invoice: frm.doc.name },
				})
				.then((r) => {
					const { payload, problems } = r.message;
					const dialog = new frappe.ui.Dialog({
						title: __("Moadian Payload"),
						size: "large",
						fields: [
							{
								fieldname: "problems",
								fieldtype: "HTML",
								options: problems.length
									? `<div class="alert alert-warning">${problems
											.map(frappe.utils.escape_html)
											.join("<br>")}</div>`
									: `<div class="alert alert-success">${__("Ready to send")}</div>`,
							},
							{
								fieldname: "json",
								fieldtype: "Code",
								options: "JSON",
								read_only: 1,
								default: JSON.stringify(payload, null, 2),
							},
						],
					});
					// JSON must stay left-to-right inside the RTL (Persian) desk
					dialog.fields_dict.json.$wrapper.attr("dir", "ltr").css("text-align", "left");
					dialog.show();
				});
		}, __("Moadian"));
	},
});

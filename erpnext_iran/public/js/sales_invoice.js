frappe.ui.form.on("Sales Invoice", {
	refresh(frm) {
		if (frm.doc.docstatus !== 1 || !frm.doc.ir_tax_id) return;
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
		});
	},
});

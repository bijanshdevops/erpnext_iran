// Received / issued cheque: status buttons post the Journal Entry of each step.
const IR_CHEQUE_ACTIONS = {
	deposit: { label: "Deposit to Bank", bank: true },
	clear: { label: "Clear Cheque", bank: true },
	bounce: { label: "Bounce Cheque" },
	endorse: { label: "Endorse to Supplier", endorsee: true },
};

frappe.ui.form.on("IR Cheque", {
	setup(frm) {
		const account_query = () => ({ filters: { company: frm.doc.company, is_group: 0 } });
		["notes_account", "in_collection_account"].forEach((f) => frm.set_query(f, account_query));
		frm.set_query("bank_account", () => ({
			filters: { company: frm.doc.company, is_group: 0, account_type: "Bank" },
		}));
		frm.set_query("cheque_book", () => ({ filters: { company: frm.doc.company, disabled: 0 } }));
	},

	cheque_type(frm) {
		frm.set_value("party_type", frm.doc.cheque_type === "Issued" ? "Supplier" : "Customer");
		["notes_account", "in_collection_account"].forEach((f) => frm.set_value(f, ""));
	},

	party_type(frm) {
		frm.set_value("party", "");
	},

	async refresh(frm) {
		frm.set_intro("");
		if (frm.doc.docstatus === 0 && !frm.is_new()) {
			frm.set_intro(__("Submitting registers the cheque and books it into the notes account."));
		}
		if (frm.doc.docstatus !== 1) return;
		const { message: actions } = await frappe.call({
			method: "erpnext_iran.erpnext_iran.doctype.ir_cheque.ir_cheque.get_actions",
			args: { name: frm.doc.name },
		});
		(actions || []).forEach((action) => {
			frm.add_custom_button(__(IR_CHEQUE_ACTIONS[action].label), () => ir_cheque_movement(frm, action), __("Cheque"));
		});
	},
});

function ir_cheque_movement(frm, action) {
	const spec = IR_CHEQUE_ACTIONS[action];
	const fields = [
		{ fieldname: "posting_date", label: __("Posting Date"), fieldtype: "Date", reqd: 1, default: frappe.datetime.get_today() },
	];
	if (spec.bank) {
		fields.push({
			fieldname: "bank_account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: "Account",
			reqd: 1,
			default: frm.doc.bank_account,
			get_query: () => ({ filters: { company: frm.doc.company, is_group: 0, account_type: "Bank" } }),
		});
	}
	if (spec.endorsee) {
		fields.push({ fieldname: "endorsee", label: __("Supplier"), fieldtype: "Link", options: "Supplier", reqd: 1 });
	}
	const dialog = new frappe.ui.Dialog({
		title: __(spec.label),
		fields,
		primary_action_label: __(spec.label),
		async primary_action(values) {
			dialog.hide();
			const { message } = await frappe.call({
				method: "erpnext_iran.erpnext_iran.doctype.ir_cheque.ir_cheque.make_movement",
				args: { name: frm.doc.name, action, ...values },
				freeze: true,
			});
			frappe.show_alert({
				message: __("Cheque is now {0}; Journal Entry {1}", [__(message.status), message.journal_entry]),
				indicator: "green",
			});
			frm.reload_doc();
		},
	});
	dialog.show();
}

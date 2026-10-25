// Desk integration: Jalali display for Date/Datetime values and a Jalali entry helper
// under every date control. Display mode comes from Iran Localization Settings (boot).
frappe.provide("erpnext_iran");

(function () {
	const J = erpnext_iran.jalali;

	const settings = () => (frappe.boot && frappe.boot.erpnext_iran) || {};
	const mode = () => settings().jalali_display || "Off"; // Off | Jalali | Jalali and Gregorian
	const usePersianDigits = () => !!settings().persian_digits;

	erpnext_iran.format_jalali = function (value, with_time) {
		const j = J.fromISO(value);
		if (!j) return "";
		let out = J.format(value, "YYYY/MM/DD");
		if (with_time && j.time) out += " " + j.time.slice(0, 5);
		return usePersianDigits() ? J.toPersianDigits(out) : out;
	};

	function wrapFormatter(fieldtype, with_time) {
		const original = frappe.form.formatters[fieldtype];
		if (!original) return;
		frappe.form.formatters[fieldtype] = function (value, docfield, options, doc) {
			const formatted = original.apply(this, arguments);
			if (!value || mode() === "Off") return formatted;
			const jalali = erpnext_iran.format_jalali(value, with_time);
			if (!jalali) return formatted;
			// dir="ltr" isolates digits and parentheses from the RTL layout around them
			const date = `<span class="ir-date" dir="ltr">${jalali}</span>`;
			if (mode() === "Jalali") return date;
			return `${date} <span class="ir-date ir-gregorian text-muted" dir="ltr">(${formatted})</span>`;
		};
	}

	wrapFormatter("Date", false);
	wrapFormatter("Datetime", true);

	// ---- Hint + Jalali entry dialog under date inputs ----
	erpnext_iran.prompt_jalali_date = function (control) {
		const current = control.get_value();
		frappe.prompt(
			[
				{
					fieldname: "jalali",
					fieldtype: "Data",
					label: __("Jalali Date"),
					description: __("Example: 1403/01/15"),
					default: current ? J.format(current, "YYYY/MM/DD") : "",
					reqd: 1,
				},
			],
			(values) => {
				const iso = J.parse(values.jalali);
				if (!iso) {
					frappe.msgprint(__("Invalid Jalali date"));
					return;
				}
				control.set_value(iso);
			},
			__("Enter Jalali Date"),
			__("Set")
		);
	};

	function renderHint(control) {
		if (mode() === "Off" || !control.$input || !control.$wrapper) return;
		let $hint = control.$wrapper.find(".ir-jalali-hint");
		if (!$hint.length) {
			$hint = $(`<div class="ir-jalali-hint text-muted small">
				<span class="ir-jalali-text"></span>
				<a class="ir-jalali-pick" title="${__("Enter Jalali Date")}">${__("Jalali")}</a>
			</div>`);
			$hint.insertAfter(control.$input);
			$hint.find(".ir-jalali-pick").on("click", () => erpnext_iran.prompt_jalali_date(control));
		}
		const value = control.get_value && control.get_value();
		const text = value ? erpnext_iran.format_jalali(value, control.df.fieldtype === "Datetime") : "";
		$hint.find(".ir-jalali-text").text(text ? J.format(value, "dddd") + " " + text : "");
		$hint.toggle(!control.df.read_only);
	}

	const ControlDate = frappe.ui.form.ControlDate;
	if (ControlDate) {
		const original = ControlDate.prototype.set_formatted_input;
		ControlDate.prototype.set_formatted_input = function () {
			const result = original.apply(this, arguments);
			try {
				renderHint(this);
			} catch (e) {
				console.warn("erpnext_iran: jalali hint failed", e);
			}
			return result;
		};
	}
})();

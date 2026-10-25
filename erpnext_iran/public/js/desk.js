// Desk integration: Jalali display for Date/Datetime values and Jalali input and picker in
// Date/Datetime controls. Display mode comes from Iran Localization Settings (boot).
frappe.provide("erpnext_iran");

(function () {
	const J = erpnext_iran.jalali;

	const settings = () => (frappe.boot && frappe.boot.erpnext_iran) || {};
	const mode = () => settings().jalali_display || "Off"; // Off | Jalali | Jalali and Gregorian
	const usePersianDigits = () => !!settings().persian_digits;

	// font-level Persian digits (erpnext_iran.bundle.scss, html.ir-fa-digits)
	const applyDigitClass = () =>
		document.documentElement.classList.toggle("ir-fa-digits", !!settings().persian_digits_everywhere);
	applyDigitClass();
	$(document).on("app_ready", applyDigitClass);

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

	// ---- Jalali Date / Datetime controls ----
	// With Jalali display on, Date and Datetime inputs show and accept Jalali dates and open the
	// Jalali picker (jalali_picker.js). The model value stays Gregorian, so nothing stored changes.
	// Time controls (also ControlDate subclasses) keep Frappe's own picker.
	const P = erpnext_iran.jalali_picker;
	const jalaliControl = (control) =>
		mode() !== "Off" && !control.timepicker_only && ["Date", "Datetime"].includes(control.df.fieldtype);

	const digits = (text) => (usePersianDigits() ? J.toPersianDigits(text) : text);
	const toIso = (value) => (value instanceof Date ? moment(value).format("YYYY-MM-DD HH:mm:ss") : String(value));

	// Gregorian date (and weekday) under the input, since the input itself is now Jalali
	function renderHint(control) {
		if (!jalaliControl(control) || !control.$input || !control.$wrapper) return;
		let $hint = control.$wrapper.find(".ir-jalali-hint");
		if (!$hint.length) {
			$hint = $(`<div class="ir-jalali-hint text-muted small"></div>`).insertAfter(control.$input);
		}
		const value = control.get_value && control.get_value();
		let text = "";
		if (value) {
			text = J.format(String(value), "dddd");
			if (mode() === "Jalali and Gregorian") {
				const gregorian = frappe.datetime.str_to_user(value, false, control.df.fieldtype === "Date");
				text += ` · <span class="ir-date" dir="ltr">${frappe.utils.escape_html(gregorian)}</span>`;
			}
		}
		$hint.html(text).toggle(!!text && !control.df.read_only);
	}

	function override(Control, name, make) {
		if (!Control) return;
		const original = Control.prototype[name];
		Control.prototype[name] = make(original);
	}

	const ControlDate = frappe.ui.form.ControlDate;
	const ControlDatetime = frappe.ui.form.ControlDatetime;

	// ControlDatetime.set_datepicker calls this through super, so one override covers both
	override(ControlDate, "set_datepicker", (original) =>
		function () {
			if (!jalaliControl(this)) return original.apply(this, arguments);
			P.attach(this);
		}
	);

	override(ControlDate, "format_for_input", (original) =>
		function (value) {
			if (!jalaliControl(this) || !value) return original.apply(this, arguments);
			return digits(J.format(toIso(value).slice(0, 10), "YYYY/MM/DD"));
		}
	);

	override(ControlDate, "parse", (original) =>
		function (value) {
			const parsed = jalaliControl(this) && P.parseInput(value);
			return parsed ? parsed.date : original.apply(this, arguments);
		}
	);

	override(ControlDatetime, "format_for_input", (original) =>
		function (value) {
			const user_value = original.apply(this, arguments); // user time zone, user format
			if (!jalaliControl(this) || !user_value) return user_value;
			const iso = frappe.datetime.user_to_str(user_value, false);
			return digits(`${J.format(iso.slice(0, 10), "YYYY/MM/DD")} ${iso.slice(11, 19)}`);
		}
	);

	override(ControlDatetime, "parse", (original) =>
		function (value) {
			const parsed = jalaliControl(this) && P.parseInput(value);
			if (!parsed) return original.apply(this, arguments);
			let result = `${parsed.date} ${parsed.time || "00:00:00"}`;
			if (!frappe.datetime.is_system_time_zone()) {
				result = frappe.datetime.convert_to_system_tz(result, true);
			}
			return result;
		}
	);

	for (const Control of [ControlDate, ControlDatetime]) {
		override(Control, "set_formatted_input", (original) =>
			function () {
				const result = original.apply(this, arguments);
				try {
					renderHint(this);
				} catch (e) {
					console.warn("erpnext_iran: jalali hint failed", e);
				}
				return result;
			}
		);
	}
})();

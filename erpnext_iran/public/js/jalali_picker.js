// Jalali date picker for the desk's Date and Datetime controls.
// Calendar math (monthGrid, parseInput) is DOM-free and exported for node tests; the popup
// works on the control's model value, which stays a Gregorian "YYYY-MM-DD[ HH:mm:ss]".
(function (root) {
	"use strict";

	const J = (root && root.erpnext_iran && root.erpnext_iran.jalali) || require("./jalali.js");
	const DAY_MS = 864e5;
	const WEEKDAY_SHORT = ["ش", "ی", "د", "س", "چ", "پ", "ج"]; // Saturday first

	const pad = (n) => String(n).padStart(2, "0");
	const isoOf = (gy, gm, gd) => `${gy}-${pad(gm)}-${pad(gd)}`;

	// 42 cells (6 weeks, Saturday first) covering Jalali month jy/jm.
	function monthGrid(jy, jm) {
		const g = J.toGregorian(jy, jm, 1);
		const first = Date.UTC(g.gy, g.gm - 1, g.gd);
		const offset = (new Date(first).getUTCDay() + 1) % 7; // Sat=0 ... Fri=6
		const cells = [];
		for (let i = 0; i < 42; i++) {
			const d = new Date(first + (i - offset) * DAY_MS);
			const iso = isoOf(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate());
			const j = J.fromISO(iso);
			cells.push({ iso, jy: j.jy, jm: j.jm, jd: j.jd, inMonth: j.jm === jm, column: i % 7 });
		}
		return cells;
	}

	// "1405/08/03", "۱۴۰۵-۸-۳ 14:05" -> { date: "2026-10-25", time: "14:05:00" } or null.
	// Only 4-digit Jalali years 1200..1599 match, so Gregorian input falls through untouched.
	function parseInput(text) {
		const m = /^\s*(\d{4})[\/\-.](\d{1,2})[\/\-.](\d{1,2})(?:[\sT]+(\d{1,2}):(\d{2})(?::(\d{2}))?)?\s*$/.exec(
			J.toEnglishDigits(text || "")
		);
		if (!m) return null;
		const [jy, jm, jd] = [+m[1], +m[2], +m[3]];
		if (jy < 1200 || jy > 1599 || !J.isValid(jy, jm, jd)) return null;
		const g = J.toGregorian(jy, jm, jd);
		let time = "";
		if (m[4] !== undefined) {
			const [h, i, s] = [+m[4], +m[5], +(m[6] || 0)];
			if (h > 23 || i > 59 || s > 59) return null;
			time = `${pad(h)}:${pad(i)}:${pad(s)}`;
		}
		return { date: isoOf(g.gy, g.gm, g.gd), time };
	}

	const api = { monthGrid, parseInput, WEEKDAY_SHORT };
	if (typeof module !== "undefined" && module.exports) module.exports = api;
	if (!root || !root.document) return;

	// ------------------------------------------------------------------ popup (browser only)
	const fa = (n) => J.toPersianDigits(n);
	let popup = null;
	let active = null; // { control, view: {jy, jm}, time }

	function ensurePopup() {
		if (popup) return popup;
		popup = root.document.createElement("div");
		popup.className = "ir-jpicker";
		popup.setAttribute("dir", "rtl");
		popup.hidden = true;
		// keep focus in the input while clicking inside the picker
		popup.addEventListener("mousedown", (e) => {
			if (!e.target.closest("input, select")) e.preventDefault();
		});
		popup.addEventListener("click", onClick);
		popup.addEventListener("change", onChange);
		root.document.body.appendChild(popup);
		// frappe/form/grid_row.js expects an open ".datepicker.active" element when a Date cell
		// is tapped on a touch screen; without the stock datepicker it would throw.
		const placeholder = root.document.createElement("div");
		placeholder.className = "datepicker active ir-jpicker-placeholder";
		placeholder.hidden = true;
		root.document.body.appendChild(placeholder);

		root.document.addEventListener("mousedown", (e) => {
			if (active && !popup.contains(e.target) && e.target !== active.control.$input[0]) close();
		});
		root.document.addEventListener("keydown", (e) => {
			if (active && e.key === "Escape") close();
		});
		root.addEventListener("resize", () => active && position());
		root.addEventListener("scroll", (e) => active && !popup.contains(e.target) && position(), true);
		return popup;
	}

	const isDatetime = (control) => control.df.fieldtype === "Datetime";

	function selectedIso(control) {
		const value = control.get_value && control.get_value();
		if (!value) return "";
		return isDatetime(control) ? value.slice(0, 10) : String(value).slice(0, 10);
	}

	function limits(control) {
		const opts = control.get_df_options ? control.get_df_options() : {};
		const toIso = (d) => (d ? (d instanceof Date ? moment(d).format("YYYY-MM-DD") : String(d).slice(0, 10)) : "");
		return {
			min: toIso(control.df.min_date || opts.minDate),
			max: toIso(control.df.max_date || opts.maxDate),
			disabled: control.df.disabled_dates || [],
		};
	}

	function render() {
		const { control, view } = active;
		const today = frappe.datetime.get_today();
		const selected = selectedIso(control);
		const lim = limits(control);
		const years = [];
		for (let y = view.jy - 60; y <= view.jy + 20; y++) years.push(y);

		const days = monthGrid(view.jy, view.jm)
			.map((c) => {
				const off =
					(lim.min && c.iso < lim.min) || (lim.max && c.iso > lim.max) || lim.disabled.includes(c.iso);
				const cls = [
					"ir-jp-day",
					c.inMonth ? "" : "ir-jp-other",
					c.iso === today ? "ir-jp-today" : "",
					c.iso === selected ? "ir-jp-selected" : "",
					c.column === 6 ? "ir-jp-friday" : "",
				].join(" ");
				return `<button type="button" class="${cls}" data-iso="${c.iso}" ${off ? "disabled" : ""}>${fa(c.jd)}</button>`;
			})
			.join("");

		popup.innerHTML = `
			<div class="ir-jp-head">
				<button type="button" class="ir-jp-nav" data-step="-1" aria-label="${__("Previous")}">›</button>
				<select class="ir-jp-month" aria-label="${__("Month")}">${J.MONTH_NAMES.map(
					(name, i) => `<option value="${i + 1}" ${i + 1 === view.jm ? "selected" : ""}>${name}</option>`
				).join("")}</select>
				<select class="ir-jp-year" aria-label="${__("Year")}">${years
					.map((y) => `<option value="${y}" ${y === view.jy ? "selected" : ""}>${fa(y)}</option>`)
					.join("")}</select>
				<button type="button" class="ir-jp-nav" data-step="1" aria-label="${__("Next")}">‹</button>
			</div>
			<div class="ir-jp-week">${WEEKDAY_SHORT.map((d) => `<span>${d}</span>`).join("")}</div>
			<div class="ir-jp-days">${days}</div>
			${
				isDatetime(control)
					? `<div class="ir-jp-time"><input type="time" step="1" class="ir-jp-time-input" dir="ltr" value="${active.time}"></div>`
					: ""
			}
			<div class="ir-jp-foot">
				<button type="button" class="ir-jp-now">${isDatetime(control) ? __("Now") : __("Today")}</button>
			</div>`;
	}

	function position() {
		const rect = active.control.$input[0].getBoundingClientRect();
		const width = popup.offsetWidth;
		const height = popup.offsetHeight;
		const below = rect.bottom + 4 + height <= root.innerHeight || rect.top - height - 4 < 0;
		popup.style.top = `${below ? rect.bottom + 4 : rect.top - height - 4}px`;
		popup.style.left = `${Math.max(8, Math.min(rect.right - width, root.innerWidth - width - 8))}px`;
	}

	function open(control) {
		if (control.df.read_only || control.disp_status === "Read") return;
		ensurePopup();
		const iso = selectedIso(control) || frappe.datetime.get_today();
		const j = J.fromISO(iso);
		const value = control.get_value && control.get_value();
		const time =
			isDatetime(control) && value && value.length > 10
				? frappe.datetime.convert_to_user_tz(value).slice(11, 19)
				: moment().format("HH:mm:ss");
		active = { control, view: { jy: j.jy, jm: j.jm }, time };
		render();
		popup.hidden = false;
		position();
	}

	function close() {
		if (popup) popup.hidden = true;
		active = null;
	}

	// Datetime model values are in the system time zone; the picker works in the user's.
	function toModel(control, iso, time) {
		if (!isDatetime(control)) return iso;
		let value = `${iso} ${time || "00:00:00"}`;
		if (!frappe.datetime.is_system_time_zone()) value = frappe.datetime.convert_to_system_tz(value, true);
		return value;
	}

	function choose(iso) {
		const { control, time } = active;
		control.set_value(toModel(control, iso, time));
		close();
	}

	function onClick(e) {
		const btn = e.target.closest("button");
		if (!btn || !active) return;
		if (btn.dataset.iso) return choose(btn.dataset.iso);
		if (btn.dataset.step) {
			let { jy, jm } = active.view;
			jm += +btn.dataset.step;
			if (jm < 1) [jy, jm] = [jy - 1, 12];
			if (jm > 12) [jy, jm] = [jy + 1, 1];
			active.view = { jy, jm };
			return render();
		}
		if (btn.classList.contains("ir-jp-now")) {
			const { control } = active;
			if (isDatetime(control)) {
				control.set_value(frappe.datetime.now_datetime());
				return close();
			}
			return choose(frappe.datetime.get_today());
		}
	}

	function onChange(e) {
		if (!active) return;
		if (e.target.classList.contains("ir-jp-month") || e.target.classList.contains("ir-jp-year")) {
			active.view = {
				jy: +popup.querySelector(".ir-jp-year").value,
				jm: +popup.querySelector(".ir-jp-month").value,
			};
			return render();
		}
		if (e.target.classList.contains("ir-jp-time-input")) {
			active.time = e.target.value.length === 5 ? `${e.target.value}:00` : e.target.value;
			const iso = selectedIso(active.control);
			if (iso) active.control.set_value(toModel(active.control, iso, active.time));
		}
	}

	// Stands in for the air-datepicker instance Frappe's Date/Datetime code calls into.
	function stub() {
		return {
			selectedDates: [],
			opts: { timeFormat: "hh:ii:ss" },
			$datepicker: $(),
			selectDate() {},
			clear() {},
			hide: close,
			update() {},
		};
	}

	function attach(control) {
		control.datepicker = stub();
		control.$input.attr("autocomplete", "off");
		control.$input.on("focus.irjp click.irjp", () => {
			if (!active || active.control !== control) open(control);
		});
	}

	root.erpnext_iran.jalali_picker = Object.assign(api, { attach, open, close, stub });
})(typeof window !== "undefined" ? window : null);

// Jalali date picker for the desk's Date, Datetime and DateRange controls.
// Calendar math (monthGrid, parseInput, rangeShortcut) is DOM-free and exported for node tests;
// the popup works on the control's model value, which stays Gregorian: "YYYY-MM-DD[ HH:mm:ss]",
// or ["YYYY-MM-DD", "YYYY-MM-DD"] for a range.
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

	const addMonths = (jy, jm, n) => {
		const index = jy * 12 + (jm - 1) + n;
		return { jy: Math.floor(index / 12), jm: (index % 12) + 1 };
	};

	function monthRange(jy, jm, months) {
		const g1 = J.toGregorian(jy, jm, 1);
		const last = addMonths(jy, jm, months - 1);
		const g2 = J.toGregorian(last.jy, last.jm, J.monthLength(last.jy, last.jm));
		return [isoOf(g1.gy, g1.gm, g1.gd), isoOf(g2.gy, g2.gm, g2.gd)];
	}

	// Gregorian [from, to] of a Jalali period around todayIso ("YYYY-MM-DD")
	const SHORTCUTS = ["this_month", "last_month", "this_season", "this_year"];
	function rangeShortcut(name, todayIso) {
		const { jy, jm } = J.fromISO(todayIso);
		if (name === "this_month") return monthRange(jy, jm, 1);
		if (name === "last_month") {
			const prev = addMonths(jy, jm, -1);
			return monthRange(prev.jy, prev.jm, 1);
		}
		if (name === "this_season") return monthRange(jy, Math.floor((jm - 1) / 3) * 3 + 1, 3);
		if (name === "this_year") return monthRange(jy, 1, 12);
		return null;
	}

	const api = { monthGrid, parseInput, rangeShortcut, SHORTCUTS, WEEKDAY_SHORT };
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
	const isRange = (control) => control.df.fieldtype === "DateRange";

	function selectedIso(control) {
		const value = control.get_value && control.get_value();
		if (!value || isRange(control)) return "";
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

	const SHORTCUT_LABELS = {
		this_month: "This Month",
		last_month: "Last Month",
		this_season: "This Season",
		this_year: "This Year",
	};

	function monthHtml(jy, jm, ctx) {
		return monthGrid(jy, jm)
			.map((c) => {
				const off =
					(ctx.lim.min && c.iso < ctx.lim.min) ||
					(ctx.lim.max && c.iso > ctx.lim.max) ||
					ctx.lim.disabled.includes(c.iso);
				const { start, end } = ctx.range || {};
				const edge = ctx.range ? c.inMonth && (c.iso === start || c.iso === end) : c.iso === ctx.selected;
				const inside = ctx.range && c.inMonth && start && end && c.iso > start && c.iso < end;
				const cls = [
					"ir-jp-day",
					c.inMonth ? "" : "ir-jp-other",
					c.iso === ctx.today ? "ir-jp-today" : "",
					edge ? "ir-jp-selected" : "",
					inside ? "ir-jp-inrange" : "",
					c.column === 6 ? "ir-jp-friday" : "",
				].join(" ");
				return `<button type="button" class="${cls}" data-iso="${c.iso}" ${off ? "disabled" : ""}>${fa(c.jd)}</button>`;
			})
			.join("");
	}

	function render() {
		const { control, view } = active;
		const range = isRange(control);
		const ctx = {
			today: frappe.datetime.get_today(),
			selected: selectedIso(control),
			lim: limits(control),
			range: range ? active.range : null,
		};
		const years = [];
		for (let y = view.jy - 60; y <= view.jy + 20; y++) years.push(y);
		const week = `<div class="ir-jp-week">${WEEKDAY_SHORT.map((d) => `<span>${d}</span>`).join("")}</div>`;
		const second = addMonths(view.jy, view.jm, 1);
		const grid = (jy, jm) =>
			`<div class="ir-jp-month-grid">${week}<div class="ir-jp-days">${monthHtml(jy, jm, ctx)}</div></div>`;

		const foot = range
			? SHORTCUTS.map(
					(name) =>
						`<button type="button" class="ir-jp-now" data-range="${name}">${__(SHORTCUT_LABELS[name])}</button>`
			  ).join("")
			: `<button type="button" class="ir-jp-now">${isDatetime(control) ? __("Now") : __("Today")}</button>`;
		const hint =
			range && active.range.start && !active.range.end
				? `<div class="ir-jp-hint text-muted">${__("Pick the last day of the range")}</div>`
				: "";

		popup.classList.toggle("ir-jpicker-range", range);
		// the ".datepicker" wrapper makes Frappe's filter popover treat clicks here as its own
		popup.innerHTML = `<div class="datepicker ir-jp-inner">
			<div class="ir-jp-head">
				<button type="button" class="ir-jp-nav" data-step="-1" aria-label="${__("Previous")}">›</button>
				<select class="ir-jp-month" aria-label="${__("Month")}">${J.MONTH_NAMES.map(
					(name, i) => `<option value="${i + 1}" ${i + 1 === view.jm ? "selected" : ""}>${name}</option>`
				).join("")}</select>
				<select class="ir-jp-year" aria-label="${__("Year")}">${years
					.map((y) => `<option value="${y}" ${y === view.jy ? "selected" : ""}>${fa(y)}</option>`)
					.join("")}</select>
				${range ? `<span class="ir-jp-second">${J.MONTH_NAMES[second.jm - 1]} ${fa(second.jy)}</span>` : ""}
				<button type="button" class="ir-jp-nav" data-step="1" aria-label="${__("Next")}">‹</button>
			</div>
			<div class="ir-jp-months">${grid(view.jy, view.jm)}${range ? grid(second.jy, second.jm) : ""}</div>
			${hint}
			${
				isDatetime(control)
					? `<div class="ir-jp-time"><input type="time" step="1" class="ir-jp-time-input" dir="ltr" value="${active.time}"></div>`
					: ""
			}
			<div class="ir-jp-foot">${foot}</div>
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
		const value = control.get_value && control.get_value();
		const pair = isRange(control) && Array.isArray(value) ? value : [];
		const iso = pair[0] || selectedIso(control) || frappe.datetime.get_today();
		const j = J.fromISO(iso);
		const time =
			isDatetime(control) && value && value.length > 10
				? frappe.datetime.convert_to_user_tz(value).slice(11, 19)
				: moment().format("HH:mm:ss");
		active = { control, view: { jy: j.jy, jm: j.jm }, time, range: { start: pair[0] || "", end: pair[1] || "" } };
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
		const { control, time, range } = active;
		if (isRange(control)) {
			// first click starts the range, the second closes it (in either order)
			if (!range.start || range.end) {
				active.range = { start: iso, end: "" };
				return render();
			}
			control.set_value(iso < range.start ? [iso, range.start] : [range.start, iso]);
			return close();
		}
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
		if (btn.dataset.range) {
			active.control.set_value(rangeShortcut(btn.dataset.range, frappe.datetime.get_today()));
			return close();
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

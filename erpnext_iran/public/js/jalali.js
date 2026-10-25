// Jalali (Solar Hijri) calendar - port of jalaali-js (Borkowski / Pournader).
// Kept dependency free; exposed as erpnext_iran.jalali (and module.exports for tests).
(function (root) {
	"use strict";

	const BREAKS = [
		-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060, 2097, 2192, 2262, 2324,
		2394, 2456, 3178,
	];
	const MONTH_NAMES = [
		"فروردین",
		"اردیبهشت",
		"خرداد",
		"تیر",
		"مرداد",
		"شهریور",
		"مهر",
		"آبان",
		"آذر",
		"دی",
		"بهمن",
		"اسفند",
	];
	// Indexed by Date.getDay() (Sunday == 0)
	const WEEKDAY_NAMES = ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه"];
	const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";

	const div = (a, b) => ~~(a / b);
	const mod = (a, b) => a - ~~(a / b) * b;

	function jalCal(jy, withoutLeap) {
		const bl = BREAKS.length;
		const gy = jy + 621;
		let leapJ = -14;
		let jp = BREAKS[0];
		let jump = 0;
		if (jy < jp || jy >= BREAKS[bl - 1]) throw new Error("Invalid Jalali year " + jy);

		for (let i = 1; i < bl; i += 1) {
			const jm = BREAKS[i];
			jump = jm - jp;
			if (jy < jm) break;
			leapJ = leapJ + div(jump, 33) * 8 + div(mod(jump, 33), 4);
			jp = jm;
		}
		let n = jy - jp;
		leapJ = leapJ + div(n, 33) * 8 + div(mod(n, 33) + 3, 4);
		if (mod(jump, 33) === 4 && jump - n === 4) leapJ += 1;

		const leapG = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150;
		const march = 20 + leapJ - leapG;
		if (withoutLeap) return { gy, march };

		if (jump - n < 6) n = n - jump + div(jump + 4, 33) * 33;
		let leap = mod(mod(n + 1, 33) - 1, 4);
		if (leap === -1) leap = 4;
		return { leap, gy, march };
	}

	function g2d(gy, gm, gd) {
		let d =
			div((gy + div(gm - 8, 6) + 100100) * 1461, 4) +
			div(153 * mod(gm + 9, 12) + 2, 5) +
			gd -
			34840408;
		d = d - div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) + 752;
		return d;
	}

	function d2g(jdn) {
		let j = 4 * jdn + 139361631;
		j = j + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908;
		const i = div(mod(j, 1461), 4) * 5 + 308;
		const gd = div(mod(i, 153), 5) + 1;
		const gm = mod(div(i, 153), 12) + 1;
		const gy = div(j, 1461) - 100100 + div(8 - gm, 6);
		return { gy, gm, gd };
	}

	function j2d(jy, jm, jd) {
		const r = jalCal(jy, true);
		return g2d(r.gy, 3, r.march) + (jm - 1) * 31 - div(jm, 7) * (jm - 7) + jd - 1;
	}

	function d2j(jdn) {
		const gy = d2g(jdn).gy;
		let jy = gy - 621;
		const r = jalCal(jy, false);
		const jdn1f = g2d(gy, 3, r.march);
		let k = jdn - jdn1f;
		if (k >= 0) {
			if (k <= 185) return { jy, jm: 1 + div(k, 31), jd: mod(k, 31) + 1 };
			k -= 186;
		} else {
			jy -= 1;
			k += 179;
			if (r.leap === 1) k += 1;
		}
		return { jy, jm: 7 + div(k, 30), jd: mod(k, 30) + 1 };
	}

	const isLeapYear = (jy) => jalCal(jy).leap === 0;
	const monthLength = (jy, jm) => (jm <= 6 ? 31 : jm <= 11 ? 30 : isLeapYear(jy) ? 30 : 29);
	const isValid = (jy, jm, jd) => {
		try {
			return jm >= 1 && jm <= 12 && jd >= 1 && jd <= monthLength(jy, jm);
		} catch (e) {
			return false;
		}
	};

	const toJalali = (gy, gm, gd) => d2j(g2d(gy, gm, gd));
	const toGregorian = (jy, jm, jd) => d2g(j2d(jy, jm, jd));

	const pad = (n) => String(n).padStart(2, "0");
	const toPersianDigits = (s) => String(s).replace(/[0-9]/g, (d) => PERSIAN_DIGITS[d]);
	const toEnglishDigits = (s) =>
		String(s)
			.replace(/[۰-۹]/g, (d) => PERSIAN_DIGITS.indexOf(d))
			.replace(/[٠-٩]/g, (d) => d.charCodeAt(0) - 0x0660);

	// "2024-03-20" or "2024-03-20 10:15:00" -> {jy, jm, jd, time}
	function fromISO(value) {
		const m = /^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}:\d{2}(?::\d{2})?))?/.exec(String(value || ""));
		if (!m) return null;
		const j = toJalali(+m[1], +m[2], +m[3]);
		j.time = m[4] || "";
		j.weekday = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3])).getUTCDay();
		return j;
	}

	// Tokens: YYYY MM M DD D MMMM (month name) dddd (weekday name) HH:mm:ss passes through
	function format(value, fmt, persianDigits) {
		const j = fromISO(value);
		if (!j) return "";
		fmt = fmt || "YYYY/MM/DD";
		const out = fmt.replace(/YYYY|MMMM|MM|M|DD|D|dddd/g, (t) => {
			switch (t) {
				case "YYYY":
					return String(j.jy);
				case "MMMM":
					return MONTH_NAMES[j.jm - 1];
				case "MM":
					return pad(j.jm);
				case "M":
					return String(j.jm);
				case "DD":
					return pad(j.jd);
				case "D":
					return String(j.jd);
				case "dddd":
					return WEEKDAY_NAMES[j.weekday];
			}
			return t;
		});
		return persianDigits ? toPersianDigits(out) : out;
	}

	// "1403/01/15" (any digits, / - . separators) -> "2024-04-03" or null
	function parse(text) {
		const parts = toEnglishDigits(text || "")
			.trim()
			.split(/[\/\-.]/)
			.filter(Boolean);
		if (parts.length !== 3 || parts.some((p) => !/^\d+$/.test(p))) return null;
		const [jy, jm, jd] = parts.map(Number);
		if (!isValid(jy, jm, jd)) return null;
		const g = toGregorian(jy, jm, jd);
		return `${g.gy}-${pad(g.gm)}-${pad(g.gd)}`;
	}

	const api = {
		toJalali,
		toGregorian,
		isLeapYear,
		monthLength,
		isValid,
		fromISO,
		format,
		parse,
		toPersianDigits,
		toEnglishDigits,
		MONTH_NAMES,
		WEEKDAY_NAMES,
	};

	if (typeof module !== "undefined" && module.exports) module.exports = api;
	if (root) {
		root.erpnext_iran = root.erpnext_iran || {};
		root.erpnext_iran.jalali = api;
	}
})(typeof window !== "undefined" ? window : null);

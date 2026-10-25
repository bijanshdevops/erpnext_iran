"""Jalali (Solar Hijri) calendar conversion.

Port of the jalaali-js algorithm (Borkowski / Pournader), valid for Jalali years -61..3177.
Pure Python (no Frappe import) so it can be unit tested without a bench.
"""

import datetime

from erpnext_iran.utils.persian import to_english_digits, to_persian_digits

MONTH_NAMES = [
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
]

# Indexed by datetime.date.weekday() (Monday == 0)
WEEKDAY_NAMES = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]

_BREAKS = [
	-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210,
	1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178,
]  # fmt: skip

# Julian Day Number of proleptic Gregorian 0001-01-01 is 1721426.
_ORDINAL_TO_JDN = 1721425


def _div(a, b):
	"""Integer division truncating toward zero (matches JavaScript ~~(a / b))."""
	q = abs(a) // abs(b)
	return q if (a < 0) == (b < 0) else -q


def _mod(a, b):
	return a - _div(a, b) * b


def _g2d(gy, gm, gd):
	return datetime.date(gy, gm, gd).toordinal() + _ORDINAL_TO_JDN


def _d2g(jdn):
	return datetime.date.fromordinal(jdn - _ORDINAL_TO_JDN)


def _jal_cal(jy, without_leap=False):
	bl = len(_BREAKS)
	gy = jy + 621
	leap_j = -14
	jp = _BREAKS[0]
	if jy < jp or jy >= _BREAKS[bl - 1]:
		raise ValueError(f"Invalid Jalali year {jy}")

	jump = 0
	for i in range(1, bl):
		jm = _BREAKS[i]
		jump = jm - jp
		if jy < jm:
			break
		leap_j = leap_j + _div(jump, 33) * 8 + _div(_mod(jump, 33), 4)
		jp = jm

	n = jy - jp
	leap_j = leap_j + _div(n, 33) * 8 + _div(_mod(n, 33) + 3, 4)
	if _mod(jump, 33) == 4 and jump - n == 4:
		leap_j += 1

	leap_g = _div(gy, 4) - _div((_div(gy, 100) + 1) * 3, 4) - 150
	march = 20 + leap_j - leap_g
	if without_leap:
		return None, gy, march

	if jump - n < 6:
		n = n - jump + _div(jump + 4, 33) * 33
	leap = _mod(_mod(n + 1, 33) - 1, 4)
	if leap == -1:
		leap = 4
	return leap, gy, march


def _j2d(jy, jm, jd):
	_, gy, march = _jal_cal(jy, without_leap=True)
	return _g2d(gy, 3, march) + (jm - 1) * 31 - _div(jm, 7) * (jm - 7) + jd - 1


def _d2j(jdn):
	gy = _d2g(jdn).year
	jy = gy - 621
	leap, _, march = _jal_cal(jy)
	jdn1f = _g2d(gy, 3, march)
	k = jdn - jdn1f
	if k >= 0:
		if k <= 185:
			return jy, 1 + _div(k, 31), _mod(k, 31) + 1
		k -= 186
	else:
		jy -= 1
		k += 179
		if leap == 1:
			k += 1
	return jy, 7 + _div(k, 30), _mod(k, 30) + 1


def is_leap_jalali_year(jy):
	return _jal_cal(jy)[0] == 0


def jalali_month_length(jy, jm):
	if jm <= 6:
		return 31
	if jm <= 11:
		return 30
	return 30 if is_leap_jalali_year(jy) else 29


def is_valid_jalali_date(jy, jm, jd):
	try:
		return 1 <= jm <= 12 and 1 <= jd <= jalali_month_length(jy, jm)
	except ValueError:
		return False


def gregorian_to_jalali(gy, gm, gd):
	return _d2j(_g2d(gy, gm, gd))


def jalali_to_gregorian(jy, jm, jd):
	if not is_valid_jalali_date(jy, jm, jd):
		raise ValueError(f"Invalid Jalali date {jy}/{jm}/{jd}")
	d = _d2g(_j2d(jy, jm, jd))
	return d.year, d.month, d.day


def _as_date(value):
	if isinstance(value, datetime.datetime):
		return value.date()
	if isinstance(value, datetime.date):
		return value
	text = str(value).strip()
	return datetime.date.fromisoformat(text[:10])


def to_jalali(value):
	"""Return (jy, jm, jd) for a date, datetime or 'YYYY-MM-DD...' string."""
	d = _as_date(value)
	return gregorian_to_jalali(d.year, d.month, d.day)


def to_gregorian(jy, jm, jd):
	return datetime.date(*jalali_to_gregorian(jy, jm, jd))


def parse_jalali(text):
	"""Parse '1403/01/15', '1403-1-15' or Persian-digit input into a datetime.date."""
	cleaned = to_english_digits(str(text)).strip().replace("-", "/").replace(".", "/")
	parts = [p for p in cleaned.split("/") if p]
	if len(parts) != 3 or not all(p.isdigit() for p in parts):
		raise ValueError(f"Invalid Jalali date: {text}")
	jy, jm, jd = (int(p) for p in parts)
	return to_gregorian(jy, jm, jd)


def format_jalali(value, fmt="%Y/%m/%d", persian_digits=False):
	"""Format a Gregorian date in Jalali.

	Tokens: %Y year, %y 2-digit year, %m month (01), %-m month (1), %d day (01), %-d day (1),
	%B month name, %A weekday name, %H %M %S (from datetime values).
	"""
	if value in (None, ""):
		return ""
	if isinstance(value, str) and len(value.strip()) > 10:
		value = datetime.datetime.fromisoformat(value.strip())
	d = _as_date(value)
	jy, jm, jd = gregorian_to_jalali(d.year, d.month, d.day)
	t = value if isinstance(value, datetime.datetime) else None

	replacements = {
		"%Y": str(jy),
		"%y": f"{jy % 100:02d}",
		"%-m": str(jm),
		"%m": f"{jm:02d}",
		"%-d": str(jd),
		"%d": f"{jd:02d}",
		"%B": MONTH_NAMES[jm - 1],
		"%A": WEEKDAY_NAMES[d.weekday()],
		"%H": f"{t.hour:02d}" if t else "00",
		"%M": f"{t.minute:02d}" if t else "00",
		"%S": f"{t.second:02d}" if t else "00",
	}
	out = []
	i = 0
	while i < len(fmt):
		for token in ("%-m", "%-d"):
			if fmt.startswith(token, i):
				out.append(replacements[token])
				i += len(token)
				break
		else:
			token = fmt[i : i + 2]
			if token in replacements:
				out.append(replacements[token])
				i += 2
			else:
				out.append(fmt[i])
				i += 1
	result = "".join(out)
	return to_persian_digits(result) if persian_digits else result


def jalali_year_range(jy):
	"""First and last Gregorian dates of Jalali year jy (1 Farvardin .. end of Esfand)."""
	start = to_gregorian(jy, 1, 1)
	end = to_gregorian(jy, 12, jalali_month_length(jy, 12))
	return start, end

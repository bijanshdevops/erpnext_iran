"""Report periods aligned to Jalali months (Farvardin, Ordibehesht, ...). Pure Python.

ERPNext's financial statements cut a fiscal year into periods by adding Gregorian months to its
start date. For a Jalali fiscal year that drifts (Jalali months have 31, 30 or 29 days), so
these helpers cut on 1st-of-Jalali-month boundaries instead.
"""

import datetime

from erpnext_iran.utils.jalali import MONTH_NAMES, to_gregorian, to_jalali

ONE_DAY = datetime.timedelta(days=1)


def add_jalali_months(jy, jm, months):
	index = jy * 12 + (jm - 1) + months
	return index // 12, index % 12 + 1


def jalali_periods(start, end, months):
	"""[(from_date, to_date)] covering start..end; every period but the first starts on the 1st
	of a Jalali month, and each spans `months` Jalali months (the last one is cut at `end`)."""
	periods = []
	jy, jm, _ = to_jalali(start)
	current = start
	while current <= end:
		jy, jm = add_jalali_months(jy, jm, months)
		next_start = to_gregorian(jy, jm, 1)
		periods.append((current, min(next_start - ONE_DAY, end)))
		current = next_start
	return periods


def period_key(to_date):
	jy, jm, _ = to_jalali(to_date)
	return f"j{jy}_{jm:02d}"


def month_label(date):
	jy, jm, _ = to_jalali(date)
	return f"{MONTH_NAMES[jm - 1]} {jy}"


def range_label(from_date, to_date):
	if to_jalali(from_date)[:2] == to_jalali(to_date)[:2]:
		return month_label(to_date)
	return f"{month_label(from_date)} - {month_label(to_date)}"


def year_label(from_date, to_date):
	start_year, end_year = to_jalali(from_date)[0], to_jalali(to_date)[0]
	return str(start_year) if start_year == end_year else f"{start_year}-{end_year}"

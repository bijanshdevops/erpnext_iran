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


def season_range(jy, season):
	"""First and last Gregorian dates of Jalali season 1-4 (1 = Spring, Farvardin to Khordad)."""
	first_month = 3 * (season - 1) + 1
	next_year, next_month = add_jalali_months(jy, first_month, 3)
	return to_gregorian(jy, first_month, 1), to_gregorian(next_year, next_month, 1) - ONE_DAY


SEASONS = {"Spring": 1, "Summer": 2, "Autumn": 3, "Winter": 4}


def period_range(jy, period):
	"""Gregorian dates of a report period of Jalali year jy: "Whole Year", a season name
	("Spring" .. "Winter") or a month "1" .. "12"."""
	if period in SEASONS:
		return season_range(jy, SEASONS[period])
	if str(period).isdigit() and 1 <= int(period) <= 12:
		next_year, next_month = add_jalali_months(jy, int(period), 1)
		return to_gregorian(jy, int(period), 1), to_gregorian(next_year, next_month, 1) - ONE_DAY
	first = to_gregorian(jy, 1, 1)
	return first, to_gregorian(jy + 1, 1, 1) - ONE_DAY

"""Official Iranian lunar (Hijri) holidays. Pure Python.

Iran's lunar months start on the sighting of the new moon, so their dates are only known once the
official calendar of the year is published. OFFICIAL_DATES holds those published dates; for any
other year the dates are estimated with the arithmetic Islamic calendar, which can be a day or
two off and is reported as such.
"""

import datetime

from erpnext_iran.utils.jalali import jalali_year_range, to_gregorian

# key: (Hijri month, Hijri day, name). Day "last" is the last day of the month (29th or 30th).
LUNAR_HOLIDAYS = {
	"tasua": (1, 9, "تاسوعای حسینی"),
	"ashura": (1, 10, "عاشورای حسینی"),
	"arbaeen": (2, 20, "اربعین حسینی"),
	"prophet_death": (2, 28, "رحلت رسول اکرم و شهادت امام حسن مجتبی"),
	"imam_reza": (2, "last", "شهادت امام رضا"),
	"imam_askari": (3, 8, "شهادت امام حسن عسکری"),
	"prophet_birth": (3, 17, "میلاد رسول اکرم و امام جعفر صادق"),
	"fatima": (6, 3, "شهادت حضرت فاطمه زهرا"),
	"imam_ali_birth": (7, 13, "ولادت امام علی"),
	"mabath": (7, 27, "مبعث رسول اکرم"),
	"mahdi_birth": (8, 15, "ولادت حضرت قائم"),
	"imam_ali_martyrdom": (9, 21, "شهادت امام علی"),
	"fitr": (10, 1, "عید سعید فطر"),
	"fitr_2": (10, 2, "تعطیل به مناسبت عید سعید فطر"),
	"imam_sadiq": (10, 25, "شهادت امام جعفر صادق"),
	"adha": (12, 10, "عید سعید قربان"),
	"ghadir": (12, 18, "عید سعید غدیر خم"),
}

# Jalali year -> [(Jalali month, Jalali day, key)] from the official calendar of that year
# (calendar approved by the Supreme Council of the Cultural Revolution, as published by
# bahesab.ir and bargcalendar.com). Add a year here once its official calendar is out.
OFFICIAL_DATES = {
	1404: [
		(1, 2, "imam_ali_martyrdom"),
		(1, 11, "fitr"),
		(1, 12, "fitr_2"),
		(2, 4, "imam_sadiq"),
		(3, 16, "adha"),
		(3, 24, "ghadir"),
		(4, 14, "tasua"),
		(4, 15, "ashura"),
		(5, 23, "arbaeen"),
		(5, 31, "prophet_death"),
		(6, 2, "imam_reza"),
		(6, 10, "imam_askari"),
		(6, 19, "prophet_birth"),
		(9, 3, "fatima"),
		(10, 13, "imam_ali_birth"),
		(10, 27, "mabath"),
		(11, 15, "mahdi_birth"),
		(12, 20, "imam_ali_martyrdom"),
	],
	1405: [
		(1, 1, "fitr"),
		(1, 2, "fitr_2"),
		(1, 25, "imam_sadiq"),
		(3, 6, "adha"),
		(3, 14, "ghadir"),
		(4, 3, "tasua"),
		(4, 4, "ashura"),
		(5, 13, "arbaeen"),
		(5, 21, "prophet_death"),
		(5, 22, "imam_reza"),
		(5, 30, "imam_askari"),
		(6, 8, "prophet_birth"),
		(8, 22, "fatima"),
		(10, 2, "imam_ali_birth"),
		(10, 16, "mabath"),
		(11, 4, "mahdi_birth"),
		(12, 9, "imam_ali_martyrdom"),
		(12, 19, "fitr"),
		(12, 20, "fitr_2"),
	],
}

_ORDINAL_TO_JDN = 1721425


def hijri_to_gregorian(hy, hm, hd):
	"""Arithmetic (tabular) Islamic calendar, civil epoch: 1 Muharram 1 AH = 16 July 622 CE."""
	jdn = hd + (59 * (hm - 1) + 1) // 2 + (hy - 1) * 354 + (3 + 11 * hy) // 30 + 1948439
	return datetime.date.fromordinal(jdn - _ORDINAL_TO_JDN)


def _estimated_date(hy, hm, hd):
	if hd == "last":
		next_year, next_month = (hy, hm + 1) if hm < 12 else (hy + 1, 1)
		return hijri_to_gregorian(next_year, next_month, 1) - datetime.timedelta(days=1)
	return hijri_to_gregorian(hy, hm, hd)


def lunar_holidays(jalali_year):
	"""([(date, key, name)] sorted by date, estimated) for the Jalali year. estimated is True when
	the year has no official dates here and they come from the arithmetic calendar."""
	jalali_year = int(jalali_year)
	official = OFFICIAL_DATES.get(jalali_year)
	if official:
		days = [(to_gregorian(jalali_year, jm, jd), key, LUNAR_HOLIDAYS[key][2]) for jm, jd, key in official]
		return sorted(days), False

	start, end = jalali_year_range(jalali_year)
	first_hijri_year = (start.year - 622) * 33 // 32 - 1
	days = []
	for hy in range(first_hijri_year, first_hijri_year + 4):
		for key, (hm, hd, name) in LUNAR_HOLIDAYS.items():
			day = _estimated_date(hy, hm, hd)
			if start <= day <= end:
				days.append((day, key, name))
	return sorted(days), True

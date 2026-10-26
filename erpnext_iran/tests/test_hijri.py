import datetime
import unittest

from erpnext_iran.utils import hijri
from erpnext_iran.utils.jalali import jalali_year_range, to_gregorian

SOLAR_DAYS = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 12), (1, 13), (3, 14), (3, 15), (11, 22), (12, 29)]


class TestHijriCalendar(unittest.TestCase):
	def test_epoch(self):
		# 1 Muharram 1 AH = 16 July 622 Julian = 19 July 622 proleptic Gregorian
		self.assertEqual(hijri.hijri_to_gregorian(1, 1, 1), datetime.date(622, 7, 19))

	def test_months_alternate_30_29(self):
		for hm in range(1, 12):
			length = (hijri.hijri_to_gregorian(1446, hm + 1, 1) - hijri.hijri_to_gregorian(1446, hm, 1)).days
			self.assertIn(length, (29, 30))


class TestOfficialDates(unittest.TestCase):
	def test_keys_and_range(self):
		for jy, rows in hijri.OFFICIAL_DATES.items():
			start, end = jalali_year_range(jy)
			for jm, jd, key in rows:
				self.assertIn(key, hijri.LUNAR_HOLIDAYS)
				self.assertTrue(start <= to_gregorian(jy, jm, jd) <= end)

	def test_26_official_holidays(self):
		# 1404 and 1405 both have 26 official holiday days (some lunar days fall on solar ones)
		for jy in (1404, 1405):
			lunar = {to_gregorian(jy, jm, jd) for jm, jd, _key in hijri.OFFICIAL_DATES[jy]}
			solar = {to_gregorian(jy, jm, jd) for jm, jd in SOLAR_DAYS}
			self.assertEqual(len(lunar | solar), 26, jy)

	def test_published_weekdays(self):
		saturday, sunday, wednesday = 5, 6, 2
		for jy, jm, jd, weekday in [
			(1404, 1, 2, saturday),  # martyrdom of Imam Ali
			(1404, 4, 14, saturday),  # Tasua
			(1404, 12, 20, wednesday),  # martyrdom of Imam Ali
			(1405, 1, 1, saturday),  # Eid al-Fitr
			(1405, 4, 3, wednesday),  # Tasua
			(1405, 12, 9, sunday),  # martyrdom of Imam Ali
		]:
			self.assertEqual(to_gregorian(jy, jm, jd).weekday(), weekday, (jy, jm, jd))

	def test_dates_follow_hijri_days(self):
		# within a Hijri month the gaps between holidays are fixed
		pairs = [("ashura", "tasua", 1), ("fitr_2", "fitr", 1), ("prophet_death", "arbaeen", 8),
				 ("prophet_birth", "imam_askari", 9), ("mabath", "imam_ali_birth", 14), ("ghadir", "adha", 8)]  # fmt: skip
		for jy, rows in hijri.OFFICIAL_DATES.items():
			dates = {}
			for jm, jd, key in rows:
				dates.setdefault(key, []).append(to_gregorian(jy, jm, jd))
			for later, earlier, gap in pairs:
				if later in dates and earlier in dates:
					self.assertEqual((dates[later][0] - dates[earlier][0]).days, gap, (jy, later))
			# Imam Reza is the last day of Safar: one or two days after the 28th
			self.assertIn((dates["imam_reza"][0] - dates["prophet_death"][0]).days, (1, 2), jy)

	def test_official_year_is_not_estimated(self):
		days, estimated = hijri.lunar_holidays(1405)
		self.assertFalse(estimated)
		self.assertEqual(days[0], (datetime.date(2026, 3, 21), "fitr", "عید سعید فطر"))


class TestEstimate(unittest.TestCase):
	def test_estimate_within_a_day_of_official(self):
		for jy, rows in hijri.OFFICIAL_DATES.items():
			for jm, jd, key in rows:
				official = to_gregorian(jy, jm, jd)
				hm, hd, _name = hijri.LUNAR_HOLIDAYS[key]
				first_hijri_year = (official.year - 622) * 33 // 32 - 1
				closest = min(
					(hijri._estimated_date(hy, hm, hd) for hy in range(first_hijri_year, first_hijri_year + 4)),
					key=lambda d: abs((d - official).days),
				)
				self.assertLessEqual(abs((closest - official).days), 1, (jy, jm, jd, key))

	def test_unpublished_year_is_estimated(self):
		days, estimated = hijri.lunar_holidays(1406)
		self.assertTrue(estimated)
		start, end = jalali_year_range(1406)
		self.assertTrue(all(start <= day <= end for day, _key, _name in days))
		self.assertTrue(16 <= len(days) <= 19)
		self.assertEqual(len({key for _day, key, _name in days}), 17)  # every lunar holiday occurs

import datetime
import unittest

from erpnext_iran.utils import jalali
from erpnext_iran.utils.jalali_periods import (
	add_jalali_months,
	jalali_periods,
	period_key,
	range_label,
	year_label,
)

D = datetime.date


class TestJalaliPeriods(unittest.TestCase):
	def test_add_months(self):
		self.assertEqual(add_jalali_months(1405, 1, 1), (1405, 2))
		self.assertEqual(add_jalali_months(1405, 12, 1), (1406, 1))
		self.assertEqual(add_jalali_months(1405, 11, 3), (1406, 2))
		self.assertEqual(add_jalali_months(1405, 1, 12), (1406, 1))

	def test_monthly_fiscal_year(self):
		start, end = jalali.jalali_year_range(1405)
		periods = jalali_periods(start, end, 1)
		self.assertEqual(len(periods), 12)
		self.assertEqual(periods[0], (D(2026, 3, 21), D(2026, 4, 20)))  # Farvardin, 31 days
		self.assertEqual(periods[1], (D(2026, 4, 21), D(2026, 5, 21)))  # Ordibehesht
		self.assertEqual(periods[6], (D(2026, 9, 23), D(2026, 10, 22)))  # Mehr, 30 days
		self.assertEqual(periods[-1], (D(2027, 2, 20), D(2027, 3, 20)))  # Esfand, 29 days (1405)
		for (_, prev_end), (next_start, _) in zip(periods, periods[1:]):
			self.assertEqual(next_start - prev_end, datetime.timedelta(days=1))
		for i, (f, t) in enumerate(periods, start=1):
			self.assertEqual(jalali.to_jalali(f), (1405, i, 1))
			self.assertEqual(jalali.to_jalali(t), (1405, i, jalali.jalali_month_length(1405, i)))

	def test_leap_year_esfand(self):
		start, end = jalali.jalali_year_range(1403)
		self.assertEqual(jalali_periods(start, end, 1)[-1], (D(2025, 2, 19), D(2025, 3, 20)))  # 30 days

	def test_quarterly_and_half_yearly(self):
		start, end = jalali.jalali_year_range(1405)
		quarters = jalali_periods(start, end, 3)
		self.assertEqual([jalali.to_jalali(f)[1] for f, _ in quarters], [1, 4, 7, 10])
		self.assertEqual(quarters[1], (D(2026, 6, 22), D(2026, 9, 22)))  # Tir - Shahrivar
		self.assertEqual(len(jalali_periods(start, end, 6)), 2)

	def test_date_range_starting_mid_month(self):
		periods = jalali_periods(D(2026, 10, 25), D(2026, 12, 31), 1)  # 3 Aban .. 10 Dey 1405
		self.assertEqual(periods[0], (D(2026, 10, 25), D(2026, 11, 21)))  # rest of Aban
		self.assertEqual(periods[1], (D(2026, 11, 22), D(2026, 12, 21)))  # Azar
		self.assertEqual(periods[2], (D(2026, 12, 22), D(2026, 12, 31)))  # Dey, cut at end

	def test_labels_and_keys(self):
		self.assertEqual(period_key(D(2026, 4, 20)), "j1405_01")
		self.assertEqual(range_label(D(2026, 3, 21), D(2026, 4, 20)), "فروردین 1405")
		self.assertEqual(range_label(D(2026, 3, 21), D(2026, 6, 21)), "فروردین 1405 - خرداد 1405")
		self.assertEqual(year_label(D(2026, 3, 21), D(2027, 3, 20)), "1405")
		self.assertEqual(year_label(D(2025, 3, 21), D(2027, 3, 20)), "1404-1405")
		start, end = jalali.jalali_year_range(1405)
		keys = [period_key(t) for _, t in jalali_periods(start, end, 1)]
		self.assertEqual(len(keys), len(set(keys)))

import datetime
import unittest

from erpnext_iran.payroll.core import insurance, salary_tax, taxable_income, years_of_service

# 1405 monthly brackets (rial): exempt to 400m, 10% to 800m, 15% to 1,000m, 20% to 1,200m,
# 25% to 1,400m, 30% above
BRACKETS_1405 = [(0, 0), (400_000_000, 10), (800_000_000, 15), (1_000_000_000, 20),
				 (1_200_000_000, 25), (1_400_000_000, 30)]  # fmt: skip


class TestSalaryTax(unittest.TestCase):
	def test_exempt(self):
		self.assertEqual(salary_tax(400_000_000, BRACKETS_1405), 0)
		self.assertEqual(salary_tax(218_255_500, BRACKETS_1405), 0)  # 1405 minimum pay

	def test_progressive(self):
		# 1,000m: 40m on the 10% step and 30m on the 15% step (the published example)
		self.assertEqual(salary_tax(1_000_000_000, BRACKETS_1405), 70_000_000)
		self.assertEqual(salary_tax(500_000_000, BRACKETS_1405), 10_000_000)
		# 1,500m: 40 + 30 + 40 + 50 + 30 (top step) million
		self.assertEqual(salary_tax(1_500_000_000, BRACKETS_1405), 190_000_000)

	def test_brackets_in_any_order(self):
		self.assertEqual(salary_tax(1_000_000_000, list(reversed(BRACKETS_1405))), 70_000_000)


class TestInsurance(unittest.TestCase):
	def test_shares(self):
		self.assertEqual(insurance(218_255_500, 1_163_789_500, 7, 23), (218_255_500, 15_277_885, 50_198_765))

	def test_ceiling(self):
		ceiling = 7 * 5_541_850 * 30  # 1405, a 30-day month
		self.assertEqual(insurance(2_000_000_000, ceiling, 7, 23)[0], 1_163_788_500)

	def test_taxable_income(self):
		# 2/7 of the employee's 7% share is exempt from salary tax
		self.assertEqual(taxable_income(700_000_000, 49_000_000, 2 / 7), 686_000_000)
		self.assertEqual(taxable_income(0, 10, 2 / 7), 0)


class TestService(unittest.TestCase):
	def test_years(self):
		self.assertEqual(years_of_service("2024-03-20", "2026-11-01"), 2)
		self.assertEqual(years_of_service(datetime.date(2025, 11, 2), datetime.date(2026, 11, 1)), 0)
		self.assertEqual(years_of_service("2025-11-01", "2026-11-01"), 1)
		self.assertEqual(years_of_service(None, "2026-11-01"), 0)

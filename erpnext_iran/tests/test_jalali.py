import datetime
import json
import shutil
import subprocess
import unittest
from pathlib import Path

from erpnext_iran.utils import jalali

JS_FILE = Path(__file__).resolve().parent.parent / "public" / "js" / "jalali.js"


class TestJalali(unittest.TestCase):
	def test_known_dates(self):
		cases = {
			(2024, 3, 20): (1403, 1, 1),
			(2025, 3, 21): (1404, 1, 1),
			(2026, 3, 21): (1405, 1, 1),
			(2021, 3, 20): (1399, 12, 30),
			(2025, 3, 20): (1403, 12, 30),
			(1979, 2, 11): (1357, 11, 22),
			(2026, 10, 25): (1405, 8, 3),
		}
		for g, j in cases.items():
			self.assertEqual(jalali.gregorian_to_jalali(*g), j, g)
			self.assertEqual(jalali.jalali_to_gregorian(*j), g, j)

	def test_leap_years(self):
		leaps = [y for y in range(1390, 1415) if jalali.is_leap_jalali_year(y)]
		self.assertEqual(leaps, [1391, 1395, 1399, 1403, 1408, 1412])
		self.assertEqual(jalali.jalali_month_length(1403, 12), 30)
		self.assertEqual(jalali.jalali_month_length(1404, 12), 29)
		self.assertEqual(jalali.jalali_month_length(1404, 7), 30)

	def test_round_trip(self):
		start = datetime.date(1950, 1, 1)
		for i in range(0, 120 * 366):
			day = start + datetime.timedelta(days=i)
			self.assertEqual(jalali.to_gregorian(*jalali.to_jalali(day)), day)

	def test_invalid(self):
		self.assertFalse(jalali.is_valid_jalali_date(1404, 12, 30))
		self.assertTrue(jalali.is_valid_jalali_date(1403, 12, 30))
		with self.assertRaises(ValueError):
			jalali.jalali_to_gregorian(1404, 12, 30)
		with self.assertRaises(ValueError):
			jalali.parse_jalali("1404/13/01")

	def test_format_and_parse(self):
		self.assertEqual(jalali.format_jalali("2024-03-20"), "1403/01/01")
		self.assertEqual(jalali.format_jalali(datetime.date(2026, 10, 25), "%A %-d %B %Y"), "یکشنبه 3 آبان 1405")
		self.assertEqual(jalali.format_jalali("2024-03-20 14:05:09", "%Y/%m/%d %H:%M"), "1403/01/01 14:05")
		self.assertEqual(jalali.format_jalali("2024-03-20", persian_digits=True), "۱۴۰۳/۰۱/۰۱")
		self.assertEqual(jalali.format_jalali(None), "")
		self.assertEqual(jalali.parse_jalali("۱۴۰۳/۱/۱"), datetime.date(2024, 3, 20))
		self.assertEqual(jalali.parse_jalali("1405-08-03"), datetime.date(2026, 10, 25))

	def test_year_range(self):
		self.assertEqual(
			jalali.jalali_year_range(1404), (datetime.date(2025, 3, 21), datetime.date(2026, 3, 20))
		)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class TestJalaliJSParity(unittest.TestCase):
	"""public/js/jalali.js must agree with the Python implementation."""

	def test_parity(self):
		start = datetime.date(1990, 1, 1)
		days = [(start + datetime.timedelta(days=i)).isoformat() for i in range(0, 50 * 366, 3)]
		script = (
			f"const J = require({json.dumps(str(JS_FILE))});"
			"const days = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
			"console.log(JSON.stringify(days.map(d => { const j = J.fromISO(d);"
			" return [j.jy, j.jm, j.jd, J.parse(`${j.jy}/${j.jm}/${j.jd}`), J.format(d, 'dddd')]; })));"
		)
		out = subprocess.run(
			["node", "-e", script], input=json.dumps(days), capture_output=True, text=True,
			encoding="utf-8", check=True,
		).stdout  # fmt: skip
		for iso, (jy, jm, jd, back, weekday) in zip(days, json.loads(out)):
			day = datetime.date.fromisoformat(iso)
			self.assertEqual((jy, jm, jd), jalali.to_jalali(day), iso)
			self.assertEqual(back, iso)
			self.assertEqual(weekday, jalali.WEEKDAY_NAMES[day.weekday()], iso)

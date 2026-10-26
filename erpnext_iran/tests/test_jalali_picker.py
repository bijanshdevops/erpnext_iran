"""Calendar logic of public/js/jalali_picker.js, checked against the Python Jalali implementation."""

import datetime
import json
import shutil
import subprocess
import unittest
from pathlib import Path

from erpnext_iran.utils import jalali

JS_FILE = Path(__file__).resolve().parent.parent / "public" / "js" / "jalali_picker.js"


def run_node(script, data):
	return json.loads(
		subprocess.run(
			["node", "-e", f"const P = require({json.dumps(str(JS_FILE))});" + script],
			input=json.dumps(data), capture_output=True, text=True, encoding="utf-8", check=True,
		).stdout  # fmt: skip
	)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class TestJalaliPicker(unittest.TestCase):
	def test_month_grids(self):
		months = [(jy, jm) for jy in range(1395, 1416) for jm in range(1, 13)]
		grids = run_node(
			"const months = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
			"console.log(JSON.stringify(months.map(([y, m]) => P.monthGrid(y, m))));",
			months,
		)
		for (jy, jm), cells in zip(months, grids):
			label = f"{jy}/{jm}"
			self.assertEqual(len(cells), 42, label)
			# Saturday first: first cell is a Saturday (weekday 5), columns 0..6 repeat
			self.assertEqual(datetime.date.fromisoformat(cells[0]["iso"]).weekday(), 5, label)
			self.assertEqual([c["column"] for c in cells[:7]], list(range(7)), label)
			# consecutive days with matching Jalali labels
			for a, b in zip(cells, cells[1:]):
				self.assertEqual(
					datetime.date.fromisoformat(b["iso"]) - datetime.date.fromisoformat(a["iso"]),
					datetime.timedelta(days=1),
					label,
				)
			for c in cells:
				self.assertEqual(jalali.to_jalali(c["iso"]), (c["jy"], c["jm"], c["jd"]), label)
			# every day of the month exactly once, in order
			in_month = [c["jd"] for c in cells if c["inMonth"]]
			self.assertEqual(in_month, list(range(1, jalali.jalali_month_length(jy, jm) + 1)), label)

	def test_parse_input(self):
		cases = {
			"1405/08/03": {"date": "2026-10-25", "time": ""},
			"۱۴۰۵/۰۸/۰۳": {"date": "2026-10-25", "time": ""},
			"1405-8-3": {"date": "2026-10-25", "time": ""},
			"1405.08.03 14:05": {"date": "2026-10-25", "time": "14:05:00"},
			"۱۴۰۵/۰۸/۰۳ ۰۹:۰۵:۰۷": {"date": "2026-10-25", "time": "09:05:07"},
			"1403/12/30": {"date": "2025-03-20", "time": ""},
			"1404/12/30": None,  # 1404 is not a leap year
			"1405/13/01": None,
			"1405/08/03 24:00": None,
			"10-25-2026": None,  # Gregorian user format falls through to Frappe's parser
			"2026-10-25": None,
			"": None,
		}
		results = run_node(
			"const cases = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
			"console.log(JSON.stringify(cases.map((c) => P.parseInput(c))));",
			list(cases),
		)
		for (text, expected), got in zip(cases.items(), results):
			self.assertEqual(got, expected, text)

	def test_range_shortcuts(self):
		from erpnext_iran.utils.jalali_periods import period_range

		days = [datetime.date(2024, 3, 1) + datetime.timedelta(days=n) for n in range(0, 365 * 3, 5)]
		results = run_node(
			"const days = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
			"console.log(JSON.stringify(days.map((d) => P.SHORTCUTS.map((n) => P.rangeShortcut(n, d)))));",
			[d.isoformat() for d in days],
		)
		seasons = ["Spring", "Summer", "Autumn", "Winter"]
		for day, (this_month, last_month, this_season, this_year) in zip(days, results):
			jy, jm, _ = jalali.to_jalali(day)
			prev_y, prev_m = (jy, jm - 1) if jm > 1 else (jy - 1, 12)
			expected = [
				period_range(jy, str(jm)),
				period_range(prev_y, str(prev_m)),
				period_range(jy, seasons[(jm - 1) // 3]),
				period_range(jy, "Whole Year"),
			]
			got = [this_month, last_month, this_season, this_year]
			self.assertEqual([[d.isoformat() for d in pair] for pair in expected], got, day)

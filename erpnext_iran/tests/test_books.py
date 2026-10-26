import datetime
import unittest

from erpnext_iran.books.core import build_journal, build_ledger, level_map, paginate
from erpnext_iran.utils.jalali_periods import period_range

D = datetime.date

ACCOUNTS = [
	{"name": "1 Assets", "parent_account": None},
	{"name": "11 Current", "parent_account": "1 Assets"},
	{"name": "1101 Cash", "parent_account": "11 Current"},
	{"name": "110101 Till", "parent_account": "1101 Cash"},
	{"name": "110103 Bank", "parent_account": "1101 Cash"},
	{"name": "1103 Receivables", "parent_account": "11 Current"},
	{"name": "110301 Customers", "parent_account": "1103 Receivables"},
	{"name": "4 Income", "parent_account": None},
	{"name": "41 Operating", "parent_account": "4 Income"},
	{"name": "4101 Sales", "parent_account": "41 Operating"},
]


def entry(voucher, account, debit=0, credit=0, date=D(2026, 10, 25)):
	return {"posting_date": date, "voucher_type": "Journal Entry", "voucher_no": voucher,
			"account": account, "debit": debit, "credit": credit, "description": f"desc {voucher}"}  # fmt: skip


class TestLevels(unittest.TestCase):
	def test_general_level(self):
		mapping = level_map(ACCOUNTS, 2)
		self.assertEqual(mapping["110101 Till"], "1101 Cash")
		self.assertEqual(mapping["110301 Customers"], "1103 Receivables")
		self.assertEqual(mapping["4101 Sales"], "4101 Sales")  # a general account with no subsidiaries
		self.assertEqual(mapping["11 Current"], "11 Current")

	def test_subsidiary_level(self):
		self.assertEqual(level_map(ACCOUNTS, None)["110101 Till"], "110101 Till")


class TestJournal(unittest.TestCase):
	def test_netting_and_numbering(self):
		level = level_map(ACCOUNTS, 2)
		entries = [
			entry("JV-1", "4101 Sales", credit=1000),
			entry("JV-1", "110101 Till", debit=400),
			entry("JV-1", "110103 Bank", debit=600),
			# a transfer inside one general account nets to nothing and is skipped
			entry("JV-2", "110101 Till", debit=50),
			entry("JV-2", "110103 Bank", credit=50),
			entry("JV-3", "110301 Customers", debit=200),
			entry("JV-3", "4101 Sales", credit=200),
		]
		rows = build_journal(entries, level, start_number=7)
		self.assertEqual(
			[(r["voucher_number"], r["first"], r["account"], r["debit"], r["credit"]) for r in rows],
			[
				(7, True, "1101 Cash", 1000, 0),  # debit line first
				(7, False, "4101 Sales", 0, 1000),
				(8, True, "1103 Receivables", 200, 0),
				(8, False, "4101 Sales", 0, 200),
			],
		)


class TestLedger(unittest.TestCase):
	def test_opening_and_running_balance(self):
		journal = [
			{"account": "1101 Cash", "debit": 1000.0, "credit": 0.0, "voucher_number": 1},
			{"account": "1101 Cash", "debit": 0.0, "credit": 300.0, "voucher_number": 2},
			{"account": "4101 Sales", "debit": 0.0, "credit": 1000.0, "voucher_number": 1},
		]
		ledger = build_ledger(journal, {"1101 Cash": 500, "1103 Receivables": 0, "2101 Payables": -80},
							  ["1101 Cash", "1103 Receivables", "2101 Payables", "4101 Sales"])  # fmt: skip
		self.assertEqual(list(ledger), ["1101 Cash", "2101 Payables", "4101 Sales"])
		cash = ledger["1101 Cash"]
		self.assertEqual([r["balance"] for r in cash["rows"]], [500, 1500, 1200])
		self.assertTrue(cash["rows"][0]["opening"])
		self.assertEqual((cash["debit"], cash["credit"], cash["balance"]), (1500, 300, 1200))
		self.assertEqual(ledger["2101 Payables"]["rows"][0]["credit"], 80)
		self.assertEqual(ledger["4101 Sales"]["balance"], -1000)


class TestPaginate(unittest.TestCase):
	def test_carry_forward(self):
		rows = [{"debit": 10, "credit": 0}] * 5 + [{"debit": 0, "credit": 7}]
		pages = paginate(rows, 4)
		self.assertEqual(len(pages), 2)
		self.assertEqual(pages[0]["brought_forward"], {"debit": 0, "credit": 0})
		self.assertEqual(pages[0]["carried_forward"], {"debit": 40, "credit": 0})
		self.assertEqual(pages[1]["brought_forward"], {"debit": 40, "credit": 0})
		self.assertEqual(pages[1]["page_total"], {"debit": 10, "credit": 7})
		self.assertEqual(pages[1]["carried_forward"], {"debit": 50, "credit": 7})
		self.assertTrue(pages[0]["first"] and pages[1]["last"])

	def test_empty_book_has_one_page(self):
		self.assertEqual(len(paginate([], 30)), 1)


class TestPeriodRange(unittest.TestCase):
	def test_periods(self):
		self.assertEqual(period_range(1405, "Whole Year"), (D(2026, 3, 21), D(2027, 3, 20)))
		self.assertEqual(period_range(1405, "Autumn"), (D(2026, 9, 23), D(2026, 12, 21)))
		self.assertEqual(period_range(1405, "8"), (D(2026, 10, 23), D(2026, 11, 21)))  # Aban
		self.assertEqual(period_range(1405, "12"), (D(2027, 2, 20), D(2027, 3, 20)))

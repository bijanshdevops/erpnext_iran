"""Checks on shipped JSON/CSV data (chart of accounts, doctype, print format, translations)."""

import ast
import csv
import json
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parent.parent
CHART = APP / "setup" / "data" / "ir_chart_of_accounts.json"
PROPERTY_KEYS = {"account_number", "account_type", "root_type", "is_group", "tax_rate", "account_currency"}
ACCOUNT_TYPES = {
	"Accumulated Depreciation", "Asset Received But Not Billed", "Bank", "Cash", "Chargeable",
	"Capital Work in Progress", "Cost of Goods Sold", "Current Asset", "Current Liability", "Depreciation",
	"Direct Expense", "Direct Income", "Equity", "Expense Account", "Expenses Included In Asset Valuation",
	"Expenses Included In Valuation", "Fixed Asset", "Income Account", "Indirect Expense", "Indirect Income",
	"Liability", "Payable", "Receivable", "Round Off", "Stock", "Stock Adjustment",
	"Stock Received But Not Billed", "Service Received But Not Billed", "Tax", "Temporary",
}  # fmt: skip


def literal_assignment(path, name):
	"""Read a module-level literal without importing the module (it may import frappe)."""
	tree = ast.parse(path.read_text(encoding="utf-8"))
	return next(
		ast.literal_eval(node.value)
		for node in tree.body
		if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == name
	)


def walk(tree, parent_number="", depth=0):
	for name, node in tree.items():
		if name in PROPERTY_KEYS:
			continue
		children = {k: v for k, v in node.items() if k not in PROPERTY_KEYS}
		yield name, node, parent_number, depth, bool(children)
		yield from walk(children, node.get("account_number", ""), depth + 1)


class TestChartOfAccounts(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.chart = json.loads(CHART.read_text(encoding="utf-8"))
		cls.accounts = list(walk(cls.chart["tree"]))

	def test_roots(self):
		roots = {node["root_type"] for name, node, _, depth, _ in self.accounts if depth == 0}
		self.assertEqual(roots, {"Asset", "Liability", "Equity", "Income", "Expense"})

	def test_unique_names_and_numbers(self):
		names = [a[0] for a in self.accounts]
		numbers = [a[1]["account_number"] for a in self.accounts]
		self.assertEqual(len(names), len(set(names)))
		self.assertEqual(len(numbers), len(set(numbers)))

	def test_numbers_nest_under_parent(self):
		for name, node, parent_number, depth, _ in self.accounts:
			self.assertTrue(node["account_number"].startswith(parent_number), name)

	def test_account_types(self):
		for name, node, *_ in self.accounts:
			if "account_type" in node:
				self.assertIn(node["account_type"], ACCOUNT_TYPES, name)

	def test_company_default_accounts_exist_as_leaves(self):
		mapping = literal_assignment(APP / "setup" / "chart_of_accounts.py", "COMPANY_DEFAULTS")
		leaves = {node["account_number"] for _, node, _, _, has_children in self.accounts if not has_children}
		for fieldname, number in mapping.items():
			self.assertIn(number, leaves, fieldname)
		self.assertIn("210201", leaves)  # VAT output
		self.assertIn("110401", leaves)  # VAT input


class TestShippedFiles(unittest.TestCase):
	def test_doctype_json(self):
		path = APP / "erpnext_iran/doctype/iran_localization_settings/iran_localization_settings.json"
		doc = json.loads(path.read_text(encoding="utf-8"))
		fieldnames = [f["fieldname"] for f in doc["fields"]]
		self.assertEqual(fieldnames, doc["field_order"])

		defaults = literal_assignment(APP / "utils" / "settings.py", "DEFAULTS")
		self.assertTrue(set(defaults) <= set(fieldnames))

	def test_print_format_in_sync(self):
		folder = APP / "erpnext_iran/print_format/ir_official_invoice"
		doc = json.loads((folder / "ir_official_invoice.json").read_text(encoding="utf-8"))
		html = (folder / "ir_official_invoice.html").read_text(encoding="utf-8")
		self.assertEqual(doc["html"], html, "run tools/build_print_format.py")

	def test_translations(self):
		with open(APP / "translations" / "fa.csv", encoding="utf-8", newline="") as f:
			rows = list(csv.reader(f))
		self.assertTrue(all(len(row) == 2 and row[0] and row[1] for row in rows), "two columns per row")
		sources = [row[0] for row in rows]
		self.assertEqual(len(sources), len(set(sources)))

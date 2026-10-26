import unittest

from erpnext_iran.utils.vat import classify_invoice, is_exempt_line, split_invoice

VAT = "2102 - VAT - IRT"


class TestVat(unittest.TestCase):
	def test_exempt_line(self):
		self.assertTrue(is_exempt_line('{"2102 - VAT - IRT": 0}', VAT))
		self.assertFalse(is_exempt_line('{"2102 - VAT - IRT": 10}', VAT))
		self.assertFalse(is_exempt_line('{"Other - IRT": 0}', VAT))
		self.assertFalse(is_exempt_line("", VAT))
		self.assertFalse(is_exempt_line(None, VAT))

	def test_split_invoice(self):
		lines = [(1000, None), (500, '{"2102 - VAT - IRT": 0}')]
		self.assertEqual(split_invoice(1500, 100, lines, VAT), (1000, 500))
		# no VAT on the invoice at all: everything is exempt
		self.assertEqual(split_invoice(1500, 0, lines, VAT), (0, 1500))

	def test_credit_note(self):
		self.assertEqual(split_invoice(-1000, -100, [(-1000, None)], VAT), (-1000, 0))

	def test_export_invoice(self):
		lines = [(1000, None), (500, '{"2102 - VAT - IRT": 0}')]
		# what is not taxed on an export invoice is export, not exempt
		self.assertEqual(classify_invoice(1500, 0, lines, VAT, is_export=True), (0, 0, 1500))
		self.assertEqual(classify_invoice(1500, 100, lines, VAT, is_export=True), (1000, 0, 500))
		self.assertEqual(classify_invoice(1500, 0, lines, VAT), (0, 1500, 0))

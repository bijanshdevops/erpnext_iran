import unittest

from erpnext_iran.cheques.core import (
	TRANSITIONS,
	allowed_actions,
	is_valid_sayad_id,
	next_step,
	normalize_sayad_id,
	serial_in_book,
)


class TestChequeLifeCycle(unittest.TestCase):
	def test_received_cheque(self):
		self.assertEqual(next_step("Received", "submit", None), ("Received", [("notes", "party")]))
		self.assertEqual(allowed_actions("Received", "Received"), ["deposit", "clear", "bounce", "endorse"])
		self.assertEqual(next_step("Received", "deposit", "Received"), ("Deposited", [("in_collection", "notes")]))
		self.assertEqual(allowed_actions("Received", "Deposited"), ["clear", "bounce"])
		self.assertEqual(next_step("Received", "clear", "Deposited"), ("Cleared", [("bank", "in_collection")]))
		self.assertEqual(next_step("Received", "bounce", "Deposited"), ("Bounced", [("party", "in_collection")]))
		self.assertEqual(next_step("Received", "endorse", "Received"), ("Endorsed", [("endorsee", "notes")]))
		self.assertEqual(next_step("Received", "bounce", "Endorsed"), ("Bounced", [("party", "endorsee")]))

	def test_final_statuses(self):
		for status in ("Cleared", "Bounced"):
			self.assertEqual(allowed_actions("Received", status), [])
			self.assertEqual(allowed_actions("Issued", status), [])
		self.assertIsNone(next_step("Received", "deposit", "Deposited"))

	def test_issued_cheque(self):
		self.assertEqual(next_step("Issued", "submit", None), ("Issued", [("party", "notes")]))
		self.assertEqual(allowed_actions("Issued", "Issued"), ["clear", "bounce"])
		self.assertEqual(next_step("Issued", "clear", "Issued"), ("Cleared", [("notes", "bank")]))
		self.assertIsNone(next_step("Issued", "deposit", "Issued"))
		self.assertIsNone(next_step("Issued", "endorse", "Issued"))

	def test_every_step_balances(self):
		# each line is one debit and one credit of the cheque amount
		for steps in TRANSITIONS.values():
			for _status, lines in steps.values():
				for debit, credit in lines:
					self.assertNotEqual(debit, credit)


class TestSayadId(unittest.TestCase):
	def test_sayad_id(self):
		self.assertTrue(is_valid_sayad_id("1234567890123456"))
		self.assertTrue(is_valid_sayad_id("۱۲۳۴۵۶۷۸۹۰۱۲۳۴۵۶"))
		self.assertTrue(is_valid_sayad_id("1234-5678-9012-3456"))
		self.assertFalse(is_valid_sayad_id("123456789012345"))
		self.assertFalse(is_valid_sayad_id("12345678901234567"))
		self.assertFalse(is_valid_sayad_id("12345678901234ab"))
		self.assertFalse(is_valid_sayad_id(None))
		self.assertEqual(normalize_sayad_id(" ۱۲۳۴ ۵۶۷۸ ۹۰۱۲ ۳۴۵۶ "), "1234567890123456")

	def test_serial_in_book(self):
		self.assertTrue(serial_in_book("100", 100, 25))
		self.assertTrue(serial_in_book("۱۲۴", 100, 25))
		self.assertFalse(serial_in_book("125", 100, 25))
		self.assertFalse(serial_in_book("99", 100, 25))
		self.assertFalse(serial_in_book("abc", 100, 25))

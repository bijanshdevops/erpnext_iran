import unittest
from pathlib import Path

from erpnext_iran.tests.test_static_files import literal_assignment
from erpnext_iran.utils.iran_system import encode

DSK = Path(__file__).resolve().parent.parent / "payroll" / "dsk.py"


class TestIranSystem(unittest.TestCase):
	def test_letter_shapes(self):
		self.assertEqual(encode("علی"), bytes([0xFC, 0xF3, 0xE4]))  # initial, medial, final
		self.assertEqual(encode("محمد"), bytes([0xA2, 0xF5, 0x9F, 0xF5]))
		# ر does not join the next letter, so ض starts a new shape
		self.assertEqual(encode("رضا"), bytes([0x91, 0xAE, 0xA4]))
		self.assertEqual(encode("مرد"), bytes([0xA2, 0xA4, 0xF5]))
		self.assertEqual(encode("زن"), bytes([0xF6, 0xA5]))

	def test_lam_alef(self):
		self.assertEqual(encode("سلام"), bytes([0xF4, 0xF2, 0xA8]))
		self.assertEqual(encode("عبدالله"), bytes([0xF9, 0xF3, 0xF3, 0x90, 0xA2, 0x93, 0xE4]))

	def test_digits_and_arabic_letters(self):
		self.assertEqual(encode("1405"), bytes([0x85, 0x80, 0x84, 0x81]))
		self.assertEqual(encode("۱۴۰۵"), encode("1405"))
		self.assertEqual(encode("علي"), encode("علی"))

	def test_zwnj_and_brackets(self):
		self.assertEqual(encode("می‌رود"), bytes([0xA2, 0xF8, 0xA4, 0xFC, 0xF5]))
		self.assertEqual(encode("(الف)"), bytes([0x28, 0xE9, 0xF3, 0x90, 0x29]))
		self.assertEqual(encode(""), b"")
		self.assertEqual(encode(None), b"")


class TestInsuranceListLayout(unittest.TestCase):
	def test_record_lengths_match_list_disk(self):
		# record lengths of the empty DSKKAR00.DBF / DSKWOR00.DBF shipped with List Disk 6
		for name, length in (("KAR_FIELDS", 310), ("WOR_FIELDS", 468)):
			fields = literal_assignment(DSK, name)
			self.assertEqual(sum(f[2] for f in fields), length, name)
			self.assertTrue(all(len(f[0]) <= 10 and f[1] in "CNP" for f in fields), name)


if __name__ == "__main__":
	unittest.main()

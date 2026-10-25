import unittest

from erpnext_iran.utils import persian, validators

COEF = (29, 27, 23, 19, 17, 29, 27, 23, 19, 17)


def make_national_code(first9):
	total = sum(int(first9[i]) * (10 - i) for i in range(9))
	r = total % 11
	return first9 + str(r if r < 2 else 11 - r)


def make_legal_id(first10):
	d = int(first10[9]) + 2
	r = sum((int(first10[i]) + d) * COEF[i] for i in range(10)) % 11
	return first10 + str(0 if r == 10 else r)


def make_iban(bban):
	numeric = "".join(str(int(ch, 36)) for ch in bban + "IR00")
	return f"IR{98 - int(numeric) % 97:02d}{bban}"


class TestNationalCode(unittest.TestCase):
	def test_known(self):
		self.assertTrue(validators.is_valid_national_code("0499370899"))
		self.assertTrue(validators.is_valid_national_code("۰۴۹۹۳۷۰۸۹۹"))
		self.assertTrue(validators.is_valid_national_code("049-937089-9"))
		self.assertFalse(validators.is_valid_national_code("0499370898"))

	def test_rejects(self):
		for code in ("", None, "1111111111", "0000000000", "123", "04993708990"):
			self.assertFalse(validators.is_valid_national_code(code), code)

	def test_every_check_digit_branch(self):
		for first9 in ("001234567", "123456789", "287654321", "000000013", "999999990"):
			code = make_national_code(first9)
			self.assertTrue(validators.is_valid_national_code(code), code)
			wrong = code[:9] + str((int(code[9]) + 1) % 10)
			self.assertFalse(validators.is_valid_national_code(wrong), wrong)


class TestLegalId(unittest.TestCase):
	def test_generated(self):
		for first10 in ("1010012345", "1086081457", "1032000110", "1400000999"):
			nid = make_legal_id(first10)
			self.assertTrue(validators.is_valid_legal_national_id(nid), nid)
			wrong = nid[:10] + str((int(nid[10]) + 1) % 10)
			self.assertFalse(validators.is_valid_legal_national_id(wrong), wrong)

	def test_rejects(self):
		for nid in ("", "11111111111", "1234567890", "123456789012"):
			self.assertFalse(validators.is_valid_legal_national_id(nid), nid)

	def test_economic_code(self):
		self.assertTrue(validators.is_valid_economic_code("0499370899"))
		self.assertTrue(validators.is_valid_economic_code(make_legal_id("1010012345")))
		self.assertTrue(validators.is_valid_economic_code("411111111111"))
		self.assertTrue(validators.is_valid_economic_code("14000000000001"))
		self.assertFalse(validators.is_valid_economic_code("0499370898"))
		self.assertFalse(validators.is_valid_economic_code("12345"))


class TestIban(unittest.TestCase):
	def test_published_example(self):
		iban = "IR820540102680020817909002"
		self.assertTrue(validators.is_valid_iban(iban))
		self.assertTrue(validators.is_valid_iban("ir82 0540 1026 8002 0817 9090 02"))
		self.assertEqual(validators.get_bank_from_iban(iban), "بانک پارسیان")

	def test_generated_and_mutated(self):
		iban = make_iban("017" + "0" * 7 + "123456789012")
		self.assertEqual(len(iban), 26)
		self.assertTrue(validators.is_valid_iban(iban), iban)
		self.assertEqual(validators.get_bank_from_iban(iban), "بانک ملی ایران")
		self.assertFalse(validators.is_valid_iban(iban[:-1] + str((int(iban[-1]) + 1) % 10)))

	def test_rejects(self):
		for iban in ("", "IR82054010268002081790900", "DE89370400440532013000", "IRAB0540102680020817909002"):
			self.assertFalse(validators.is_valid_iban(iban), iban)


class TestOtherValidators(unittest.TestCase):
	def test_card(self):
		self.assertTrue(validators.is_valid_card_number("4111 1111 1111 1111"))
		self.assertFalse(validators.is_valid_card_number("4111111111111112"))
		self.assertFalse(validators.is_valid_card_number("0000000000000000"))

	def test_postal_code(self):
		self.assertTrue(validators.is_valid_postal_code("1193653471"))
		self.assertTrue(validators.is_valid_postal_code("۱۱۹۳۶-۵۳۴۷۱"))
		self.assertFalse(validators.is_valid_postal_code("1203653471"))  # 0 in first five
		self.assertFalse(validators.is_valid_postal_code("1111153471"))  # repeated digits
		self.assertFalse(validators.is_valid_postal_code("119365347"))

	def test_mobile(self):
		for value in ("09121234567", "+989121234567", "00989121234567", "9121234567", "۰۹۱۲ ۱۲۳ ۴۵۶۷"):
			self.assertEqual(validators.normalize_mobile(value), "09121234567", value)
		self.assertIsNone(validators.normalize_mobile("02112345678"))


class TestPersian(unittest.TestCase):
	def test_digits(self):
		self.assertEqual(persian.to_english_digits("۱۲۳٤٥"), "12345")
		self.assertEqual(persian.to_persian_digits("1403/01/01"), "۱۴۰۳/۰۱/۰۱")
		self.assertEqual(persian.digits_only("IR-۱۲ ۳"), "123")

	def test_arabic_letters(self):
		self.assertEqual(persian.normalize_arabic_letters("علي كريمي"), "علی کریمی")

	def test_words(self):
		cases = {
			0: "صفر",
			7: "هفت",
			15: "پانزده",
			40: "چهل",
			101: "صد و یک",
			1250: "یک هزار و دویست و پنجاه",
			1000000: "یک میلیون",
			2005000: "دو میلیون و پنج هزار",
			-12: "منفی دوازده",
		}
		for number, words in cases.items():
			self.assertEqual(persian.number_to_words(number), words, number)

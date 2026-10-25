"""Validators for Iranian identifiers. Pure Python (no Frappe import)."""

import re

from erpnext_iran.utils.persian import digits_only, to_english_digits

# Bank code = IBAN characters 5..7 (after "IRkk"). Editable list; codes from the
# Central Bank of Iran "Sheba" scheme.
IBAN_BANK_CODES = {
	"010": "بانک مرکزی",
	"011": "بانک صنعت و معدن",
	"012": "بانک ملت",
	"013": "بانک رفاه کارگران",
	"014": "بانک مسکن",
	"015": "بانک سپه",
	"016": "بانک کشاورزی",
	"017": "بانک ملی ایران",
	"018": "بانک تجارت",
	"019": "بانک صادرات ایران",
	"020": "بانک توسعه صادرات",
	"021": "پست بانک",
	"022": "بانک توسعه تعاون",
	"053": "بانک کارآفرین",
	"054": "بانک پارسیان",
	"055": "بانک اقتصاد نوین",
	"056": "بانک سامان",
	"057": "بانک پاسارگاد",
	"058": "بانک سرمایه",
	"059": "بانک سینا",
	"060": "بانک قرض‌الحسنه مهر ایران",
	"061": "بانک شهر",
	"062": "بانک آینده",
	"064": "بانک گردشگری",
	"066": "بانک دی",
	"069": "بانک ایران زمین",
	"070": "بانک قرض‌الحسنه رسالت",
	"078": "بانک خاورمیانه",
}

_LEGAL_ID_COEFFICIENTS = (29, 27, 23, 19, 17, 29, 27, 23, 19, 17)
_POSTAL_CODE_RE = re.compile(r"^(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}$")
_MOBILE_RE = re.compile(r"^(?:\+98|0098|98|0)?(9\d{9})$")


def is_valid_national_code(code):
	"""کد ملی - 10 digit national code of a natural person."""
	code = digits_only(code)
	if len(code) != 10 or len(set(code)) == 1:
		return False
	check = int(code[9])
	total = sum(int(code[i]) * (10 - i) for i in range(9))
	r = total % 11
	return check == r if r < 2 else check == 11 - r


def is_valid_legal_national_id(nid):
	"""شناسه ملی - 11 digit national ID of a legal entity."""
	nid = digits_only(nid)
	if len(nid) != 11 or len(set(nid)) == 1:
		return False
	d = int(nid[9]) + 2
	total = sum((int(nid[i]) + d) * _LEGAL_ID_COEFFICIENTS[i] for i in range(10))
	r = total % 11
	if r == 10:
		r = 0
	return r == int(nid[10])


def is_valid_economic_code(code):
	"""کد اقتصادی / شناسه مالیاتی.

	Accepts the legacy 12-digit code, the 14-digit code, a 10-digit national code
	(natural persons) or an 11-digit legal national ID (legal entities).
	"""
	code = digits_only(code)
	if len(code) == 10:
		return is_valid_national_code(code)
	if len(code) == 11:
		return is_valid_legal_national_id(code)
	return len(code) in (12, 14) and len(set(code)) > 1


def normalize_iban(iban):
	if not iban:
		return ""
	text = to_english_digits(iban).upper()
	return "".join(ch for ch in text if ch.isalnum())


def is_valid_iban(iban):
	"""شماره شبا - IR + 24 digits, ISO 13616 mod-97 check."""
	iban = normalize_iban(iban)
	if not re.fullmatch(r"IR\d{24}", iban):
		return False
	rearranged = iban[4:] + iban[:4]
	numeric = "".join(str(int(ch, 36)) for ch in rearranged)
	return int(numeric) % 97 == 1


def get_bank_from_iban(iban):
	iban = normalize_iban(iban)
	if len(iban) < 7:
		return None
	return IBAN_BANK_CODES.get(iban[4:7])


def is_valid_card_number(card):
	"""شماره کارت بانکی - 16 digits, Luhn check."""
	card = digits_only(card)
	if len(card) != 16 or len(set(card)) == 1:
		return False
	total = 0
	for i, ch in enumerate(card):
		n = int(ch)
		if i % 2 == 0:
			n *= 2
			if n > 9:
				n -= 9
		total += n
	return total % 10 == 0


def is_valid_postal_code(code):
	"""کد پستی - 10 digits; first five digits never contain 0 or 2."""
	return bool(_POSTAL_CODE_RE.match(digits_only(code)))


def normalize_mobile(mobile):
	"""Return '09xxxxxxxxx' for any common Iranian mobile notation, else None."""
	if not mobile:
		return None
	text = "".join(ch for ch in to_english_digits(mobile) if ch.isdigit() or ch == "+")
	m = _MOBILE_RE.match(text)
	return "0" + m.group(1) if m else None

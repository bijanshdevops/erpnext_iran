"""Persian text helpers: digit conversion, Arabic->Persian letters, numbers to words.

Pure Python (no Frappe import) so it can be unit tested without a bench.
"""

_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
_ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

_TO_ASCII = str.maketrans(_PERSIAN_DIGITS + _ARABIC_DIGITS, "0123456789" * 2)
_TO_PERSIAN = str.maketrans("0123456789", _PERSIAN_DIGITS)

# Arabic Yeh / Alef Maksura / Kaf -> Persian Yeh / Keheh
_ARABIC_LETTERS = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک", "ة": "ه"})


def to_english_digits(value):
	if value is None:
		return None
	return str(value).translate(_TO_ASCII)


def to_persian_digits(value):
	if value is None:
		return None
	return str(value).translate(_TO_PERSIAN)


def digits_only(value):
	"""Normalise Persian/Arabic digits and drop every non-digit (spaces, dashes...)."""
	if value is None:
		return ""
	return "".join(ch for ch in to_english_digits(value) if ch.isdigit())


def normalize_arabic_letters(value):
	if not value:
		return value
	return str(value).translate(_ARABIC_LETTERS)


_ONES = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
_TEENS = ["ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"]
_TENS = ["", "", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"]
_HUNDREDS = ["", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"]
_SCALES = ["", "هزار", "میلیون", "میلیارد", "تریلیون", "کوادریلیون"]


def _three_digits_to_words(n):
	parts = []
	hundreds, rest = divmod(n, 100)
	if hundreds:
		parts.append(_HUNDREDS[hundreds])
	if 10 <= rest < 20:
		parts.append(_TEENS[rest - 10])
	else:
		tens, ones = divmod(rest, 10)
		if tens:
			parts.append(_TENS[tens])
		if ones:
			parts.append(_ONES[ones])
	return " و ".join(parts)


def number_to_words(number):
	"""Convert an integer to Persian words, e.g. 1250 -> 'یک هزار و دویست و پنجاه'."""
	number = int(number)
	if number == 0:
		return "صفر"
	if number < 0:
		return "منفی " + number_to_words(-number)

	groups = []
	while number:
		number, group = divmod(number, 1000)
		groups.append(group)
	if len(groups) > len(_SCALES):
		raise ValueError("Number too large")

	words = []
	for scale_index in range(len(groups) - 1, -1, -1):
		group = groups[scale_index]
		if not group:
			continue
		text = _three_digits_to_words(group)
		if _SCALES[scale_index]:
			text = f"{text} {_SCALES[scale_index]}"
		words.append(text)
	return " و ".join(words)

"""Persian text in the Iran System code page, the DOS encoding the social security list files use.

Iran System stores the shape of each letter (isolated, final, initial or medial) as its own byte,
in visual order: the string is reversed, as the reference converter used for these files does.

Pure Python (no Frappe import) so it can be unit tested without a bench.
"""

from erpnext_iran.utils.persian import normalize_arabic_letters, to_english_digits

ZWNJ = "‌"

# letter: (isolated, final, initial, medial)
_SHAPES = {
	"ب": (0x92, 0x92, 0x93, 0x93),
	"پ": (0x94, 0x94, 0x95, 0x95),
	"ت": (0x96, 0x96, 0x97, 0x97),
	"ث": (0x98, 0x98, 0x99, 0x99),
	"ج": (0x9A, 0x9A, 0x9B, 0x9B),
	"چ": (0x9C, 0x9C, 0x9D, 0x9D),
	"ح": (0x9E, 0x9E, 0x9F, 0x9F),
	"خ": (0xA0, 0xA0, 0xA1, 0xA1),
	"س": (0xA7, 0xA7, 0xA8, 0xA8),
	"ش": (0xA9, 0xA9, 0xAA, 0xAA),
	"ص": (0xAB, 0xAB, 0xAC, 0xAC),
	"ض": (0xAD, 0xAD, 0xAE, 0xAE),
	"ط": (0xAF, 0xAF, 0xAF, 0xAF),
	"ظ": (0xE0, 0xE0, 0xE0, 0xE0),
	"ع": (0xE1, 0xE2, 0xE4, 0xE3),
	"غ": (0xE5, 0xE6, 0xE8, 0xE7),
	"ف": (0xE9, 0xE9, 0xEA, 0xEA),
	"ق": (0xEB, 0xEB, 0xEC, 0xEC),
	"ک": (0xED, 0xED, 0xEE, 0xEE),
	"گ": (0xEF, 0xEF, 0xF0, 0xF0),
	"ل": (0xF1, 0xF1, 0xF3, 0xF3),
	"م": (0xF4, 0xF4, 0xF5, 0xF5),
	"ن": (0xF6, 0xF6, 0xF7, 0xF7),
	"ه": (0xF9, 0xF9, 0xFB, 0xFA),
	"ی": (0xFD, 0xFC, 0xFE, 0xFE),
	"ئ": (0xFD, 0xFC, 0x8E, 0x8E),
	"ـ": (0x8B, 0x8B, 0x8B, 0x8B),
	# letters that never join the next one: (isolated, final)
	"ا": (0x90, 0x91),
	"أ": (0x90, 0x91),
	"إ": (0x90, 0x91),
	"آ": (0x8D, 0x8D),
	"د": (0xA2, 0xA2),
	"ذ": (0xA3, 0xA3),
	"ر": (0xA4, 0xA4),
	"ز": (0xA5, 0xA5),
	"ژ": (0xA6, 0xA6),
	"و": (0xF8, 0xF8),
	"ؤ": (0xF8, 0xF8),
	"ء": (0x8F, 0x8F),
}
_PUNCTUATION = {"،": 0x8A, "؟": 0x8C, "؛": ord(";")}
_LAM_ALEF = 0xF2
_ALEFS = "اأإآ"
# the text is reversed, so paired brackets swap to keep facing the right way
_MIRROR = str.maketrans("()[]{}<>", ")(][}{><")


def _joins_next(ch):
	return len(_SHAPES.get(ch, ())) == 4


def _joins_previous(ch):
	return ch in _SHAPES and ch != "ء"


def encode(text):
	"""Iran System bytes of text, in visual (reversed) order."""
	text = normalize_arabic_letters(to_english_digits(str(text or "")))
	logical = []
	i = 0
	while i < len(text):
		ch = text[i]
		prev = text[i - 1] if i else ""
		nxt = text[i + 1] if i + 1 < len(text) else ""
		joined = _joins_next(prev) and _joins_previous(ch)
		if ch == ZWNJ:
			pass  # it only stops the letters around it from joining, which the checks above see
		elif ch == "ل" and nxt and nxt in _ALEFS:
			logical.append(_LAM_ALEF)
			i += 1
		elif ch in _SHAPES:
			shapes = _SHAPES[ch]
			if len(shapes) == 4:
				links_next = _joins_previous(nxt)
				logical.append(shapes[(2 if links_next else 0) + (1 if joined else 0)])
			else:
				logical.append(shapes[1 if joined else 0])
		elif ch.isdigit() and ch.isascii():
			logical.append(0x80 + int(ch))
		elif ch in _PUNCTUATION:
			logical.append(_PUNCTUATION[ch])
		elif " " <= ch <= "~":
			logical.append(ord(ch.translate(_MIRROR)))
		else:
			logical.append(ord("?"))
		i += 1
	return bytes(reversed(logical))

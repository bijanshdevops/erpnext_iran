"""Moadian 22 character tax ID (شماره منحصر به فرد مالیاتی). Pure Python.

Layout: memory ID (6) + days since Unix epoch in hex (5) + internal serial in hex (10)
+ Verhoeff check digit (1), computed over the decimal form of the same three parts.
Verify against the Tax Organization's current technical guide before production use.
"""

import re

_D = [
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
	[2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
	[3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
	[4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
	[5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
	[6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
	[7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
	[8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
	[9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
_P = [
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
	[5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
	[8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
	[9, 4, 5, 3, 1, 2, 7, 6, 8, 0],
	[4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
	[2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
	[7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]
_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def verhoeff_check_digit(number):
	c = 0
	for i, ch in enumerate(reversed(str(number))):
		c = _D[c][_P[(i + 1) % 8][int(ch)]]
	return _INV[c]


def verhoeff_is_valid(number):
	c = 0
	for i, ch in enumerate(reversed(str(number))):
		c = _D[c][_P[i % 8][int(ch)]]
	return c == 0


def _memory_id_to_decimal(memory_id):
	return "".join(ch if ch.isdigit() else str(ord(ch)) for ch in memory_id)


def generate_tax_id(memory_id, timestamp, serial):
	"""memory_id: 6 char fiscal memory ID, timestamp: invoice time (Unix seconds), serial: int."""
	memory_id = (memory_id or "").strip().upper()
	if not re.fullmatch(r"[A-Z0-9]{6}", memory_id):
		raise ValueError("Fiscal memory ID must be 6 letters or digits")
	serial = int(serial)
	if not 0 < serial < 16**10:
		raise ValueError("Serial out of range")

	days = int(timestamp // 86400)
	decimal = _memory_id_to_decimal(memory_id).zfill(6) + str(days).zfill(6) + str(serial).zfill(12)
	check = verhoeff_check_digit(decimal)
	return f"{memory_id}{days:05x}{serial:010x}{check}".upper()


def serial_from_tax_id(tax_id):
	return int(tax_id[11:21], 16)

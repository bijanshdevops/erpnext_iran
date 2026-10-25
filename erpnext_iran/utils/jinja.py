"""Helpers available in print formats and Jinja templates."""

from erpnext_iran.utils.jalali import format_jalali
from erpnext_iran.utils.persian import number_to_words, to_persian_digits


def jalali_date(value, fmt="%Y/%m/%d", persian=False):
	return format_jalali(value, fmt, persian_digits=persian)


def persian_digits(value):
	return to_persian_digits(value)


def amount_in_words_fa(amount, currency="ریال"):
	words = number_to_words(int(round(float(amount or 0))))
	return f"{words} {currency}".strip()


def ir_invoice_lines(doc):
	from erpnext_iran.moadian.api import get_invoice_lines

	return get_invoice_lines(doc)


def ir_invoice_totals(lines):
	from erpnext_iran.moadian.payload import compute_totals

	return compute_totals(lines)

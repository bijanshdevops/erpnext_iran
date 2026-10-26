"""VAT return arithmetic shared by the IR VAT Return report. Pure Python."""

import json


def is_exempt_line(item_tax_rate, vat_account):
	"""True when the line's Item Tax Template sets the VAT account to 0% (e.g. "VAT Exempt")."""
	if not item_tax_rate:
		return False
	rates = json.loads(item_tax_rate) if isinstance(item_tax_rate, str) else item_tax_rate
	return vat_account in rates and float(rates[vat_account] or 0) == 0


def split_invoice(net_total, vat, lines, vat_account):
	"""(taxable, exempt) part of an invoice's net total.

	lines are (net_amount, item_tax_rate) pairs. An invoice without VAT is exempt as a whole;
	otherwise lines whose item tax template zeroes the VAT account are exempt.
	"""
	if not vat:
		return 0.0, float(net_total)
	taxable = sum(float(amount) for amount, rate in lines if not is_exempt_line(rate, vat_account))
	return taxable, float(net_total) - taxable

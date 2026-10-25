"""Build the Moadian invoice JSON (header / body / payments) from a Sales Invoice.

Field names follow the Tax Organization's invoice schema. Amounts are in Rial (company
currency) and rounded to integers. compute_invoice_lines() is shared with the print format.
"""

import json

PERSON_TYPE_CODES = {
	"Natural Person": 1,
	"Legal Entity": 2,
	"Civil Partnership": 3,
	"Foreign National": 4,
}
END_CONSUMER = 5


def _flt(value):
	try:
		return float(value or 0)
	except (TypeError, ValueError):
		return 0.0


def _rial(value):
	return int(round(_flt(value)))


def item_tax_rates(doc):
	"""{item_code: total rate} parsed from item_wise_tax_detail, or None when unavailable."""
	rates = {}
	for tax in doc.get("taxes") or []:
		detail = tax.get("item_wise_tax_detail")
		if not detail:
			return None
		if isinstance(detail, str):
			try:
				detail = json.loads(detail)
			except ValueError:
				return None
		if not isinstance(detail, dict):
			return None
		for item_code, value in detail.items():
			rate = value[0] if isinstance(value, (list, tuple)) else value
			rates[item_code] = rates.get(item_code, 0.0) + _flt(rate)
	return rates


def compute_invoice_lines(doc, default_vat_rate=0):
	taxes = doc.get("taxes") or []
	rates = item_tax_rates(doc) if taxes else {}
	lines = []
	for row in doc.get("items") or []:
		qty = abs(_flt(row.get("qty")))
		after_discount = abs(_rial(row.get("base_net_amount")))
		unit_price = abs(_flt(row.get("base_price_list_rate"))) or abs(_flt(row.get("base_rate")))
		before_discount = _rial(qty * unit_price)
		if before_discount < after_discount:
			# priced above list (margin) or no list price: no discount to report
			before_discount = after_discount
			unit_price = after_discount / qty if qty else 0
		discount = before_discount - after_discount

		if not taxes:
			vat_rate = 0.0
		elif rates is None:
			vat_rate = _flt(default_vat_rate)
		else:
			vat_rate = rates.get(row.get("item_code") or row.get("item_name"), 0.0)
		vat_amount = _rial(after_discount * vat_rate / 100)

		lines.append(
			{
				"idx": row.get("idx"),
				"item_code": row.get("item_code"),
				"description": row.get("item_name") or row.get("description"),
				"stuff_id": row.get("ir_stuff_id"),
				"uom": row.get("uom"),
				"unit_code": row.get("ir_moadian_unit_code"),
				"qty": qty,
				"unit_price": _rial(unit_price),
				"before_discount": before_discount,
				"discount": discount,
				"after_discount": after_discount,
				"vat_rate": vat_rate,
				"vat_amount": vat_amount,
				"total": after_discount + vat_amount,
			}
		)
	return lines


def compute_totals(lines):
	totals = {
		key: sum(line[key] for line in lines)
		for key in ("before_discount", "discount", "after_discount", "vat_amount", "total")
	}
	return totals


def build_payload(invoice, seller, buyer, lines, tax_id, timestamp_ms, invoice_type=1, reference_tax_id=None):
	"""invoice/seller/buyer are plain dicts; see moadian.api for how they are filled."""
	totals = compute_totals(lines)
	paid = min(_rial(invoice.get("paid_amount")), totals["total"])
	credit = totals["total"] - paid
	settlement = 1 if credit == 0 else (2 if paid == 0 else 3)

	header = {
		"taxid": tax_id,
		"indatim": timestamp_ms,
		"indati2m": timestamp_ms,
		"inty": int(invoice_type),
		"inno": tax_id[11:21] if tax_id else None,
		"irtaxid": reference_tax_id,
		"inp": 1,
		"ins": int(invoice.get("subject") or 1),
		"tins": seller.get("tax_code"),
		"tprdis": totals["before_discount"],
		"tdis": totals["discount"],
		"tadis": totals["after_discount"],
		"tvam": totals["vat_amount"],
		"todam": 0,
		"tbill": totals["total"],
		"setm": settlement,
		"cap": paid,
		"insp": credit,
	}
	if int(invoice_type) == 1:
		header.update(
			{
				"tob": PERSON_TYPE_CODES.get(buyer.get("person_type"), END_CONSUMER),
				"bid": buyer.get("national_id"),
				"tinb": buyer.get("economic_code") or buyer.get("national_id"),
				"bpc": buyer.get("postal_code"),
			}
		)

	body = [
		{
			"sstid": line["stuff_id"],
			"sstt": line["description"],
			"am": line["qty"],
			"mu": line["unit_code"],
			"fee": line["unit_price"],
			"prdis": line["before_discount"],
			"dis": line["discount"],
			"adis": line["after_discount"],
			"vra": line["vat_rate"],
			"vam": line["vat_amount"],
			"tsstam": line["total"],
		}
		for line in lines
	]
	return {"header": header, "body": body, "payments": []}


def validate_payload(payload):
	"""Return a list of problems that would make the Tax Organization reject the invoice."""
	problems = []
	header = payload["header"]
	if not header.get("taxid") or len(header["taxid"]) != 22:
		problems.append("Tax ID missing or not 22 characters")
	if not header.get("tins"):
		problems.append("Seller economic code / national ID missing")
	if header.get("inty") == 1 and not header.get("bid") and not header.get("tinb"):
		problems.append("Buyer national ID or economic code missing (invoice type 1)")
	if header.get("ins") in (2, 3, 4) and not header.get("irtaxid"):
		problems.append("Reference tax ID required for correction, cancellation or return")
	for i, row in enumerate(payload["body"], start=1):
		if not row.get("sstid") or len(str(row["sstid"])) != 13:
			problems.append(f"Row {i}: 13 digit goods/service ID missing")
		if not row.get("mu"):
			problems.append(f"Row {i}: Moadian unit code missing on UOM")
	return problems

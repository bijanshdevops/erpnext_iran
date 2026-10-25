import datetime
import json
import unittest

from erpnext_iran.moadian import payload, taxid


class TestTaxId(unittest.TestCase):
	def test_verhoeff(self):
		self.assertEqual(taxid.verhoeff_check_digit("236"), 3)
		self.assertTrue(taxid.verhoeff_is_valid("2363"))
		self.assertFalse(taxid.verhoeff_is_valid("2364"))

	def test_structure(self):
		ts = datetime.datetime(2025, 3, 21, 10, 0, tzinfo=datetime.timezone.utc).timestamp()
		tax_id = taxid.generate_tax_id("a1b2c3", ts, 1234)
		self.assertEqual(len(tax_id), 22)
		self.assertTrue(tax_id.startswith("A1B2C3"))
		days = int(ts // 86400)
		self.assertEqual(int(tax_id[6:11], 16), days)
		self.assertEqual(taxid.serial_from_tax_id(tax_id), 1234)

		numeric_memory = "".join(c if c.isdigit() else str(ord(c)) for c in "A1B2C3")
		decimal = numeric_memory.zfill(6) + str(days).zfill(6) + str(1234).zfill(12)
		self.assertTrue(taxid.verhoeff_is_valid(decimal + tax_id[-1]))

	def test_rejects(self):
		with self.assertRaises(ValueError):
			taxid.generate_tax_id("ABC", 0, 1)
		with self.assertRaises(ValueError):
			taxid.generate_tax_id("ABCDEF", 0, 0)


def make_invoice(taxes=True, detail_as_json=True):
	items = [
		{"idx": 1, "item_code": "A", "item_name": "کالای الف", "ir_stuff_id": "2710000138624",
		 "uom": "Nos", "qty": 2, "base_price_list_rate": 1_000_000, "base_rate": 900_000,
		 "base_net_amount": 1_800_000},
		{"idx": 2, "item_code": "B", "item_name": "خدمت ب", "ir_stuff_id": "2720000114542",
		 "uom": "Hour", "qty": 3, "base_price_list_rate": 0, "base_rate": 500_000,
		 "base_net_amount": 1_500_000},
	]  # fmt: skip
	detail = {"A": [10, 180_000], "B": [0, 0]}
	tax_rows = [{"item_wise_tax_detail": json.dumps(detail) if detail_as_json else detail}]
	return {"items": items, "taxes": tax_rows if taxes else []}


class TestPayload(unittest.TestCase):
	def test_lines(self):
		lines = payload.compute_invoice_lines(make_invoice(), default_vat_rate=10)
		a, b = lines
		self.assertEqual(
			(a["unit_price"], a["before_discount"], a["discount"], a["after_discount"]),
			(1_000_000, 2_000_000, 200_000, 1_800_000),
		)
		self.assertEqual((a["vat_rate"], a["vat_amount"], a["total"]), (10, 180_000, 1_980_000))
		self.assertEqual((b["unit_price"], b["discount"], b["vat_amount"], b["total"]), (500_000, 0, 0, 1_500_000))

	def test_vat_fallbacks(self):
		no_tax = payload.compute_invoice_lines(make_invoice(taxes=False), 10)
		self.assertEqual([line["vat_rate"] for line in no_tax], [0, 0])
		dict_detail = payload.compute_invoice_lines(make_invoice(detail_as_json=False), 10)
		self.assertEqual([line["vat_rate"] for line in dict_detail], [10, 0])
		unparsed = make_invoice()
		unparsed["taxes"][0]["item_wise_tax_detail"] = "not json"
		self.assertEqual([line["vat_rate"] for line in payload.compute_invoice_lines(unparsed, 10)], [10, 10])

	def test_return_invoice_amounts_are_positive(self):
		inv = make_invoice()
		for row in inv["items"]:
			row["qty"] = -row["qty"]
			row["base_net_amount"] = -row["base_net_amount"]
		lines = payload.compute_invoice_lines(inv, 10)
		self.assertEqual(lines[0]["after_discount"], 1_800_000)
		self.assertEqual(lines[0]["qty"], 2)

	def test_build_and_validate(self):
		lines = payload.compute_invoice_lines(make_invoice(), 10)
		for line in lines:
			line["unit_code"] = "1627"
		tax_id = taxid.generate_tax_id("A1B2C3", 1_742_550_000, 7)
		data = payload.build_payload(
			{"subject": 1, "paid_amount": 1_000_000},
			{"tax_code": "14000000000001"},
			{"person_type": "Legal Entity", "national_id": "10100123459", "postal_code": "1193653471"},
			lines,
			tax_id,
			1_742_550_000_000,
		)
		h = data["header"]
		self.assertEqual((h["tprdis"], h["tdis"], h["tadis"], h["tvam"], h["tbill"]),
			(3_500_000, 200_000, 3_300_000, 180_000, 3_480_000))  # fmt: skip
		self.assertEqual((h["setm"], h["cap"], h["insp"]), (3, 1_000_000, 2_480_000))
		self.assertEqual((h["tob"], h["tinb"], h["inno"]), (2, "10100123459", tax_id[11:21]))
		self.assertEqual(len(data["body"]), 2)
		self.assertEqual(payload.validate_payload(data), [])

		without_buyer = payload.build_payload({}, {"tax_code": "1"}, {}, lines, tax_id, 0, invoice_type=2)
		self.assertNotIn("tob", without_buyer["header"])
		self.assertEqual(without_buyer["header"]["setm"], 2)

	def test_validate_reports_problems(self):
		lines = payload.compute_invoice_lines(make_invoice(), 10)
		lines[0]["stuff_id"] = None
		data = payload.build_payload({"subject": 4}, {}, {}, lines, None, 0)
		problems = payload.validate_payload(data)
		self.assertEqual(len(problems), 7, problems)

"""End-to-end tests against a real ERPNext site.

    bench --site <site> run-tests --module erpnext_iran.tests.test_integration
"""

import unittest

try:
	import frappe
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	raise unittest.SkipTest("frappe is not installed") from None

from erpnext.controllers.accounts_controller import get_taxes_and_charges
from frappe import _
from frappe.utils import getdate

from erpnext_iran.moadian.api import get_moadian_payload
from erpnext_iran.setup.api import setup_company
from erpnext_iran.setup.chart_of_accounts import get_account
from erpnext_iran.utils.jalali import format_jalali

COMPANY = "شرکت آزمایشی ایران"
ABBR = "IRT"
VALID_NATIONAL_CODE = "0499370899"
VALID_IBAN = "IR820540102680020817909002"


def iran_country():
	return frappe.db.get_value("Country", {"code": "ir"}, "name")


CUSTOMER_GROUP = "IR Test Customers"
ITEM_GROUP = "IR Test Items"


def ensure_groups():
	"""A site created without the setup wizard only has the (group) root nodes."""
	if not frappe.db.exists("Customer Group", CUSTOMER_GROUP):
		frappe.get_doc(
			{"doctype": "Customer Group", "customer_group_name": CUSTOMER_GROUP,
			 "parent_customer_group": "All Customer Groups"}
		).insert()  # fmt: skip
	if not frappe.db.exists("Item Group", ITEM_GROUP):
		frappe.get_doc(
			{"doctype": "Item Group", "item_group_name": ITEM_GROUP, "parent_item_group": "All Item Groups"}
		).insert()


def ensure_company():
	if frappe.db.exists("Company", COMPANY):
		return frappe.get_doc("Company", COMPANY)
	company = frappe.get_doc(
		{
			"doctype": "Company",
			"company_name": "شركت آزمايشي ايران",  # Arabic Kaf/Yeh on purpose
			"abbr": ABBR,
			"country": iran_country(),
			"default_currency": "IRR",
			"ir_economic_code": "411111111111",
			"ir_moadian_memory_id": "A1B2C3",
		}
	).insert()
	return company


class TestIranLocalization(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		settings = frappe.get_doc("Iran Localization Settings")
		settings.moadian_enabled = 1
		settings.moadian_memory_id = "A1B2C3"
		settings.save()
		ensure_groups()
		cls.company = ensure_company()
		if not get_account(COMPANY, "110101"):
			setup_company(
				COMPANY,
				apply_chart=1,
				create_taxes=1,
				vat_rate=10,
				jalali_year=1405,
				create_holiday_list=1,
			)

	def test_custom_fields_and_settings(self):
		for doctype, fieldname in [
			("Customer", "ir_national_id"),
			("Supplier", "ir_economic_code"),
			("Company", "ir_moadian_memory_id"),
			("Item", "ir_stuff_id"),
			("UOM", "ir_moadian_unit_code"),
			("Sales Invoice", "ir_tax_id"),
			("Sales Invoice Item", "ir_stuff_id"),
		]:
			self.assertTrue(frappe.get_meta(doctype).has_field(fieldname), f"{doctype}.{fieldname}")
		self.assertEqual(frappe.db.get_value("Currency", "IRR", "number_format"), "#,###")
		self.assertEqual(frappe.db.get_value("Currency", "IRR", "enabled"), 1)

	def test_warehouses_and_system_defaults(self):
		from erpnext_iran.setup.localization import apply_system_defaults, rename_default_warehouses

		rename_default_warehouses(COMPANY)
		names = set(frappe.get_all("Warehouse", filters={"company": COMPANY}, pluck="warehouse_name"))
		self.assertTrue({"همه انبارها", "انبار اصلی", "انبار محصول", "کالای در راه"} <= names, names)
		stores = frappe.db.get_value("Warehouse", {"company": COMPANY, "warehouse_name": "انبار اصلی"})
		self.assertEqual(frappe.db.get_value("Warehouse", stores, "parent_warehouse"), f"همه انبارها - {ABBR}")
		self.assertEqual(rename_default_warehouses(COMPANY), [])  # idempotent

		# record already Tehran but site defaults stale: the form would show the stale value
		frappe.db.set_single_value("System Settings", "time_zone", "Asia/Tehran")
		frappe.db.set_default("time_zone", "America/New_York")
		apply_system_defaults()
		fields = ["time_zone", "currency", "date_format", "first_day_of_the_week", "country"]
		values = frappe.db.get_values("System Settings", "System Settings", fields)[0]
		self.assertEqual(tuple(values), ("Asia/Tehran", "IRR", "yyyy-mm-dd", "Saturday", "Iran"))
		# what the System Settings form loads
		from frappe.core.doctype.system_settings.system_settings import load

		loaded = load()["defaults"]  # only Select / Data fields (time zone, date format, week start)
		for fieldname, value in zip(fields, values):
			if fieldname in loaded:
				self.assertEqual(loaded[fieldname], value, fieldname)
		self.assertEqual(loaded["time_zone"], "Asia/Tehran")
		self.assertEqual(frappe.db.get_default("country"), "Iran")

	def test_profit_and_loss_by_jalali_month(self):
		from erpnext.accounts.report.profit_and_loss_statement import profit_and_loss_statement

		from erpnext_iran.overrides import report_periods

		report_periods.apply()
		filters = frappe._dict(
			company=COMPANY,
			filter_based_on="Fiscal Year",
			period_start_date="2026-03-21",
			period_end_date="2027-03-20",
			from_fiscal_year="1405",
			to_fiscal_year="1405",
			periodicity="Monthly",
			presentation_currency="IRR",
		)
		columns, data = profit_and_loss_statement.execute(filters)[:2]
		period_columns = [c for c in columns if c["fieldname"].startswith("j1405_")]
		self.assertEqual(len(period_columns), 12)
		self.assertEqual(period_columns[0]["label"], "فروردین 1405")
		self.assertEqual(period_columns[7]["label"], "آبان 1405")

		income = next(r for r in data if r.get("account", "").startswith("4 - "))
		self.assertGreater(income["j1405_08"], 0)  # demo invoice of 3 Aban 1405 falls in Aban
		self.assertEqual(income.get("j1405_07", 0), 0)
		self.assertAlmostEqual(sum(income[c["fieldname"]] for c in period_columns), income["total"], places=2)

		# switched off: ERPNext's own Gregorian months
		frappe.db.set_single_value("Iran Localization Settings", "jalali_report_periods", 0)
		frappe.clear_document_cache("Iran Localization Settings", "Iran Localization Settings")
		columns = profit_and_loss_statement.execute(filters)[0]
		self.assertFalse([c for c in columns if c["fieldname"].startswith("j1405_")])
		frappe.db.set_single_value("Iran Localization Settings", "jalali_report_periods", 1)
		frappe.clear_document_cache("Iran Localization Settings", "Iran Localization Settings")

	def test_rial_found_by_persian_name(self):
		from frappe.desk.search import search_link

		results = search_link("Currency", "ریال", page_length=20)
		self.assertIn("IRR", [r["value"] for r in results])
		irr = next(r for r in results if r["value"] == "IRR")
		self.assertIn("ریال ایران", irr.get("description") or "")
		self.assertTrue(frappe.db.exists("Print Format", "IR Official Invoice"))

	def test_company_name_normalized(self):
		# created with Arabic letters; both the record ID and the name must be Persian
		self.assertEqual(self.company.name, COMPANY)
		self.assertEqual(self.company.company_name, COMPANY)
		self.assertEqual(frappe.db.get_value("Company", COMPANY, "ir_person_type"), "Legal Entity")

	def test_chart_and_defaults(self):
		accounts = frappe.get_all("Account", filters={"company": COMPANY}, pluck="account_number")
		self.assertIn("110401", accounts)
		self.assertIn("210201", accounts)
		company = frappe.get_doc("Company", COMPANY)
		self.assertEqual(company.default_receivable_account, get_account(COMPANY, "110301"))
		self.assertEqual(company.default_income_account, get_account(COMPANY, "4101"))
		self.assertEqual(company.round_off_account, get_account(COMPANY, "5213"))

	def test_tax_templates(self):
		template = frappe.get_doc("Sales Taxes and Charges Template", {"company": COMPANY})
		self.assertEqual(template.taxes[0].rate, 10)
		self.assertEqual(template.taxes[0].account_head, get_account(COMPANY, "210201"))
		self.assertTrue(frappe.db.exists("Purchase Taxes and Charges Template", {"company": COMPANY}))
		self.assertTrue(frappe.db.exists("Item Tax Template", {"company": COMPANY}))

	def test_fiscal_year_and_holidays(self):
		fy = frappe.get_doc("Fiscal Year", "1405")
		self.assertEqual(getdate(fy.year_start_date), getdate("2026-03-21"))
		self.assertEqual(getdate(fy.year_end_date), getdate("2027-03-20"))
		from erpnext_iran.setup.iran_calendar import add_iran_holidays, create_iran_holiday_list

		holiday_list = frappe.db.get_value("Company", COMPANY, "default_holiday_list")
		# a list made before the lunar holidays existed gets the missing days; running again adds none
		add_iran_holidays(holiday_list, 1405)
		self.assertEqual(add_iran_holidays(holiday_list, 1405), {"added": 0, "lunar_estimated": False})
		holidays = {
			str(h.holiday_date): h
			for h in frappe.get_all(
				"Holiday", filters={"parent": holiday_list}, fields=["holiday_date", "weekly_off", "description"]
			)
		}
		self.assertEqual(sum(1 for h in holidays.values() if not h.weekly_off), 26)  # official 1405 calendar
		self.assertEqual(holidays["2026-06-24"].description, "تاسوعای حسینی")  # 3 Tir 1405
		new_year = holidays["2026-03-21"].description  # 1 Farvardin: Nowruz and Eid al-Fitr
		self.assertIn("نوروز", new_year)
		self.assertIn("عید سعید فطر", new_year)
		self.assertEqual(holidays["2026-06-05"].weekly_off, 0)  # 15 Khordad, a Friday, counts as official

		# no official calendar for 1406 yet: estimated lunar days, marked as such
		estimated = frappe.get_all(
			"Holiday",
			filters={"parent": create_iran_holiday_list(1406), "description": ["like", "%پیش‌بینی%"]},
			pluck="holiday_date",
		)
		self.assertGreaterEqual(len(estimated), 16)

	def test_customer_validation(self):
		customer = frappe.get_doc(
			{
				"doctype": "Customer",
				"customer_name": "علي كريمي",
				"customer_type": "Individual",
				"customer_group": CUSTOMER_GROUP,
				"ir_national_id": "0499370898",
			}
		)
		self.assertRaisesRegex(frappe.ValidationError, "0499370898", customer.insert)
		customer.ir_national_id = "۰۴۹۹۳۷۰۸۹۹"
		customer.insert()
		self.assertEqual(customer.customer_name, "علی کریمی")
		self.assertEqual(customer.ir_national_id, VALID_NATIONAL_CODE)
		self.assertEqual(customer.ir_person_type, "Natural Person")

	def test_bank_account_iban(self):
		if not frappe.db.exists("Bank", "بانک پارسیان"):
			frappe.get_doc({"doctype": "Bank", "bank_name": "بانک پارسیان"}).insert()
		account = frappe.get_doc(
			{
				"doctype": "Bank Account",
				"account_name": "حساب جاری",
				"bank": "بانک پارسیان",
				"iban": "IR82 0540 1026 8002 0817 9090 03",
			}
		)
		self.assertRaisesRegex(frappe.ValidationError, "IBAN", account.insert)
		account.iban = "ir82 0540 1026 8002 0817 9090 02"
		account.insert()
		self.assertEqual(account.iban, VALID_IBAN)

	def test_item_stuff_id(self):
		item = frappe.get_doc(
			{
				"doctype": "Item",
				"item_code": "IR-TEST-BAD",
				"item_name": "كالا",
				"item_group": ITEM_GROUP,
				"stock_uom": "Nos",
				"is_stock_item": 0,
				"ir_stuff_id": "123",
			}
		)
		self.assertRaisesRegex(frappe.ValidationError, "13 digits", item.insert)

	def test_sales_invoice_moadian_and_print(self):
		frappe.db.set_value("UOM", "Nos", "ir_moadian_unit_code", "1627")
		if not frappe.db.exists("Item", "IR-TEST-ITEM"):
			frappe.get_doc(
				{
					"doctype": "Item",
					"item_code": "IR-TEST-ITEM",
					"item_name": "کالای آزمایشی",
					"item_group": ITEM_GROUP,
					"stock_uom": "Nos",
					"is_stock_item": 0,
					"ir_stuff_id": "2710000138624",
				}
			).insert()
		customer = frappe.get_doc(
			{
				"doctype": "Customer",
				"customer_name": "مشتری مودیان",
				"customer_type": "Individual",
				"customer_group": CUSTOMER_GROUP,
				"ir_national_id": VALID_NATIONAL_CODE,
			}
		).insert()

		template = frappe.db.get_value("Sales Taxes and Charges Template", {"company": COMPANY}, "name")
		si = frappe.get_doc(
			{
				"doctype": "Sales Invoice",
				"company": COMPANY,
				"customer": customer.name,
				"posting_date": "2026-10-25",
				"set_posting_time": 1,
				"due_date": "2026-11-25",
				"currency": "IRR",
				"conversion_rate": 1,
				"taxes_and_charges": template,
				"items": [{"item_code": "IR-TEST-ITEM", "qty": 2, "rate": 1_500_000}],
			}
		)
		si.extend("taxes", get_taxes_and_charges("Sales Taxes and Charges Template", template))
		si.insert()
		self.assertEqual(si.ir_jalali_posting_date, "1405/08/03")
		self.assertEqual(si.total_taxes_and_charges, 300_000)
		si.submit()
		si.reload()

		self.assertEqual(len(si.ir_tax_id), 22)
		self.assertTrue(si.ir_tax_id.startswith("A1B2C3"))
		self.assertEqual(si.ir_moadian_status, "Pending")

		result = get_moadian_payload(si.name)
		header = result["payload"]["header"]
		self.assertEqual(result["problems"], [], result["problems"])
		self.assertEqual((header["tadis"], header["tvam"], header["tbill"]), (3_000_000, 300_000, 3_300_000))
		self.assertEqual(header["tob"], 1)
		self.assertEqual(header["bid"], VALID_NATIONAL_CODE)
		self.assertEqual(result["payload"]["body"][0]["mu"], "1627")

		html = frappe.get_print("Sales Invoice", si.name, print_format="IR Official Invoice")
		self.assertIn("صورتحساب فروش کالا و خدمات", html)
		self.assertIn(format_jalali(si.posting_date), html)
		self.assertIn("سه میلیون و سیصد هزار ریال", html)
		self.assertIn("3,300,000", html)
		self.assertIn(si.ir_tax_id, html)

	def test_vat_return(self):
		from erpnext_iran.erpnext_iran.report.ir_vat_return import ir_vat_return

		filters = {"company": COMPANY, "jalali_year": 1405, "season": "Autumn"}

		def summary():
			rows = ir_vat_return.execute(filters)[1]
			return {r["description"]: (r["base_amount"] or 0, r["vat_amount"] or 0) for r in rows}

		before = summary()
		ensure_item("IR-VAT-ITEM", "کالای مشمول")
		exempt_template = frappe.db.get_value("Item Tax Template", {"company": COMPANY}, "name")
		ensure_item("IR-EXEMPT-ITEM", "کالای معاف", [{"item_tax_template": exempt_template}])
		customer = frappe.get_doc(
			{"doctype": "Customer", "customer_name": "مشتری ارزش افزوده", "customer_group": CUSTOMER_GROUP,
			 "ir_economic_code": "411111111111"}
		).insert()  # fmt: skip
		if not frappe.db.exists("Supplier Group", "IR Test Suppliers"):
			frappe.get_doc(
				{"doctype": "Supplier Group", "supplier_group_name": "IR Test Suppliers",
				 "parent_supplier_group": "All Supplier Groups"}
			).insert()  # fmt: skip
		supplier = frappe.get_doc(
			{"doctype": "Supplier", "supplier_name": "تامین کننده ارزش افزوده", "supplier_group": "IR Test Suppliers"}
		).insert()

		# Aban 1405: 2,000,000 taxable + 500,000 exempt sold, 1,000,000 taxable bought
		sales_template = frappe.db.get_value("Sales Taxes and Charges Template", {"company": COMPANY}, "name")
		si = frappe.get_doc(
			{
				"doctype": "Sales Invoice",
				"company": COMPANY,
				"customer": customer.name,
				"posting_date": "2026-11-01",
				"set_posting_time": 1,
				"due_date": "2026-11-30",
				"currency": "IRR",  # a fresh site's price lists are in USD
				"conversion_rate": 1,
				"taxes_and_charges": sales_template,
				"items": [
					{"item_code": "IR-VAT-ITEM", "qty": 1, "rate": 2_000_000},
					{"item_code": "IR-EXEMPT-ITEM", "qty": 1, "rate": 500_000},
				],
			}
		)  # fmt: skip
		si.extend("taxes", get_taxes_and_charges("Sales Taxes and Charges Template", sales_template))
		si.insert()
		self.assertEqual(si.total_taxes_and_charges, 200_000)
		si.submit()

		purchase_template = frappe.db.get_value("Purchase Taxes and Charges Template", {"company": COMPANY}, "name")
		pi = frappe.get_doc(
			{
				"doctype": "Purchase Invoice",
				"company": COMPANY,
				"supplier": supplier.name,
				"posting_date": "2026-11-02",
				"set_posting_time": 1,
				"due_date": "2026-11-30",
				"currency": "IRR",
				"conversion_rate": 1,
				"taxes_and_charges": purchase_template,
				"items": [{"item_code": "IR-VAT-ITEM", "qty": 1, "rate": 1_000_000}],
			}
		)
		pi.extend("taxes", get_taxes_and_charges("Purchase Taxes and Charges Template", purchase_template))
		pi.insert()
		pi.submit()

		after = summary()

		def delta(label):
			return tuple(round(a - b, 2) for a, b in zip(after[label], before.get(label, (0, 0))))

		self.assertEqual(delta(_("Taxable Sales")), (2_000_000, 200_000))
		self.assertEqual(delta(_("Exempt and Zero-Rated Sales")), (500_000, 0))
		self.assertEqual(delta(_("Taxable Purchases")), (1_000_000, 100_000))
		# invoices and the ledger agree
		self.assertEqual(after[_("Difference From Invoices")][1], 0)

		# by party: the customer's economic code is listed
		columns, rows = ir_vat_return.execute(dict(filters, view="Sales by Party"))[:2]
		row = next(r for r in rows if r["party"] == customer.name)
		self.assertEqual((row["taxable"], row["exempt"], row["vat"]), (2_000_000, 500_000, 200_000))
		self.assertEqual(row["ir_economic_code"], "411111111111")
		self.assertEqual(row["grand_total"], 2_700_000)

		# a season without these invoices
		spring = ir_vat_return.execute(dict(filters, season="Spring", view="Purchases by Party"))[1]
		self.assertFalse([r for r in spring if r["party"] == supplier.name])


	def test_legal_books(self):
		from erpnext_iran.books import api
		from erpnext_iran.books.data import get_journal, get_ledger

		cash, bank, sales = (get_account(COMPANY, n) for n in ("110101", "110103", "4101"))
		general_cash = frappe.db.get_value("Account", cash, "parent_account")  # 1101
		filters = frappe._dict(company=COMPANY, jalali_year=1405, period="9", level="General")  # Azar

		opening = get_ledger(filters)[0].get(general_cash, {}).get("balance", 0)
		vouchers_before = {r["voucher_number"] for r in get_journal(dict(filters, period="Whole Year"))[0]
						   if str(r["posting_date"]) < "2026-11-22"}  # fmt: skip

		def journal_entry(date, debit_account, amount, remark):
			je = frappe.get_doc(
				{
					"doctype": "Journal Entry",
					"company": COMPANY,
					"posting_date": date,
					"user_remark": remark,
					"accounts": [
						{"account": debit_account, "debit_in_account_currency": amount},
						{"account": sales, "credit_in_account_currency": amount},
					],
				}
			).insert()
			je.submit()
			return je

		first = journal_entry("2026-11-25", cash, 1_000_000, "فروش نقدی")  # 4 Azar 1405
		second = journal_entry("2026-12-01", bank, 500_000, "فروش بانکی")  # 10 Azar 1405
		transfer = frappe.get_doc(
			{"doctype": "Journal Entry", "company": COMPANY, "posting_date": "2026-12-02", "accounts": [
				{"account": bank, "debit_in_account_currency": 200_000},
				{"account": cash, "credit_in_account_currency": 200_000}]}
		).insert()  # fmt: skip
		transfer.submit()

		rows = get_journal(filters)[0]
		mine = [r for r in rows if r["voucher_no"] in (first.name, second.name, transfer.name)]
		# cash to bank inside general account 1101 nets to nothing at the general level
		self.assertEqual({r["voucher_no"] for r in mine}, {first.name, second.name})
		self.assertEqual([(r["first"], r["debit"], r["credit"]) for r in mine],
						 [(True, 1_000_000, 0), (False, 0, 1_000_000), (True, 500_000, 0), (False, 0, 500_000)])  # fmt: skip
		self.assertEqual(mine[0]["jalali_date"], "1405/09/04")
		self.assertEqual(mine[0]["account_number"], "1101")
		self.assertIn("فروش نقدی", mine[0]["description"])
		# numbering continues the fiscal year's
		self.assertGreater(mine[0]["voucher_number"], max(vouchers_before, default=0))
		self.assertEqual(mine[2]["voucher_number"], mine[0]["voucher_number"] + 1)
		self.assertEqual(sum(r["debit"] for r in rows), sum(r["credit"] for r in rows))

		# subsidiary level shows the transfer
		subsidiary = get_journal(dict(filters, level="Subsidiary"))[0]
		self.assertIn(transfer.name, {r["voucher_no"] for r in subsidiary})

		ledger = get_ledger(filters)[0]
		self.assertAlmostEqual(ledger[general_cash]["balance"], opening + 1_500_000)
		bank_ledger = get_ledger(dict(filters, level="Subsidiary", account=bank))[0]
		self.assertEqual(list(bank_ledger), [bank])
		mine = [r["debit"] for r in bank_ledger[bank]["rows"] if r.get("voucher_no") in (second.name, transfer.name)]
		self.assertEqual(mine, [500_000, 200_000])

		# PDF pages carry their totals forward (rendered in Persian, as for a Persian user)
		lang, frappe.local.lang = frappe.local.lang, "fa"
		self.addCleanup(setattr, frappe.local, "lang", lang)
		api.ROWS_PER_PAGE = 2
		try:
			html = api.render_book("journal", filters)
		finally:
			api.ROWS_PER_PAGE = 30
		self.assertIn("دفتر روزنامه", html)
		self.assertIn("جمع نقل به صفحه بعد", html)
		self.assertIn("جمع نقل از صفحه قبل", html)
		html = api.render_book("ledger", filters)
		self.assertIn("دفتر کل", html)
		self.assertIn("جمع و مانده", html)
		api.download_pdf("ledger", frappe.as_json(filters))
		self.assertTrue(frappe.local.response.filecontent.startswith(b"%PDF"))

	def test_cheques(self):
		from erpnext.accounts.utils import get_balance_on

		from erpnext_iran.erpnext_iran.doctype.ir_cheque.ir_cheque import get_actions, make_movement
		from erpnext_iran.erpnext_iran.report.ir_cheque_register import ir_cheque_register

		notes_receivable, in_collection, notes_payable, bank = (
			get_account(COMPANY, n) for n in ("110302", "110303", "210102", "110103")
		)
		customer = frappe.get_doc(
			{"doctype": "Customer", "customer_name": "مشتری چک", "customer_group": CUSTOMER_GROUP}
		).insert()
		if not frappe.db.exists("Supplier Group", "IR Test Suppliers"):
			frappe.get_doc(
				{"doctype": "Supplier Group", "supplier_group_name": "IR Test Suppliers",
				 "parent_supplier_group": "All Supplier Groups"}
			).insert()  # fmt: skip
		supplier = frappe.get_doc(
			{"doctype": "Supplier", "supplier_name": "تامین کننده چک", "supplier_group": "IR Test Suppliers"}
		).insert()

		def balances():
			return {
				"notes_receivable": get_balance_on(notes_receivable, "2027-03-20"),
				"in_collection": get_balance_on(in_collection, "2027-03-20"),
				"notes_payable": get_balance_on(notes_payable, "2027-03-20"),
				"bank": get_balance_on(bank, "2027-03-20"),
				"customer": get_balance_on(party_type="Customer", party=customer.name, company=COMPANY, date="2027-03-20"),
				"supplier": get_balance_on(party_type="Supplier", party=supplier.name, company=COMPANY, date="2027-03-20"),
			}

		def changes(before):
			after = balances()
			return {key: round(after[key] - before[key]) for key in after if round(after[key] - before[key])}

		def cheque(cheque_type, sayad_id, amount, **extra):
			doc = frappe.get_doc(
				{
					"doctype": "IR Cheque",
					"cheque_type": cheque_type,
					"company": COMPANY,
					"party_type": "Customer" if cheque_type == "Received" else "Supplier",
					"party": customer.name if cheque_type == "Received" else supplier.name,
					"sayad_id": sayad_id,
					"amount": amount,
					"issue_date": "2026-10-25",
					"due_date": "2026-12-15",
					**extra,
				}
			)
			return doc.insert()

		# received cheque: register, deposit, clear
		before = balances()
		received = cheque("Received", "۱۱۱۱۲۲۲۲۳۳۳۳۴۴۴۴", 5_000_000, serial="۱۲۳۴۵")
		self.assertEqual(received.sayad_id, "1111222233334444")
		self.assertEqual(received.notes_account, notes_receivable)
		received.submit()
		self.assertEqual(received.status, "Received")
		self.assertEqual(changes(before), {"notes_receivable": 5_000_000, "customer": -5_000_000})
		self.assertEqual(get_actions(received.name), ["deposit", "clear", "bounce", "endorse"])

		make_movement(received.name, "deposit", "2026-12-14", bank_account=bank)
		self.assertEqual(changes(before), {"in_collection": 5_000_000, "customer": -5_000_000})
		result = make_movement(received.name, "clear", "2026-12-16")
		self.assertEqual(result["status"], "Cleared")
		self.assertEqual(changes(before), {"bank": 5_000_000, "customer": -5_000_000})
		received.reload()
		self.assertEqual([m.to_status for m in received.movements], ["Received", "Deposited", "Cleared"])
		self.assertEqual(get_actions(received.name), [])
		self.assertRaises(frappe.ValidationError, make_movement, received.name, "bounce")

		# same Sayad ID twice, or a malformed one
		self.assertRaises(frappe.ValidationError, cheque, "Received", "1111222233334444", 1_000)
		self.assertRaises(frappe.ValidationError, cheque, "Received", "12345", 1_000)

		# endorsed to the supplier, then handed back bounced
		before = balances()
		endorsed = cheque("Received", "5555666677778888", 2_000_000)
		endorsed.submit()
		self.assertRaises(frappe.ValidationError, make_movement, endorsed.name, "endorse")  # no supplier
		make_movement(endorsed.name, "endorse", "2026-11-01", endorsee=supplier.name)
		self.assertEqual(changes(before), {"customer": -2_000_000, "supplier": 2_000_000})
		make_movement(endorsed.name, "bounce", "2026-12-20")
		self.assertEqual(changes(before), {})  # the customer owes again, so do we
		self.assertEqual(frappe.db.get_value("IR Cheque", endorsed.name, "status"), "Bounced")

		# issued cheque from a cheque book
		book = frappe.get_doc(
			{"doctype": "IR Cheque Book", "company": COMPANY, "bank_account": bank, "series": "۱۲/ب",
			 "first_serial": 1000, "leaves": 25}
		).insert()  # fmt: skip
		self.assertRaises(frappe.ValidationError, cheque, "Issued", "9999000011112222", 1_000,
						  cheque_book=book.name, serial="1025")  # fmt: skip
		before = balances()
		issued = cheque("Issued", "9999000011112222", 3_000_000, cheque_book=book.name, serial="1001")
		self.assertEqual((issued.bank_account, issued.notes_account), (bank, notes_payable))
		issued.submit()
		self.assertEqual(frappe.db.get_value("IR Cheque Book", book.name, "used_leaves"), 1)
		self.assertRaises(frappe.ValidationError, cheque, "Issued", "9999000011113333", 1_000,
						  cheque_book=book.name, serial="1001")  # fmt: skip
		self.assertEqual(changes(before), {"notes_payable": -3_000_000, "supplier": 3_000_000})
		make_movement(issued.name, "clear", "2026-12-15")
		self.assertEqual(changes(before), {"bank": -3_000_000, "supplier": 3_000_000})

		# the register lists open cheques by due date
		pending = cheque("Received", "1212343456567878", 700_000)
		pending.submit()
		rows = ir_cheque_register.execute({"company": COMPANY, "status": "Open"})[1]
		self.assertIn(pending.name, [r.name for r in rows])
		self.assertNotIn(received.name, [r.name for r in rows])

		# cancelling undoes every step
		before = balances()
		entries = [m.journal_entry for m in frappe.get_doc("IR Cheque", issued.name).movements]
		frappe.get_doc("IR Cheque", issued.name).cancel()
		self.assertEqual(changes(before), {"bank": 3_000_000, "supplier": -3_000_000})
		self.assertEqual({frappe.db.get_value("Journal Entry", je, "docstatus") for je in entries}, {2})
		self.assertEqual(frappe.db.get_value("IR Cheque", issued.name, "status"), "Cancelled")
		self.assertEqual(frappe.db.get_value("IR Cheque Book", book.name, "used_leaves"), 0)

def ensure_item(item_code, item_name, taxes=None):
	if not frappe.db.exists("Item", item_code):
		frappe.get_doc(
			{"doctype": "Item", "item_code": item_code, "item_name": item_name, "item_group": ITEM_GROUP,
			 "stock_uom": "Nos", "is_stock_item": 0, "taxes": taxes or []}
		).insert()  # fmt: skip

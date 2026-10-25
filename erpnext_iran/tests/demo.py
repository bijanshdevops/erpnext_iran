"""Seed demo data on a test site (committed, not rolled back):

    bench --site <site> execute erpnext_iran.tests.demo.make
"""

import frappe
from erpnext.controllers.accounts_controller import get_taxes_and_charges

from erpnext_iran.setup.api import setup_company
from erpnext_iran.setup.chart_of_accounts import get_account
from erpnext_iran.tests.test_integration import (
	COMPANY,
	CUSTOMER_GROUP,
	ITEM_GROUP,
	VALID_NATIONAL_CODE,
	ensure_company,
	ensure_groups,
)


def make():
	frappe.set_user("Administrator")
	settings = frappe.get_doc("Iran Localization Settings")
	settings.moadian_enabled = 1
	settings.moadian_memory_id = "A1B2C3"
	settings.save()

	ensure_groups()
	ensure_company()
	if not get_account(COMPANY, "110101"):
		setup_company(COMPANY, apply_chart=1, create_taxes=1, vat_rate=10, jalali_year=1405, create_holiday_list=1)

	frappe.db.set_value("UOM", "Nos", "ir_moadian_unit_code", "1627")
	if not frappe.db.exists("Item", "IR-DEMO-ITEM"):
		frappe.get_doc(
			{"doctype": "Item", "item_code": "IR-DEMO-ITEM", "item_name": "لپ‌تاپ نمونه",
			 "item_group": ITEM_GROUP, "stock_uom": "Nos", "is_stock_item": 0,
			 "ir_stuff_id": "2710000138624"}
		).insert()  # fmt: skip
	customer = frappe.db.get_value("Customer", {"customer_name": "مشتری نمونه"})
	if not customer:
		customer = frappe.get_doc(
			{"doctype": "Customer", "customer_name": "مشتری نمونه", "customer_type": "Individual",
			 "customer_group": CUSTOMER_GROUP, "ir_national_id": VALID_NATIONAL_CODE}
		).insert().name  # fmt: skip

	template = frappe.db.get_value("Sales Taxes and Charges Template", {"company": COMPANY}, "name")
	si = frappe.get_doc(
		{
			"doctype": "Sales Invoice",
			"company": COMPANY,
			"customer": customer,
			"currency": "IRR",
			"conversion_rate": 1,
			"taxes_and_charges": template,
			"items": [{"item_code": "IR-DEMO-ITEM", "qty": 2, "price_list_rate": 1_600_000, "rate": 1_500_000}],
		}
	)
	si.extend("taxes", get_taxes_and_charges("Sales Taxes and Charges Template", template))
	si.insert()
	si.submit()
	frappe.db.commit()
	print(si.name, si.ir_tax_id, si.ir_jalali_posting_date, si.grand_total)

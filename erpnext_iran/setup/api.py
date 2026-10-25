"""Whitelisted setup actions used by the Company and Holiday List form buttons."""

import frappe
from frappe import _
from frappe.utils import cint

from erpnext_iran.setup import chart_of_accounts, iran_calendar, taxes
from erpnext_iran.utils.settings import get_settings


@frappe.whitelist()
def setup_company(
	company,
	apply_chart=0,
	create_taxes=1,
	vat_rate=None,
	vat_output_account=None,
	vat_input_account=None,
	jalali_year=None,
	create_holiday_list=0,
	include_thursday=0,
):
	frappe.only_for(("System Manager", "Accounts Manager"))
	frappe.has_permission("Company", "write", company, throw=True)
	done = []

	if cint(apply_chart):
		chart_of_accounts.apply_chart(company)
		done.append(_("Iranian chart of accounts"))

	if cint(create_taxes):
		rate = vat_rate if vat_rate not in (None, "") else get_settings().vat_rate
		taxes.create_vat_templates(company, rate, vat_output_account, vat_input_account)
		done.append(_("VAT templates"))

	if jalali_year:
		iran_calendar.create_jalali_fiscal_year(jalali_year, company)
		done.append(_("Fiscal Year {0}").format(jalali_year))

		if cint(create_holiday_list):
			holiday_list = iran_calendar.create_iran_holiday_list(jalali_year, cint(include_thursday))
			if not frappe.db.get_value("Company", company, "default_holiday_list"):
				frappe.db.set_value("Company", company, "default_holiday_list", holiday_list)
			done.append(_("Holiday List {0}").format(holiday_list))

	return done


@frappe.whitelist()
def add_iran_holidays(holiday_list, jalali_year, include_thursday=0):
	frappe.has_permission("Holiday List", "write", holiday_list, throw=True)
	return iran_calendar.add_iran_holidays(holiday_list, jalali_year, cint(include_thursday))

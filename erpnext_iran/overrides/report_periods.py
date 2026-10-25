"""Jalali-month periods for ERPNext's financial statements (P&L, Balance Sheet, Cash Flow, ...).

ERPNext has no hook for its period builder, so apply() (run from before_request / before_job)
replaces financial_statements.get_period_list, and the copies report modules took with
`from ... import get_period_list`, with a wrapper. The wrapper calls ERPNext's original for the
fiscal-year handling and validation, then re-cuts the periods on Jalali month boundaries.
"""

import sys

import frappe

from erpnext_iran.utils.jalali_periods import jalali_periods, month_label, period_key, range_label, year_label
from erpnext_iran.utils.settings import get_settings

FINANCIAL_STATEMENTS = "erpnext.accounts.report.financial_statements"
REPORT_MODULES = (
	"erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement",
	"erpnext.accounts.report.balance_sheet.balance_sheet",
	"erpnext.accounts.report.cash_flow.cash_flow",
	"erpnext.accounts.report.gross_and_net_profit_report.gross_and_net_profit_report",
	"erpnext.accounts.report.financial_ratios.financial_ratios",
	"erpnext.accounts.report.deferred_revenue_and_expense.deferred_revenue_and_expense",
	"erpnext.assets.report.fixed_asset_register.fixed_asset_register",
	"erpnext.manufacturing.report.exponential_smoothing_forecasting.exponential_smoothing_forecasting",
	"erpnext.selling.report.sales_partner_target_variance_based_on_item_group.item_group_wise_sales_target_variance",
)
MONTHS = {"Half-Yearly": 6, "Quarterly": 3, "Monthly": 1}

_original = None


def apply(*args, **kwargs):
	"""Idempotent; also patches report modules imported before the first call."""
	global _original
	try:
		module = __import__(FINANCIAL_STATEMENTS, fromlist=["get_period_list"])
	except ImportError:
		return
	if _original is None:
		_original = module.get_period_list
	module.get_period_list = get_period_list
	for name in REPORT_MODULES:
		report = sys.modules.get(name)
		if report is not None and getattr(report, "get_period_list", None) is not get_period_list:
			report.get_period_list = get_period_list


def get_period_list(
	from_fiscal_year,
	to_fiscal_year,
	period_start_date,
	period_end_date,
	filter_based_on,
	periodicity,
	accumulated_values=False,
	company=None,
	reset_period_on_fy_change=True,
	ignore_fiscal_year=False,
):
	periods = _original(
		from_fiscal_year,
		to_fiscal_year,
		period_start_date,
		period_end_date,
		filter_based_on,
		periodicity,
		accumulated_values,
		company,
		reset_period_on_fy_change,
		ignore_fiscal_year,
	)
	if not periods or not get_settings().jalali_report_periods:
		return periods

	year_start_date, year_end_date = periods[0].year_start_date, periods[-1].year_end_date
	if periodicity == "Yearly":
		for period in periods:
			period.label = year_label(period.from_date, period.to_date)
		return periods

	from erpnext.accounts.utils import get_fiscal_year

	result = []
	for from_date, to_date in jalali_periods(year_start_date, year_end_date, MONTHS[periodicity]):
		period = frappe._dict(from_date=from_date, to_date=to_date)
		if not ignore_fiscal_year:
			period.to_date_fiscal_year = get_fiscal_year(to_date, company=company)[0]
			period.from_date_fiscal_year_start_date = get_fiscal_year(from_date, company=company)[1]
		result.append(period)

	for period in result:
		if periodicity == "Monthly" and not accumulated_values:
			label = month_label(period.to_date)
		elif not accumulated_values:
			label = range_label(period.from_date, period.to_date)
		elif reset_period_on_fy_change:
			label = range_label(period.from_date_fiscal_year_start_date, period.to_date)
		else:
			label = range_label(result[0].from_date, period.to_date)
		period.update(
			key=period_key(period.to_date),
			label=label,
			year_start_date=year_start_date,
			year_end_date=year_end_date,
		)
	return result

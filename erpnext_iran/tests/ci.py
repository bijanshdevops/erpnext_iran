"""Helpers for the CI integration run (.github/ci/integration.sh)."""

import frappe

from erpnext_iran.utils.jalali import jalali_year_range, to_jalali


def before_tests():
	"""Finish the setup wizard of a fresh site (root groups, a company), which the demo data and the
	tests need. The apps' own before_tests hooks are not used: ERPNext v16's bootstraps its whole
	test data set and breaks outside `bench run-tests`; this works the same on v15 and v16."""
	if frappe.is_setup_complete():
		return
	from frappe.desk.page.setup_wizard.setup_wizard import setup_complete

	start, end = jalali_year_range(to_jalali(frappe.utils.getdate())[0])
	setup_complete(
		{
			"language": "English",
			"country": "Iran",
			"timezone": "Asia/Tehran",
			"currency": "IRR",
			"full_name": "Test User",
			"email": "test@example.com",
			"company_name": "IR CI Company",
			"company_abbr": "IRC",
			"chart_of_accounts": "Standard",
			"fy_start_date": str(start),
			"fy_end_date": str(end),
		}
	)
	frappe.db.commit()

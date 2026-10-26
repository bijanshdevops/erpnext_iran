"""PDF of the statutory books: fixed rows per page, so every page can carry its totals forward
("brought forward from previous page" / "carried forward to next page")."""

import json

import frappe
from frappe import _
from frappe.utils import fmt_money
from frappe.utils.pdf import get_pdf

from erpnext_iran.books.core import paginate
from erpnext_iran.books.data import account_label, get_journal, get_ledger
from erpnext_iran.utils.jalali import format_jalali

ROWS_PER_PAGE = 30
REPORTS = {"journal": "IR Journal Book", "ledger": "IR General Ledger Book"}
# ASCII file names: browsers mangle non-Latin names in the Content-Disposition header
FILE_NAMES = {"journal": "journal-book", "ledger": "general-ledger-book"}


@frappe.whitelist()
def download_pdf(book, filters):
	if book not in REPORTS:
		frappe.throw(_("Unknown book {0}").format(book))
	if not frappe.has_permission("Report", "read", REPORTS[book]) or not frappe.has_permission("GL Entry", "read"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)
	filters = frappe._dict(json.loads(filters) if isinstance(filters, str) else filters)
	html = render_book(book, filters)
	frappe.local.response.filename = f"{FILE_NAMES[book]}-{filters.jalali_year}.pdf"
	frappe.local.response.filecontent = get_pdf(html, {"orientation": "Portrait", "page-size": "A4"})
	frappe.local.response.type = "pdf"


def render_book(book, filters):
	company = frappe.get_cached_doc("Company", filters.company)
	number_format = frappe.db.get_value("Currency", company.default_currency, "number_format")

	def amount(value):
		return fmt_money(abs(value), precision=0, format=number_format) if round(value or 0, 6) else ""

	if book == "journal":
		rows, _accounts, from_date, to_date = get_journal(filters)
		sections = [{"title": None, "pages": paginate(rows, ROWS_PER_PAGE)}]
	else:
		ledger, accounts, from_date, to_date = get_ledger(filters)
		sections = [
			{"title": account_label(accounts[account]), "pages": paginate(data["rows"], ROWS_PER_PAGE)}
			for account, data in ledger.items()
		] or [{"title": None, "pages": paginate([], ROWS_PER_PAGE)}]

	from frappe.www.printview import get_print_style

	return frappe.render_template(
		"erpnext_iran/templates/books/legal_book.html",
		{
			"book": book,
			"title": _("Journal Book") if book == "journal" else _("General Ledger Book"),
			"company": company,
			"period": _("{0} to {1}").format(format_jalali(from_date), format_jalali(to_date)),
			"sections": sections,
			"amount": amount,
			"dr_cr": lambda balance: "" if not round(balance, 6) else (_("Dr") if balance > 0 else _("Cr")),
			"css": get_print_style(),
			"printed_on": format_jalali(frappe.utils.now_datetime(), "%Y/%m/%d %H:%M"),
		},
	)

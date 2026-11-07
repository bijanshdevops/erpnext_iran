"""The public demo site (demo/ in the repository): a sample company with Iranian settings and some
documents of each kind, and a guest user with limited roles.

The guards below only act on a site whose config names its demo user (erpnext_iran_demo_user),
so they keep visitors from locking each other out there and do nothing anywhere else.
"""

import frappe
from frappe import _
from frappe.utils import add_days, getdate, nowdate

from erpnext_iran.utils.jalali import jalali_year_range, to_jalali
from erpnext_iran.utils.validators import is_valid_legal_national_id, is_valid_national_code

COMPANY = "شرکت نمونه فانوس"
ABBR = "FNS"
ROLES = [
	"Accounts User", "Accounts Manager", "Sales User", "Sales Manager", "Purchase User",
	"Purchase Manager", "Stock User", "Stock Manager", "HR User", "HR Manager", "Report Manager",
]  # fmt: skip


def demo_user():
	return frappe.conf.get("erpnext_iran_demo_user")


def protect_demo_user(doc, method=None):
	"""User.validate: the demo user's password, roles and status stay as the demo set them."""
	if not demo_user() or doc.name != demo_user() or frappe.session.user == "Administrator":
		return
	if doc.get("new_password") or not doc.enabled or doc.is_new():
		frappe.throw(_("The demo user cannot be changed in the demo"))


@frappe.whitelist(allow_guest=True)
def update_password(new_password, logout_all_sessions=0, key=None, old_password=None):
	"""Frappe's update_password, refused for the demo user (it does not go through User.validate)."""
	from frappe.core.doctype.user.user import update_password as frappe_update_password

	if demo_user() and frappe.session.user == demo_user():
		frappe.throw(_("The demo user cannot be changed in the demo"))
	return frappe_update_password(new_password, logout_all_sessions, key, old_password)


def _valid(prefix, is_valid, length):
	"""prefix completed to a valid code with the one check digit that makes it valid."""
	return next(code for code in (prefix + str(d) for d in range(10)) if len(code) == length and is_valid(code))


def setup(user, password, reset_hours=6):
	"""Complete the setup wizard and fill a fresh site with the demo company and documents."""
	frappe.set_user("Administrator")
	jalali_year = to_jalali(getdate(nowdate()))[0]
	_setup_wizard(jalali_year)

	from erpnext_iran.setup.api import setup_company

	setup_company(COMPANY, apply_chart=1, create_taxes=1, vat_rate=10, jalali_year=jalali_year,
				  create_holiday_list=1, rename_warehouses=1, system_defaults=1)  # fmt: skip
	_site_settings(user, password, reset_hours)
	_master_data()
	_documents()
	_payroll()
	_user(user, password)
	frappe.db.commit()


def _setup_wizard(jalali_year):
	if frappe.is_setup_complete():
		return
	from frappe.desk.page.setup_wizard.setup_wizard import setup_complete

	start, end = jalali_year_range(jalali_year)
	setup_complete({
		"language": "English", "country": "Iran", "timezone": "Asia/Tehran", "currency": "IRR",
		"full_name": "مدیر سیستم", "email": "admin@example.com", "company_name": COMPANY,
		"company_abbr": ABBR, "chart_of_accounts": "Standard", "fy_start_date": str(start), "fy_end_date": str(end),
	})  # fmt: skip
	frappe.db.commit()


def _site_settings(user, password, reset_hours):
	frappe.db.set_single_value("System Settings", "language", "fa")
	frappe.db.set_single_value("System Settings", "app_name", "ERPNext Iran")
	frappe.db.set_single_value("System Settings", "login_with_email_link", 0)  # emails are muted
	frappe.db.set_single_value("Website Settings", "app_name", "ERPNext Iran")  # "Login to ..." on the login page
	frappe.db.set_single_value("Website Settings", "disable_signup", 1)
	frappe.db.set_single_value("Website Settings", "head_html", LOGIN_NOTICE.format(
		user=user, password=password, hours=reset_hours))  # fmt: skip
	settings = frappe.get_doc("Iran Localization Settings")
	settings.moadian_enabled = 0
	settings.save()
	frappe.get_doc({
		"doctype": "Note", "title": "به دموی ERPNext Iran خوش آمدید", "public": 1, "notify_on_login": 1,
		"notify_on_every_login": 1,
		"content": (
			"<p>این یک نمونهٔ آزمایشی از <b>ERPNext Iran</b> است: تقویم شمسی، کدینگ حساب‌های ایرانی، "
			"ارزش افزوده، چک صیادی، دفاتر قانونی و حقوق و دستمزد با داده‌های فرضی «" + COMPANY + "».</p>"
			f"<p>هر تغییری بدهید، هر {reset_hours} ساعت همه‌چیز به حالت اول برمی‌گردد. ارسال ایمیل و ارسال به "
			"سامانهٔ مؤدیان در این دمو خاموش است.</p>"
			'<p>کد و راهنمای نصب: <a href="https://github.com/bijanshdevops/erpnext_iran">github.com/bijanshdevops/erpnext_iran</a></p>'
		),
	}).insert(ignore_permissions=True)  # fmt: skip


LOGIN_NOTICE = """<script>
document.addEventListener("DOMContentLoaded", function () {{
	if (!location.pathname.startsWith("/login")) return;
	var form = document.querySelector(".login-content form, form.form-login");
	if (!form) return;
	var box = document.createElement("div");
	box.setAttribute("dir", "rtl");
	box.style.cssText = "border:1px solid #2e7d32;border-radius:8px;padding:12px;margin-bottom:16px;line-height:1.9;text-align:right";
	box.innerHTML = "<b>دموی ERPNext Iran</b><br>نام کاربری: <code>{user}</code><br>رمز: <code>{password}</code>"
		+ "<br><small>داده‌ها فرضی‌اند و هر {hours} ساعت بازنشانی می‌شوند.</small>";
	form.parentNode.insertBefore(box, form);
	var email = document.getElementById("login_email"), pass = document.getElementById("login_password");
	if (email && !email.value) email.value = "{user}";
	if (pass && !pass.value) pass.value = "{password}";
}});
</script>"""


def _group(doctype, name, parent):
	field = frappe.scrub(doctype) + "_name"
	if not frappe.db.exists(doctype, name):
		frappe.get_doc({"doctype": doctype, field: name, "parent_" + frappe.scrub(doctype): parent}).insert()
	return name


ITEMS = [
	# code, name, group, stock item, buying rate, selling rate, Moadian goods ID
	("LAPTOP-14", "لپ‌تاپ ۱۴ اینچ", "کالاهای دیجیتال", 1, 380_000_000, 450_000_000, "2710000138624"),
	("PRINTER-LJ", "چاپگر لیزری", "کالاهای دیجیتال", 1, 95_000_000, 120_000_000, "2710000138631"),
	("MOUSE-W", "ماوس بی‌سیم", "کالاهای دیجیتال", 1, 2_400_000, 3_500_000, "2710000138648"),
	("SRV-INSTALL", "خدمات نصب و راه‌اندازی", "خدمات", 0, 0, 15_000_000, "2720000114542"),
]
CUSTOMERS = [
	# name, type, national ID prefix (completed to a valid one)
	("فروشگاه رایان", "Company", "1032065476", is_valid_legal_national_id, 11),
	("سارا احمدی", "Individual", "006824593", is_valid_national_code, 10),
	("شرکت ساختمانی البرز", "Company", "1010217304", is_valid_legal_national_id, 11),
]
SUPPLIERS = [
	("شرکت فناوران پارس", "1040056283", is_valid_legal_national_id, 11),
	("بازرگانی آریا", "1086147929", is_valid_legal_national_id, 11),
]


def _master_data():
	for group in ("کالاهای دیجیتال", "خدمات"):
		_group("Item Group", group, "All Item Groups")
	customers = _group("Customer Group", "مشتریان", "All Customer Groups")
	suppliers = _group("Supplier Group", "تأمین‌کنندگان داخلی", "All Supplier Groups")
	frappe.db.set_value("UOM", "Nos", "ir_moadian_unit_code", "1627")

	for code, name, group, stock, buying, selling, stuff_id in ITEMS:
		if frappe.db.exists("Item", code):
			continue
		frappe.get_doc({
			"doctype": "Item", "item_code": code, "item_name": name, "item_group": group, "stock_uom": "Nos",
			"is_stock_item": stock, "ir_stuff_id": stuff_id, "valuation_rate": buying or 0,
		}).insert()  # fmt: skip
		frappe.get_doc({"doctype": "Item Price", "item_code": code, "price_list": "Standard Selling",
						"price_list_rate": selling}).insert()  # fmt: skip
		if buying:
			frappe.get_doc({"doctype": "Item Price", "item_code": code, "price_list": "Standard Buying",
							"price_list_rate": buying}).insert()  # fmt: skip

	for name, kind, prefix, is_valid, length in CUSTOMERS:
		if not frappe.db.exists("Customer", {"customer_name": name}):
			frappe.get_doc({
				"doctype": "Customer", "customer_name": name, "customer_type": kind, "customer_group": customers,
				"ir_person_type": "Legal Entity" if kind == "Company" else "Natural Person",
				"ir_national_id": _valid(prefix, is_valid, length),
			}).insert()  # fmt: skip
	for name, prefix, is_valid, length in SUPPLIERS:
		if not frappe.db.exists("Supplier", {"supplier_name": name}):
			frappe.get_doc({
				"doctype": "Supplier", "supplier_name": name, "supplier_group": suppliers,
				"ir_person_type": "Legal Entity", "ir_national_id": _valid(prefix, is_valid, length),
			}).insert()  # fmt: skip


def _party(doctype, name):
	field = "customer_name" if doctype == "Customer" else "supplier_name"
	return frappe.db.get_value(doctype, {field: name})


def _taxes(doctype, invoice):
	from erpnext.controllers.accounts_controller import get_taxes_and_charges

	template_doctype = f"{'Sales' if doctype == 'Sales Invoice' else 'Purchase'} Taxes and Charges Template"
	template = frappe.db.get_value(template_doctype, {"company": COMPANY}, "name")
	if template:
		invoice.taxes_and_charges = template
		invoice.extend("taxes", get_taxes_and_charges(template_doctype, template))


def _invoice(doctype, party, days_ago, items, update_stock=1):
	party_field = "customer" if doctype == "Sales Invoice" else "supplier"
	warehouse = frappe.db.get_value("Warehouse", {"company": COMPANY, "is_group": 0}, "name", order_by="creation")
	date = add_days(nowdate(), -days_ago)
	invoice = frappe.get_doc({
		"doctype": doctype, "company": COMPANY, party_field: party, "posting_date": date, "set_posting_time": 1,
		"due_date": add_days(date, 30), "currency": "IRR", "conversion_rate": 1, "update_stock": update_stock,
		"items": [{"item_code": code, "qty": qty, "rate": rate, "warehouse": warehouse} for code, qty, rate in items],
	})  # fmt: skip
	_taxes(doctype, invoice)
	invoice.insert()
	invoice.submit()
	return invoice


def _documents():
	if frappe.db.exists("Purchase Invoice", {"company": COMPANY}):
		return
	from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

	pars, arya = _party("Supplier", "شرکت فناوران پارس"), _party("Supplier", "بازرگانی آریا")
	_invoice("Purchase Invoice", pars, 40, [("LAPTOP-14", 10, 380_000_000), ("PRINTER-LJ", 6, 95_000_000)])
	_invoice("Purchase Invoice", arya, 35, [("MOUSE-W", 50, 2_400_000)])

	rayan, sara, alborz = (_party("Customer", n) for n in ("فروشگاه رایان", "سارا احمدی", "شرکت ساختمانی البرز"))
	first = _invoice("Sales Invoice", rayan, 25, [("LAPTOP-14", 3, 450_000_000), ("MOUSE-W", 10, 3_500_000)])
	_invoice("Sales Invoice", sara, 18, [("LAPTOP-14", 1, 450_000_000), ("SRV-INSTALL", 1, 15_000_000)])
	third = _invoice("Sales Invoice", alborz, 9, [("PRINTER-LJ", 2, 120_000_000), ("SRV-INSTALL", 2, 15_000_000)])

	payment = get_payment_entry("Sales Invoice", first.name)
	payment.posting_date = add_days(nowdate(), -20)
	payment.reference_no, payment.reference_date = "واریز ۱۲۳۴", payment.posting_date
	payment.insert()
	payment.submit()

	cheque = frappe.get_doc({
		"doctype": "IR Cheque", "cheque_type": "Received", "company": COMPANY, "party_type": "Customer",
		"party": alborz, "sayad_id": "1405123456789012", "serial": "۴۵۶۷۸", "amount": third.grand_total,
		"issue_date": add_days(nowdate(), -9), "due_date": add_days(nowdate(), 21),
	}).insert()  # fmt: skip
	cheque.submit()


def _payroll():
	if "hrms" not in frappe.get_installed_apps() or frappe.db.exists("Salary Slip", {"company": COMPANY}):
		return
	from erpnext_iran.payroll.setup import setup_iran_payroll
	from erpnext_iran.utils.jalali import to_gregorian
	from erpnext_iran.utils.jalali_periods import add_jalali_months

	structure = setup_iran_payroll(COMPANY)
	frappe.db.set_value("Company", COMPANY, {"ir_ss_workshop_code": "1234567890",
											 "ir_ss_workshop_address": "تهران، خیابان آزادی"})  # fmt: skip
	jy, jm, _jd = to_jalali(getdate(nowdate()))
	py, pm = add_jalali_months(jy, jm, -1)  # last month, so the slip is complete
	start = to_gregorian(py, pm, 1)
	end = add_days(to_gregorian(jy, jm, 1), -1)
	for first, last, gender, married, base, joined in (
		("رضا", "محمدی", "Male", "Married", 12_000_000, "2021-04-10"),
		("مریم", "کریمی", "Female", "Single", 9_000_000, "2024-06-01"),
	):
		employee = frappe.get_doc({
			"doctype": "Employee", "first_name": first, "last_name": last, "gender": gender,
			"date_of_birth": "1990-05-20", "date_of_joining": joined, "company": COMPANY,
			"marital_status": married, "ir_children": 1 if married == "Married" else 0,
			"ir_national_id": _valid("00123456" + str(len(first)), is_valid_national_code, 10),
			"ir_insurance_number": "00" + str(12345670 + len(first)), "ir_father_name": "علی",
			"ir_id_number": "1234", "ir_id_issue_place": "تهران", "ir_ss_job_code": "123456",
			"designation": None, "status": "Active",
		}).insert()  # fmt: skip
		frappe.get_doc({
			"doctype": "Salary Structure Assignment", "employee": employee.name, "salary_structure": structure,
			"company": COMPANY, "from_date": start, "base": base, "currency": "IRR",
		}).insert().submit()  # fmt: skip
		slip = frappe.get_doc({
			"doctype": "Salary Slip", "employee": employee.name, "posting_date": end, "start_date": start,
			"end_date": end, "payroll_frequency": "Monthly",
		}).insert()  # fmt: skip
		slip.submit()


def _user(user, password):
	if not frappe.db.exists("User", user):
		frappe.get_doc({
			"doctype": "User", "email": user, "first_name": "کاربر دمو", "language": "fa",
			"send_welcome_email": 0, "user_type": "System User",
			"roles": [{"role": role} for role in ROLES if frappe.db.exists("Role", role)],
		}).insert(ignore_permissions=True)  # fmt: skip
	from frappe.utils.password import update_password

	update_password(user, password)
	frappe.defaults.set_user_default("Company", COMPANY, user)

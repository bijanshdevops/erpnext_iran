"""Social security list files (دیسکت لیست بیمه): DSKKAR00.DBF (the workshop) and DSKWOR00.DBF
(one row per insured person), as the List Disk program of the Social Security Organization makes
them and its portal takes them.

The field layout is the one of the empty files shipped with List Disk 6, which added the
seniority base (DSW_INC) and marital allowance (DSW_SPOUSE). Persian text is in the Iran System
code page. Amounts are rials.
"""

import datetime
import io
import json
import zipfile

import frappe
from frappe import _
from frappe.utils import cint, flt, getdate

from erpnext_iran.payroll.lists import get_slips
from erpnext_iran.utils import iran_system
from erpnext_iran.utils.jalali import format_jalali
from erpnext_iran.utils.jalali_periods import period_range
from erpnext_iran.utils.persian import digits_only

# (name, type, length); "P" is Persian text, written as Iran System into a C field
KAR_FIELDS = [
	("DSK_ID", "C", 10), ("DSK_NAME", "P", 30), ("DSK_FARM", "P", 30), ("DSK_ADRS", "P", 40),
	("DSK_KIND", "N", 1), ("DSK_YY", "N", 2), ("DSK_MM", "N", 2), ("DSK_LISTNO", "C", 12),
	("DSK_DISC", "P", 30), ("DSK_NUM", "N", 5), ("DSK_TDD", "N", 6), ("DSK_TROOZ", "N", 12),
	("DSK_TMAH", "N", 12), ("DSK_TMAZ", "N", 12), ("DSK_TMASH", "N", 12), ("DSK_TTOTL", "N", 12),
	("DSK_TBIME", "N", 12), ("DSK_TKOSO", "N", 12), ("DSK_BIC", "N", 12), ("DSK_RATE", "N", 5),
	("DSK_PRATE", "N", 2), ("DSK_BIMH", "N", 12), ("MON_PYM", "C", 3), ("DSK_INC", "N", 12),
	("DSK_SPOUSE", "N", 12),
]  # fmt: skip
WOR_FIELDS = [
	("DSW_ID", "C", 10), ("DSW_YY", "N", 2), ("DSW_MM", "N", 2), ("DSW_LISTNO", "C", 12),
	("DSW_ID1", "C", 8), ("DSW_FNAME", "P", 60), ("DSW_LNAME", "P", 60), ("DSW_DNAME", "P", 60),
	("DSW_IDNO", "C", 15), ("DSW_IDPLC", "P", 30), ("DSW_IDATE", "C", 8), ("DSW_BDATE", "C", 8),
	("DSW_SEX", "P", 3), ("DSW_NAT", "P", 10), ("DSW_OCP", "P", 50), ("DSW_SDATE", "C", 8),
	("DSW_EDATE", "C", 8), ("DSW_DD", "N", 2), ("DSW_ROOZ", "N", 12), ("DSW_MAH", "N", 12),
	("DSW_MAZ", "N", 12), ("DSW_MASH", "N", 12), ("DSW_TOTL", "N", 12), ("DSW_BIME", "N", 12),
	("DSW_PRATE", "N", 2), ("DSW_JOB", "C", 6), ("PER_NATCOD", "C", 10), ("DSW_INC", "N", 12),
	("DSW_SPOUSE", "C", 10),
]  # fmt: skip

UNEMPLOYMENT_RATE = 3  # part of the employer's 23%, reported on its own (DSK_BIC)
GENDERS = {"Male": "مرد", "Female": "زن"}


def dbf(fields, records, today=None):
	"""dBASE III file in the shape of the List Disk files (code page mark 0x7E, as theirs)."""
	today = today or datetime.date.today()
	record_length = 1 + sum(length for _name, _kind, length in fields)
	header_length = 32 + 32 * len(fields) + 1
	out = bytearray()
	out += bytes([0x03, today.year - 1900, today.month, today.day])
	out += len(records).to_bytes(4, "little") + header_length.to_bytes(2, "little") + record_length.to_bytes(2, "little")
	out += bytes(17) + bytes([0x7E]) + bytes(2)
	for name, kind, length in fields:
		out += name.encode("ascii").ljust(11, b"\0") + (b"N" if kind == "N" else b"C") + bytes(4)
		out += bytes([length, 0]) + bytes(14)
	out += b"\r"
	for record in records:
		out += b" "  # not deleted
		for name, kind, length in fields:
			out += _value(name, kind, length, record.get(name))
	out += b"\x1a"
	return bytes(out)


def _value(name, kind, length, value):
	if kind == "N":
		text = str(int(round(flt(value))))
		if len(text) > length:
			frappe.throw(_("{0} does not fit in field {1} of the insurance list file").format(text, name))
		return text.rjust(length).encode("ascii")
	if kind == "P":
		return iran_system.encode(_fit(value, length)).ljust(length, b" ")
	text = str(value or "")
	if len(text) > length or not text.isascii():
		frappe.throw(_("{0} does not fit in field {1} of the insurance list file").format(text, name))
	return text.ljust(length).encode("ascii")


def _fit(text, length):
	"""Cut Persian text so its Iran System form fits (lam-alef takes one byte for two letters)."""
	text = str(text or "").strip()
	while len(iran_system.encode(text)) > length:
		text = text[:-1]
	return text


def jalali_date(value):
	return format_jalali(getdate(value), "%Y%m%d") if value else ""


def insurance_number(value):
	"""The list keeps the old 8-digit numbers: drop the zeros newer 10-digit numbers start with."""
	return digits_only(value).lstrip("0")


EMPLOYEE_FIELDS = (
	"name", "first_name", "middle_name", "last_name", "gender", "date_of_birth", "date_of_joining",
	"relieving_date", "designation", "ir_national_id", "ir_insurance_number", "ir_father_name",
	"ir_id_number", "ir_id_issue_place", "ir_id_issue_date", "ir_nationality", "ir_ss_job_code",
)  # fmt: skip


def build(filters):
	"""(DSKKAR00.DBF, DSKWOR00.DBF) bytes for a month's submitted Salary Slips of a company."""
	filters = frappe._dict(filters)
	filters.include_drafts = 0
	company = frappe.get_doc("Company", filters.company)
	workshop = digits_only(company.get("ir_ss_workshop_code"))
	if not workshop:
		frappe.throw(_("Set the Social Security Workshop Code on company {0}").format(company.name))
	slips = get_slips(filters)
	if not slips:
		frappe.throw(_("No submitted Salary Slip in this month"))

	year, month = int(filters.jalali_year), int(filters.month)
	from_date, to_date = period_range(year, str(month))
	list_no = str(filters.get("list_no") or "1").zfill(2)
	rate = cint(frappe.db.get_value("IR Payroll Year", str(year), "employer_insurance_rate")) or 23
	parts = _component_amounts([s.name for s in slips])
	employees = {e.name: e for e in frappe.get_all("Employee", filters={"name": ["in", [s.employee for s in slips]]},
												   fields=list(EMPLOYEE_FIELDS))}  # fmt: skip

	workers, problems = [], []
	for slip in slips:
		employee = employees[slip.employee]
		number = insurance_number(employee.ir_insurance_number)
		if not number or len(number) > 8:
			problems.append(_("{0}: social security number {1} is missing or longer than 8 digits").format(
				slip.employee_name, employee.ir_insurance_number or "-"))  # fmt: skip
			continue
		amounts = parts.get(slip.name, {})
		days = cint(slip.payment_days)
		monthly = flt(amounts.get("IR_B"))
		seniority, marital = flt(amounts.get("IR_S")), flt(amounts.get("IR_M"))
		insurable = flt(slip.ir_insurable_wage)  # after the ceiling, the base the shares are on
		joined = employee.date_of_joining and from_date <= getdate(employee.date_of_joining) <= to_date
		left = employee.relieving_date and from_date <= getdate(employee.relieving_date) <= to_date
		workers.append({
			"DSW_ID": workshop, "DSW_YY": year % 100, "DSW_MM": month, "DSW_LISTNO": list_no,
			"DSW_ID1": number, "DSW_FNAME": employee.first_name,
			"DSW_LNAME": " ".join(p for p in (employee.middle_name, employee.last_name) if p),
			"DSW_DNAME": employee.ir_father_name, "DSW_IDNO": digits_only(employee.ir_id_number),
			"DSW_IDPLC": employee.ir_id_issue_place, "DSW_IDATE": jalali_date(employee.ir_id_issue_date),
			"DSW_BDATE": jalali_date(employee.date_of_birth), "DSW_SEX": GENDERS.get(employee.gender, ""),
			"DSW_NAT": employee.ir_nationality or "ایرانی", "DSW_OCP": employee.designation,
			"DSW_SDATE": jalali_date(employee.date_of_joining) if joined else "",
			"DSW_EDATE": jalali_date(employee.relieving_date) if left else "",
			"DSW_DD": days, "DSW_ROOZ": round(monthly / days) if days else 0, "DSW_MAH": monthly,
			"DSW_MAZ": max(insurable - monthly - seniority - marital, 0), "DSW_MASH": insurable,
			"DSW_TOTL": slip.gross_pay, "DSW_BIME": slip.ir_employee_insurance, "DSW_PRATE": 0,
			"DSW_JOB": digits_only(employee.ir_ss_job_code), "PER_NATCOD": digits_only(employee.ir_national_id),
			"DSW_INC": seniority, "DSW_SPOUSE": str(int(round(marital))),
		})  # fmt: skip
	if problems:
		frappe.throw("<br>".join(problems), title=_("Fix these employees first"))

	def total(field):
		return sum(int(round(flt(w[field]))) for w in workers)

	employer = sum(flt(s.ir_employer_insurance) for s in slips)
	unemployment = round(total("DSW_MASH") * UNEMPLOYMENT_RATE / 100)
	workshop_row = {
		"DSK_ID": workshop, "DSK_NAME": company.get("ir_ss_workshop_name") or company.company_name,
		"DSK_FARM": company.get("ir_ss_employer_name") or company.company_name,
		"DSK_ADRS": company.get("ir_ss_workshop_address"), "DSK_KIND": 0, "DSK_YY": year % 100,
		"DSK_MM": month, "DSK_LISTNO": list_no, "DSK_DISC": filters.get("description") or "",
		"DSK_NUM": len(workers), "DSK_TDD": total("DSW_DD"), "DSK_TROOZ": total("DSW_ROOZ"),
		"DSK_TMAH": total("DSW_MAH"), "DSK_TMAZ": total("DSW_MAZ"), "DSK_TMASH": total("DSW_MASH"),
		"DSK_TTOTL": total("DSW_TOTL"), "DSK_TBIME": total("DSW_BIME"),
		"DSK_TKOSO": round(employer) - unemployment, "DSK_BIC": unemployment, "DSK_RATE": rate,
		"DSK_PRATE": 0, "DSK_BIMH": 0, "MON_PYM": (company.get("ir_ss_contract_row") or "")[:3],
		"DSK_INC": total("DSW_INC"), "DSK_SPOUSE": total("DSW_SPOUSE"),
	}  # fmt: skip
	return dbf(KAR_FIELDS, [workshop_row]), dbf(WOR_FIELDS, workers)


def _component_amounts(slip_names):
	amounts = {}
	for row in frappe.get_all("Salary Detail", filters={"parenttype": "Salary Slip", "parent": ["in", slip_names]},
							  fields=["parent", "abbr", "amount"]):  # fmt: skip
		amounts.setdefault(row.parent, {})
		amounts[row.parent][row.abbr] = amounts[row.parent].get(row.abbr, 0) + flt(row.amount)
	return amounts


@frappe.whitelist()
def download(filters):
	if not frappe.has_permission("Report", "read", "IR Insurance List") or not frappe.has_permission("Salary Slip", "read"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)
	filters = frappe._dict(json.loads(filters) if isinstance(filters, str) else filters)
	kar, wor = build(filters)
	buffer = io.BytesIO()
	with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
		archive.writestr("DSKKAR00.DBF", kar)
		archive.writestr("DSKWOR00.DBF", wor)
	frappe.local.response.filename = f"insurance-list-{filters.jalali_year}-{int(filters.month):02d}.zip"
	frappe.local.response.filecontent = buffer.getvalue()
	frappe.local.response.type = "download"

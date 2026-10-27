"""Jalali fiscal years and Iranian holiday lists."""

import datetime

import frappe
from frappe import _
from frappe.utils import getdate

from erpnext_iran.utils.hijri import lunar_holidays
from erpnext_iran.utils.jalali import jalali_year_range, to_gregorian

# Fixed (solar) official holidays. Lunar ones: erpnext_iran.utils.hijri.
SOLAR_HOLIDAYS = [
	(1, 1, "نوروز"),
	(1, 2, "نوروز"),
	(1, 3, "نوروز"),
	(1, 4, "نوروز"),
	(1, 12, "روز جمهوری اسلامی"),
	(1, 13, "روز طبیعت"),
	(3, 14, "رحلت امام خمینی"),
	(3, 15, "قیام ۱۵ خرداد"),
	(11, 22, "پیروزی انقلاب اسلامی"),
	(12, 29, "ملی شدن صنعت نفت"),
]

FRIDAY = 4  # datetime.date.weekday()
THURSDAY = 3


def create_jalali_fiscal_year(jalali_year, company=None):
	jalali_year = int(jalali_year)
	name = str(jalali_year)
	start, end = jalali_year_range(jalali_year)

	if frappe.db.exists("Fiscal Year", name):
		fy = frappe.get_doc("Fiscal Year", name)
		if company and company not in [row.company for row in fy.companies]:
			fy.append("companies", {"company": company})
			fy.save(ignore_permissions=True)
		return fy.name

	fy = frappe.get_doc(
		{
			"doctype": "Fiscal Year",
			"year": name,
			"year_start_date": start,
			"year_end_date": end,
			"companies": [{"company": company}] if company else [],
		}
	)
	fy.insert(ignore_permissions=True)
	return fy.name


ESTIMATED_SUFFIX = " (پیش‌بینی)"


def get_iran_holidays(jalali_year, include_thursday=False):
	"""([(date, description, weekly_off)] sorted by date, lunar_estimated) for the Jalali year.

	Official holidays (solar and lunar) falling on the same day share one row; lunar_estimated is
	True when the year's lunar dates are estimates (their descriptions end in "(پیش‌بینی)")."""
	jalali_year = int(jalali_year)
	start, end = jalali_year_range(jalali_year)
	weekly = {}
	official = {}

	day = start
	while day <= end:
		if day.weekday() == FRIDAY:
			weekly[day] = _("Friday")
		elif include_thursday and day.weekday() == THURSDAY:
			weekly[day] = _("Thursday")
		day += datetime.timedelta(days=1)

	for jm, jd, description in SOLAR_HOLIDAYS:
		official.setdefault(to_gregorian(jalali_year, jm, jd), []).append(description)
	lunar, estimated = lunar_holidays(jalali_year)
	for day, _key, name in lunar:
		official.setdefault(day, []).append(name + (ESTIMATED_SUFFIX if estimated else ""))

	holidays = {day: (description, 1) for day, description in weekly.items()}
	for day, names in official.items():
		holidays[day] = ("؛ ".join(names), 0)
	return [(d, desc, weekly_off) for d, (desc, weekly_off) in sorted(holidays.items())], estimated


def add_iran_holidays(holiday_list, jalali_year, include_thursday=False):
	"""Add the year's missing holidays to a Holiday List: {"added": n, "lunar_estimated": bool}.
	Days already in the list keep their row; a weekly-off row (a Friday) on an official holiday
	becomes that holiday, and an official row gains the occasions now known for its day."""
	doc = frappe.get_doc("Holiday List", holiday_list)
	from_date, to_date = getdate(doc.from_date), getdate(doc.to_date)
	existing = {getdate(row.holiday_date): row for row in doc.holidays}

	holidays, estimated = get_iran_holidays(jalali_year, include_thursday)
	added = 0
	for day, description, weekly_off in holidays:
		if not from_date <= day <= to_date:
			continue
		row = existing.get(day)
		if row is None:
			doc.append(
				"holidays", {"holiday_date": day, "description": description, "weekly_off": weekly_off}
			)
			added += 1
		elif row.weekly_off and not weekly_off:
			row.description, row.weekly_off = description, 0
			added += 1
		elif not weekly_off and row.description != description and (row.description or "") in description:
			row.description = description  # e.g. "نوروز" -> "نوروز؛ عید سعید فطر"; edited text stays
			added += 1
	doc.save()
	return {"added": added, "lunar_estimated": estimated}


def create_iran_holiday_list(jalali_year, include_thursday=False):
	start, end = jalali_year_range(int(jalali_year))
	name = _("Iran Holidays {0}").format(jalali_year)
	if not frappe.db.exists("Holiday List", name):
		frappe.get_doc(
			{"doctype": "Holiday List", "holiday_list_name": name, "from_date": start, "to_date": end}
		).insert(ignore_permissions=True)
	add_iran_holidays(name, jalali_year, include_thursday)
	return name


def assign_to_company(company, holiday_list):
	"""Frappe HR v16 finds employees' holidays through Holiday List Assignments rather than the
	company's default list: assign the list to the whole company (no-op without that doctype)."""
	if not frappe.db.exists("DocType", "Holiday List Assignment"):
		return
	if frappe.db.exists(
		"Holiday List Assignment",
		{"applicable_for": "Company", "assigned_to": company, "holiday_list": holiday_list, "docstatus": 1},
	):
		return
	doc = frappe.get_doc(
		{
			"doctype": "Holiday List Assignment",
			"applicable_for": "Company",
			"assigned_to": company,
			"holiday_list": holiday_list,
			"from_date": frappe.db.get_value("Holiday List", holiday_list, "from_date"),
		}
	)
	doc.insert(ignore_permissions=True)
	doc.submit()

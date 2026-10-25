"""Jalali fiscal years and Iranian holiday lists."""

import datetime

import frappe
from frappe import _
from frappe.utils import getdate

from erpnext_iran.utils.jalali import jalali_year_range, to_gregorian

# Fixed (solar) official holidays. Lunar holidays move every year and must be added
# from the official calendar published for that year.
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


def get_iran_holidays(jalali_year, include_thursday=False):
	"""[(date, description, weekly_off)] for the Jalali year, sorted by date."""
	jalali_year = int(jalali_year)
	start, end = jalali_year_range(jalali_year)
	holidays = {}

	day = start
	while day <= end:
		if day.weekday() == FRIDAY:
			holidays[day] = (_("Friday"), 1)
		elif include_thursday and day.weekday() == THURSDAY:
			holidays[day] = (_("Thursday"), 1)
		day += datetime.timedelta(days=1)

	for jm, jd, description in SOLAR_HOLIDAYS:
		holidays[to_gregorian(jalali_year, jm, jd)] = (description, 0)

	return [(d, desc, weekly) for d, (desc, weekly) in sorted(holidays.items())]


def add_iran_holidays(holiday_list, jalali_year, include_thursday=False):
	doc = frappe.get_doc("Holiday List", holiday_list)
	from_date, to_date = getdate(doc.from_date), getdate(doc.to_date)
	existing = {getdate(row.holiday_date) for row in doc.holidays}

	added = 0
	for day, description, weekly_off in get_iran_holidays(jalali_year, include_thursday):
		if from_date <= day <= to_date and day not in existing:
			doc.append(
				"holidays", {"holiday_date": day, "description": description, "weekly_off": weekly_off}
			)
			added += 1
	doc.save()
	return added


def create_iran_holiday_list(jalali_year, include_thursday=False):
	start, end = jalali_year_range(int(jalali_year))
	name = _("Iran Holidays {0}").format(jalali_year)
	if not frappe.db.exists("Holiday List", name):
		frappe.get_doc(
			{"doctype": "Holiday List", "holiday_list_name": name, "from_date": start, "to_date": end}
		).insert(ignore_permissions=True)
	add_iran_holidays(name, jalali_year, include_thursday)
	return name

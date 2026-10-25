import frappe
from frappe import _

from erpnext_iran.utils.persian import digits_only, normalize_arabic_letters
from erpnext_iran.utils.settings import get_settings


def validate_item(doc, method=None):
	if get_settings().normalize_arabic_letters and doc.item_name:
		doc.item_name = normalize_arabic_letters(doc.item_name)

	if doc.get("ir_stuff_id"):
		doc.ir_stuff_id = digits_only(doc.ir_stuff_id)
		if len(doc.ir_stuff_id) != 13:
			frappe.throw(_("Moadian Goods/Service ID must be 13 digits"))

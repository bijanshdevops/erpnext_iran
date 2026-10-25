import frappe
from frappe import _

from erpnext_iran.utils.persian import digits_only, normalize_arabic_letters
from erpnext_iran.utils.settings import get_settings
from erpnext_iran.utils.validators import is_valid_postal_code, normalize_mobile

IRAN_COUNTRY_NAMES = ("Iran", "Iran, Islamic Republic of")


def validate_address(doc, method=None):
	if doc.get("country") not in IRAN_COUNTRY_NAMES:
		return
	settings = get_settings()

	if settings.normalize_arabic_letters:
		for fieldname in ("address_line1", "address_line2", "city", "state"):
			if doc.get(fieldname):
				doc.set(fieldname, normalize_arabic_letters(doc.get(fieldname)))

	if doc.get("phone"):
		doc.phone = normalize_mobile(doc.phone) or doc.phone

	if doc.get("pincode"):
		doc.pincode = digits_only(doc.pincode) or doc.pincode
		if settings.validate_postal_code and not is_valid_postal_code(doc.pincode):
			frappe.msgprint(
				_("Postal code {0} does not look like a valid Iranian postal code").format(doc.pincode),
				indicator="orange",
				alert=True,
			)

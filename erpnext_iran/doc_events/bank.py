import frappe
from frappe import _

from erpnext_iran.utils.settings import get_settings
from erpnext_iran.utils.validators import get_bank_from_iban, is_valid_iban, normalize_iban


def validate_bank_account(doc, method=None):
	if not doc.get("iban"):
		return
	doc.iban = normalize_iban(doc.iban)
	if not doc.iban.startswith("IR") or not get_settings().validate_iban:
		return
	if not is_valid_iban(doc.iban):
		frappe.throw(_("IBAN (Sheba) {0} is not valid").format(doc.iban), title=_("Invalid IBAN"))

	bank_name = get_bank_from_iban(doc.iban)
	if bank_name and doc.get("bank") and bank_name not in doc.bank:
		frappe.msgprint(
			_("This IBAN belongs to {0}, but the selected bank is {1}").format(bank_name, doc.bank),
			indicator="orange",
			alert=True,
		)

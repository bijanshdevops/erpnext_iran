"""Customer / Supplier / Company: Iranian ID validation and name normalisation."""

import frappe
from frappe import _

from erpnext_iran.utils.persian import digits_only, normalize_arabic_letters
from erpnext_iran.utils.settings import get_settings
from erpnext_iran.utils.validators import (
	is_valid_economic_code,
	is_valid_legal_national_id,
	is_valid_national_code,
)

NAME_FIELDS = {
	"Customer": ("customer_name",),
	"Supplier": ("supplier_name",),
	"Company": ("company_name",),
}


def infer_person_type(doc):
	if doc.get("ir_person_type"):
		return doc.ir_person_type
	if doc.doctype == "Company":
		return "Legal Entity"
	party_type = doc.get("customer_type") or doc.get("supplier_type")
	if party_type == "Individual":
		return "Natural Person"
	if party_type in ("Company", "Partnership"):
		return "Legal Entity"
	nid = digits_only(doc.get("ir_national_id"))
	return {10: "Natural Person", 11: "Legal Entity"}.get(len(nid))


def normalize_names(doc, method=None):
	"""Also hooked on before_insert: the document name is set from these fields before validate."""
	if get_settings().normalize_arabic_letters:
		for fieldname in NAME_FIELDS.get(doc.doctype, ()):
			if doc.get(fieldname):
				doc.set(fieldname, normalize_arabic_letters(doc.get(fieldname)))


def validate_party(doc, method=None):
	settings = get_settings()
	normalize_names(doc)

	if doc.get("ir_national_id"):
		doc.ir_national_id = digits_only(doc.ir_national_id)
	if doc.get("ir_economic_code"):
		doc.ir_economic_code = digits_only(doc.ir_economic_code)
	if doc.meta.has_field("ir_person_type") and not doc.get("ir_person_type"):
		doc.ir_person_type = infer_person_type(doc)

	if not settings.validate_national_id:
		return

	person_type = infer_person_type(doc)
	nid = doc.get("ir_national_id")
	if nid:
		if person_type == "Natural Person" and not is_valid_national_code(nid):
			frappe.throw(_("National code {0} is not valid").format(nid), title=_("Invalid National ID"))
		if person_type == "Legal Entity" and not is_valid_legal_national_id(nid):
			frappe.throw(
				_("Legal entity national ID {0} is not valid").format(nid), title=_("Invalid National ID")
			)

	code = doc.get("ir_economic_code")
	if code and not is_valid_economic_code(code):
		frappe.throw(_("Economic code {0} is not valid").format(code), title=_("Invalid Economic Code"))

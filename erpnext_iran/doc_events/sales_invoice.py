from erpnext_iran.utils.jalali import format_jalali
from erpnext_iran.utils.settings import get_settings


def validate(doc, method=None):
	if doc.posting_date:
		doc.ir_jalali_posting_date = format_jalali(doc.posting_date)


def on_submit(doc, method=None):
	if not get_settings().moadian_enabled or doc.get("ir_tax_id"):
		return
	from erpnext_iran.moadian.api import assign_tax_id

	doc.db_set({"ir_tax_id": assign_tax_id(doc), "ir_moadian_status": "Pending"})

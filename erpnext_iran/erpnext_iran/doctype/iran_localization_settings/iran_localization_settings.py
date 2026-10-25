import re

import frappe
from frappe import _
from frappe.model.document import Document


class IranLocalizationSettings(Document):
	def validate(self):
		if self.vat_rate is not None and not (0 <= self.vat_rate <= 100):
			frappe.throw(_("VAT Rate must be between 0 and 100"))
		if self.moadian_memory_id:
			self.moadian_memory_id = self.moadian_memory_id.strip().upper()
			if not re.fullmatch(r"[A-Z0-9]{6}", self.moadian_memory_id):
				frappe.throw(_("Fiscal Memory ID must be 6 letters or digits"))
		if self.moadian_enabled and not self.moadian_memory_id:
			frappe.msgprint(
				_("Set a Fiscal Memory ID here or on each Company before submitting invoices"),
				indicator="orange",
			)

	def on_update(self):
		# boot info carries the display mode
		frappe.clear_cache()

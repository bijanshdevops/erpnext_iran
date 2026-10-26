import frappe
from frappe import _
from frappe.model.document import Document


class IRPayrollYear(Document):
	def validate(self):
		starts = [row.from_amount for row in self.tax_brackets]
		if len(starts) != len(set(starts)):
			frappe.throw(_("Two salary tax brackets start at the same amount"))
		self.tax_brackets.sort(key=lambda row: row.from_amount)
		for i, row in enumerate(self.tax_brackets, start=1):
			row.idx = i

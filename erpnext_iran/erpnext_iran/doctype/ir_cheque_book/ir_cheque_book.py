import frappe
from frappe import _
from frappe.model.document import Document


class IRChequeBook(Document):
	def validate(self):
		if self.first_serial is None or self.first_serial < 0:
			frappe.throw(_("First Serial must be zero or more"))
		if not self.leaves or self.leaves <= 0:
			frappe.throw(_("Number of Leaves must be greater than zero"))
		if frappe.db.get_value("Account", self.bank_account, "company") != self.company:
			frappe.throw(_("Account {0} does not belong to company {1}").format(self.bank_account, self.company))

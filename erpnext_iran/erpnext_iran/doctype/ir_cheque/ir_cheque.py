"""A received or issued cheque. Submitting books it into notes receivable / payable; deposit,
clear, bounce and endorse each post a Journal Entry (see erpnext_iran.cheques.core)."""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate

from erpnext_iran.cheques.core import (
	ISSUED,
	RECEIVED,
	allowed_actions,
	is_valid_sayad_id,
	next_step,
	normalize_sayad_id,
	serial_in_book,
)
from erpnext_iran.setup.chart_of_accounts import get_account
from erpnext_iran.utils.jalali import format_jalali

DEFAULT_ACCOUNTS = {
	(RECEIVED, "notes_account"): "110302",  # اسناد دریافتنی تجاری
	(RECEIVED, "in_collection_account"): "110303",  # چک‌های در جریان وصول
	(ISSUED, "notes_account"): "210102",  # اسناد پرداختنی تجاری
}


class IRCheque(Document):
	def validate(self):
		self.sayad_id = normalize_sayad_id(self.sayad_id)
		if not is_valid_sayad_id(self.sayad_id):
			frappe.throw(_("Sayad ID must be 16 digits"))
		duplicate = frappe.db.get_value(
			"IR Cheque",
			{"sayad_id": self.sayad_id, "cheque_type": self.cheque_type, "docstatus": ["<", 2], "name": ["!=", self.name]},
		)
		if duplicate:
			frappe.throw(_("Sayad ID {0} is already used by {1}").format(self.sayad_id, duplicate))
		if flt(self.amount) <= 0:
			frappe.throw(_("Amount must be greater than zero"))
		if self.issue_date and getdate(self.issue_date) > getdate(self.due_date):
			frappe.throw(_("Due Date cannot be before Issue Date"))

		self.party_name = frappe.db.get_value(
			self.party_type, self.party, "customer_name" if self.party_type == "Customer" else "supplier_name"
		)
		self.set_default_accounts()
		self.validate_cheque_book()
		if self.docstatus == 0:
			self.status = "Draft"

	def set_default_accounts(self):
		for (cheque_type, fieldname), number in DEFAULT_ACCOUNTS.items():
			if cheque_type == self.cheque_type and not self.get(fieldname):
				self.set(fieldname, get_account(self.company, number))
		if self.cheque_type == ISSUED:
			self.in_collection_account = None
		for fieldname in ("notes_account", "in_collection_account", "bank_account"):
			account = self.get(fieldname)
			if account and frappe.db.get_value("Account", account, "company") != self.company:
				frappe.throw(_("Account {0} does not belong to company {1}").format(account, self.company))

	def validate_cheque_book(self):
		if self.cheque_type != ISSUED or not self.cheque_book:
			return
		book = frappe.get_cached_doc("IR Cheque Book", self.cheque_book)
		if book.company != self.company:
			frappe.throw(_("Cheque Book {0} belongs to another company").format(self.cheque_book))
		if not serial_in_book(self.serial or "", book.first_serial, book.leaves):
			frappe.throw(
				_("Serial {0} is not a leaf of cheque book {1} ({2} to {3})").format(
					self.serial, book.series or book.name, book.first_serial, book.first_serial + book.leaves - 1
				)
			)
		used = frappe.db.get_value(
			"IR Cheque",
			{"cheque_book": self.cheque_book, "serial": self.serial, "docstatus": ["<", 2], "name": ["!=", self.name]},
		)
		if used:
			frappe.throw(_("Leaf {0} of this cheque book is already used by {1}").format(self.serial, used))
		self.series = self.series or book.series
		self.bank = self.bank or book.bank
		self.bank_account = self.bank_account or book.bank_account

	def before_submit(self):
		for fieldname in ("notes_account",) + (("in_collection_account",) if self.cheque_type == RECEIVED else ()):
			if not self.get(fieldname):
				frappe.throw(_("Set {0}").format(_(self.meta.get_label(fieldname))))

	def on_submit(self):
		self.apply("submit", self.issue_date or nowdate())
		self.update_cheque_book()

	def on_cancel(self):
		self.ignore_linked_doctypes = ("Journal Entry",)
		for movement in reversed(self.movements):
			if movement.journal_entry and not movement.cancelled:
				je = frappe.get_doc("Journal Entry", movement.journal_entry)
				if je.docstatus == 1:
					je.flags.ignore_links = True
					je.cancel()
				movement.db_set("cancelled", 1)
		self.db_set("status", "Cancelled")
		self.update_cheque_book()

	def update_cheque_book(self):
		if self.cheque_book:
			used = frappe.db.count("IR Cheque", {"cheque_book": self.cheque_book, "docstatus": 1})
			frappe.db.set_value("IR Cheque Book", self.cheque_book, "used_leaves", used)

	def apply(self, action, posting_date, endorsee=None):
		"""Move the cheque to its next status and post the ledger lines of the step."""
		current = None if action == "submit" else self.status
		step = next_step(self.cheque_type, action, current)
		if not step:
			frappe.throw(_("Cannot {0}: the cheque is {1}").format(_(ACTION_LABELS.get(action, action)), _(current or "Draft")))
		to_status, lines = step

		if action == "endorse":
			if not endorsee:
				frappe.throw(_("Select the supplier the cheque is endorsed to"))
			self.endorsed_to = endorsee
		accounts = self.resolve_roles(lines)
		je = self.make_journal_entry(action, posting_date, accounts)

		row = self.append(
			"movements",
			{
				"posting_date": posting_date,
				"action": action,
				"from_status": current or "",
				"to_status": to_status,
				"journal_entry": je.name,
			},
		)
		self.status = to_status
		if action == "submit":  # on_submit runs after the document is written
			row.db_insert()
			self.db_set("status", to_status)
		else:
			self.save()
		return je

	def resolve_roles(self, lines):
		from erpnext.accounts.party import get_party_account

		def resolve(role):
			if role == "party":
				return get_party_account(self.party_type, self.party, self.company), self.party_type, self.party
			if role == "endorsee":
				return get_party_account("Supplier", self.endorsed_to, self.company), "Supplier", self.endorsed_to
			account = {"notes": self.notes_account, "in_collection": self.in_collection_account, "bank": self.bank_account}[role]
			if not account:
				label = {"notes": "Notes Account", "in_collection": "Cheques in Collection Account", "bank": "Bank Account"}[role]
				frappe.throw(_("Set {0}").format(_(label)))
			return account, None, None

		return [(resolve(debit), resolve(credit)) for debit, credit in lines]

	def make_journal_entry(self, action, posting_date, accounts):
		je = frappe.new_doc("Journal Entry")
		je.update(
			{
				"voucher_type": "Journal Entry",
				"company": self.company,
				"posting_date": posting_date,
				"cheque_no": self.serial or self.sayad_id,
				"cheque_date": self.due_date,
				"user_remark": _("Cheque {0}: {1}, Sayad ID {2}, due {3}").format(
					self.name, _(ACTION_LABELS[action]), self.sayad_id, format_jalali(self.due_date)
				),
			}
		)
		for debit, credit in accounts:
			for (account, party_type, party), side in ((debit, "debit"), (credit, "credit")):
				je.append(
					"accounts",
					{
						"account": account,
						"party_type": party_type,
						"party": party,
						f"{side}_in_account_currency": flt(self.amount),
					},
				)
		je.insert()
		je.submit()
		return je


ACTION_LABELS = {
	"submit": "Register Cheque",
	"deposit": "Deposit to Bank",
	"clear": "Clear Cheque",
	"bounce": "Bounce Cheque",
	"endorse": "Endorse to Supplier",
}


@frappe.whitelist()
def make_movement(name, action, posting_date=None, bank_account=None, endorsee=None):
	cheque = frappe.get_doc("IR Cheque", name)
	cheque.check_permission("submit")
	if cheque.docstatus != 1:
		frappe.throw(_("Submit the cheque first"))
	if bank_account:
		cheque.bank_account = bank_account
	je = cheque.apply(action, posting_date or nowdate(), endorsee)
	return {"status": cheque.status, "journal_entry": je.name}


@frappe.whitelist()
def get_actions(name):
	cheque = frappe.get_doc("IR Cheque", name)
	if cheque.docstatus != 1:
		return []
	return allowed_actions(cheque.cheque_type, cheque.status)

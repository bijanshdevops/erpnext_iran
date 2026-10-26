"""Cheque life cycle and the ledger lines of each step. Pure Python.

A received cheque sits in notes receivable, moves to cheques in collection when deposited and to
the bank when cleared. Bouncing hands the debt back to the customer; endorsing passes the
cheque to a supplier. An issued cheque sits in notes payable until the bank pays it.

Lines are (account role, side, party role): roles are resolved to real accounts by the caller
("party" is the cheque's customer or supplier, "endorsee" the supplier it was endorsed to).
"""

import re

from erpnext_iran.utils.persian import to_english_digits

RECEIVED, ISSUED = "Received", "Issued"

# (cheque type, action) -> {from status: (to status, [(debit role, credit role)])}
TRANSITIONS = {
	(RECEIVED, "submit"): {None: ("Received", [("notes", "party")])},
	(RECEIVED, "deposit"): {"Received": ("Deposited", [("in_collection", "notes")])},
	(RECEIVED, "clear"): {
		"Received": ("Cleared", [("bank", "notes")]),
		"Deposited": ("Cleared", [("bank", "in_collection")]),
	},
	(RECEIVED, "bounce"): {
		"Received": ("Bounced", [("party", "notes")]),
		"Deposited": ("Bounced", [("party", "in_collection")]),
		# the supplier hands back a cheque we endorsed to them: we owe them again
		"Endorsed": ("Bounced", [("party", "endorsee")]),
	},
	(RECEIVED, "endorse"): {"Received": ("Endorsed", [("endorsee", "notes")])},
	(ISSUED, "submit"): {None: ("Issued", [("party", "notes")])},
	(ISSUED, "clear"): {"Issued": ("Cleared", [("notes", "bank")])},
	(ISSUED, "bounce"): {"Issued": ("Bounced", [("notes", "party")])},
}

ACTIONS = ("deposit", "clear", "bounce", "endorse")


def next_step(cheque_type, action, status):
	"""(new status, [(debit role, credit role)]) or None when the action is not allowed."""
	return TRANSITIONS.get((cheque_type, action), {}).get(status)


def allowed_actions(cheque_type, status):
	return [action for action in ACTIONS if next_step(cheque_type, action, status)]


def normalize_sayad_id(value):
	return re.sub(r"[\s\-]", "", to_english_digits(value or ""))


def is_valid_sayad_id(value):
	"""The Sayad ID printed on every cheque leaf is 16 digits."""
	return bool(re.fullmatch(r"\d{16}", normalize_sayad_id(value)))


def serial_in_book(serial, first_serial, leaves):
	try:
		serial = int(to_english_digits(str(serial)))
	except ValueError:
		return False
	return int(first_serial) <= serial < int(first_serial) + int(leaves)

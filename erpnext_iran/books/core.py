"""Statutory books (journal and general ledger) built from ledger lines. Pure Python.

A journal voucher is one ERPNext voucher (invoice, payment, journal entry, ...), numbered in date
order from the start of the fiscal year. Its lines are netted per account at the chosen level, so
the journal and the ledger show the same amounts.
"""

from collections import OrderedDict


def level_map(accounts, depth):
	"""{account: account it is reported under}. accounts are dicts with name and parent_account;
	depth 0 is a root group, so depth 2 is the general account (e.g. 1101 under 1 > 11). An
	account above that depth is reported as itself. depth None keeps every account."""
	parents = {a["name"]: a.get("parent_account") for a in accounts}

	def chain(name):
		path = [name]
		while parents.get(path[-1]):
			path.append(parents[path[-1]])
		return path[::-1]  # root first

	mapping = {}
	for name in parents:
		path = chain(name)
		mapping[name] = name if depth is None or len(path) <= depth else path[depth]
	return mapping


def build_journal(entries, level_of, start_number=1):
	"""Journal rows from ledger lines sorted in posting order.

	entries: dicts with posting_date, voucher_type, voucher_no, account, debit, credit and
	description (the voucher's). Returns rows with voucher_number, first (first line of its
	voucher), account, debit, credit; debit lines come before credit lines in a voucher."""
	vouchers = OrderedDict()
	for e in entries:
		key = (e["voucher_type"], e["voucher_no"])
		voucher = vouchers.setdefault(
			key, {"posting_date": e["posting_date"], "description": e.get("description") or "", "lines": OrderedDict()}
		)
		account = level_of.get(e["account"], e["account"])
		voucher["lines"][account] = voucher["lines"].get(account, 0) + float(e["debit"] or 0) - float(e["credit"] or 0)

	rows = []
	number = start_number
	for (voucher_type, voucher_no), voucher in vouchers.items():
		lines = [(acc, round(net, 6)) for acc, net in voucher["lines"].items() if round(net, 6)]
		if not lines:
			continue
		lines.sort(key=lambda line: line[1] < 0)  # debits first, order kept otherwise
		for i, (account, net) in enumerate(lines):
			rows.append(
				{
					"voucher_number": number,
					"first": i == 0,
					"posting_date": voucher["posting_date"],
					"voucher_type": voucher_type,
					"voucher_no": voucher_no,
					"description": voucher["description"],
					"account": account,
					"debit": net if net > 0 else 0.0,
					"credit": -net if net < 0 else 0.0,
				}
			)
		number += 1
	return rows


def build_ledger(journal_rows, openings, accounts=None):
	"""General ledger: {account: {"opening", "rows", "debit", "credit", "balance"}} in account
	order. The opening balance (debit positive) is the first row, so totals include it and
	balance = debit - credit. Accounts with neither an opening balance nor movements are left out."""
	ledger = OrderedDict()
	names = accounts or sorted(set(openings) | {r["account"] for r in journal_rows})

	by_account = {}
	for row in journal_rows:
		by_account.setdefault(row["account"], []).append(row)

	for account in names:
		opening = round(float(openings.get(account, 0)), 6)
		movements = by_account.get(account, [])
		if not opening and not movements:
			continue
		rows = []
		if opening:
			rows.append(
				{"opening": True, "debit": opening if opening > 0 else 0.0, "credit": -opening if opening < 0 else 0.0}
			)
		rows.extend(dict(r) for r in movements)
		balance = 0.0
		for row in rows:
			balance += row["debit"] - row["credit"]
			row["balance"] = balance
		ledger[account] = {
			"opening": opening,
			"rows": rows,
			"debit": sum(r["debit"] for r in rows),
			"credit": sum(r["credit"] for r in rows),
			"balance": balance,
		}
	return ledger


def paginate(rows, per_page, keys=("debit", "credit")):
	"""Pages of at most per_page rows, each with the totals brought forward from the previous
	page, its own totals, and the totals carried forward to the next page."""
	pages = []
	carried = {k: 0.0 for k in keys}
	for start in range(0, max(len(rows), 1), per_page):
		chunk = rows[start : start + per_page]
		own = {k: sum(float(r.get(k) or 0) for r in chunk) for k in keys}
		out = {k: carried[k] + own[k] for k in keys}
		pages.append({"rows": chunk, "brought_forward": carried, "page_total": own, "carried_forward": out})
		carried = out
	for i, page in enumerate(pages):
		page["first"], page["last"] = i == 0, i == len(pages) - 1
	return pages

"""Merge tools/fa_missing.py and tools/fa_overrides.py into erpnext_iran/translations/fa.csv.

Needs a site (onboarding English is read from its records):

    <bench>/env/bin/python <bench>/apps/erpnext_iran/tools/update_translations.py <site>

Rows the app already has for other strings are kept; rows for these sources are replaced.
"""

import csv
import io
import pathlib
import sys

APP = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = APP / "erpnext_iran" / "translations" / "fa.csv"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fa_missing import MISSING  # noqa: E402
from fa_overrides import CORRECTIONS, FORM_TOURS, ONBOARDING  # noqa: E402


def onboarding_sources(frappe):
	sources = {}
	for mo in frappe.get_all("Module Onboarding", fields=["name", "title", "subtitle", "success_message"]):
		for field in ("title", "subtitle", "success_message"):
			sources[(f"MO:{mo.name}", field)] = mo[field]
	for step in frappe.get_all("Onboarding Step", fields=["name", "title", "description", "action_label"]):
		for field in ("title", "description", "action_label"):
			sources[(f"OS:{step.name}", field)] = step[field]
	return sources


def main(site):
	import os

	import frappe

	os.chdir(APP.parent.parent / "sites")  # frappe resolves logs/ and config relative to sites/
	frappe.init(site=site, sites_path=".")
	frappe.connect()
	sources = onboarding_sources(frappe)

	# MISSING first so that hand-picked CORRECTIONS win where both define a string
	new_rows = dict(MISSING)
	new_rows.update(CORRECTIONS)
	new_rows.update(FORM_TOURS)
	stale = []
	for key, persian in ONBOARDING.items():
		english = sources.get(key)
		if english:
			# desk JS looks the text up as-is, frappe._() strips it first: keep both keys
			new_rows[english] = persian
			new_rows[english.strip()] = persian.strip()
		else:
			stale.append(key)

	# a key is a source string, or (source, context) for context-specific translations
	def as_row(key, persian):
		return [key[0], persian, key[1]] if isinstance(key, tuple) else [key, persian]

	def row_key(row):
		return (row[0], row[2]) if len(row) > 2 and row[2] else row[0]

	# frappe._() strips its input before the lookup, desk JS does not: give padded strings
	# (e.g. "Date: ") a stripped key too
	for key, persian in list(new_rows.items()):
		if isinstance(key, str) and key != key.strip() and key.strip() not in new_rows:
			new_rows[key.strip()] = persian.strip()

	with open(CSV_PATH, encoding="utf-8", newline="") as f:
		kept = [row for row in csv.reader(f) if row and row_key(row) not in new_rows]

	out = io.StringIO()
	writer = csv.writer(out, lineterminator="\n")
	writer.writerows(kept)
	writer.writerows(sorted((as_row(k, v) for k, v in new_rows.items()), key=lambda r: (r[0], r[2:])))
	CSV_PATH.write_text(out.getvalue(), encoding="utf-8", newline="\n")

	print(f"kept {len(kept)}, wrote {len(new_rows)} (corrections, form tours and onboarding)")
	if stale:
		print("no longer on this site (skipped):", stale)


if __name__ == "__main__":
	main(sys.argv[1])

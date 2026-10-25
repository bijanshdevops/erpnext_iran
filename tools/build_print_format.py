"""Embed ir_official_invoice.html into its Print Format JSON. Run after editing the HTML:

    python tools/build_print_format.py
"""

import json
import pathlib

FOLDER = pathlib.Path(__file__).resolve().parent.parent / "erpnext_iran/erpnext_iran/print_format/ir_official_invoice"


def main():
	html = (FOLDER / "ir_official_invoice.html").read_text(encoding="utf-8")
	doc = {
		"align_labels_right": 1,
		"creation": "2026-10-25 00:00:00.000000",
		"custom_format": 1,
		"disabled": 0,
		"doc_type": "Sales Invoice",
		"docstatus": 0,
		"doctype": "Print Format",
		"font_size": 0,
		"html": html,
		"idx": 0,
		"line_breaks": 0,
		"margin_bottom": 10.0,
		"margin_left": 8.0,
		"margin_right": 8.0,
		"margin_top": 10.0,
		"modified": "2026-10-25 00:00:00.000000",
		"modified_by": "Administrator",
		"module": "ERPNext Iran",
		"name": "IR Official Invoice",
		"owner": "Administrator",
		"page_number": "Hide",
		"print_format_builder": 0,
		"print_format_type": "Jinja",
		"raw_printing": 0,
		"show_section_headings": 0,
		"standard": "Yes",
	}
	out = FOLDER / "ir_official_invoice.json"
	text = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
	out.write_text(text, encoding="utf-8", newline="\n")
	print(f"wrote {out}")


if __name__ == "__main__":
	main()

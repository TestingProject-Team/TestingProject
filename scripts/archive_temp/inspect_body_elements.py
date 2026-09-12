# -*- coding: utf-8 -*-
import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1)_BACKUP.docx")

body = doc._body._element

print(f"Body direct children count: {len(body)}")

# Tìm vị trí các heading quan trọng trong body
for idx, child in enumerate(body):
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(child, doc)
        text = p.text.strip()
        if text.startswith("V. ") or text.startswith("IV. ") or text.startswith("VI. ") or text.startswith("Phụ lục"):
            print(f"Child[{idx}] <p>: {text[:80]}")
    elif tag == 'tbl':
        t = docx.table.Table(child, doc)
        first_row_text = " | ".join(c.text.strip() for c in t.rows[0].cells)[:60] if len(t.rows) > 0 else ""
        # print(f"Child[{idx}] <tbl>: {first_row_text}")

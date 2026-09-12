# -*- coding: utf-8 -*-
import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1)_BACKUP.docx")
body = doc._body._element

print("=== CHƯƠNG IV (Child 400 -> 440) ===")
for i in range(400, 440):
    child = body[i]
    if child.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(child, doc)
        if p.text.strip():
            print(f"{i} (p): [{p.style.name}] {p.text[:70]}")
    elif child.tag.endswith('tbl'):
        t = docx.table.Table(child, doc)
        row_str = " | ".join(c.text.strip() for c in t.rows[0].cells)[:60] if len(t.rows) > 0 else ""
        print(f"{i} (tbl): [Rows={len(t.rows)}, Cols={len(t.columns)}] {row_str}")

print("\n=== CHƯƠNG VI (Child 682 -> 720) ===")
for i in range(682, 720):
    child = body[i]
    if child.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(child, doc)
        if p.text.strip():
            print(f"{i} (p): [{p.style.name}] {p.text[:70]}")
    elif child.tag.endswith('tbl'):
        t = docx.table.Table(child, doc)
        row_str = " | ".join(c.text.strip() for c in t.rows[0].cells)[:60] if len(t.rows) > 0 else ""
        print(f"{i} (tbl): [Rows={len(t.rows)}, Cols={len(t.columns)}] {row_str}")

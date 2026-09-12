# -*- coding: utf-8 -*-
import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1)_BACKUP.docx")
body = doc._body._element

print("=== MỤC LỤC ===")
for i in range(25, 52):
    child = body[i]
    if child.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(child, doc)
        print(f"{i}: [{p.style.name}] {p.text}")

print("\n=== CHƯƠNG V HIỆN TẠI (Child 627 -> 682) ===")
for i in range(627, 682):
    child = body[i]
    if child.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(child, doc)
        if p.text.strip():
            print(f"{i} (p): [{p.style.name}] {p.text[:70]}")
    elif child.tag.endswith('tbl'):
        t = docx.table.Table(child, doc)
        row_str = " | ".join(c.text.strip() for c in t.rows[0].cells)[:60] if len(t.rows) > 0 else ""
        print(f"{i} (tbl): [Rows={len(t.rows)}, Cols={len(t.columns)}] {row_str}")

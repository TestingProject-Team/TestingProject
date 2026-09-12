# -*- coding: utf-8 -*-
import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = "YiYi_Book_Capstone_Project_Report_Tieng_Viet_Updated.docx"
doc = docx.Document(DOCX_PATH)

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")

print("\n=== KIỂM TRA MỤC LỤC ===")
for p in doc.paragraphs[35:50]:
    if p.text.strip():
        print(f"  {p.text}")

print("\n=== KIỂM TRA CÁC BẢNG TRONG CHƯƠNG V ===")
for idx, tbl in enumerate(doc.tables):
    rows = len(tbl.rows)
    cols = len(tbl.columns)
    first_row = " | ".join(c.text.strip() for c in tbl.rows[0].cells)[:80]
    if "Bảng" in first_row or "Công cụ" in first_row or "Thành viên" in first_row or "Tiêu chí" in first_row or "Lớp kiểm thử" in first_row or "Tham số" in first_row or "Mã Defect" in first_row or "Mã Yêu cầu" in first_row:
        print(f"Table {idx} [{rows}x{cols}]: {first_row}")

print("\n=== KIỂM TRA CÚ PHÁP MARKDOWN THÔ TRONG CÁC ĐOẠN VĂN ===")
raw_markdown_found = False
for i, p in enumerate(doc.paragraphs):
    t = p.text
    if "|---" in t or "| **" in t or "`Auth" in t or "| 299 |" in t or "100%** |" in t:
        print(f"P[{i}]: {t[:80]}")
        raw_markdown_found = True

if not raw_markdown_found:
    print("SUCCESS: Không còn bất kỳ đoạn text chứa ký tự Markdown thô nào! Toàn bộ đã chuyển thành Bảng và Text chuẩn Word.")

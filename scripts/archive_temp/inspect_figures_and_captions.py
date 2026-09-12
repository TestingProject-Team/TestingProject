# -*- coding: utf-8 -*-
"""
inspect_figures_and_captions.py
Quét toàn bộ các caption hình ảnh hiện có trong tài liệu và in ra danh sách theo từng chương.
"""
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def check_all_captions():
    doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx")
    
    print("=== TẤT CẢ CÁC CAPTION / PLACEHOLDER HIỆN CÓ ===")
    for idx, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t.startswith("Hình ") or "Hình " in t[:15] or "Chèn screenshot" in t:
            print(f"[P {idx:04d}] {t[:120]}")

if __name__ == "__main__":
    check_all_captions()

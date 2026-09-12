# -*- coding: utf-8 -*-
"""
inspect_sections_detail.py
Quét chi tiết nội dung đoạn văn quanh các điểm cần chèn/sửa ở các Chương I, II, III, IV, VI.
"""
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_sections():
    doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx")
    body = doc._body._body
    
    ranges_to_check = [
        ("Chương I - Mục 3 Benchmark", 75, 95),
        ("Chương II - Quy trình Agile & Đào tạo", 130, 155),
        ("Chương III - System Context & NFR", 170, 185),
        ("Chương III - 4. Yêu cầu phi chức năng", 380, 400),
        ("Chương IV - 1. Thiết kế hệ thống & Detailed Design", 405, 645),
        ("Chương VI - 2. Hướng dẫn cài đặt & Manual", 870, 910)
    ]
    
    for title, start, end in ranges_to_check:
        print(f"\n==================== {title} (Idx {start} - {end}) ====================")
        for idx in range(start, min(end, len(body))):
            child = body[idx]
            tag = child.tag.split('}')[-1]
            text = "".join(child.itertext()).strip()
            if len(text) > 0:
                print(f"[{idx:04d}] <{tag}> : {text[:120]}")

if __name__ == "__main__":
    inspect_sections()

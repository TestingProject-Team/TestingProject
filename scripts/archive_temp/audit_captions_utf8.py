# -*- coding: utf-8 -*-
"""
audit_captions_utf8.py
"""

import docx
import io
import sys

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full.docx")
captions = []
for p in doc.paragraphs:
    t = p.text.strip()
    if t.startswith("Hình ") and ":" not in t and len(t) < 150:
        captions.append(t)

print(f"Total captions found: {len(captions)}")
with open("all_refined_captions_list.txt", "w", encoding="utf-8") as f:
    for c in captions:
        f.write(c + "\n")
        print(c)

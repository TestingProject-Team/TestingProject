# -*- coding: utf-8 -*-
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Updated.docx")
body = doc._body._element

print("Searching for paragraphs/tables under Section III...")
for idx, elem in enumerate(body):
    tag = elem.tag.split("}")[-1]
    text = "".join(elem.itertext())
    if "Hình 3.1" in text or "Hình 3.2" in text:
        print(f"Body[{idx}] <{tag}>: {text[:120]}")
        for neighbor in range(max(0, idx-4), min(len(body), idx+6)):
            n_elem = body[neighbor]
            n_tag = n_elem.tag.split("}")[-1]
            n_text = "".join(n_elem.itertext())
            print(f"   [{neighbor}] <{n_tag}>: {n_text[:120]}")
        print("="*60)

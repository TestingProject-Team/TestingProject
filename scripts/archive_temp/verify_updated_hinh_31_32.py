# -*- coding: utf-8 -*-
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Updated.docx")
body = doc._body._element

print("Verifying updated paragraphs under Section III...")
for idx in range(185, min(205, len(body))):
    elem = body[idx]
    tag = elem.tag.split("}")[-1]
    text = "".join(elem.itertext())
    print(f"[{idx}] <{tag}>: {text[:100]}")

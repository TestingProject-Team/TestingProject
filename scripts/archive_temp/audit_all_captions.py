# -*- coding: utf-8 -*-
import docx

doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full.docx")

captions = []
for p in doc.paragraphs:
    text = p.text.strip()
    if text.startswith("Hình "):
        captions.append(text)

# Also check tables and all body elements
for elem in doc._body._element:
    tag = elem.tag.split('}')[-1]
    if tag == "p":
        t = "".join(elem.itertext()).strip()
        if t.startswith("Hình ") and t not in captions:
            captions.append(t)

print(f"Total Figures Found: {len(captions)}")
print("-" * 60)
for c in captions:
    print(c)

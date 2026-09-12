import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx")

print("--- PARAGRAPHS 1 TO 55 (Table of Contents) ---")
for i in range(56):
    p = doc.paragraphs[i]
    if p.text.strip():
        print(f"[{i}] ({p.style.name}): {p.text.strip()}")

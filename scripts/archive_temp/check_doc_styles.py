import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx")

print("Styles available in document:")
for s in doc.styles:
    if "Heading" in s.name or "Normal" in s.name or "Title" in s.name:
        print(f"Style: {s.name}")

print("\nTotal sections:", len(doc.sections))
for i, sec in enumerate(doc.sections):
    print(f"Section {i}: page_width={sec.page_width}, page_height={sec.page_height}, orientation={sec.orientation}")

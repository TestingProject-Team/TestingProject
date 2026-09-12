import docx
import re

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Content_Final.docx'
doc = docx.Document(doc_path)

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")

# Check Chapter I: Target Users in Table 3 and anywhere in text
t3 = doc.tables[3]
print("Table 3 Row 4:", t3.rows[4].cells[0].text, "->", t3.rows[4].cells[1].text)

# Check all occurrences of "Người dùng mục tiêu" or "QA" or "content operator"
for i, p in enumerate(doc.paragraphs[:100]):
    if any(k in p.text.lower() for k in ['người dùng mục tiêu', 'content operator', 'qa/dự án', 'xem chi tiết sách & đánh giá']):
        print(f"P{i}: {p.text}")

# Check Table 28 (Use Cases) UC-03
t28 = doc.tables[28]
for r in t28.rows:
    if r.cells[0].text.strip() == 'UC-03':
        print("UC-03 in Table 28:", [c.text for c in r.cells])

import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

with open(r'E:\TestingProject\chap4_sections_detail.txt', 'w', encoding='utf-8') as f:
    for idx in range(413, 555):
        p = doc.paragraphs[idx]
        t = p.text.strip()
        if p.style.name.startswith('Heading') or t.startswith('Hình 4.') or t.startswith('[CẦN') or t.startswith('Bảng'):
            f.write(f"[P{idx}][{p.style.name}] {t}\n")

print("Dumped Chap 4 sections detail.")

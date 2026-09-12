import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

with open(r'E:\TestingProject\chap4_p414_to_430.txt', 'w', encoding='utf-8') as f:
    for idx in range(414, 431):
        p = doc.paragraphs[idx]
        f.write(f"[P{idx}][{p.style.name}] {p.text}\n")

print("Dumped 414 to 430.")

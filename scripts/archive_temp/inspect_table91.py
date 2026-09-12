import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

with open(r'E:\TestingProject\table91_rtm.txt', 'w', encoding='utf-8') as f:
    t91 = doc.tables[91]
    f.write(f"=== TABLE 91: RTM (rows={len(t91.rows)}, cols={len(t91.columns)}) ===\n")
    for r_idx, r in enumerate(t91.rows):
        f.write(f"Row {r_idx}: {[c.text.strip().replace('\n', ' ') for c in r.cells]}\n")

print("Dumped Table 91.")

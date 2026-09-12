import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

with open(r'E:\TestingProject\table71_inspection.txt', 'w', encoding='utf-8') as f:
    table = doc.tables[71]
    f.write(f"=== TABLE 71 (rows={len(table.rows)}, cols={len(table.columns)}) ===\n")
    for r_idx, row in enumerate(table.rows):
        cells_text = [c.text.strip().replace('\n', ' ') for c in row.cells]
        f.write(f"Row {r_idx}: {cells_text}\n")

print("Dumped table 71.")

# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_details(file_path):
    doc = docx.Document(file_path)
    
    print("=== Table 0 to Table 10 Sample Text ===")
    for t_idx in range(min(12, len(doc.tables))):
        table = doc.tables[t_idx]
        print(f"\n--- Table {t_idx} ({len(table.rows)} rows x {len(table.columns)} cols) ---")
        for r_idx, row in enumerate(table.rows[:5]):
            row_vals = [cell.text.replace('\n', ' ') for cell in row.cells]
            print(f"  Row {r_idx}: {' | '.join(row_vals)}")

    print("\n=== Table 62 (Wrong member names) ===")
    if len(doc.tables) > 62:
        table = doc.tables[62]
        for r_idx, row in enumerate(table.rows):
            row_vals = [cell.text.replace('\n', ' ') for cell in row.cells]
            print(f"  Row {r_idx}: {' | '.join(row_vals)}")

    print("\n=== Inspecting Paragraphs 50 to 70 ===")
    for p_idx in range(50, min(70, len(doc.paragraphs))):
        print(f"  [P{p_idx}]: {doc.paragraphs[p_idx].text}")

    print("\n=== Inspecting Paragraph 635 (Credentials) ===")
    if len(doc.paragraphs) > 635:
        print(f"  [P635]: {doc.paragraphs[635].text}")

    print("\n=== Inspecting Appendix / Last 30 Paragraphs ===")
    for p_idx in range(max(0, len(doc.paragraphs)-30), len(doc.paragraphs)):
        print(f"  [P{p_idx}]: {doc.paragraphs[p_idx].text}")

if __name__ == "__main__":
    inspect_details("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Updated.docx")

# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_table_cells(file_path):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    for idx in [741, 770, 783, 806]:
        elem = body[idx]
        text = "".join(elem.itertext())
        print(f"Element {idx}: length {len(text)}, snippet: {text[:80]}")

if __name__ == "__main__":
    inspect_table_cells("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx")

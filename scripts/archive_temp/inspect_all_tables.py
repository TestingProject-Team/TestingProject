# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_tables(file_path):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    for idx in range(740, 815):
        elem = body[idx]
        tag = elem.tag.split('}')[-1]
        if tag == "tbl":
            text = "".join(elem.itertext()).strip()
            print(f"Table at element {idx}: {text[:200]}\n---")

if __name__ == "__main__":
    inspect_tables("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx")

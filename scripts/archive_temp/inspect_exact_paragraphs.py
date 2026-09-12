# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_range(file_path, start, end):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    for idx in range(start, min(end, len(body))):
        child = body[idx]
        tag = child.tag.split('}')[-1]
        text = "".join(child.itertext()).strip()
        print(f"[{idx}] <{tag}>: {text[:100]}")

if __name__ == "__main__":
    inspect_range("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx", 735, 815)

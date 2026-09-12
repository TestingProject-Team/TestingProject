# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_all_occurrences(file_path):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    print(f"Total elements in body: {len(body)}")
    
    chap5_indices = []
    for idx, child in enumerate(body):
        text = "".join(child.itertext()).strip()
        if "V. Tài liệu kiểm thử" in text:
            chap5_indices.append((idx, text[:60]))
            
    print(f"Occurrences of 'V. Tài liệu kiểm thử': {chap5_indices}")
    
    if len(chap5_indices) > 1:
        start_idx = chap5_indices[1][0] # The body one
        print(f"\nListing elements starting from {start_idx}:")
        for idx in range(start_idx, min(start_idx + 180, len(body))):
            child = body[idx]
            tag = child.tag.split('}')[-1]
            text = "".join(child.itertext()).strip()
            if tag == "tbl":
                print(f"  [Elem {idx}] <TABLE>: {text[:60]}")
            elif tag == "p" and len(text) > 0:
                if any(text.startswith(h) for h in ["V.", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12.", "VI."]):
                    print(f"  [Elem {idx}] <p>: {text[:80]}")

if __name__ == "__main__":
    inspect_all_occurrences("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx")

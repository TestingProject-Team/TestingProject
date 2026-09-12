# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_all_body_elements_chap5(file_path):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    in_chap5 = False
    print(f"=== Traversing XML Children of Body for Chapter V ===")
    
    count = 0
    for idx, child in enumerate(body):
        tag = child.tag.split('}')[-1]
        text = "".join(child.itertext()).strip()
        
        if "V. Tài liệu kiểm thử" in text or "V. TÀI LIỆU KIỂM THỬ" in text:
            in_chap5 = True
            print(f"\n[START CHAP 5 at Body Element {idx}] <{tag}>: {text[:80]}")
        elif in_chap5 and ("VI. Gói phát hành" in text or "VI. GÓI PHÁT HÀNH" in text or "VI. TRIỂN KHAI" in text or text.startswith("VI.")):
            in_chap5 = False
            print(f"\n[END CHAP 5 at Body Element {idx}] <{tag}>: {text[:80]}")
            break
            
        if in_chap5:
            if tag == "tbl":
                print(f"  [Elem {idx}] <TABLE>: {text[:70]}...")
            elif any(text.startswith(h) for h in ["5.", "6.", "7.", "8.", "9.", "10.", "11.", "1.", "2.", "3.", "4."]):
                print(f"  [Elem {idx}] <{tag}>: {text[:80]}")

if __name__ == "__main__":
    inspect_all_body_elements_chap5("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx")

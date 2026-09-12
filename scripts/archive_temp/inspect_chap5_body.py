# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_all_chap5_body(file_path):
    doc = docx.Document(file_path)
    print("=== Scanning for Body Chapter V Headings ===")
    
    in_chap5_body = False
    for p_idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if not text:
            continue
        # Check if we reached Chapter V in body (after TOC)
        if p_idx > 60 and ("V. TÀI LIỆU KIỂM THỬ PHẦN MỀM" in text.upper() or "V. BÁO CÁO KIỂM THỬ" in text.upper() or text.startswith("V. ")):
            in_chap5_body = True
            print(f"\n---> BODY START CHAP 5 at [P{p_idx}]: {text}")
        elif in_chap5_body and (text.startswith("VI. ") or "VI. GÓI PHÁT HÀNH" in text.upper() or "VI. TRIỂN KHAI" in text.upper()):
            in_chap5_body = False
            print(f"\n---> BODY END CHAP 5 at [P{p_idx}]: {text}")
            break
            
        if in_chap5_body:
            if p.style.name.startswith("Heading") or any(text.startswith(k) for k in ["5.", "6.", "7.", "8.", "9.", "10.", "11.", "1.", "2.", "3.", "4."]):
                print(f"  [P{p_idx}] (Style: {p.style.name}): {text[:90]}")

if __name__ == "__main__":
    inspect_all_chap5_body("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx")

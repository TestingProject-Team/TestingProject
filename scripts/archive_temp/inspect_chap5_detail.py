# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_chap5_structure(file_path):
    doc = docx.Document(file_path)
    in_chap5 = False
    print(f"=== Inspecting Headings & Structure in {file_path} ===")
    
    # We will inspect paragraphs in body
    for p_idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if not text:
            continue
        if "V. BÁO CÁO KIỂM THỬ" in text or "V. TÀI LIỆU KIỂM THỬ" in text or "V. KẾT QUẢ KIỂM THỬ" in text or text.startswith("V."):
            in_chap5 = True
            print(f"\n---> START CHAP 5 at [P{p_idx}]: {text}")
        elif in_chap5 and (text.startswith("VI.") or "VI. HƯỚNG DẪN" in text or "VI. TRIỂN KHAI" in text):
            in_chap5 = False
            print(f"\n---> END CHAP 5 at [P{p_idx}]: {text}")
            break
            
        if in_chap5:
            if p.style.name.startswith("Heading") or any(text.startswith(prefix) for prefix in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "5.1", "5.2", "5.3", "6.1", "6.2", "6.3", "7.1", "7.2", "7.3", "8.1", "8.2", "8.3", "9.1"]):
                print(f"  [P{p_idx}] (Style: {p.style.name}): {text[:90]}")

if __name__ == "__main__":
    inspect_chap5_structure("YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx")

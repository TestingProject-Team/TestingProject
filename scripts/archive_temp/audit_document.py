# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def detailed_chap5_audit(file_path):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    print(f"Auditing file: {file_path}")
    print(f"Total elements: {len(body)}")
    
    start_v = False
    in_v = False
    count_p = 0
    count_t = 0
    
    for idx, child in enumerate(body):
        text = "".join(child.itertext()).strip()
        tag = child.tag.split('}')[-1]
        
        if "V. Tài liệu kiểm thử phần mềm" in text and idx > 200:
            in_v = True
            print(f"--> Found Chapter V at element {idx}")
            
        if in_v:
            if "VI. Kết luận" in text and idx > 600:
                print(f"--> Reached Chapter VI at element {idx}")
                in_v = False
                break
                
            if tag == "p":
                count_p += 1
                if text.startswith("Hình 5."):
                    print(f"  [Figure] {text}")
            elif tag == "tbl":
                count_t += 1
                if "[CẦN BỔ SUNG EVIDENCE:" in text:
                    print(f"  [Placeholder Box] {text[:90]}...")
                elif any(h in text for h in ["Lớp kiểm thử", "Nhóm Module", "Bộ kịch bản", "Hạng mục kiểm thử"]):
                    print(f"  [Original Test Table] {text[:60]}...")
                    
    print(f"\nChapter V Summary: {count_p} paragraphs, {count_t} tables.")

if __name__ == "__main__":
    detailed_chap5_audit("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx")

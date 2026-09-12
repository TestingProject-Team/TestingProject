# -*- coding: utf-8 -*-
import docx
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_full_structure(file_path):
    doc = docx.Document(file_path)
    body = doc._body._body
    
    with open("structure_full_dump.txt", "w", encoding="utf-8") as f:
        for idx, child in enumerate(body):
            tag = child.tag.split('}')[-1]
            text = "".join(child.itertext()).strip()
            if tag == "tbl":
                f.write(f"[Elem {idx:04d}] <TABLE> (rows={len(child.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr'))}) : {text[:100]}\n")
            elif tag == "p":
                # print heading-like or caption-like or placeholder-like paragraphs
                if len(text) > 0:
                    if any(text.startswith(h) for h in ["I.", "II.", "III.", "IV.", "V.", "VI.", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "Hình", "[CẦN BỔ SUNG"]):
                        f.write(f"[Elem {idx:04d}] <P> : {text[:100]}\n")

    print("Structure written to structure_full_dump.txt")

if __name__ == "__main__":
    inspect_full_structure("YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx")

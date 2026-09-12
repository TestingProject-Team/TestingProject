# -*- coding: utf-8 -*-
import os
import zipfile
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

files = [
    "YiYi_Book_Capstone_Project_Report_Tieng_Viet (1)_BACKUP.docx",
    "YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx"
]

for name in files:
    if os.path.exists(name):
        size = os.path.getsize(name)
        with zipfile.ZipFile(name, 'r') as z:
            doc_xml_size = z.getinfo('word/document.xml').file_size
            media_files = [f.filename for f in z.infolist() if 'media/' in f.filename]
            total_compressed = sum(f.compress_size for f in z.infolist())
        print(f"File: {name}")
        print(f"  Total Zip Size: {size:,} bytes")
        print(f"  word/document.xml size: {doc_xml_size:,} bytes")
        print(f"  Number of media/images: {len(media_files)}")
    else:
        print(f"File not found: {name}")

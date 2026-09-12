# -*- coding: utf-8 -*-
import os
import shutil
import time

SRC = "YiYi_Book_Capstone_Project_Report_Tieng_Viet_Updated.docx"
DST = "YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx"

print("Attempting to overwrite original file...")
for attempt in range(5):
    try:
        shutil.copy2(SRC, DST)
        print("SUCCESS: Successfully copied updated report to original file name!")
        break
    except PermissionError:
        print(f"Attempt {attempt+1}: File is still open in Microsoft Word. Retrying in 1s...")
        time.sleep(1)

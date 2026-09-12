# -*- coding: utf-8 -*-
import os
import shutil

def sync_to_final():
    src = "YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx.tmp.docx"
    dst = "YiYi_Book_Capstone_Project_Report_Tieng_Viet_Final_Refined.docx"
    dst_orig = "YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx"
    
    # 1. Update dst_orig with tmp
    shutil.copy2(src, dst_orig)
    print(f"Updated {dst_orig} successfully with the 12 placeholders!")
    
    # 2. Try copying to dst
    try:
        shutil.copy2(src, dst)
        print(f"Updated {dst} successfully!")
        os.remove(src)
    except Exception as e:
        print(f"Notice: {dst} is currently open in Word. Once you close it, you can overwrite it or use {dst_orig}.")

if __name__ == "__main__":
    sync_to_final()

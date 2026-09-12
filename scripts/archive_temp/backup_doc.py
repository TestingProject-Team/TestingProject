import shutil
import os

src = "YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx"
dst = "YiYi_Book_Capstone_Project_Report_Tieng_Viet (1)_BACKUP.docx"
shutil.copyfile(src, dst)
print(f"Backed up {src} to {dst}")

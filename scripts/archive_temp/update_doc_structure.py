# -*- coding: utf-8 -*-
"""
Script tái cấu trúc và bổ sung khung sườn chi tiết cho YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx
Chuẩn hóa theo format bài mẫu PDCMS và khớp 100% mã nguồn thực tế của YiYi Book.
Chưa chèn hình ảnh, chỉ chuẩn hóa nội dung, bảng biểu, mục lục và khung thiết kế/kiểm thử.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

DOCX_FILE = "YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx"
doc = docx.Document(DOCX_FILE)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

print("Document loaded. Total paragraphs:", len(doc.paragraphs))

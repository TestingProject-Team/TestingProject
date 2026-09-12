# -*- coding: utf-8 -*-
with open("scripts/refine_all_chapters_placeholders.py", "r", encoding="utf-8") as f:
    code = f.read()

# Thay thế hàm set_p_text và make_caption_p và make_heading_p để luôn escape xml
target_old = """def set_p_text(p_elem, text):
    \"\"\"Xóa các run cũ và thêm text mới cho một CT_P xml element.\"\"\"
    # Xóa toàn bộ child <w:r>
    for r in p_elem.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
        p_elem.remove(r)
    # Tạo run mới
    r_elem = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:b/><w:i/>'
        f'<w:sz w:val="20"/>'
        f'<w:color w:val="1E293B"/>'
        f'</w:rPr>'
        f'<w:t>{text}</w:t>'
        f'</w:r>'
    )
    p_elem.append(r_elem)"""

target_new = """def escape_xml(text):
    return str(text).replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace("'", ''')

def set_p_text(p_elem, text):
    \"\"\"Xóa các run cũ và thêm text mới cho một CT_P xml element.\"\"\"
    for r in p_elem.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
        p_elem.remove(r)
    esc_text = escape_xml(text)
    r_elem = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:b/><w:i/>'
        f'<w:sz w:val="20"/>'
        f'<w:color w:val="1E293B"/>'
        f'</w:rPr>'
        f'<w:t>{esc_text}</w:t>'
        f'</w:r>'
    )
    p_elem.append(r_elem)"""

code = code.replace(target_old, target_new)

# Cũng cập nhật make_caption_p và make_heading_p
code = code.replace("f'<w:t>{caption_text}</w:t>'", "f'<w:t>{escape_xml(caption_text)}</w:t>'")
code = code.replace("f'<w:t>{text}</w:t>'", "f'<w:t>{escape_xml(text)}</w:t>'")

with open("scripts/refine_all_chapters_placeholders.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated scripts/refine_all_chapters_placeholders.py successfully!")

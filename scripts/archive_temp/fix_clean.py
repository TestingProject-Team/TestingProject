# -*- coding: utf-8 -*-
from xml.sax.saxutils import escape

with open("scripts/refine_all_chapters_placeholders.py", "rb") as f:
    content = f.read().decode('utf-8', errors='ignore')

# Thay vì tự replace chuỗi, ta dùng hàm escape từ thư viện chuẩn xml.sax.saxutils
old_block = """def escape_xml(text):
    return str(text).replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace("'", ''')"""

# Tìm đoạn def escape_xml và thay thế
lines = content.splitlines()
new_lines = ["from xml.sax.saxutils import escape as escape_xml"]
skip = False
for line in lines:
    if line.startswith("def escape_xml"):
        skip = True
        continue
    if skip:
        if line.startswith("def set_p_text"):
            skip = False
            new_lines.append(line)
        continue
    new_lines.append(line)

with open("scripts/refine_all_chapters_placeholders.py", "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("Applied xml.sax.saxutils escape cleanly!")

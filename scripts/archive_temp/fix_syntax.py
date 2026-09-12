# -*- coding: utf-8 -*-
with open("scripts/refine_all_chapters_placeholders.py", "rb") as f:
    raw = f.read().decode('utf-8', errors='ignore')

# Sửa hàm escape_xml chuẩn xác
lines = raw.split('\n')
new_lines = []
for line in lines:
    if line.startswith("def escape_xml(text):"):
        new_lines.append("def escape_xml(text):")
        new_lines.append("    t = str(text)")
        new_lines.append("    t = t.replace('&', '&')")
        new_lines.append("    t = t.replace('<', '<')")
        new_lines.append("    t = t.replace('>', '>')")
        new_lines.append("    t = t.replace('\"', '"')")
        new_lines.append("    t = t.replace(\"'\", ''')")
        new_lines.append("    return t")
    elif "return str(text).replace" in line:
        continue
    else:
        new_lines.append(line)

with open("scripts/refine_all_chapters_placeholders.py", "w", encoding="utf-8") as f:
    f.write('\n'.join(new_lines))

print("Fixed refine_all_chapters_placeholders.py successfully!")

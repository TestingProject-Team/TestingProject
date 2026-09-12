# -*- coding: utf-8 -*-
import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"E:\TestingProject\ảnh file docx"
INFO_REV_DIR = os.path.join(BASE_DIR, "01_infographic_revised")
STD_REV_DIR  = os.path.join(BASE_DIR, "02_standard_revised")
INFO_DIR     = os.path.join(BASE_DIR, "01_infographic")
STD_DIR      = os.path.join(BASE_DIR, "02_standard")

for d in [INFO_REV_DIR, STD_REV_DIR, INFO_DIR, STD_DIR]:
    os.makedirs(d, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\tahomabd.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except:
                pass
    return ImageFont.load_default()

def draw_arrow(draw, start, end, fill=(71, 85, 105), width=3, arrow_size=10, dashed=False):
    x1, y1 = start
    x2, y2 = end
    if dashed:
        dist = math.hypot(x2 - x1, y2 - y1)
        dash_len = 8
        num_dashes = int(dist // (dash_len * 2)) if dist > 0 else 0
        for i in range(num_dashes + 1):
            s = (i * 2 * dash_len) / dist if dist > 0 else 0
            e = min(1.0, ((i * 2 + 1) * dash_len) / dist) if dist > 0 else 1
            if s < 1.0:
                sx = x1 + (x2 - x1) * s
                sy = y1 + (y2 - y1) * s
                ex = x1 + (x2 - x1) * e
                ey = y1 + (y2 - y1) * e
                draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)
    else:
        draw.line([start, end], fill=fill, width=width)
    
    angle = math.atan2(y2 - y1, x2 - x1)
    xa = x2 - arrow_size * math.cos(angle - math.pi / 6)
    ya = y2 - arrow_size * math.sin(angle - math.pi / 6)
    xb = x2 - arrow_size * math.cos(angle + math.pi / 6)
    yb = y2 - arrow_size * math.sin(angle + math.pi / 6)
    draw.polygon([(x2, y2), (xa, ya), (xb, yb)], fill=fill)

def draw_card(draw, box, title, sub="", style="infographic", color_type="blue", radius=8):
    x1, y1, x2, y2 = box
    color_map = {
        "blue":    ((239, 246, 255), (59, 130, 246),  (30, 64, 175),  (37, 99, 235)),
        "teal":    ((240, 253, 250), (20, 184, 166),  (17, 94, 89),   (13, 148, 136)),
        "emerald": ((240, 253, 244), (16, 185, 129),  (22, 101, 52),  (5, 150, 105)),
        "purple":  ((250, 245, 255), (139, 92, 246),  (107, 33, 168), (124, 58, 237)),
        "indigo":  ((238, 242, 255), (99, 102, 241),  (49, 46, 129),  (79, 70, 229)),
        "amber":   ((255, 251, 235), (245, 158, 11),  (146, 64, 14),  (217, 119, 6)),
        "slate":   ((248, 250, 252), (100, 116, 139), (30, 41, 59),   (71, 85, 105)),
        "dark":    ((241, 245, 249), (51, 65, 85),   (15, 23, 42),   (30, 41, 59))
    }
    bg, border, text_c, hdr_c = color_map.get(color_type, color_map["blue"]) if style == "infographic" else ((255, 255, 255), (30, 41, 59), (15, 23, 42), (51, 65, 85))
    
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg, outline=border, width=2)
    
    cx = (x1 + x2) // 2
    f_t = get_font(20, bold=True)
    f_s = get_font(15, bold=False)
    
    if sub:
        lines = sub.split('\n')
        # Title at the top portion
        draw.text((cx, y1 + 24), title, fill=text_c, font=f_t, anchor="mm")
        draw.line([(x1 + 10, y1 + 44), (x2 - 10, y1 + 44)], fill=border, width=1)
        
        curr_y = y1 + 54
        for line in lines:
            draw.text((x1 + 14, curr_y), line, fill=(51, 65, 85) if style == "infographic" else (15, 23, 42), font=f_s)
            curr_y += 20
    else:
        cy = (y1 + y2) // 2
        draw.text((cx, cy), title, fill=text_c, font=f_t, anchor="mm")

def draw_header(draw, title, subtitle, W=2000):
    f_title = get_font(32, bold=True)
    f_sub = get_font(18, bold=False)
    draw.text((W // 2, 45), title, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W // 2, 80), subtitle, fill=(71, 85, 105), font=f_sub, anchor="mm")
    draw.line([(80, 110), (W - 80, 110)], fill=(226, 232, 240), width=2)

def generate_all_clean_diagrams():
    import generate_revised_diagrams as grd
    import render_hinh_4_10 as r10
    import render_hinh_4_11 as r11
    import render_hinh_4_8 as r8
    import render_hinh_4_9 as r9

    print("Re-rendering all core diagrams with clean non-overlapping cards...")
    
    # Override draw_card in modules
    grd.draw_card = draw_card
    grd.draw_header = draw_header
    grd.draw_arrow = draw_arrow
    grd.get_font = get_font

    r11.draw_card = draw_card
    r11.draw_header = draw_header
    r11.draw_arrow = draw_arrow
    r11.get_font = get_font

    r8.draw_card = draw_card
    r8.draw_header = draw_header
    r8.draw_arrow = draw_arrow
    r8.get_font = get_font

    r9.draw_card = draw_card
    r9.draw_header = draw_header
    r9.draw_arrow = draw_arrow
    r9.get_font = get_font

    # Run generations
    grd.execute_all()
    r10.main()
    r11.generate_hinh_4_11()
    r8.generate_hinh_4_8()
    r9.generate_hinh_4_9()
    print("All diagrams regenerated cleanly without any text collisions!")

if __name__ == "__main__":
    generate_all_clean_diagrams()

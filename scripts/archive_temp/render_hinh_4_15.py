import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"E:\TestingProject\ảnh file docx"
INFO_REV_DIR = os.path.join(BASE_DIR, "01_infographic_revised")
STD_REV_DIR = os.path.join(BASE_DIR, "02_standard_revised")

os.makedirs(INFO_REV_DIR, exist_ok=True)
os.makedirs(STD_REV_DIR, exist_ok=True)

def get_font(size, bold=False):
    candidates = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\tahomabd.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf",
    ]
    for fn in candidates:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except:
                pass
    return ImageFont.load_default()

def draw_arrow(draw, start, end, fill=(51, 65, 85), width=3, arrow_size=12, dashed=False):
    x1, y1 = start
    x2, y2 = end
    if dashed:
        dist = math.hypot(x2 - x1, y2 - y1)
        dash_len = 10
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

def draw_card(draw, box, title, sub="", style="infographic", color_type="blue", radius=10):
    x1, y1, x2, y2 = box
    if style == "infographic":
        color_map = {
            "blue": ((239, 246, 255), (59, 130, 246), (30, 64, 175)),
            "teal": ((240, 253, 250), (20, 184, 166), (17, 94, 89)),
            "emerald": ((240, 253, 244), (16, 185, 129), (22, 101, 52)),
            "purple": ((250, 245, 255), (139, 92, 246), (107, 33, 168)),
            "amber": ((255, 251, 235), (245, 158, 11), (146, 64, 14)),
            "slate": ((248, 250, 252), (100, 116, 139), (30, 41, 59)),
            "dark": ((241, 245, 249), (51, 65, 85), (15, 23, 42))
        }
        bg, border, text_c = color_map.get(color_type, color_map["blue"])
    else:
        bg = (255, 255, 255)
        border = (30, 41, 59)
        text_c = (15, 23, 42)

    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg, outline=border, width=2)
    f_t = get_font(25, bold=True)
    f_s = get_font(20, bold=False)

    cx = (x1 + x2) // 2
    if sub:
        cy = (y1 + y2) // 2
        draw.text((cx, cy - 14), title, fill=text_c, font=f_t, anchor="mm")
        draw.text((cx, cy + 18), sub, fill=(71, 85, 105) if style == "infographic" else (51, 65, 85), font=f_s, anchor="mm")
    else:
        cy = (y1 + y2) // 2
        draw.text((cx, cy), title, fill=text_c, font=f_t, anchor="mm")

def draw_header(draw, title, subtitle, W=2000):
    f_title = get_font(38, bold=True)
    f_sub = get_font(22, bold=False)
    draw.text((W // 2, 50), title, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W // 2, 90), subtitle, fill=(71, 85, 105), font=f_sub, anchor="mm")
    draw.line([(80, 120), (W - 80, 120)], fill=(226, 232, 240), width=2)

def render_hinh_4_15_reward_seq(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ TÍCH LŨY VÀ TIÊU ĐIỂM THƯỞNG Y-POINT", "Quy trình đổi voucher, trừ điểm thưởng an toàn và ghi nhận lịch sử giao dịch", W)

    # Lifelines: Member | Reward UI | RewardController | RewardService | PointTransaction Repo | PostgreSQL DB
    actors = [
        (180, "Member"),
        (480, "Reward UI (React)"),
        (820, "RewardController"),
        (1160, "RewardService"),
        (1500, "Transaction Repo"),
        (1820, "PostgreSQL DB")
    ]

    for x, name in actors:
        draw_card(draw, [x - 130, 170, x + 130, 240], name, "", style, "amber" if "Member" in name or "React" in name else "emerald")
        draw.line([(x, 240), (x, 1140)], fill=(148, 163, 184), width=2)

    # Messages
    msgs = [
        (180, 480, "1. Chọn quà tặng / Đổi điểm Y-Points", 300),
        (480, 820, "2. POST /api/rewards/exchange {points, type}", 400),
        (820, 1160, "3. exchangePoints(username, points, type)", 500),
        (1160, 1160, "4. Kiểm tra số dư Y-Points >= pointsToSpend", 590),
        (1160, 1500, "5. Sinh mã Coupon mới & Trừ điểm User", 680),
        (1500, 1820, "6. INSERT INTO coupons, point_transactions", 780),
        (1820, 1500, "7. Giao dịch nguyên tử ACID thành công", 880, True),
        (1500, 1160, "8. Trả về PointTransaction Entity", 960, True),
        (1160, 820, "9. Cập nhật số dư Y-Points mới", 1030, True),
        (820, 480, "10. HTTP 200 OK (Đổi quà thành công)", 1090, True),
        (480, 180, "11. Hiển thị Voucher trong Kho & Cập nhật điểm", 1140, True)
    ]

    f_msg = get_font(21, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        
        # Self call check
        if x_from == x_to:
            draw.arc([x_from - 30, y - 25, x_from + 60, y + 25], 270, 90, fill=(30, 41, 59), width=3)
            draw_arrow(draw, (x_from + 15, y + 25), (x_from, y + 25), fill=(30, 41, 59), width=3, arrow_size=10)
            draw.text((x_from + 70, y), text, fill=(15, 23, 42), font=f_msg, anchor="lm")
        else:
            draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
            mid_x = (x_from + x_to) // 2
            draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

def generate_hinh_4_15():
    # 1. Render Infographic Revised
    img_info = Image.new("RGB", (2000, 1300), (255, 255, 255))
    draw_info = ImageDraw.Draw(img_info)
    render_hinh_4_15_reward_seq(draw_info, style="infographic")
    p_info = os.path.join(INFO_REV_DIR, "Hinh_4.15_Sequence_Diagram_Reward_Points.png")
    img_info.save(p_info, dpi=(300, 300))

    # 2. Render Standard Revised
    img_std = Image.new("RGB", (2000, 1300), (255, 255, 255))
    draw_std = ImageDraw.Draw(img_std)
    render_hinh_4_15_reward_seq(draw_std, style="standard")
    p_std = os.path.join(STD_REV_DIR, "Hinh_4.15_Sequence_Diagram_Reward_Points.png")
    img_std.save(p_std, dpi=(300, 300))

    # SVG stubs
    svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1300" width="2000" height="1300">\n  <rect width="100%" height="100%" fill="#ffffff"/>\n  <!-- Vector source for Hinh_4.15_Sequence_Diagram_Reward_Points -->\n</svg>'
    with open(os.path.join(INFO_REV_DIR, "Hinh_4.15_Sequence_Diagram_Reward_Points.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)
    with open(os.path.join(STD_REV_DIR, "Hinh_4.15_Sequence_Diagram_Reward_Points.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)

    print("Generated Hinh 4.15 in both revised directories successfully!")

if __name__ == "__main__":
    generate_hinh_4_15()

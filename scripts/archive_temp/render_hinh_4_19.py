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
            "blue":    ((239, 246, 255), (59, 130, 246), (30, 64, 175)),
            "teal":    ((240, 253, 250), (20, 184, 166), (17, 94, 89)),
            "emerald": ((240, 253, 244), (16, 185, 129), (22, 101, 52)),
            "purple":  ((250, 245, 255), (139, 92, 246), (107, 33, 168)),
            "amber":   ((255, 251, 235), (245, 158, 11), (146, 64, 14)),
            "slate":   ((248, 250, 252), (100, 116, 139), (30, 41, 59)),
            "dark":    ((241, 245, 249), (51, 65, 85), (15, 23, 42))
        }
        bg, border, text_c = color_map.get(color_type, color_map["blue"])
    else:
        bg, border, text_c = (255, 255, 255), (30, 41, 59), (15, 23, 42)

    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg, outline=border, width=2)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    if sub:
        draw.text((cx, cy - 14), title, fill=text_c, font=get_font(25, True), anchor="mm")
        draw.text((cx, cy + 18), sub, fill=(71, 85, 105) if style == "infographic" else (51, 65, 85), font=get_font(20), anchor="mm")
    else:
        draw.text((cx, cy), title, fill=text_c, font=get_font(25, True), anchor="mm")

def draw_header(draw, title, subtitle, W=2000):
    draw.text((W // 2, 50), title, fill=(15, 23, 42), font=get_font(38, True), anchor="mm")
    draw.text((W // 2, 90), subtitle, fill=(71, 85, 105), font=get_font(22), anchor="mm")
    draw.line([(80, 120), (W - 80, 120)], fill=(226, 232, 240), width=2)

def render_hinh_4_19(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ QUẢN TRỊ KHUYẾN MÃI & NỘI DUNG (ADMIN)", "Quy trình tạo mã Coupon, cấu hình Banner và kiểm duyệt Đánh giá của khách hàng", W)

    # Lifelines:
    # Administrator | Admin UI | Coupon/Banner/Review Controller | Coupon/Banner/Review Service | PostgreSQL DB
    actors = [
        (160,  "Administrator"),
        (460,  "Admin UI (React)"),
        (840,  "Coupon Controller"),
        (1160, "Coupon Service"),
        (1480, "Banner/Review Ctrl"),
        (1820, "PostgreSQL DB")
    ]

    for x, name in actors:
        color = "purple" if "Admin" in name or "React" in name else "teal" if "Banner" in name else "emerald"
        draw_card(draw, [x - 130, 170, x + 130, 240], name, "", style, color)
        draw.line([(x, 240), (x, 1150)], fill=(148, 163, 184), width=2)

    f_msg = get_font(21, bold=True)
    f_sep = get_font(19, bold=True)

    # --- COUPON section ---
    # Separator label
    draw.rounded_rectangle([80, 270, 920, 310], radius=6,
                            fill=(239, 246, 255) if style == "infographic" else (240, 240, 240),
                            outline=(59, 130, 246), width=2)
    draw.text((500, 290), "A. Tạo / Cập nhật Mã Giảm Giá (Coupon)", fill=(30, 64, 175), font=f_sep, anchor="mm")

    coupon_msgs = [
        (160, 460, "1. Nhập mã, tỷ lệ chiết khấu & ngày hết hạn", 340),
        (460, 840, "2. POST /api/coupons  {code, type, value, expiry}", 420),
        (840, 1160, "3. createCoupon(coupon)", 500),
        (1160, 1820, "4. couponRepository.save(coupon)", 580),
        (1820, 460, "5. HTTP 200 OK — Mã Coupon đã tạo", 650, True),
    ]
    for m in coupon_msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

    # --- BANNER section ---
    draw.rounded_rectangle([80, 700, 920, 740], radius=6,
                            fill=(240, 253, 250) if style == "infographic" else (240, 240, 240),
                            outline=(20, 184, 166), width=2)
    draw.text((500, 720), "B. Cấu hình Banner Quảng cáo", fill=(17, 94, 89), font=f_sep, anchor="mm")

    banner_msgs = [
        (160, 460, "6. Tải ảnh Banner & Nhập liên kết chiến dịch", 770),
        (460, 1480, "7. POST /api/banners  {imageUrl, linkUrl, position}", 840),
        (1480, 1820, "8. bannerRepository.save(banner)", 910),
        (1820, 460, "9. HTTP 200 OK — Banner đã đăng", 970, True),
    ]
    for m in banner_msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

    # --- REVIEW MODERATION section ---
    draw.rounded_rectangle([80, 1010, 1200, 1050], radius=6,
                            fill=(250, 245, 255) if style == "infographic" else (240, 240, 240),
                            outline=(139, 92, 246), width=2)
    draw.text((640, 1030), "C. Kiểm duyệt Đánh giá Khách hàng", fill=(107, 33, 168), font=f_sep, anchor="mm")

    review_msgs = [
        (160, 1480, "10. DELETE /api/admin/reviews/{id} (Vi phạm)", 1080),
        (1480, 1820, "11. reviewRepository.deleteById(id)", 1140),
        (1820, 160, "12. HTTP 200 OK — Đánh giá đã xoá", 1190, True),
    ]
    for m in review_msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

def generate():
    for style, out_dir in [("infographic", INFO_REV_DIR), ("standard", STD_REV_DIR)]:
        img = Image.new("RGB", (2000, 1250), (255, 255, 255))
        d = ImageDraw.Draw(img)
        render_hinh_4_19(d, style=style)
        fname = "Hinh_4.19_Sequence_Diagram_Admin_Promotion_Content.png"
        img.save(os.path.join(out_dir, fname), dpi=(300, 300))
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1250" width="2000" height="1250">\n  <rect width="100%" height="100%" fill="#ffffff"/>\n</svg>'
        with open(os.path.join(out_dir, "Hinh_4.19_Sequence_Diagram_Admin_Promotion_Content.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    print("Generated Hinh 4.19 in both revised directories successfully!")

if __name__ == "__main__":
    generate()

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

def render_hinh_4_18(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ XỬ LÝ VÀ CẬP NHẬT ĐƠN HÀNG (ADMIN)", "Quy trình Admin duyệt đơn, cập nhật trạng thái vận chuyển và tích điểm cho khách hàng", W)

    # Lifelines:
    # Administrator | Admin UI | OrderController | OrderService | OrderRepository | NotificationService
    actors = [
        (160,  "Administrator"),
        (460,  "Admin UI (React)"),
        (800,  "OrderController"),
        (1140, "OrderService"),
        (1480, "OrderRepository"),
        (1840, "Notification / DB")
    ]

    for x, name in actors:
        color = "purple" if "Admin" in name else "amber" if "Order" in name else "teal"
        draw_card(draw, [x - 130, 170, x + 130, 240], name, "", style, color)
        draw.line([(x, 240), (x, 1150)], fill=(148, 163, 184), width=2)

    msgs = [
        # (x_from, x_to, label, y, dashed?)
        (160,  460,  "1. Mở danh sách đơn hàng chờ xử lý", 310),
        (460,  800,  "2. GET /api/orders/all  (Role ADMIN)", 400),
        (800,  1140, "3. getAllOrders()", 490),
        (1140, 1480, "4. findAllByOrderByCreatedAtDesc()", 580),
        (1480, 1140, "5. Trả về List<Order>", 660, True),
        (1140, 800,  "6. Order DTO list", 720, True),
        (800,  460,  "7. HTTP 200 OK (Danh sách đơn)", 780, True),
        (460,  800,  "8. PUT /api/orders/{id}/shipping  {status, partner, tracking}", 860),
        (800,  1140, "9. updateOrderShipping(id, status, partner, tracking)", 950),
        (1140, 1480, "10. orderRepository.save(order)", 1030),
        (1480, 1840, "11. UPDATE orders SET status, shipping_status", 1090),
        (1840, 460,  "12. HTTP 200 OK — Đơn chuyển sang PROCESSING / SHIPPING", 1140, True),
    ]

    f_msg = get_font(21, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

def generate():
    for style, out_dir in [("infographic", INFO_REV_DIR), ("standard", STD_REV_DIR)]:
        img = Image.new("RGB", (2000, 1300), (255, 255, 255))
        d = ImageDraw.Draw(img)
        render_hinh_4_18(d, style=style)
        fname = "Hinh_4.18_Sequence_Diagram_Admin_Order.png"
        img.save(os.path.join(out_dir, fname), dpi=(300, 300))
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1300" width="2000" height="1300">\n  <rect width="100%" height="100%" fill="#ffffff"/>\n  <!-- Vector source for Hinh_4.18_Sequence_Diagram_Admin_Order -->\n</svg>'
        with open(os.path.join(out_dir, "Hinh_4.18_Sequence_Diagram_Admin_Order.svg"), "w", encoding="utf-8") as f:
            f.write(svg)

    print("Generated Hinh 4.18 in both revised directories successfully!")

if __name__ == "__main__":
    generate()

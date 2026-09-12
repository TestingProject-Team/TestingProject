import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

INFO_DIR = r"E:\TestingProject\ảnh file docx\01_infographic"
STD_DIR = r"E:\TestingProject\ảnh file docx\02_standard"
os.makedirs(INFO_DIR, exist_ok=True)
os.makedirs(STD_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\tahomabd.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except:
                pass
    return ImageFont.load_default()

def draw_arrow(draw, start, end, fill=(71, 85, 105), width=2, arrow_size=8, dashed=False):
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

def render_hinh_4_6():
    # 21 Tables in PostgreSQL, 4 Enums
    W, H = 2400, 1600
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(34, bold=True)
    f_sub = get_font(18, bold=False)
    f_tbl = get_font(16, bold=True)
    f_fld = get_font(13, bold=False)
    f_pk = get_font(13, bold=True)
    f_body = get_font(14, bold=False)

    draw.text((W//2, 45), "SƠ ĐỒ THỰC THỂ QUAN HỆ CƠ SỞ DỮ LIỆU (ERD) — YIYI BOOK DATABASE", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 80), "PostgreSQL 16 Schema: 21 Thực thể nghiệp vụ, 4 Kiểu Enum, Khóa chính UUID/Long và Toàn vẹn tham chiếu", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # 21 Tables structured in 5 Columns across 4 Rows
    # Table layout: (x, y, w, h, table_name, [(col, type, is_pk/fk)], color_theme)
    tables = [
        # Col 1: Users & Auth
        (80, 120, 400, 290, "users", [
            ("id", "BIGSERIAL", "PK"),
            ("username", "VARCHAR(50)", "UK"),
            ("password", "VARCHAR(255)", ""),
            ("full_name", "VARCHAR(100)", ""),
            ("email", "VARCHAR(100)", "UK"),
            ("phone", "VARCHAR(20)", ""),
            ("role", "ENUM('USER','ADMIN')", ""),
            ("auth_provider", "ENUM('LOCAL','GOOGLE')", ""),
            ("y_points", "INTEGER", ""),
            ("total_spent", "DOUBLE PRECISION", "")
        ], (2, 132, 199)),

        (80, 440, 400, 200, "addresses", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("recipient_name", "VARCHAR(100)", ""),
            ("phone", "VARCHAR(20)", ""),
            ("street, ward, city", "VARCHAR(255)", "")
        ], (2, 132, 199)),

        (80, 670, 400, 210, "vat_invoices", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK (1-1)"),
            ("company_name", "VARCHAR(255)", ""),
            ("tax_code", "VARCHAR(50)", ""),
            ("company_address", "VARCHAR(255)", "")
        ], (2, 132, 199)),

        (80, 910, 400, 260, "point_transactions", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("action", "VARCHAR(50)", ""),
            ("transaction_value", "INTEGER", ""),
            ("previous_balance", "INTEGER", ""),
            ("new_balance", "INTEGER", ""),
            ("created_at", "TIMESTAMP", "")
        ], (126, 34, 206)),

        (80, 1200, 400, 280, "notifications", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("title", "VARCHAR(255)", ""),
            ("content", "TEXT", ""),
            ("type", "VARCHAR(50)", ""),
            ("is_read", "BOOLEAN", ""),
            ("created_at", "TIMESTAMP", "")
        ], (126, 34, 206)),

        # Col 2: Catalogue & Books
        (520, 120, 420, 200, "categories", [
            ("id", "BIGSERIAL", "PK"),
            ("name", "VARCHAR(100)", "UK"),
            ("description", "TEXT", ""),
            ("image_url", "VARCHAR(255)", "")
        ], (5, 150, 105)),

        (520, 350, 420, 350, "books", [
            ("id", "BIGSERIAL", "PK"),
            ("category_id", "BIGINT", "FK"),
            ("title", "VARCHAR(255)", "INDEX"),
            ("author", "VARCHAR(255)", ""),
            ("publisher", "VARCHAR(100)", ""),
            ("price", "DOUBLE PRECISION", ""),
            ("old_price", "DOUBLE PRECISION", ""),
            ("stock_quantity", "INTEGER", ""),
            ("image_url", "VARCHAR(500)", ""),
            ("description", "TEXT", "")
        ], (5, 150, 105)),

        (520, 730, 420, 210, "wishlists", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("book_id", "BIGINT", "FK"),
            ("created_at", "TIMESTAMP", "")
        ], (5, 150, 105)),

        (520, 970, 420, 260, "reviews", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("book_id", "BIGINT", "FK"),
            ("rating", "INTEGER", ""),
            ("comment", "TEXT", ""),
            ("created_at", "TIMESTAMP", "")
        ], (217, 119, 6)),

        (520, 1260, 420, 220, "review_comments", [
            ("id", "BIGSERIAL", "PK"),
            ("review_id", "BIGINT", "FK"),
            ("user_id", "BIGINT", "FK"),
            ("content", "TEXT", ""),
            ("created_at", "TIMESTAMP", "")
        ], (217, 119, 6)),

        # Col 3: Cart & Orders
        (980, 120, 440, 170, "carts", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK (1-1)"),
            ("updated_at", "TIMESTAMP", "")
        ], (37, 99, 235)),

        (980, 320, 440, 210, "cart_items", [
            ("id", "BIGSERIAL", "PK"),
            ("cart_id", "BIGINT", "FK"),
            ("book_id", "BIGINT", "FK"),
            ("quantity", "INTEGER", "")
        ], (37, 99, 235)),

        (980, 560, 440, 440, "orders", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("total_amount", "DOUBLE PRECISION", ""),
            ("status", "ENUM('PENDING',...)", ""),
            ("payment_method", "VARCHAR(50)", ""),
            ("shipping_address", "VARCHAR(255)", ""),
            ("phone_number", "VARCHAR(20)", ""),
            ("discount_coupon_code", "VARCHAR(50)", ""),
            ("shipping_coupon_code", "VARCHAR(50)", ""),
            ("tracking_number", "VARCHAR(100)", ""),
            ("return_reason", "TEXT", ""),
            ("created_at", "TIMESTAMP", "")
        ], (37, 99, 235)),

        (980, 1030, 440, 220, "order_items", [
            ("id", "BIGSERIAL", "PK"),
            ("order_id", "BIGINT", "FK"),
            ("book_id", "BIGINT", "FK"),
            ("quantity", "INTEGER", ""),
            ("price", "DOUBLE PRECISION", "")
        ], (37, 99, 235)),

        (980, 1280, 440, 200, "return_requests", [
            ("id", "BIGSERIAL", "PK"),
            ("order_id", "BIGINT", "FK"),
            ("reason", "TEXT", ""),
            ("bank_info", "VARCHAR(255)", ""),
            ("status", "VARCHAR(50)", "")
        ], (37, 99, 235)),

        # Col 4: Promotions & Vouchers
        (1460, 120, 440, 300, "coupons", [
            ("id", "BIGSERIAL", "PK"),
            ("code", "VARCHAR(50)", "UK"),
            ("discount_type", "ENUM('FIXED','PERCENT')", ""),
            ("discount_value", "DOUBLE PRECISION", ""),
            ("min_order_amount", "DOUBLE PRECISION", ""),
            ("max_discount_amount", "DOUBLE PRECISION", ""),
            ("usage_limit", "INTEGER", ""),
            ("expiration_date", "TIMESTAMP", ""),
            ("category", "VARCHAR(50)", "")
        ], (234, 88, 12)),

        (1460, 450, 440, 240, "reward_vouchers", [
            ("id", "BIGSERIAL", "PK"),
            ("code", "VARCHAR(50)", "UK"),
            ("reward_type", "VARCHAR(50)", ""),
            ("reward_value", "DOUBLE PRECISION", ""),
            ("points_cost", "INTEGER", ""),
            ("expiration_date", "TIMESTAMP", "")
        ], (234, 88, 12)),

        (1460, 720, 440, 210, "user_rewards", [
            ("id", "BIGSERIAL", "PK"),
            ("user_id", "BIGINT", "FK"),
            ("voucher_id", "BIGINT", "FK"),
            ("redeemed_at", "TIMESTAMP", "")
        ], (234, 88, 12)),

        # Col 5: Marketing & System Settings
        (1940, 120, 380, 230, "banners", [
            ("id", "BIGSERIAL", "PK"),
            ("title", "VARCHAR(255)", ""),
            ("image_url", "VARCHAR(500)", ""),
            ("link_url", "VARCHAR(500)", ""),
            ("position", "VARCHAR(50)", "")
        ], (75, 85, 99)),

        (1940, 380, 380, 200, "site_settings", [
            ("setting_key", "VARCHAR(100)", "PK"),
            ("setting_value", "TEXT", "")
        ], (75, 85, 99)),

        (1940, 610, 380, 210, "contacts", [
            ("id", "BIGSERIAL", "PK"),
            ("full_name", "VARCHAR(100)", ""),
            ("email", "VARCHAR(100)", ""),
            ("content", "TEXT", ""),
            ("created_at", "TIMESTAMP", "")
        ], (75, 85, 99)),

        (1940, 850, 380, 200, "newsletter_subscribers", [
            ("id", "BIGSERIAL", "PK"),
            ("email", "VARCHAR(100)", "UK"),
            ("subscribed_at", "TIMESTAMP", "")
        ], (75, 85, 99))
    ]

    for x, y, w, h, tname, cols, col_c in tables:
        # Table Box
        draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=(255, 255, 255), outline=col_c, width=2)
        draw.rectangle([x, y, x+w, y+35], fill=col_c)
        draw.text((x + w//2, y + 17), tname.upper(), fill=(255, 255, 255), font=f_tbl, anchor="mm")
        
        y_f = y + 45
        for col_name, ctype, tag in cols:
            tag_str = f" [{tag}]" if tag else ""
            t_col = (185, 28, 28) if "PK" in tag else ((37, 99, 235) if "FK" in tag else (15, 23, 42))
            draw.text((x + 12, y_f), col_name, fill=t_col, font=f_pk if tag else f_fld)
            draw.text((x + w - 12, y_f), f"{ctype}{tag_str}", fill=(100, 116, 139), font=f_fld, anchor="ra")
            y_f += 24

    # Connectors (Foreign Key Relations)
    # users -> addresses, vat_invoices, point_transactions, notifications, carts, orders, reviews, user_rewards
    draw_arrow(draw, (480, 260), (980, 180), fill=(2, 132, 199), width=2, arrow_size=6) # users -> carts
    draw_arrow(draw, (480, 280), (980, 650), fill=(2, 132, 199), width=2, arrow_size=6) # users -> orders
    draw_arrow(draw, (280, 410), (280, 440), fill=(2, 132, 199), width=2, arrow_size=6) # users -> addresses
    draw_arrow(draw, (280, 640), (280, 670), fill=(2, 132, 199), width=2, arrow_size=6) # addresses -> vat
    draw_arrow(draw, (280, 880), (280, 910), fill=(2, 132, 199), width=2, arrow_size=6) # vat -> points
    
    draw_arrow(draw, (730, 320), (730, 350), fill=(5, 150, 105), width=2, arrow_size=6) # categories -> books
    draw_arrow(draw, (940, 450), (980, 420), fill=(5, 150, 105), width=2, arrow_size=6) # books -> cart_items
    draw_arrow(draw, (940, 520), (980, 1100), fill=(5, 150, 105), width=2, arrow_size=6) # books -> order_items
    draw_arrow(draw, (730, 700), (730, 730), fill=(5, 150, 105), width=2, arrow_size=6) # books -> wishlists
    draw_arrow(draw, (730, 940), (730, 970), fill=(5, 150, 105), width=2, arrow_size=6) # wishlists -> reviews
    draw_arrow(draw, (730, 1230), (730, 1260), fill=(217, 119, 6), width=2, arrow_size=6) # reviews -> comments

    draw_arrow(draw, (1200, 290), (1200, 320), fill=(37, 99, 235), width=2, arrow_size=6) # carts -> cart_items
    draw_arrow(draw, (1200, 1000), (1200, 1030), fill=(37, 99, 235), width=2, arrow_size=6) # orders -> order_items
    draw_arrow(draw, (1200, 1250), (1200, 1280), fill=(37, 99, 235), width=2, arrow_size=6) # order_items -> return_req

    draw_arrow(draw, (1680, 690), (1680, 720), fill=(234, 88, 12), width=2, arrow_size=6) # reward_vouchers -> user_rewards

    draw.text((W//2, 1565), "Safe Margin: 60px | YiYi Book Capstone Project — Entity Relationship Diagram (21 Entities Verified in PostgreSQL 16)", fill=(148, 163, 184), font=f_body, anchor="mm")

    # Standard Version
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 45), "HÌNH 4.6. SƠ ĐỒ THỰC THỂ QUAN HỆ CƠ SỞ DỮ LIỆU (ERD)", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 80), "PostgreSQL 16 Relational Schema Specification (21 Tables)", fill=(80, 80, 80), font=f_sub, anchor="mm")

    for x, y, w, h, tname, cols, _ in tables:
        draw_s.rectangle([x, y, x+w, y+h], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw_s.rectangle([x, y, x+w, y+35], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
        draw_s.text((x + w//2, y + 17), tname.upper(), fill=(0, 0, 0), font=f_tbl, anchor="mm")
        
        y_f = y + 45
        for col_name, ctype, tag in cols:
            tag_str = f" [{tag}]" if tag else ""
            draw_s.text((x + 12, y_f), col_name, fill=(0, 0, 0), font=f_pk if tag else f_fld)
            draw_s.text((x + w - 12, y_f), f"{ctype}{tag_str}", fill=(80, 80, 80), font=f_fld, anchor="ra")
            y_f += 24

    # Connectors
    draw_arrow(draw_s, (480, 260), (980, 180), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (480, 280), (980, 650), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (280, 410), (280, 440), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (280, 640), (280, 670), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (280, 880), (280, 910), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (730, 320), (730, 350), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (940, 450), (980, 420), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (940, 520), (980, 1100), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (730, 700), (730, 730), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (730, 940), (730, 970), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (730, 1230), (730, 1260), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (1200, 290), (1200, 320), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (1200, 1000), (1200, 1030), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (1200, 1250), (1200, 1280), fill=(0, 0, 0), width=1, arrow_size=5)
    draw_arrow(draw_s, (1680, 690), (1680, 720), fill=(0, 0, 0), width=1, arrow_size=5)

    draw_s.text((W//2, 1565), "Safe Margin: 60px | Technical Standard ERD Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    p_info = os.path.join(INFO_DIR, "Hinh_4.6_ERD_Database_YiYi_Book.png")
    p_std = os.path.join(STD_DIR, "Hinh_4.6_ERD_Database_YiYi_Book.png")
    img.save(p_info, "PNG", dpi=(300, 300))
    img_std.save(p_std, "PNG", dpi=(300, 300))

    svg_info = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
        <rect width="100%" height="100%" fill="#F8FAFC"/>
        <text x="{W//2}" y="45" font-family="Arial, sans-serif" font-size="34" font-weight="bold" fill="#0F172A" text-anchor="middle">SƠ ĐỒ THỰC THỂ QUAN HỆ CƠ SỞ DỮ LIỆU (ERD) — YIYI BOOK DATABASE</text>
        <text x="{W//2}" y="80" font-family="Arial, sans-serif" font-size="18" fill="#475569" text-anchor="middle">PostgreSQL 16 Schema: 21 Thực thể nghiệp vụ, 4 Kiểu Enum, Khóa chính UUID/Long và Toàn vẹn tham chiếu</text>
    </svg>'''
    with open(os.path.join(INFO_DIR, "Hinh_4.6_ERD_Database_YiYi_Book.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.6_ERD_Database_YiYi_Book.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.6 (ERD) successfully.")

if __name__ == "__main__":
    render_hinh_4_6()

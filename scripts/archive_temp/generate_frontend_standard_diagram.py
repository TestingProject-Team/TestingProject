import os
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# HÌNH 4.2: CẤU TRÚC FRONTEND COMPONENT VÀ ROUTE
# Thiết kế chuẩn phong cách Academic / Box Diagram đồng bộ 100% với Figure 1.1.1
# ==============================================================================
W, H = 2600, 2050
img = Image.new("RGBA", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

def get_font(size, bold=False):
    fonts = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\tahomabd.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf",
    ]
    for f in fonts:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                pass
    return ImageFont.load_default()

# 1. Khung to lớn bao quanh: REACT.JS FRONTEND APPLICATION
APP_X1, APP_Y1 = 440, 100
APP_X2, APP_Y2 = 2480, 1850

# Header vàng nhạt chuẩn giống Hình 1.1.1
draw.rounded_rectangle([APP_X1, APP_Y1, APP_X2, APP_Y2], radius=6, outline=(220, 190, 100), width=2, fill=(255, 255, 255))
draw.rectangle([APP_X1, APP_Y1, APP_X2, APP_Y1 + 75], fill=(254, 243, 199))
draw.line([APP_X1, APP_Y1 + 75, APP_X2, APP_Y1 + 75], fill=(220, 190, 100), width=2)
draw.text(((APP_X1 + APP_X2)//2, APP_Y1 + 38), "REACT.JS FRONTEND APPLICATION (SPA)", fill=(0, 0, 0), font=get_font(32, bold=True), anchor="mm")

INNER_W = APP_X2 - APP_X1 - 80
INNER_X = APP_X1 + 40

# --- TẦNG 1: React Context Layer (State Management) (Màu Xanh Dương Nhạt) ---
L1_Y1 = APP_Y1 + 115
L1_H = 175
L1_Y2 = L1_Y1 + L1_H

draw.rectangle([INNER_X, L1_Y1, INNER_X + INNER_W, L1_Y2], outline=(147, 197, 253), width=2, fill=(239, 246, 255))
draw.rectangle([INNER_X, L1_Y1, INNER_X + INNER_W, L1_Y1 + 48], fill=(219, 234, 254))
draw.line([INNER_X, L1_Y1 + 48, INNER_X + INNER_W, L1_Y1 + 48], fill=(147, 197, 253), width=2)
draw.text((INNER_X + INNER_W//2, L1_Y1 + 24), "React Context Layer (Global State Management)", fill=(0, 0, 0), font=get_font(25, bold=True), anchor="mm")

ctx_boxes = ["AuthContext (JWT, User)", "CartContext (Cart & Point)", "LanguageContext (i18n)", "WebSocketContext (STOMP)"]
ctx_gap = 20
ctx_w = (INNER_W - 40 - (ctx_gap * (len(ctx_boxes)-1))) // len(ctx_boxes)
for i, name in enumerate(ctx_boxes):
    cx = INNER_X + 20 + i * (ctx_w + ctx_gap)
    cy = L1_Y1 + 65
    draw.rounded_rectangle([cx, cy, cx + ctx_w, cy + 85], radius=8, outline=(96, 165, 250), width=2, fill=(255, 255, 255))
    draw.text((cx + ctx_w//2, cy + 42), name, fill=(30, 64, 175), font=get_font(20, bold=True), anchor="mm")

# Mũi tên từ Context xuống Layout/Router
ARR1_Y1 = L1_Y2
ARR1_Y2 = ARR1_Y1 + 45
draw.line([INNER_X + INNER_W//2, ARR1_Y1, INNER_X + INNER_W//2, ARR1_Y2], fill=(100, 100, 100), width=4)
draw.polygon([(INNER_X + INNER_W//2, ARR1_Y2), (INNER_X + INNER_W//2 - 10, ARR1_Y2 - 12), (INNER_X + INNER_W//2 + 10, ARR1_Y2 - 12)], fill=(100, 100, 100))

# --- TẦNG 2: Layout & Router Layer (App.jsx) (Màu Xanh Lá) ---
L2_Y1 = ARR1_Y2
L2_H = 175
L2_Y2 = L2_Y1 + L2_H

draw.rectangle([INNER_X, L2_Y1, INNER_X + INNER_W, L2_Y2], outline=(134, 239, 172), width=2, fill=(240, 253, 244))
draw.rectangle([INNER_X, L2_Y1, INNER_X + INNER_W, L2_Y1 + 48], fill=(220, 252, 231))
draw.line([INNER_X, L2_Y1 + 48, INNER_X + INNER_W, L2_Y1 + 48], fill=(134, 239, 172), width=2)
draw.text((INNER_X + INNER_W//2, L2_Y1 + 24), "Layout & Router Layer (BrowserRouter & Route Tree)", fill=(0, 0, 0), font=get_font(25, bold=True), anchor="mm")

layout_boxes = ["ClientLayout (/)", "AdminLayout (/admin/*)", "Route Guards (Role-based)", "Suspense (<PageLoader />)"]
for i, name in enumerate(layout_boxes):
    cx = INNER_X + 20 + i * (ctx_w + ctx_gap)
    cy = L2_Y1 + 65
    draw.rounded_rectangle([cx, cy, cx + ctx_w, cy + 85], radius=8, outline=(74, 222, 128), width=2, fill=(255, 255, 255))
    draw.text((cx + ctx_w//2, cy + 42), name, fill=(22, 101, 52), font=get_font(20, bold=True), anchor="mm")

# Mũi tên từ Layout xuống Route-level Pages
ARR2_Y1 = L2_Y2
ARR2_Y2 = ARR2_Y1 + 45
draw.line([INNER_X + INNER_W//2, ARR2_Y1, INNER_X + INNER_W//2, ARR2_Y2], fill=(100, 100, 100), width=4)
draw.polygon([(INNER_X + INNER_W//2, ARR2_Y2), (INNER_X + INNER_W//2 - 10, ARR2_Y2 - 12), (INNER_X + INNER_W//2 + 10, ARR2_Y2 - 12)], fill=(100, 100, 100))

# --- TẦNG 3: Route-level Pages Layer (2 Cột Song Song: Customer Pages vs Admin Pages) ---
L3_Y1 = ARR2_Y2
L3_H = 430
L3_Y2 = L3_Y1 + L3_H

HALF_W = (INNER_W - 30) // 2

# Khung Trái: Customer Pages (Xanh ngọc / Mint)
CUST_X = INNER_X
draw.rectangle([CUST_X, L3_Y1, CUST_X + HALF_W, L3_Y2], outline=(110, 231, 183), width=2, fill=(236, 253, 245))
draw.rectangle([CUST_X, L3_Y1, CUST_X + HALF_W, L3_Y1 + 48], fill=(209, 250, 229))
draw.line([CUST_X, L3_Y1 + 48, CUST_X + HALF_W, L3_Y1 + 48], fill=(110, 231, 183), width=2)
draw.text((CUST_X + HALF_W//2, L3_Y1 + 24), "Customer Pages (Client Portal)", fill=(0, 0, 0), font=get_font(24, bold=True), anchor="mm")

# Các hộp trang con trong Customer
c_sub_pages = [
    ["Home", "Category", "ProductDetail"],
    ["Cart", "Checkout", "PaymentResult"],
    ["Orders", "OrderDetail", "OrderSuccess"],
    ["Profile", "Login / Register", "Coupons / FlashSale"],
    ["Policy Pages (Terms, Privacy, Returns, Warranty, Shipping, FAQ, Contact)"]
]

cpy = L3_Y1 + 65
for row in c_sub_pages[:-1]:
    rgap = 12
    rw = (HALF_W - 30 - (rgap * (len(row)-1))) // len(row)
    for j, ptitle in enumerate(row):
        r_x = CUST_X + 15 + j * (rw + rgap)
        draw.rounded_rectangle([r_x, cpy, r_x + rw, cpy + 55], radius=6, outline=(52, 211, 153), width=2, fill=(255, 255, 255))
        draw.text((r_x + rw//2, cpy + 27), ptitle, fill=(6, 95, 70), font=get_font(19, bold=True), anchor="mm")
    cpy += 68

# Hàng Policy pages
draw.rounded_rectangle([CUST_X + 15, cpy, CUST_X + HALF_W - 15, cpy + 55], radius=6, outline=(52, 211, 153), width=2, fill=(255, 255, 255))
draw.text((CUST_X + HALF_W//2, cpy + 27), c_sub_pages[-1][0], fill=(6, 95, 70), font=get_font(18, bold=True), anchor="mm")

# Khung Phải: Administration Pages (Vàng / Cam nhạt)
ADM_X = INNER_X + HALF_W + 30
draw.rectangle([ADM_X, L3_Y1, ADM_X + HALF_W, L3_Y2], outline=(253, 186, 116), width=2, fill=(255, 247, 237))
draw.rectangle([ADM_X, L3_Y1, ADM_X + HALF_W, L3_Y1 + 48], fill=(254, 237, 213))
draw.line([ADM_X, L3_Y1 + 48, ADM_X + HALF_W, L3_Y1 + 48], fill=(253, 186, 116), width=2)
draw.text((ADM_X + HALF_W//2, L3_Y1 + 24), "Administration Pages (Admin Portal)", fill=(0, 0, 0), font=get_font(24, bold=True), anchor="mm")

# Các hộp trang con trong Admin
a_sub_pages = [
    ["AdminDashboard", "AdminBooks", "AdminFeaturedBooks"],
    ["AdminCategories", "AdminBanners", "AdminOrders"],
    ["AdminUsers", "AdminReviews", "AdminContacts"],
    ["AdminCoupons", "AdminRewardVouchers", "AdminNotifications"],
    ["AdminNewsletter", "AdminSiteSettings", "... (Lazy Loaded)"]
]

apy = L3_Y1 + 65
for row in a_sub_pages:
    rgap = 12
    rw = (HALF_W - 30 - (rgap * (len(row)-1))) // len(row)
    for j, ptitle in enumerate(row):
        r_x = ADM_X + 15 + j * (rw + rgap)
        draw.rounded_rectangle([r_x, apy, r_x + rw, apy + 55], radius=6, outline=(251, 146, 60), width=2, fill=(255, 255, 255))
        draw.text((r_x + rw//2, apy + 27), ptitle, fill=(154, 52, 18), font=get_font(19, bold=True if ptitle!="..." else False), anchor="mm")
    apy += 68

# Mũi tên từ Pages xuống Reusable Components
ARR3_Y1 = L3_Y2
ARR3_Y2 = ARR3_Y1 + 45
draw.line([INNER_X + INNER_W//2, ARR3_Y1, INNER_X + INNER_W//2, ARR3_Y2], fill=(100, 100, 100), width=4)
draw.polygon([(INNER_X + INNER_W//2, ARR3_Y2), (INNER_X + INNER_W//2 - 10, ARR3_Y2 - 12), (INNER_X + INNER_W//2 + 10, ARR3_Y2 - 12)], fill=(100, 100, 100))

# --- TẦNG 4: Reusable Component Layer (Màu Tím Nhạt) ---
L4_Y1 = ARR3_Y2
L4_H = 200
L4_Y2 = L4_Y1 + L4_H

draw.rectangle([INNER_X, L4_Y1, INNER_X + INNER_W, L4_Y2], outline=(216, 180, 254), width=2, fill=(250, 245, 255))
draw.rectangle([INNER_X, L4_Y1, INNER_X + INNER_W, L4_Y1 + 48], fill=(243, 232, 255))
draw.line([INNER_X, L4_Y1 + 48, INNER_X + INNER_W, L4_Y1 + 48], fill=(216, 180, 254), width=2)
draw.text((INNER_X + INNER_W//2, L4_Y1 + 24), "Reusable Component Layer", fill=(0, 0, 0), font=get_font(25, bold=True), anchor="mm")

# 3 khối trong Reusable Component
rc_groups = [
    {"title": "Home Components", "items": "HeroBanner, FlashSale, BestSellerRank, ComboTrending"},
    {"title": "Common & Shared UI", "items": "AIChatWidget, Intro, AddressModal, ScrollToTop"},
    {"title": "Layout Components", "items": "Header (Search, Menu), Footer, AdminSidebar"}
]
rc_gap = 18
rc_w = (INNER_W - 40 - (rc_gap * 2)) // 3
for i, rc in enumerate(rc_groups):
    rx = INNER_X + 20 + i * (rc_w + rc_gap)
    ry = L4_Y1 + 65
    draw.rounded_rectangle([rx, ry, rx + rc_w, ry + 115], radius=8, outline=(192, 132, 252), width=2, fill=(255, 255, 255))
    draw.text((rx + rc_w//2, ry + 35), rc["title"], fill=(107, 33, 168), font=get_font(22, bold=True), anchor="mm")
    draw.text((rx + rc_w//2, ry + 75), rc["items"], fill=(71, 85, 105), font=get_font(18, bold=False), anchor="mm")

# --- TẦNG 5: Hai khối dưới cùng: Utility Functions & Security vs Assets & Localization ---
BOTTOM_Y1 = L4_Y2 + 35
BOTTOM_H = 150

# Khối Trái: Utility Functions & Security (Đỏ / Hồng nhạt)
draw.rectangle([INNER_X, BOTTOM_Y1, INNER_X + HALF_W, BOTTOM_Y1 + BOTTOM_H], outline=(252, 165, 165), width=2, fill=(254, 242, 242))
draw.rectangle([INNER_X, BOTTOM_Y1, INNER_X + HALF_W, BOTTOM_Y1 + 45], fill=(254, 226, 226))
draw.line([INNER_X, BOTTOM_Y1 + 45, INNER_X + HALF_W, BOTTOM_Y1 + 45], fill=(252, 165, 165), width=2)
draw.text((INNER_X + HALF_W//2, BOTTOM_Y1 + 22), "Utility Functions & API Client", fill=(0, 0, 0), font=get_font(23, bold=True), anchor="mm")

u_boxes = ["Axios Client (JWT)", "alert.js (Toast)", "Anti-F12 / Anti-Copy Guard"]
u_gap = 12
u_w = (HALF_W - 30 - (u_gap * 2)) // 3
for i, uname in enumerate(u_boxes):
    ux = INNER_X + 15 + i * (u_w + u_gap)
    uy = BOTTOM_Y1 + 60
    draw.rounded_rectangle([ux, uy, ux + u_w, uy + 70], radius=8, outline=(248, 113, 113), width=2, fill=(255, 255, 255))
    draw.text((ux + u_w//2, uy + 35), uname, fill=(153, 27, 27), font=get_font(18, bold=True), anchor="mm")

# Khối Phải: Assets & Localization (Xanh lam nhạt)
LOC_X = INNER_X + HALF_W + 30
draw.rectangle([LOC_X, BOTTOM_Y1, LOC_X + HALF_W, BOTTOM_Y1 + BOTTOM_H], outline=(186, 230, 253), width=2, fill=(240, 249, 255))
draw.rectangle([LOC_X, BOTTOM_Y1, LOC_X + HALF_W, BOTTOM_Y1 + 45], fill=(224, 242, 254))
draw.line([LOC_X, BOTTOM_Y1 + 45, LOC_X + HALF_W, BOTTOM_Y1 + 45], fill=(186, 230, 253), width=2)
draw.text((LOC_X + HALF_W//2, BOTTOM_Y1 + 22), "Data, Assets & Localization (i18n)", fill=(0, 0, 0), font=get_font(23, bold=True), anchor="mm")

a_boxes = ["provinces.json (34 Tỉnh)", "vi.js / en.js Dictionary", "Tailwind CSS v4 Styles"]
for i, aname in enumerate(a_boxes):
    ax = LOC_X + 15 + i * (u_w + u_gap)
    ay = BOTTOM_Y1 + 60
    draw.rounded_rectangle([ax, ay, ax + u_w, ay + 70], radius=8, outline=(56, 189, 248), width=2, fill=(255, 255, 255))
    draw.text((ax + u_w//2, ay + 35), aname, fill=(3, 105, 161), font=get_font(18, bold=True), anchor="mm")

# --- 6. CÁC KHỐI BÊN NGOÀI (BÊN TRÁI) ---
def draw_double_dash_arrow(x1, y1, x2, y2):
    dash_len = 10
    space_len = 6
    curr = x1
    while curr < x2:
        end = min(curr + dash_len, x2)
        draw.line([curr, y1, end, y1], fill=(100, 100, 100), width=2)
        curr += dash_len + space_len
    draw.polygon([(x1, y1), (x1 + 10, y1 - 6), (x1 + 10, y1 + 6)], fill=(100, 100, 100))
    draw.polygon([(x2, y1), (x2 - 10, y1 - 6), (x2 - 10, y1 + 6)], fill=(100, 100, 100))

# Khối 1: Spring Boot Backend API
EXT1_X1, EXT1_Y1 = 80, 520
EXT1_X2, EXT1_Y2 = 360, 680
draw.rounded_rectangle([EXT1_X1, EXT1_Y1, EXT1_X2, EXT1_Y2], radius=12, outline=(74, 222, 128), width=2, fill=(240, 253, 244))
draw.text(((EXT1_X1+EXT1_X2)//2, EXT1_Y1 + 45), "Spring Boot API", fill=(22, 101, 52), font=get_font(23, bold=True), anchor="mm")
draw.text(((EXT1_X1+EXT1_X2)//2, EXT1_Y1 + 90), "(Port 8081)", fill=(71, 85, 105), font=get_font(19, bold=False), anchor="mm")
draw.text(((EXT1_X1+EXT1_X2)//2, EXT1_Y1 + 125), "REST / JSON", fill=(22, 101, 52), font=get_font(18, bold=True), anchor="mm")

draw_double_dash_arrow(EXT1_X2, (EXT1_Y1+EXT1_Y2)//2, APP_X1, (EXT1_Y1+EXT1_Y2)//2)

# Khối 2: Groq Cloud AI (Llama 3.3 70B)
EXT2_X1, EXT2_Y1 = 80, 820
EXT2_X2, EXT2_Y2 = 360, 980
draw.rounded_rectangle([EXT2_X1, EXT2_Y1, EXT2_X2, EXT2_Y2], radius=12, outline=(251, 191, 36), width=2, fill=(254, 243, 199))
draw.text(((EXT2_X1+EXT2_X2)//2, EXT2_Y1 + 45), "Groq Cloud AI", fill=(180, 83, 9), font=get_font(23, bold=True), anchor="mm")
draw.text(((EXT2_X1+EXT2_X2)//2, EXT2_Y1 + 90), "(Llama 3.3 70B)", fill=(71, 85, 105), font=get_font(19, bold=False), anchor="mm")
draw.text(((EXT2_X1+EXT2_X2)//2, EXT2_Y1 + 125), "Streaming SSE", fill=(180, 83, 9), font=get_font(18, bold=True), anchor="mm")

draw_double_dash_arrow(EXT2_X2, (EXT2_Y1+EXT2_Y2)//2, APP_X1, (EXT2_Y1+EXT2_Y2)//2)

# Khối 3: WebSocket STOMP Server
EXT3_X1, EXT3_Y1 = 80, 1120
EXT3_X2, EXT3_Y2 = 360, 1280
draw.rounded_rectangle([EXT3_X1, EXT3_Y1, EXT3_X2, EXT3_Y2], radius=12, outline=(192, 132, 252), width=2, fill=(250, 245, 255))
draw.text(((EXT3_X1+EXT3_X2)//2, EXT3_Y1 + 45), "WebSocket Server", fill=(107, 33, 168), font=get_font(22, bold=True), anchor="mm")
draw.text(((EXT3_X1+EXT3_X2)//2, EXT3_Y1 + 90), "(STOMP Broker)", fill=(71, 85, 105), font=get_font(19, bold=False), anchor="mm")
draw.text(((EXT3_X1+EXT3_X2)//2, EXT3_Y1 + 125), "Push Notification", fill=(107, 33, 168), font=get_font(18, bold=True), anchor="mm")

draw_double_dash_arrow(EXT3_X2, (EXT3_Y1+EXT3_Y2)//2, APP_X1, (EXT3_Y1+EXT3_Y2)//2)

# Chú thích cuối ảnh
draw.text((W // 2, 1960), "Hình 4.2. Cấu trúc Frontend component và route.", fill=(0, 0, 0), font=get_font(30, bold=False), anchor="mm")

# Lưu ảnh ra thư mục docs/ và thư mục gốc
out_file = "docs/Hinh_4.2_Frontend_Component_Route_YiYi_Book.png"
img.save(out_file, "PNG", dpi=(300, 300))
img.save("Hinh_4.2_Frontend_Component_Route_YiYi_Book.png", "PNG", dpi=(300, 300))
print("Saved clean Figure 4.2 at:", out_file)

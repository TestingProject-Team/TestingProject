# -*- coding: utf-8 -*-
import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# HÌNH 3.2: SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG (OVERALL USE CASE DIAGRAM) - V2 REDESIGN
# Bố cục 3 Phân hệ chuẩn mực: Khách Vãng Lai, Khách Hàng Thành Viên, Quản Trị Viên
# ==============================================================================
W, H = 2600, 1600
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

# 1. Khung lớn toàn bộ Diagram
BORDER_X1, BORDER_Y1 = 50, 40
BORDER_X2, BORDER_Y2 = W - 50, H - 40

draw.rounded_rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y2], radius=14, outline=(190, 205, 220), width=3, fill=(255, 255, 255))

# Header của Diagram
HEADER_H = 85
draw.rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(238, 242, 255))
draw.line([BORDER_X1, BORDER_Y1 + HEADER_H, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(199, 210, 254), width=3)
draw.text(((BORDER_X1 + BORDER_X2) // 2, BORDER_Y1 + 42), 
          "SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG YIYI BOOK (OVERALL USE CASE DIAGRAM)", 
          fill=(30, 58, 138), font=get_font(34, bold=True), anchor="mm")

# Subtitle
SUB_Y = BORDER_Y1 + HEADER_H + 22
draw.text(((BORDER_X1 + BORDER_X2) // 2, SUB_Y),
          "Ranh giới hệ thống phân định theo 3 gói chức năng độc lập: Khách Vãng Lai, Khách Hàng Thành Viên và Quản Trị Viên",
          fill=(75, 85, 99), font=get_font(21, bold=False), anchor="mm")

# Hàm vẽ Stick Figure Actor chuẩn UML
def draw_actor(x, y, name, role_sub, color=(30, 64, 175)):
    # Đầu (Head)
    draw.ellipse([x - 26, y - 65, x + 26, y - 13], outline=color, width=3, fill=(255, 255, 255))
    # Thân (Body)
    draw.line([x, y - 13, x, y + 48], fill=color, width=3)
    # Tay (Arms)
    draw.line([x - 42, y + 10, x + 42, y + 10], fill=color, width=3)
    # Chân trái (Left Leg)
    draw.line([x, y + 48, x - 30, y + 95], fill=color, width=3)
    # Chân phải (Right Leg)
    draw.line([x, y + 48, x + 30, y + 95], fill=color, width=3)
    # Tên Actor (Label)
    draw.text((x, y + 120), name, fill=color, font=get_font(20, bold=True), anchor="mm")
    draw.text((x, y + 146), f"({role_sub})", fill=(100, 116, 139), font=get_font(15, bold=False), anchor="mm")

# 2. BỐ CỤC 3 PHÂN VÙNG (3 SYSTEM BOUNDARY PANELS)
PANEL_Y1 = 175
PANEL_Y2 = H - 95

# PANEL 1: GUEST PACKAGE (Trái)
P1_X1 = 80
P1_W = 740
P1_X2 = P1_X1 + P1_W

# PANEL 2: MEMBER PACKAGE (Giữa)
P2_X1 = 860
P2_W = 800
P2_X2 = P2_X1 + P2_W

# PANEL 3: ADMIN PACKAGE (Phải)
P3_X1 = 1700
P3_W = 820
P3_X2 = P3_X1 + P3_W

# Hàm vẽ khung Panel Phân hệ
def draw_package_panel(x1, y1, x2, y2, title, code_range, col_border, col_hdr, col_t):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=12, outline=col_border, width=3, fill=(248, 250, 252))
    # Header panel
    draw.rounded_rectangle([x1, y1, x2, y1 + 55], radius=12, outline=col_border, width=3, fill=col_hdr)
    draw.rectangle([x1, y1 + 42, x2, y1 + 55], fill=col_hdr)
    draw.line([x1, y1 + 55, x2, y1 + 55], fill=col_border, width=2)
    
    draw.text((x1 + 25, y1 + 27), title, fill=col_t, font=get_font(21, bold=True), anchor="lm")
    draw.text((x2 - 25, y1 + 27), code_range, fill=col_t, font=get_font(16, bold=True), anchor="rm")

# Vẽ 3 Panel
draw_package_panel(P1_X1, PANEL_Y1, P1_X2, PANEL_Y2, "PHÂN HỆ KHÁCH VÃNG LAI", "[UC-01 → UC-06]", (20, 184, 166), (204, 251, 241), (15, 118, 110))
draw_package_panel(P2_X1, PANEL_Y1, P2_X2, PANEL_Y2, "PHÂN HỆ KHÁCH HÀNG THÀNH VIÊN", "[UC-07 → UC-16]", (59, 130, 246), (219, 234, 254), (30, 64, 175))
draw_package_panel(P3_X1, PANEL_Y1, P3_X2, PANEL_Y2, "PHÂN HỆ QUẢN TRỊ VIÊN (ADMIN)", "[UC-17 → UC-26]", (236, 72, 153), (252, 231, 243), (190, 24, 93))

# Hàm vẽ Use Case Oval chuẩn UML sắc nét
def draw_usecase(x, y, w, h, code, title, col_border, col_bg, col_code):
    x1, y1 = x - w//2, y - h//2
    x2, y2 = x + w//2, y + h//2
    draw.ellipse([x1, y1, x2, y2], outline=col_border, width=2, fill=col_bg)
    draw.text((x, y - 10), code, fill=col_code, font=get_font(15, bold=True), anchor="mm")
    draw.text((x, y + 12), title, fill=(30, 41, 59), font=get_font(16, bold=True), anchor="mm")
    return (x1, y, x2, y, x, y1, x, y2) # left, right, top, bottom anchors

# 3. VẼ NỘI DUNG PANEL 1: GUEST
# Actor Guest nằm bên trái trong Panel 1
GUEST_ACT_X, GUEST_ACT_Y = P1_X1 + 140, PANEL_Y1 + 380
draw_actor(GUEST_ACT_X, GUEST_ACT_Y, "Khách Vãng Lai", "Guest Actor", (15, 118, 110))

# 6 Use Cases của Guest nằm bên phải Actor Guest
GUEST_UCS = [
    ("UC-01", "Duyệt danh mục & Trang chủ"),
    ("UC-02", "Tìm kiếm & Lọc sách"),
    ("UC-03", "Xem chi tiết sách & Đánh giá"),
    ("UC-04", "Tư vấn qua Trợ lý ảo AI"),
    ("UC-05", "Đăng ký tài khoản mới"),
    ("UC-06", "Đăng nhập & Quên mật khẩu"),
]

G_UC_X = P1_X1 + 490
G_UC_START_Y = PANEL_Y1 + 105
G_UC_GAP = 90
G_ANCHORS = []

for idx, (code, title) in enumerate(GUEST_UCS):
    uy = G_UC_START_Y + idx * G_UC_GAP
    anch = draw_usecase(G_UC_X, uy, 400, 68, code, title, (20, 184, 166), (255, 255, 255), (15, 118, 110))
    G_ANCHORS.append(anch)
    # Đường nối Actor -> Use Case
    draw.line([GUEST_ACT_X + 45, GUEST_ACT_Y - 10, anch[0], anch[1]], fill=(20, 184, 166), width=2)

# Panel 1 Footer Note
draw.rounded_rectangle([P1_X1 + 25, PANEL_Y2 - 60, P1_X2 - 25, PANEL_Y2 - 15], radius=6, fill=(240, 253, 250), outline=(20, 184, 166), width=1)
draw.text(((P1_X1 + P1_X2)//2, PANEL_Y2 - 37), "Truy cập công khai không yêu cầu JWT Token", fill=(15, 118, 110), font=get_font(15, bold=True), anchor="mm")


# 4. VẼ NỘI DUNG PANEL 2: MEMBER
# Actor Member nằm bên trái trong Panel 2
MEMBER_ACT_X, MEMBER_ACT_Y = P2_X1 + 140, PANEL_Y1 + 460
draw_actor(MEMBER_ACT_X, MEMBER_ACT_Y, "Khách Hàng", "Member Actor", (30, 64, 175))

# 10 Use Cases của Member nằm bên phải Actor Member
MEMBER_UCS = [
    ("UC-07", "Quản lý Giỏ hàng (Cart)"),
    ("UC-08", "Quản lý Sách yêu thích"),
    ("UC-09", "Áp dụng Mã giảm giá & Điểm"),
    ("UC-10", "Tạo Đơn hàng & COD"),
    ("UC-11", "Thanh toán Online VNPAY/MoMo"),
    ("UC-12", "Theo dõi Trạng thái đơn hàng"),
    ("UC-13", "Hủy đơn & Yêu cầu hoàn tiền"),
    ("UC-14", "Viết Đánh giá & Bình luận"),
    ("UC-15", "Quản lý Hồ sơ (Profile)"),
    ("UC-16", "Nhận Thông báo & Liên hệ"),
]

M_UC_X = P2_X1 + 530
M_UC_START_Y = PANEL_Y1 + 100
M_UC_GAP = 85
M_ANCHORS = []

for idx, (code, title) in enumerate(MEMBER_UCS):
    uy = M_UC_START_Y + idx * M_UC_GAP
    anch = draw_usecase(M_UC_X, uy, 440, 66, code, title, (59, 130, 246), (255, 255, 255), (30, 64, 175))
    M_ANCHORS.append(anch)
    # Đường nối Actor -> Use Case
    draw.line([MEMBER_ACT_X + 45, MEMBER_ACT_Y - 10, anch[0], anch[1]], fill=(59, 130, 246), width=2)

# Panel 2 Footer Note
draw.rounded_rectangle([P2_X1 + 25, PANEL_Y2 - 60, P2_X2 - 25, PANEL_Y2 - 15], radius=6, fill=(239, 246, 255), outline=(59, 130, 246), width=1)
draw.text(((P2_X1 + P2_X2)//2, PANEL_Y2 - 37), "Yêu cầu Đăng nhập & Xác thực Bearer JWT Token", fill=(30, 64, 175), font=get_font(15, bold=True), anchor="mm")


# 5. VẼ NỘI DUNG PANEL 3: ADMIN
# 10 Use Cases của Admin nằm bên trái Actor Admin
ADMIN_UCS = [
    ("UC-17", "Dashboard & Thống kê doanh thu"),
    ("UC-18", "Quản lý Danh mục & Tác giả"),
    ("UC-19", "Quản trị Kho sách (CRUD & Stock)"),
    ("UC-20", "Quản lý Đơn hàng & Vận chuyển"),
    ("UC-21", "Quản lý Người dùng & RBAC"),
    ("UC-22", "Quản lý Mã giảm giá (Coupon)"),
    ("UC-23", "Quản lý Đánh giá & Phản hồi"),
    ("UC-24", "Quản trị Banner quảng cáo"),
    ("UC-25", "Quản lý Yêu cầu liên hệ CSKH"),
    ("UC-26", "Cấu hình Thông số hệ thống"),
]

A_UC_X = P3_X1 + 280
A_UC_START_Y = PANEL_Y1 + 100
A_UC_GAP = 85
A_ANCHORS = []

# Actor Admin nằm bên phải trong Panel 3
ADMIN_ACT_X, ADMIN_ACT_Y = P3_X1 + 680, PANEL_Y1 + 460
draw_actor(ADMIN_ACT_X, ADMIN_ACT_Y, "Quản Trị Viên", "Admin / Staff", (190, 24, 93))

for idx, (code, title) in enumerate(ADMIN_UCS):
    uy = A_UC_START_Y + idx * A_UC_GAP
    anch = draw_usecase(A_UC_X, uy, 450, 66, code, title, (236, 72, 153), (255, 255, 255), (190, 24, 93))
    A_ANCHORS.append(anch)
    # Đường nối Use Case -> Actor Admin
    draw.line([anch[2], anch[1], ADMIN_ACT_X - 45, ADMIN_ACT_Y - 10], fill=(236, 72, 153), width=2)

# Panel 3 Footer Note
draw.rounded_rectangle([P3_X1 + 25, PANEL_Y2 - 60, P3_X2 - 25, PANEL_Y2 - 15], radius=6, fill=(253, 242, 248), outline=(236, 72, 153), width=1)
draw.text(((P3_X1 + P3_X2)//2, PANEL_Y2 - 37), "Yêu cầu Quyền hạn Quản trị: ROLE_ADMIN / ROLE_STAFF", fill=(190, 24, 93), font=get_font(15, bold=True), anchor="mm")


# 6. KHUNG CHÚ THÍCH DƯỚI CÙNG (BOTTOM LEGEND BAR)
LEG_Y1 = H - 80
LEG_Y2 = H - 35
draw.rectangle([BORDER_X1, LEG_Y1, BORDER_X2, LEG_Y2], fill=(248, 250, 252))
draw.line([BORDER_X1, LEG_Y1, BORDER_X2, LEG_Y1], fill=(226, 232, 240), width=2)

leg_items = [
    ("● Khách Vãng Lai: 6 Use Cases cơ bản", (15, 118, 110)),
    ("● Khách Hàng Thành Viên: 10 Use Cases giao dịch & tài khoản", (30, 64, 175)),
    ("● Quản Trị Viên: 10 Use Cases vận hành & cấu hình hệ thống", (190, 24, 93)),
    ("● Chuẩn UML 2.5: Phân rã System Boundary theo Package & Role", (71, 85, 105))
]

for l_idx, (l_text, l_col) in enumerate(leg_items):
    lx = BORDER_X1 + 60 + l_idx * 600
    draw.text((lx, (LEG_Y1 + LEG_Y2)//2), l_text, fill=l_col, font=get_font(16, bold=True), anchor="lm")

# Lưu ảnh
out1 = "Hinh_3.2_Overall_Use_Case_Diagram_YiYi_Book.png"
out2 = os.path.join("docs", "Hinh_3.2_Overall_Use_Case_Diagram_YiYi_Book.png")
img.save(out1, "PNG", dpi=(300, 300))
img.save(out2, "PNG", dpi=(300, 300))

print(f"Generated clean Hình 3.2 successfully: {out1} and {out2}")
print(f"Dimensions: {W}x{H} px (High Resolution 300 DPI)")

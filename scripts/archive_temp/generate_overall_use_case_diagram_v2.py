# -*- coding: utf-8 -*-
import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# HÌNH 3.2: SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG YIYI BOOK (OVERALL USE CASE DIAGRAM)
# Phiên bản chuẩn mực UML 2.5 theo 13 yêu cầu khắt khe của bài mẫu học thuật:
# 1. Một SYSTEM BOUNDARY duy nhất: "YIYI BOOK ONLINE BOOKSTORE MANAGEMENT SYSTEM"
# 2. Toàn bộ Primary Actors & External Actors nằm NGOÀI System Boundary
# 3. Quan hệ Generalization chuẩn UML: Khách Hàng Thành Viên -> Khách Vãng Lai
# 4. Ba phân vùng màu bên trong: PUBLIC / GUEST, CUSTOMER / MEMBER, ADMINISTRATION
# 5. External Actors có căn cứ từ source code: Groq AI Service, VNPay Gateway, Gmail SMTP Service
# 6. Sửa UC-03: "Xem chi tiết sách & Xem đánh giá"
# 7. Loại bỏ ROLE_STAFF (Source code chỉ có USER và ADMIN)
# 8. Không có các đường đè cắt chéo qua oval
# ==============================================================================

W, H = 2800, 1680
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

# 1. Khung viền ngoài toàn bộ Diagram
BORDER_X1, BORDER_Y1 = 40, 30
BORDER_X2, BORDER_Y2 = W - 40, H - 30

draw.rounded_rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y2], radius=14, outline=(190, 205, 220), width=3, fill=(255, 255, 255))

# Header của Diagram
HEADER_H = 80
draw.rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(238, 242, 255))
draw.line([BORDER_X1, BORDER_Y1 + HEADER_H, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(199, 210, 254), width=3)
draw.text(((BORDER_X1 + BORDER_X2) // 2, BORDER_Y1 + 40), 
          "SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG YIYI BOOK (OVERALL USE CASE DIAGRAM)", 
          fill=(30, 58, 138), font=get_font(32, bold=True), anchor="mm")

# Subtitle
SUB_Y = BORDER_Y1 + HEADER_H + 20
draw.text(((BORDER_X1 + BORDER_X2) // 2, SUB_Y),
          "Phân rã chức năng theo 3 nhóm tác vụ, tích hợp quan hệ Kế thừa Actor (Generalization) và Dịch vụ ngoài (External Services)",
          fill=(75, 85, 99), font=get_font(20, bold=False), anchor="mm")

# 2. MỘT SYSTEM BOUNDARY LỚN DUY NHẤT
SB_X1 = 360
SB_Y1 = 160
SB_X2 = 2420
SB_Y2 = H - 85

# Khung System Boundary
draw.rectangle([SB_X1, SB_Y1, SB_X2, SB_Y2], outline=(37, 99, 235), width=3, fill=(255, 255, 255))

# Tiêu đề System Boundary duy nhất
SB_HDR_H = 50
draw.rectangle([SB_X1, SB_Y1, SB_X2, SB_Y1 + SB_HDR_H], fill=(219, 234, 254))
draw.line([SB_X1, SB_Y1 + SB_HDR_H, SB_X2, SB_Y1 + SB_HDR_H], fill=(37, 99, 235), width=2)
draw.text(((SB_X1 + SB_X2)//2, SB_Y1 + 25), 
          "YIYI BOOK ONLINE BOOKSTORE MANAGEMENT SYSTEM", 
          fill=(30, 64, 175), font=get_font(22, bold=True), anchor="mm")

# 3. BA VÙNG MÀU PHÂN NHÓM CHỨC NĂNG BÊN TRONG SYSTEM BOUNDARY
ZONE_GAP = 20
TOTAL_ZONE_W = SB_X2 - SB_X1 - 40
ZONE_W = (TOTAL_ZONE_W - ZONE_GAP * 2) // 3

# Vùng 1: PUBLIC / GUEST FEATURES (Xanh ngọc pastel)
Z1_X1 = SB_X1 + 20
Z1_X2 = Z1_X1 + ZONE_W
Z1_Y1 = SB_Y1 + SB_HDR_H + 15
Z1_Y2 = SB_Y2 - 15

# Vùng 2: CUSTOMER / MEMBER FEATURES (Xanh dương pastel)
Z2_X1 = Z1_X2 + ZONE_GAP
Z2_X2 = Z2_X1 + ZONE_W
Z2_Y1 = Z1_Y1
Z2_Y2 = Z1_Y2

# Vùng 3: ADMINISTRATION FEATURES (Hồng tím pastel)
Z3_X1 = Z2_X2 + ZONE_GAP
Z3_X2 = Z3_X1 + ZONE_W
Z3_Y1 = Z1_Y1
Z3_Y2 = Z1_Y2

def draw_feature_zone(x1, y1, x2, y2, title, code_badge, bg_col, border_col, hdr_col, text_col, note_text):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, outline=border_col, width=2, fill=bg_col)
    # Zone Header
    draw.rounded_rectangle([x1, y1, x2, y1 + 45], radius=10, outline=border_col, width=2, fill=hdr_col)
    draw.rectangle([x1, y1 + 32, x2, y1 + 45], fill=hdr_col)
    draw.line([x1, y1 + 45, x2, y1 + 45], fill=border_col, width=2)
    
    draw.text((x1 + 18, y1 + 22), title, fill=text_col, font=get_font(18, bold=True), anchor="lm")
    draw.text((x2 - 18, y1 + 22), code_badge, fill=text_col, font=get_font(15, bold=True), anchor="rm")
    
    # Zone Footer Note (Security requirement note nhỏ)
    draw.rounded_rectangle([x1 + 15, y2 - 42, x2 - 15, y2 - 12], radius=6, fill=(255, 255, 255), outline=border_col, width=1)
    draw.text(((x1 + x2)//2, y2 - 27), note_text, fill=text_col, font=get_font(14, bold=True), anchor="mm")

draw_feature_zone(Z1_X1, Z1_Y1, Z1_X2, Z1_Y2, "PUBLIC / GUEST FEATURES", "[UC-01 → UC-06]", (240, 253, 250), (20, 184, 166), (204, 251, 241), (15, 118, 110), "Public Access (Không yêu cầu đăng nhập)")
draw_feature_zone(Z2_X1, Z2_Y1, Z2_X2, Z2_Y2, "CUSTOMER / MEMBER FEATURES", "[UC-07 → UC-16]", (239, 246, 255), (59, 130, 246), (219, 234, 254), (30, 64, 175), "Authenticated Customer (Xác thực tài khoản)")
draw_feature_zone(Z3_X1, Z3_Y1, Z3_X2, Z3_Y2, "ADMINISTRATION FEATURES", "[UC-17 → UC-26]", (253, 242, 248), (236, 72, 153), (252, 231, 243), (190, 24, 93), "Authorized Administrator (Phân quyền ROLE_ADMIN)")

# 4. HÀM VẼ ACTOR STICK FIGURE CHUẨN UML
def draw_actor(x, y, name, role_sub, color=(30, 64, 175)):
    # Đầu (Head)
    draw.ellipse([x - 24, y - 60, x + 24, y - 12], outline=color, width=3, fill=(255, 255, 255))
    # Thân (Body)
    draw.line([x, y - 12, x, y + 45], fill=color, width=3)
    # Tay (Arms)
    draw.line([x - 38, y + 10, x + 38, y + 10], fill=color, width=3)
    # Chân trái (Left Leg)
    draw.line([x, y + 45, x - 26, y + 90], fill=color, width=3)
    # Chân phải (Right Leg)
    draw.line([x, y + 45, x + 26, y + 90], fill=color, width=3)
    # Tên Actor (Label)
    draw.text((x, y + 115), name, fill=color, font=get_font(18, bold=True), anchor="mm")
    draw.text((x, y + 138), f"({role_sub})", fill=(100, 116, 139), font=get_font(14, bold=False), anchor="mm")

# HÀM VẼ EXTERNAL ACTOR (HÌNH HỘP CHUẨN UML «actor» HOẶC «system»)
def draw_external_actor(x1, y1, x2, y2, title, sub, col_border, col_bg, col_t):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8, outline=col_border, width=2, fill=col_bg)
    draw.text(((x1 + x2)//2, y1 + 18), "«external service»", fill=(100, 116, 139), font=get_font(13, bold=False), anchor="mm")
    draw.text(((x1 + x2)//2, y1 + 42), title, fill=col_t, font=get_font(17, bold=True), anchor="mm")
    draw.text(((x1 + x2)//2, y1 + 68), sub, fill=(71, 85, 105), font=get_font(13, bold=False), anchor="mm")

# HÀM VẼ USE CASE OVAL CHUẨN UML
def draw_usecase_oval(x, y, w, h, code, title, col_border, col_bg, col_code):
    x1, y1 = x - w//2, y - h//2
    x2, y2 = x + w//2, y + h//2
    draw.ellipse([x1, y1, x2, y2], outline=col_border, width=2, fill=col_bg)
    draw.text((x, y - 10), code, fill=col_code, font=get_font(14, bold=True), anchor="mm")
    draw.text((x, y + 12), title, fill=(30, 41, 59), font=get_font(16, bold=True), anchor="mm")
    return (x1, y, x2, y, x, y1, x, y2) # left, right, top, bottom, center

# 5. VẼ CÁC USE CASE OVALS TRONG TỪNG VÙNG

# VÙNG 1: GUEST USE CASES
GUEST_UCS = [
    ("UC-01", "Duyệt danh mục & Trang chủ"),
    ("UC-02", "Tìm kiếm & Lọc sách"),
    ("UC-03", "Xem chi tiết sách & Xem đánh giá"),
    ("UC-04", "Tư vấn qua Trợ lý AI"),
    ("UC-05", "Đăng ký tài khoản mới"),
    ("UC-06", "Đăng nhập & Quên mật khẩu"),
]
Z1_MID_X = (Z1_X1 + Z1_X2) // 2
Z1_START_Y = Z1_Y1 + 105
Z1_GAP = 175
GUEST_ANCHORS = []

for idx, (code, title) in enumerate(GUEST_UCS):
    uy = Z1_START_Y + idx * Z1_GAP
    anch = draw_usecase_oval(Z1_MID_X, uy, 560, 72, code, title, (20, 184, 166), (255, 255, 255), (15, 118, 110))
    GUEST_ANCHORS.append(anch)

# VÙNG 2: MEMBER USE CASES
MEMBER_UCS = [
    ("UC-07", "Quản lý Giỏ hàng"),
    ("UC-08", "Quản lý Sách yêu thích"),
    ("UC-09", "Áp dụng Mã giảm giá & Điểm"),
    ("UC-10", "Tạo Đơn hàng & COD"),
    ("UC-11", "Thanh toán Online VNPay/MoMo"),
    ("UC-12", "Theo dõi Trạng thái đơn hàng"),
    ("UC-13", "Hủy đơn & Yêu cầu hoàn tiền"),
    ("UC-14", "Viết Đánh giá & Bình luận"),
    ("UC-15", "Quản lý Hồ sơ"),
    ("UC-16", "Nhận Thông báo & Liên hệ"),
]
Z2_MID_X = (Z2_X1 + Z2_X2) // 2
Z2_START_Y = Z2_Y1 + 80
Z2_GAP = 118
MEMBER_ANCHORS = []

for idx, (code, title) in enumerate(MEMBER_UCS):
    uy = Z2_START_Y + idx * Z2_GAP
    anch = draw_usecase_oval(Z2_MID_X, uy, 580, 68, code, title, (59, 130, 246), (255, 255, 255), (30, 64, 175))
    MEMBER_ANCHORS.append(anch)

# VÙNG 3: ADMIN USE CASES
ADMIN_UCS = [
    ("UC-17", "Dashboard & Thống kê doanh thu"),
    ("UC-18", "Quản lý Danh mục & Tác giả"),
    ("UC-19", "Quản trị Kho sách (CRUD & Stock)"),
    ("UC-20", "Quản lý Đơn hàng & Vận chuyển"),
    ("UC-21", "Quản lý Người dùng & RBAC"),
    ("UC-22", "Quản lý Mã giảm giá (Coupon)"),
    ("UC-23", "Quản lý Đánh giá & Phản hồi"),
    ("UC-24", "Quản lý Banner quảng cáo"),
    ("UC-25", "Quản lý Yêu cầu liên hệ / CSKH"),
    ("UC-26", "Cấu hình Thông số hệ thống"),
]
Z3_MID_X = (Z3_X1 + Z3_X2) // 2
Z3_START_Y = Z3_Y1 + 80
Z3_GAP = 118
ADMIN_ANCHORS = []

for idx, (code, title) in enumerate(ADMIN_UCS):
    uy = Z3_START_Y + idx * Z3_GAP
    anch = draw_usecase_oval(Z3_MID_X, uy, 580, 68, code, title, (236, 72, 153), (255, 255, 255), (190, 24, 93))
    ADMIN_ANCHORS.append(anch)

# 6. VẼ PRIMARY ACTORS Ở NGOÀI SYSTEM BOUNDARY

# Actor 1: Khách Vãng Lai (Bên ngoài góc trái trên)
GUEST_ACT_X = 180
GUEST_ACT_Y = 380
draw_actor(GUEST_ACT_X, GUEST_ACT_Y, "Khách Vãng Lai", "Guest Actor", (15, 118, 110))

# Actor 2: Khách Hàng Thành Viên (Bên ngoài góc trái dưới)
MEMBER_ACT_X = 180
MEMBER_ACT_Y = 1150
draw_actor(MEMBER_ACT_X, MEMBER_ACT_Y, "Khách Hàng Thành Viên", "Member Actor", (30, 64, 175))

# Actor Generalization: Khách Hàng Thành Viên -> Khách Vãng Lai (Đường liền + Mũi tên tam giác rỗng)
GEN_TOP_Y = GUEST_ACT_Y + 160
GEN_BOT_Y = MEMBER_ACT_Y - 75
draw.line([MEMBER_ACT_X, GEN_BOT_Y, GUEST_ACT_X, GEN_TOP_Y + 22], fill=(71, 85, 105), width=2)
# Tam giác rỗng hướng lên Khách Vãng Lai
draw.polygon([(GUEST_ACT_X, GEN_TOP_Y), (GUEST_ACT_X - 10, GEN_TOP_Y + 22), (GUEST_ACT_X + 10, GEN_TOP_Y + 22)], 
             outline=(71, 85, 105), fill=(255, 255, 255))
# Nhãn generalization
draw.rounded_rectangle([GUEST_ACT_X - 60, (GEN_TOP_Y + GEN_BOT_Y)//2 - 12, GUEST_ACT_X + 60, (GEN_TOP_Y + GEN_BOT_Y)//2 + 12], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
draw.text((GUEST_ACT_X, (GEN_TOP_Y + GEN_BOT_Y)//2), "«generalizes»", fill=(100, 116, 139), font=get_font(13, bold=False), anchor="mm")

# Actor 3: Quản Trị Viên (Bên ngoài góc phải giữa)
ADMIN_ACT_X = 2610
ADMIN_ACT_Y = 750
draw_actor(ADMIN_ACT_X, ADMIN_ACT_Y, "Quản Trị Viên", "Administrator", (190, 24, 93))

# 7. VẼ CÁC EXTERNAL ACTORS Ở NGOÀI SYSTEM BOUNDARY (DỰA TRÊN SOURCE CODE THỰC TẾ)

# External 1: Groq AI Service (Nằm ở góc trên bên trái của System Boundary)
# Kết nối với UC-04: Tư vấn qua Trợ lý AI
EXT_GROQ_X1 = 80
EXT_GROQ_Y1 = 700
EXT_GROQ_X2 = 280
EXT_GROQ_Y2 = 790
draw_external_actor(EXT_GROQ_X1, EXT_GROQ_Y1, EXT_GROQ_X2, EXT_GROQ_Y2, "Groq AI Service", "Llama 3.3 70B API", (16, 185, 129), (236, 253, 245), (4, 120, 87))

# External 2: Gmail SMTP Service (Nằm ở góc dưới cùng bên trái)
# Kết nối với UC-06 Đăng nhập / Quên MK & UC-16 Thông báo / Email
EXT_MAIL_X1 = 80
EXT_MAIL_Y1 = 820
EXT_MAIL_X2 = 280
EXT_MAIL_Y2 = 910
draw_external_actor(EXT_MAIL_X1, EXT_MAIL_Y1, EXT_MAIL_X2, EXT_MAIL_Y2, "Gmail SMTP Server", "spring.mail.host:587", (100, 116, 139), (241, 245, 249), (30, 41, 59))

# External 3: VNPay Payment Gateway (Nằm ở góc phải dưới bên ngoài)
# Kết nối với UC-11 Thanh toán Online
EXT_VNPAY_X1 = 2510
EXT_VNPAY_Y1 = 1180
EXT_VNPAY_X2 = 2710
EXT_VNPAY_Y2 = 1270
draw_external_actor(EXT_VNPAY_X1, EXT_VNPAY_Y1, EXT_VNPAY_X2, EXT_VNPAY_Y2, "VNPay Gateway", "Sandbox VPC Pay API", (245, 158, 11), (254, 243, 199), (180, 83, 9))


# 8. VẼ CÁC ĐƯỜNG LIÊN KẾT (ASSOCIATION LINES) KHÔNG CẮT CHÉO

# A. Guest Actor -> 6 Use Cases Guest (Cột 1)
for i in range(6):
    anch = GUEST_ANCHORS[i]
    draw.line([GUEST_ACT_X + 40, GUEST_ACT_Y - 10, anch[0], anch[1]], fill=(20, 184, 166), width=2)

# B. Member Actor -> 10 Use Cases Member (Cột 2)
# Nhờ Actor Generalization (Member kế thừa Guest), Member tự động hưởng trọn 6 Use Case Guest!
# Nối Member Actor với 10 Use Cases của Member
for i in range(10):
    anch = MEMBER_ANCHORS[i]
    draw.line([MEMBER_ACT_X + 40, MEMBER_ACT_Y - 20, anch[0], anch[1]], fill=(59, 130, 246), width=2)

# C. Admin Actor -> 10 Use Cases Admin (Cột 3)
for i in range(10):
    anch = ADMIN_ANCHORS[i]
    draw.line([anch[2], anch[1], ADMIN_ACT_X - 40, ADMIN_ACT_Y], fill=(236, 72, 153), width=2)

# D. External Actors Liên kết với Use Case tương ứng
# Groq AI Service -> UC-04 (Tư vấn qua Trợ lý AI)
draw.line([EXT_GROQ_X2, (EXT_GROQ_Y1 + EXT_GROQ_Y2)//2, GUEST_ANCHORS[3][0], GUEST_ANCHORS[3][1]], fill=(16, 185, 129), width=2)

# Gmail SMTP -> UC-06 (Đăng nhập & Quên mật khẩu)
draw.line([EXT_MAIL_X2, (EXT_MAIL_Y1 + EXT_MAIL_Y2)//2, GUEST_ANCHORS[5][0], GUEST_ANCHORS[5][1]], fill=(100, 116, 139), width=2)

# VNPay Gateway -> UC-11 (Thanh toán Online VNPay/MoMo)
draw.line([MEMBER_ANCHORS[4][2], MEMBER_ANCHORS[4][1], EXT_VNPAY_X1, (EXT_VNPAY_Y1 + EXT_VNPAY_Y2)//2], fill=(245, 158, 11), width=2)


# 9. BOTTOM FOOTER BAR (CHÚ GIẢI CHUẨN MỰC HỌC THUẬT)
LEG_Y1 = H - 75
LEG_Y2 = H - 35
draw.rectangle([BORDER_X1, LEG_Y1, BORDER_X2, LEG_Y2], fill=(248, 250, 252))
draw.line([BORDER_X1, LEG_Y1, BORDER_X2, LEG_Y1], fill=(226, 232, 240), width=2)

footer_notes = "Ghi chú: Khách Hàng Thành Viên kế thừa (Generalization) toàn bộ 6 Use Case công khai của Khách Vãng Lai  |  Phân quyền: Spring Security RBAC (ROLE_USER, ROLE_ADMIN)"
draw.text(((BORDER_X1 + BORDER_X2)//2, (LEG_Y1 + LEG_Y2)//2), footer_notes, fill=(71, 85, 105), font=get_font(16, bold=True), anchor="mm")

# Lưu hình ảnh
out1 = "Hinh_3.2_Overall_Use_Case_Diagram_YiYi_Book.png"
out2 = os.path.join("docs", "Hinh_3.2_Overall_Use_Case_Diagram_YiYi_Book.png")
img.save(out1, "PNG", dpi=(300, 300))
img.save(out2, "PNG", dpi=(300, 300))

print(f"Generated UML-compliant Hình 3.2 successfully: {out1} and {out2}")
print(f"Dimensions: {W}x{H} px (High Resolution 300 DPI)")

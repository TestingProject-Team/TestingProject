# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# HÌNH 3.1: SƠ ĐỒ NGỮ CẢNH HỆ THỐNG (SYSTEM CONTEXT DIAGRAM - LEVEL 0)
# Phân định ranh giới giữa YiYi Book, Người dùng và các Hệ thống/Dịch vụ Bên ngoài
# ==============================================================================
W, H = 2600, 1650
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
BORDER_X1, BORDER_Y1 = 50, 40
BORDER_X2, BORDER_Y2 = W - 50, H - 40

draw.rounded_rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y2], radius=14, outline=(190, 205, 220), width=3, fill=(255, 255, 255))

# Header của Diagram
HEADER_H = 85
draw.rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(238, 242, 255))
draw.line([BORDER_X1, BORDER_Y1 + HEADER_H, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(199, 210, 254), width=3)
draw.text(((BORDER_X1 + BORDER_X2) // 2, BORDER_Y1 + 42), 
          "SƠ ĐỒ NGỮ CẢNH HỆ THỐNG YIYI BOOK (SYSTEM CONTEXT DIAGRAM - LEVEL 0)", 
          fill=(30, 58, 138), font=get_font(34, bold=True), anchor="mm")

# Subtitle
SUB_Y = BORDER_Y1 + HEADER_H + 25
draw.text(((BORDER_X1 + BORDER_X2) // 2, SUB_Y),
          "Phân định rõ ranh giới hệ thống, các tác nhân người dùng tương tác và dịch vụ bên thứ ba (External Services)",
          fill=(75, 85, 99), font=get_font(21, bold=False), anchor="mm")

# 2. KHỐI TRUNG TÂM: HỆ THỐNG YIYI BOOK (CENTRAL SYSTEM)
SYS_W, SYS_H = 820, 880
SYS_X1 = (W - SYS_W) // 2
SYS_Y1 = 220
SYS_X2 = SYS_X1 + SYS_W
SYS_Y2 = SYS_Y1 + SYS_H

# Vẽ khung trung tâm nổi bật (Xanh Navy / Indigo)
draw.rounded_rectangle([SYS_X1, SYS_Y1, SYS_X2, SYS_Y2], radius=16, outline=(37, 99, 235), width=4, fill=(248, 250, 252))

# Header của Khối trung tâm
SYS_HDR_H = 110
draw.rounded_rectangle([SYS_X1, SYS_Y1, SYS_X2, SYS_Y1 + SYS_HDR_H], radius=16, outline=(37, 99, 235), width=4, fill=(30, 64, 175))
draw.rectangle([SYS_X1, SYS_Y1 + SYS_HDR_H - 12, SYS_X2, SYS_Y1 + SYS_HDR_H], fill=(30, 64, 175))
draw.text(((SYS_X1 + SYS_X2)//2, SYS_Y1 + 40), "HỆ THỐNG NHÀ SÁCH TRỰC TUYẾN YIYI BOOK", fill=(255, 255, 255), font=get_font(26, bold=True), anchor="mm")
draw.text(((SYS_X1 + SYS_X2)//2, SYS_Y1 + 78), "(YiYi Book Core E-Commerce & Management System)", fill=(191, 219, 254), font=get_font(18, bold=False), anchor="mm")

# Các module chức năng bên trong khối trung tâm
CORE_MODULES = [
    ("Storefront Portal (React.js SPA)", "Giao diện khách hàng: Duyệt sách, giỏ hàng, đặt hàng & thanh toán", (239, 246, 255), (59, 130, 246), (30, 64, 175)),
    ("Admin Management Portal", "Cổng quản trị: Quản lý catalog, đơn hàng, người dùng, khuyến mãi", (245, 243, 255), (139, 92, 246), (109, 40, 217)),
    ("Spring Boot Core Backend API", "Xử lý Business Logic, REST API endpoints, JWT Security & RBAC", (254, 243, 199), (245, 158, 11), (180, 83, 9)),
    ("AI Recommendation & RAG Engine", "Tích hợp RAG phân tích ngữ nghĩa, sinh câu trả lời tư vấn sách", (236, 253, 245), (16, 185, 129), (4, 120, 87)),
    ("Order, Payment & Reward Services", "Xử lý đơn hàng, coupon, tích điểm thưởng và điều phối thanh toán", (254, 226, 226), (239, 68, 68), (185, 28, 28)),
    ("Relational Database & Storage Engine", "Lưu trữ dữ liệu quan hệ ACID: MySQL/PostgreSQL & File Cloud", (241, 245, 249), (100, 116, 139), (30, 41, 59))
]

MOD_START_Y = SYS_Y1 + SYS_HDR_H + 20
MOD_H = 105
MOD_GAP = 16
for m_idx, (m_title, m_desc, m_bg, m_border, m_tcol) in enumerate(CORE_MODULES):
    my = MOD_START_Y + m_idx * (MOD_H + MOD_GAP)
    mx1 = SYS_X1 + 25
    mx2 = SYS_X2 - 25
    draw.rounded_rectangle([mx1, my, mx2, my + MOD_H], radius=8, outline=m_border, width=2, fill=m_bg)
    draw.text((mx1 + 20, my + 30), m_title, fill=m_tcol, font=get_font(21, bold=True))
    draw.text((mx1 + 20, my + 65), m_desc, fill=(71, 85, 105), font=get_font(16, bold=False))

# 3. CÁC TÁC NHÂN NGƯỜI DÙNG (ACTORS - CỘT BÊN TRÁI)
ACTOR_W = 460
ACTOR_H = 250
ACTOR_X = BORDER_X1 + 40

ACTORS = [
    {
        "role": "KHÁCH VÃNG LAI (GUEST)",
        "sub": "Chưa đăng nhập hệ thống",
        "y": 220,
        "bg": (240, 253, 250),
        "border": (20, 184, 166),
        "tcol": (15, 118, 110),
        "actions": [
            "• Duyệt danh mục & xem chi tiết sách",
            "• Tìm kiếm & lọc sách đa tiêu chí",
            "• Hỏi đáp tư vấn cơ bản với AI Assistant",
            "• Đăng ký tài khoản thành viên mới"
        ]
    },
    {
        "role": "KHÁCH HÀNG (MEMBER)",
        "sub": "Đã đăng nhập xác thực JWT",
        "y": 525,
        "bg": (239, 246, 255),
        "border": (59, 130, 246),
        "tcol": (30, 64, 175),
        "actions": [
            "• Quản lý giỏ hàng & địa chỉ giao hàng",
            "• Đặt hàng & Áp dụng coupon / điểm thưởng",
            "• Thanh toán trực tuyến qua VNPAY/MoMo",
            "• Theo dõi đơn hàng & Đánh giá sách"
        ]
    },
    {
        "role": "QUẢN TRỊ VIÊN (ADMIN)",
        "sub": "Có quyền Administrator / Staff",
        "y": 830,
        "bg": (253, 242, 248),
        "border": (236, 72, 153),
        "tcol": (190, 24, 93),
        "actions": [
            "• Quản lý kho sách, tác giả, danh mục",
            "• Cập nhật trạng thái đơn & vận chuyển",
            "• Quản lý mã giảm giá, banner, tin tức",
            "• Phân quyền RBAC & Xem báo cáo thống kê"
        ]
    }
]

for act in ACTORS:
    ay = act["y"]
    draw.rounded_rectangle([ACTOR_X, ay, ACTOR_X + ACTOR_W, ay + ACTOR_H], radius=10, outline=act["border"], width=3, fill=act["bg"])
    
    # Header tác nhân
    draw.rounded_rectangle([ACTOR_X, ay, ACTOR_X + ACTOR_W, ay + 65], radius=10, outline=act["border"], width=3, fill=act["bg"])
    draw.rectangle([ACTOR_X, ay + 55, ACTOR_X + ACTOR_W, ay + 65], fill=act["bg"])
    draw.line([ACTOR_X, ay + 65, ACTOR_X + ACTOR_W, ay + 65], fill=act["border"], width=2)
    
    draw.text((ACTOR_X + 20, ay + 24), act["role"], fill=act["tcol"], font=get_font(20, bold=True))
    draw.text((ACTOR_X + 20, ay + 48), act["sub"], fill=(100, 116, 139), font=get_font(15, bold=False))
    
    # Danh sách hành động
    for a_idx, act_line in enumerate(act["actions"]):
        draw.text((ACTOR_X + 20, ay + 80 + a_idx * 38), act_line, fill=(30, 41, 59), font=get_font(16, bold=False))

# 4. CÁC HỆ THỐNG / DỊCH VỤ BÊN NGOÀI (EXTERNAL SERVICES - CỘT BÊN PHẢI)
EXT_W = 460
EXT_H = 250
EXT_X = BORDER_X2 - 40 - EXT_W

EXTERNALS = [
    {
        "name": "PAYMENT GATEWAY (VNPAY / MOMO)",
        "sub": "Cổng thanh toán điện tử trực tuyến",
        "y": 220,
        "bg": (254, 243, 199),
        "border": (245, 158, 11),
        "tcol": (180, 83, 9),
        "flows": [
            "• Nhận yêu cầu khởi tạo URL thanh toán",
            "• Xử lý giao dịch thẻ / quét mã QR an toàn",
            "• Gửi IPN Webhook & Kết quả giao dịch",
            "• Đối soát và hoàn tiền khi hủy đơn"
        ]
    },
    {
        "name": "AI LLM SERVICE (GEMINI / OPENAI)",
        "sub": "Dịch vụ mô hình ngôn ngữ lớn AI",
        "y": 525,
        "bg": (236, 253, 245),
        "border": (16, 185, 129),
        "tcol": (4, 120, 87),
        "flows": [
            "• Tiếp nhận prompt ngữ cảnh và câu hỏi",
            "• Trích xuất thông tin sách qua RAG Pipeline",
            "• Sinh câu trả lời tư vấn tự nhiên, thân thiện",
            "• Gợi ý sách phù hợp sở thích độc giả"
        ]
    },
    {
        "name": "EMAIL SERVICE & CLOUD STORAGE",
        "sub": "Gmail SMTP & Cloudinary CDN",
        "y": 830,
        "bg": (241, 245, 249),
        "border": (100, 116, 139),
        "tcol": (30, 41, 59),
        "flows": [
            "• Gửi email xác nhận đặt hàng & hóa đơn",
            "• Gửi email thông báo đổi trạng thái đơn",
            "• Lưu trữ và phân phối hình ảnh bìa sách CDN",
            "• Tối ưu hóa tải ảnh và bảo mật media asset"
        ]
    }
]

for ext in EXTERNALS:
    ey = ext["y"]
    draw.rounded_rectangle([EXT_X, ey, EXT_X + EXT_W, ey + EXT_H], radius=10, outline=ext["border"], width=3, fill=ext["bg"])
    
    # Header external
    draw.rounded_rectangle([EXT_X, ey, EXT_X + EXT_W, ey + 65], radius=10, outline=ext["border"], width=3, fill=ext["bg"])
    draw.rectangle([EXT_X, ey + 55, EXT_X + EXT_W, ey + 65], fill=ext["bg"])
    draw.line([EXT_X, ey + 65, EXT_X + EXT_W, ey + 65], fill=ext["border"], width=2)
    
    draw.text((EXT_X + 20, ey + 24), ext["name"], fill=ext["tcol"], font=get_font(19, bold=True))
    draw.text((EXT_X + 20, ey + 48), ext["sub"], fill=(100, 116, 139), font=get_font(15, bold=False))
    
    # Danh sách luồng tương tác
    for f_idx, flow_line in enumerate(ext["flows"]):
        draw.text((EXT_X + 20, ey + 80 + f_idx * 38), flow_line, fill=(30, 41, 59), font=get_font(16, bold=False))

# 5. VẼ MŨI TÊN KẾT NỐI HAI CHIỀU & NHÃN LUỒNG DỮ LIỆU
def draw_bidirectional_arrow(x1, y1, x2, y2, label_req, label_res, col=(59, 130, 246)):
    # Đường chính
    draw.line([x1, y1, x2, y2], fill=col, width=4)
    # Mũi tên trái / nguồn
    draw.polygon([(x1, y1), (x1 + 14, y1 - 8), (x1 + 14, y1 + 8)], fill=col)
    # Mũi tên phải / đích
    draw.polygon([(x2, y2), (x2 - 14, y2 - 8), (x2 - 14, y2 + 8)], fill=col)
    
    # Nhãn yêu cầu (trên) và phản hồi (dưới)
    mid_x = (x1 + x2) // 2
    draw.rounded_rectangle([mid_x - 170, y1 - 32, mid_x + 170, y1 - 4], radius=5, fill=(255, 255, 255), outline=col, width=1)
    draw.text((mid_x, y1 - 18), label_req, fill=col, font=get_font(14, bold=True), anchor="mm")
    
    draw.rounded_rectangle([mid_x - 170, y1 + 4, mid_x + 170, y1 + 32], radius=5, fill=(255, 255, 255), outline=col, width=1)
    draw.text((mid_x, y1 + 18), label_res, fill=(100, 116, 139), font=get_font(14, bold=False), anchor="mm")

# Nối từ Tác nhân (Trái) sang Hệ thống (Giữa)
# 1. Guest -> System
draw_bidirectional_arrow(ACTOR_X + ACTOR_W, 345, SYS_X1, 345, "HTTP GET: Catalog / Search", "JSON / HTML UI Response", (20, 184, 166))
# 2. Member -> System
draw_bidirectional_arrow(ACTOR_X + ACTOR_W, 650, SYS_X1, 650, "POST: Order / Auth / Review", "JWT Token / Order Info", (59, 130, 246))
# 3. Admin -> System
draw_bidirectional_arrow(ACTOR_X + ACTOR_W, 955, SYS_X1, 955, "CRUD: Books / Orders / Users", "Admin Data / Status Reports", (236, 72, 153))

# Nối từ Hệ thống (Giữa) sang External Services (Phải)
# 1. System -> Payment Gateway
draw_bidirectional_arrow(SYS_X2, 345, EXT_X, 345, "Create Payment URL / Payload", "IPN Webhook / Trans Status", (245, 158, 11))
# 2. System -> AI LLM Service
draw_bidirectional_arrow(SYS_X2, 650, EXT_X, 650, "Prompt + Book Context", "AI Completion / Suggestions", (16, 185, 129))
# 3. System -> Email & Cloud CDN
draw_bidirectional_arrow(SYS_X2, 955, EXT_X, 955, "Send Order Mail / Upload Img", "Delivery Status / Secure URL", (100, 116, 139))

# 6. KHUNG CHÚ THÍCH CÔNG NGHỆ BÊN DƯỚI (BOTTOM SUMMARY BAR)
TECH_Y1 = H - 195
TECH_Y2 = H - 65
draw.rectangle([BORDER_X1, TECH_Y1, BORDER_X2, TECH_Y2], fill=(248, 250, 252))
draw.line([BORDER_X1, TECH_Y1, BORDER_X2, TECH_Y1], fill=(226, 232, 240), width=2)

tech_col_w = (BORDER_X2 - BORDER_X1 - 80) // 3
tech_cards = [
    ("GIAO THỨC & BẢO MẬT (SECURITY)", "REST API qua HTTPS, JWT Authentication, Spring Security RBAC, CORS Protection, Input Sanitization."),
    ("TÍCH HỢP THANH TOÁN & AI (INTEGRATION)", "VNPAY Sandbox / MoMo API (HMAC SHA512 Signature), Google Gemini 1.5 Pro / OpenAI API qua Spring REST Client."),
    ("LƯU TRỮ & VẬN HÀNH (INFRASTRUCTURE)", "MySQL Database, Spring Data JPA, Cloudinary Media CDN, Dockerized Services & GitHub Actions CI/CD.")
]

for t_idx, (t_title, t_desc, ) in enumerate(tech_cards):
    tc_x1 = BORDER_X1 + 25 + t_idx * (tech_col_w + 15)
    tc_x2 = tc_x1 + tech_col_w
    draw.rounded_rectangle([tc_x1, TECH_Y1 + 15, tc_x2, TECH_Y2 - 15], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((tc_x1 + 16, TECH_Y1 + 35), t_title, fill=(30, 58, 138), font=get_font(16, bold=True))
    
    # 2 dòng mô tả
    words = t_desc.split()
    line1 = " ".join(words[:9])
    line2 = " ".join(words[9:])
    draw.text((tc_x1 + 16, TECH_Y1 + 65), line1, fill=(71, 85, 105), font=get_font(14, bold=False))
    draw.text((tc_x1 + 16, TECH_Y1 + 88), line2, fill=(71, 85, 105), font=get_font(14, bold=False))

# Lưu ảnh
out1 = "Hinh_3.1_System_Context_Diagram_YiYi_Book.png"
out2 = os.path.join("docs", "Hinh_3.1_System_Context_Diagram_YiYi_Book.png")
img.save(out1, "PNG", dpi=(300, 300))
img.save(out2, "PNG", dpi=(300, 300))

print(f"Generated Hình 3.1 successfully: {out1} and {out2}")
print(f"Dimensions: {W}x{H} px (High Resolution 300 DPI)")

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

def draw_arrow(draw, start, end, fill=(51, 65, 85), width=4, arrow_size=14, dashed=False):
    x1, y1 = start
    x2, y2 = end
    if dashed:
        dist = math.hypot(x2 - x1, y2 - y1)
        dash_len = 12
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

def draw_header(draw, title, subtitle, W=2000):
    f_title = get_font(38, bold=True)
    f_sub = get_font(24, bold=False)
    draw.text((W // 2, 50), title, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W // 2, 95), subtitle, fill=(71, 85, 105), font=f_sub, anchor="mm")
    draw.line([(60, 130), (W - 60, 130)], fill=(203, 213, 225), width=3)

def draw_large_card(draw, box, title, sub="", color_type="blue", r=10):
    x1, y1, x2, y2 = box
    color_map = {
        "blue":    ((239, 246, 255), (37, 99, 235),  (30, 64, 175),  (29, 78, 216)),
        "indigo":  ((238, 242, 255), (79, 70, 229),  (49, 46, 129),  (67, 56, 202)),
        "purple":  ((250, 245, 255), (147, 51, 234), (107, 33, 168), (126, 34, 206)),
        "amber":   ((255, 251, 235), (217, 119, 6),  (146, 64, 14),  (180, 83, 9)),
        "teal":    ((240, 253, 250), (13, 148, 136), (17, 94, 89),   (15, 118, 110)),
        "emerald": ((240, 253, 244), (16, 185, 129), (22, 101, 52),  (5, 150, 105)),
        "slate":   ((248, 250, 252), (100, 116, 139), (30, 41, 59),  (51, 65, 85)),
        "dark":    ((241, 245, 249), (71, 85, 105),  (15, 23, 42),   (30, 41, 59)),
        "red":     ((254, 242, 242), (220, 38, 38),  (153, 27, 27),  (185, 28, 28))
    }
    bg, border, text_c, sub_c = color_map.get(color_type, color_map["blue"])
    
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=bg, outline=border, width=3)
    
    cx = (x1 + x2) // 2
    f_t = get_font(26, bold=True)
    f_s = get_font(20, bold=False)
    
    if sub:
        lines = sub.split('\n')
        if len(lines) == 1:
            draw.text((cx, y1 + (y2 - y1) * 0.35), title, fill=text_c, font=f_t, anchor="mm")
            draw.line([(x1 + 15, y1 + (y2 - y1) * 0.55), (x2 - 15, y1 + (y2 - y1) * 0.55)], fill=border, width=2)
            draw.text((cx, y1 + (y2 - y1) * 0.75), sub, fill=sub_c, font=f_s, anchor="mm")
        else:
            draw.text((cx, y1 + 32), title, fill=text_c, font=f_t, anchor="mm")
            draw.line([(x1 + 15, y1 + 54), (x2 - 15, y1 + 54)], fill=border, width=2)
            curr_y = y1 + 68
            for l in lines:
                draw.text((x1 + 20, curr_y), l, fill=sub_c, font=f_s)
                curr_y += 26
    else:
        cy = (y1 + y2) // 2
        draw.text((cx, cy), title, fill=text_c, font=f_t, anchor="mm")

# =========================================================================
# 1. HÌNH 2.1: AGILE / SCRUM WORKFLOW - EXTRA LARGE FONT
# =========================================================================
def render_hinh_2_1():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "QUY TRÌNH PHÁT TRIỂN PHẦN MỀM AGILE / SCRUM — YIYI BOOK", 
                "Chu trình lặp Sprint, quản lý tiến độ và kiểm thử liên tục kết hợp CI/CD Pipeline", W)
    
    # Top Row: Product Backlog -> Sprint Planning
    draw_large_card(draw, [100, 160, 940, 290], "1. PRODUCT BACKLOG", "Quản lý User Stories & Danh mục yêu cầu (SRS)", "teal")
    draw_arrow(draw, (940, 225), (1060, 225), width=5, arrow_size=16)
    draw_large_card(draw, [1060, 160, 1900, 290], "2. SPRINT PLANNING", "Cam kết Sprint Goal & Phân chia công việc chi tiết", "blue")
    
    draw_arrow(draw, (1480, 290), (1480, 360), width=5, arrow_size=16)
    
    # Sprint Box Container
    draw.rounded_rectangle([100, 360, 1900, 880], radius=14, fill=(255, 255, 255), outline=(148, 163, 184), width=3)
    draw.text((140, 395), "VÒNG LẶP SPRINT (SPRINT EXECUTION)", fill=(30, 41, 59), font=get_font(28, bold=True))
    
    # Sprint Inner: Row 1
    draw_large_card(draw, [140, 440, 680, 600], "3. DESIGN & UI/UX", "Thiết kế giao diện & Đặc tả API", "purple")
    draw_arrow(draw, (680, 520), (750, 520), width=4, arrow_size=14)
    draw_large_card(draw, [750, 440, 1290, 600], "4. DEVELOPMENT", "React Frontend & Spring Boot Backend", "blue")
    draw_arrow(draw, (1290, 520), (1360, 520), width=4, arrow_size=14)
    draw_large_card(draw, [1360, 440, 1860, 600], "5. AUTOMATED TEST", "JUnit 5 Unit Tests & Newman API Suite", "emerald")
    
    draw_arrow(draw, (1610, 600), (1610, 680), width=4, arrow_size=14)
    
    # Sprint Inner: Row 2
    draw_large_card(draw, [140, 680, 960, 840], "7. CONTINUOUS INTEGRATION", "GitHub Actions CI & Docker Build tự động", "indigo")
    draw_arrow(draw, (1360, 760), (960, 760), width=4, arrow_size=14)
    draw_large_card(draw, [1040, 680, 1860, 840], "6. CODE REVIEW & QUALITY", "GitHub Pull Request & Phân tích tĩnh", "amber")
    
    draw_arrow(draw, (550, 840), (550, 940), width=5, arrow_size=16)
    
    # Bottom Row: Review -> Retrospective -> Next Iteration
    draw_large_card(draw, [100, 940, 660, 1080], "8. SPRINT REVIEW & DEMO", "Nghiệm thu tính năng hoàn thành", "teal")
    draw_arrow(draw, (660, 1010), (740, 1010), width=5, arrow_size=16)
    draw_large_card(draw, [740, 940, 1300, 1080], "9. SPRINT RETROSPECTIVE", "Đánh giá & Rút kinh nghiệm quy trình", "blue")
    draw_arrow(draw, (1300, 1010), (1380, 1010), width=5, arrow_size=16)
    draw_large_card(draw, [1380, 940, 1900, 1080], "10. NEXT ITERATION", "Lập kế hoạch Sprint tiếp theo", "purple")
    
    # Feedback loop line
    draw_arrow(draw, (1640, 1080), (1640, 1180), width=4, arrow_size=0, dashed=True)
    draw_arrow(draw, (1640, 1180), (60, 1180), width=4, arrow_size=0, dashed=True)
    draw_arrow(draw, (60, 1180), (60, 225), width=4, arrow_size=0, dashed=True)
    draw_arrow(draw, (60, 225), (100, 225), width=4, arrow_size=16, dashed=True)
    
    draw.text((W // 2, 1240), "Nguyên tắc kỹ thuật: Quản lý nhánh Git-flow • Review Code nghiêm ngặt • Kiểm thử tự động liên tục", 
              fill=(71, 85, 105), font=get_font(22, bold=True), anchor="mm")
    
    return img

# =========================================================================
# 2. HÌNH 4.3: BACKEND LAYERED ARCHITECTURE - 3 COLS CLEAR FONT
# =========================================================================
def render_hinh_4_3():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "KIẾN TRÚC PHÂN TẦNG BACKEND (SPRING BOOT 3) — YIYI BOOK", 
                "Mô hình phân tầng kiến trúc chuẩn Enterprise: Presentation, Security, Service, Persistence & External", W)
    
    # Left Column: Client & Security
    draw.rounded_rectangle([80, 160, 520, 1180], radius=14, fill=(255, 255, 255), outline=(148, 163, 184), width=3)
    draw.text((300, 205), "CLIENT & SECURITY", fill=(30, 41, 59), font=get_font(26, bold=True), anchor="mm")
    
    draw_large_card(draw, [110, 250, 490, 420], "React Frontend", "Storefront & Admin UI\nVite SPA Client", "teal")
    draw_arrow(draw, (300, 420), (300, 490), width=4, arrow_size=14)
    draw_large_card(draw, [110, 490, 490, 660], "Axios Client", "JWT Bearer Interceptor\nREST API Caller", "blue")
    draw_arrow(draw, (300, 660), (300, 730), width=4, arrow_size=14)
    draw_large_card(draw, [110, 730, 490, 900], "Spring Security", "JwtAuthFilter & RBAC\nStateless Session", "purple")
    draw_arrow(draw, (300, 900), (300, 970), width=4, arrow_size=14)
    draw_large_card(draw, [110, 970, 490, 1140], "Security Config", "CORS & BCrypt Encoder\nProtected Endpoints", "slate")
    
    draw_arrow(draw, (520, 575), (600, 575), width=5, arrow_size=16)
    
    # Center Column: Core Backend 4 Tiers
    draw.rounded_rectangle([600, 160, 1420, 1180], radius=14, fill=(240, 249, 255), outline=(37, 99, 235), width=3)
    draw.text((1010, 205), "CORE BACKEND TIERS", fill=(30, 41, 59), font=get_font(26, bold=True), anchor="mm")
    
    draw_large_card(draw, [640, 250, 1380, 420], "1. CONTROLLER LAYER (23 Lớp)", "Tiếp nhận HTTP JSON Requests (Auth, Book, Cart, Order, Admin...)", "blue")
    draw_arrow(draw, (1010, 420), (1010, 490), width=5, arrow_size=16)
    draw_large_card(draw, [640, 490, 1380, 660], "2. SERVICE LAYER (15 Lớp)", "Xử lý Business Logic, Tính toán giá, Điểm thưởng & @Transactional", "indigo")
    draw_arrow(draw, (1010, 660), (1010, 730), width=5, arrow_size=16)
    draw_large_card(draw, [640, 730, 1380, 900], "3. REPOSITORY LAYER (19 Lớp)", "Spring Data JPA & Hibernate ORM Truy xuất cơ sở dữ liệu quan hệ", "teal")
    draw_arrow(draw, (1010, 900), (1010, 970), width=5, arrow_size=16)
    draw_large_card(draw, [640, 970, 1380, 1140], "4. DATABASE LAYER (21 Bảng + 4 Enums)", "Hệ quản trị CSDL quan hệ PostgreSQL lưu trữ bền vững (ACID)", "dark")
    
    draw_arrow(draw, (1420, 575), (1500, 575), width=5, arrow_size=16)
    
    # Right Column: External & Runtime
    draw.rounded_rectangle([1500, 160, 1920, 1180], radius=14, fill=(255, 255, 255), outline=(148, 163, 184), width=3)
    draw.text((1710, 205), "EXTERNAL & RUNTIME", fill=(30, 41, 59), font=get_font(26, bold=True), anchor="mm")
    
    draw_large_card(draw, [1530, 250, 1890, 430], "VNPAY Sandbox", "Cổng thanh toán Online\nHMAC-SHA512 Checksum", "amber")
    draw_large_card(draw, [1530, 490, 1890, 670], "Groq Cloud AI", "Llama 3.3 70B Model\nServer-Sent Events (SSE)", "emerald")
    draw_large_card(draw, [1530, 730, 1890, 910], "SMTP Mail Server", "Gửi email thông báo\nKích hoạt & Đơn hàng", "teal")
    draw_large_card(draw, [1530, 970, 1890, 1140], "Docker Container", "Docker Compose Runtime\nPostgreSQL & Backend App", "slate")
    
    return img

# =========================================================================
# 3. HÌNH 4.4: AI RAG & INTENT FLOW - CLEAR LARGE FONT
# =========================================================================
def render_hinh_4_4():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "KIẾN TRÚC TRỢ LÝ ẢO YIYI AI VÀ LUỒNG XỬ LÝ MINI-RAG", 
                "Quy trình phân tích ý định (Intent), trích xuất ngữ cảnh kho sách và suy luận mô hình ngôn ngữ", W)
    
    # Row 1: Flow 1 -> 4
    draw_large_card(draw, [80, 180, 480, 360], "1. KHÁCH HÀNG", "Nhập câu hỏi tự nhiên\ntìm kiếm hoặc tư vấn sách", "teal")
    draw_arrow(draw, (480, 270), (560, 270), width=5, arrow_size=16)
    
    draw_large_card(draw, [560, 180, 960, 360], "2. AICHATWIDGET UI", "Quản lý hộp thoại chat &\nLưu lịch sử hội thoại", "blue")
    draw_arrow(draw, (960, 270), (1040, 270), width=5, arrow_size=16)
    
    draw_large_card(draw, [1040, 180, 1440, 360], "3. INTENT DETECTION", "Nhận diện mục đích câu hỏi\n(8 nhóm Intent phân loại)", "purple")
    draw_arrow(draw, (1440, 270), (1520, 270), width=5, arrow_size=16)
    
    draw_large_card(draw, [1520, 180, 1920, 360], "4. MINI-RAG RETRIEVAL", "Trích xuất danh mục sách\nthực tế phù hợp làm Context", "emerald")
    
    draw_arrow(draw, (1720, 360), (1720, 480), width=5, arrow_size=16)
    
    # Row 2: Flow 5 -> 8 (Right to Left)
    draw_large_card(draw, [1480, 480, 1920, 660], "5. PROMPT BUILDER", "Ghép kho sách + Bộ nhớ User\nvào System Prompt chuẩn", "amber")
    draw_arrow(draw, (1480, 570), (1400, 570), width=5, arrow_size=16)
    
    draw_large_card(draw, [1000, 480, 1400, 660], "6. GROQ CLOUD API", "Mô hình Llama 3.3 70B\nInference tốc độ cao", "emerald")
    draw_arrow(draw, (1000, 570), (920, 570), width=5, arrow_size=16)
    
    draw_large_card(draw, [520, 480, 920, 660], "7. STREAMING PARSER", "Giải mã luồng dữ liệu chunk\nServer-Sent Events (SSE)", "blue")
    draw_arrow(draw, (520, 570), (440, 570), width=5, arrow_size=16)
    
    draw_large_card(draw, [80, 480, 440, 660], "8. MARKDOWN CARDS", "Render câu trả lời tức thì +\nThẻ sách kèm giá & liên kết", "teal")
    
    draw_arrow(draw, (260, 660), (260, 760), width=5, arrow_size=16)
    
    # User Action Box
    draw_large_card(draw, [80, 760, 1920, 890], "Khách Hàng Đọc Gợi Ý Tư Vấn & Nhấn Mở Xem Chi Tiết / Thêm Vào Giỏ Hàng", 
                    "Toàn bộ quy trình hoàn tất trực tiếp trên cửa sổ chat mà không cần chuyển trang", "blue")
    
    # Bottom 3 Principles
    draw_large_card(draw, [80, 960, 640, 1180], "ZERO HALLUCINATION", "Chỉ tư vấn và báo giá các đầu sách\nđang thực sự có trong cơ sở dữ liệu", "slate")
    draw_large_card(draw, [720, 960, 1280, 1180], "CLIENT PRIVACY", "Tuyệt đối không gửi thông tin tài khoản\nhoặc mật khẩu của người dùng lên LLM", "slate")
    draw_large_card(draw, [1360, 960, 1920, 1180], "GRACEFUL FALLBACK", "Tự động hiển thị hướng dẫn khi thiếu\nAPI Key hoặc dịch vụ mạng gián đoạn", "slate")
    
    return img

# =========================================================================
# 4. HÌNH 4.5: PACKAGE DIAGRAM - CLEAR LARGE FONT
# =========================================================================
def render_hinh_4_5():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ PHÂN RÃ GÓI PHẦN MỀM (PACKAGE DIAGRAM) — YIYI BOOK", 
                "Cấu trúc tổ chức thư mục mã nguồn khối Spring Boot Backend và React Frontend", W)
    
    # Top: Backend Box
    draw.rounded_rectangle([80, 160, 1920, 680], radius=14, fill=(240, 249, 255), outline=(37, 99, 235), width=3)
    draw.text((120, 205), "BACKEND PACKAGES: com.bookstore", fill=(30, 41, 59), font=get_font(28, bold=True))
    
    draw_large_card(draw, [120, 250, 520, 420], "controller", "23 REST Controllers\nXử lý API Endpoints", "blue")
    draw_large_card(draw, [570, 250, 970, 420], "service", "15 Business Services\nLogic & @Transactional", "indigo")
    draw_large_card(draw, [1020, 250, 1420, 420], "repository", "19 JPA Repositories\nTruy xuất PostgreSQL", "teal")
    draw_large_card(draw, [1470, 250, 1870, 420], "entity", "21 Bảng Dữ liệu +\n4 Miền giá trị Enums", "dark")
    
    draw_large_card(draw, [120, 470, 520, 640], "security", "JwtAuthFilter, JwtService\nUserDetailsService", "purple")
    draw_large_card(draw, [570, 470, 970, 640], "config", "SecurityConfig, WebConfig\nVNPayConfig, MoMoConfig", "slate")
    draw_large_card(draw, [1020, 470, 1420, 640], "dto", "Request & Response DTOs\nĐóng gói dữ liệu truyền tải", "amber")
    draw_large_card(draw, [1470, 470, 1870, 640], "utils & listener", "WebSocket Notification\nExcel Import Helper", "emerald")
    
    draw_arrow(draw, (1000, 680), (1000, 750), width=5, arrow_size=16)
    
    # Bottom: Frontend Box
    draw.rounded_rectangle([80, 750, 1920, 1220], radius=14, fill=(240, 253, 250), outline=(13, 148, 136), width=3)
    draw.text((120, 795), "FRONTEND STRUCTURE: src/", fill=(30, 41, 59), font=get_font(28, bold=True))
    
    draw_large_card(draw, [120, 840, 440, 1030], "pages", "Giao diện Khách hàng &\nQuản trị viên (43 Trang)", "teal")
    draw_large_card(draw, [480, 840, 800, 1030], "components", "Khối Layout, Thẻ sách,\nWidget Chat AI", "blue")
    draw_large_card(draw, [840, 840, 1160, 1030], "context", "AuthContext, CartContext,\nLanguageContext", "purple")
    draw_large_card(draw, [1200, 840, 1520, 1030], "services / api", "Axios Interceptor cấu hình\nGọi REST API Backend", "amber")
    draw_large_card(draw, [1560, 840, 1870, 1030], "locales & data", "Đa ngôn ngữ vi/en &\nBộ dữ liệu mẫu Seed Data", "emerald")
    
    draw.text((W // 2, 1120), "Giao tiếp toàn diện giữa React Frontend và Spring Boot Backend thực thi qua giao thức HTTP / JSON REST API", 
              fill=(71, 85, 105), font=get_font(22, bold=True), anchor="mm")
    
    return img

def render_and_save_all():
    print("Regenerating all architectural and state diagrams with LARGE high-visibility text...")
    
    from render_high_visibility_diagrams import (
        render_hinh_4_14_order_state,
        render_hinh_4_10a,
        render_hinh_4_10b,
        render_hinh_4_11,
        render_hinh_4_8,
        render_hinh_4_9
    )
    
    tasks = [
        ("Hinh_2.1_Agile_Scrum_Workflow_YiYi_Book", render_hinh_2_1),
        ("Hinh_4.3_Backend_Layered_Architecture", render_hinh_4_3),
        ("Hinh_4.4_AI_RAG_Intent_Flow_Architecture", render_hinh_4_4),
        ("Hinh_4.5_Package_Diagram_YiYi_Book", render_hinh_4_5),
        ("Hinh_4.14_Order_State_Diagram", render_hinh_4_14_order_state),
        ("Hinh_4.10a_Class_Diagram_BookDetail_Review", render_hinh_4_10a),
        ("Hinh_4.10b_Sequence_Diagram_BookDetail_Review", render_hinh_4_10b),
        ("Hinh_4.11_Sequence_Diagram_Cart_Management", render_hinh_4_11),
        ("Hinh_4.8_Sequence_Diagram_Product_List", render_hinh_4_8),
        ("Hinh_4.9_Sequence_Diagram_Search_Filter", render_hinh_4_9),
    ]
    
    for name, fn in tasks:
        img = fn()
        for out_dir in [INFO_REV_DIR, STD_REV_DIR, INFO_DIR, STD_DIR]:
            out_p = os.path.join(out_dir, name + ".png")
            img.save(out_p, dpi=(300, 300))
            print(f"  -> Saved large text diagram: {out_p}")

if __name__ == "__main__":
    render_and_save_all()

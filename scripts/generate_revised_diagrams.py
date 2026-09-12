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

# =========================================================================
# 1. HÌNH 2.1: AGILE / SCRUM WORKFLOW
# =========================================================================
def render_hinh_2_1(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "QUY TRÌNH PHÁT TRIỂN PHẦN MỀM AGILE / SCRUM", "Chu trình lặp Sprint, kiểm thử liên tục và tích hợp CI/CD", W)

    # Top Row: Product Backlog -> Sprint Planning
    draw_card(draw, [120, 160, 950, 270], "1. PRODUCT BACKLOG", "Quản lý User Stories & Yêu cầu (SRS)", style, "teal")
    draw_arrow(draw, (950, 215), (1050, 215), width=4, arrow_size=14)
    draw_card(draw, [1050, 160, 1880, 270], "2. SPRINT PLANNING", "Cam kết Sprint Goal & Phân chia công việc", style, "blue")

    draw_arrow(draw, (1465, 270), (1465, 340), width=4, arrow_size=14)

    # Enclosed Container: SPRINT EXECUTION
    draw.rounded_rectangle([120, 340, 1880, 850], radius=14, fill=(250, 250, 252) if style == "infographic" else (255, 255, 255), outline=(148, 163, 184), width=2)
    f_hdr = get_font(26, bold=True)
    draw.text((150, 370), "VÒNG LẶP SPRINT (SPRINT EXECUTION)", fill=(30, 41, 59), font=f_hdr)

    # Inside Sprint Grid: Row 1 (Design -> Dev -> Test)
    draw_card(draw, [160, 420, 680, 560], "3. DESIGN & ARCHITECTURE", "Thiết kế UI/UX & API Contract", style, "purple")
    draw_arrow(draw, (680, 490), (760, 490), width=3, arrow_size=12)
    draw_card(draw, [760, 420, 1280, 560], "4. DEVELOPMENT", "React Frontend & Spring Boot Backend", style, "blue")
    draw_arrow(draw, (1280, 490), (1360, 490), width=3, arrow_size=12)
    draw_card(draw, [1360, 420, 1840, 560], "5. AUTOMATED TESTING", "JUnit 5 Unit Tests & Newman API Tests", style, "emerald")

    draw_arrow(draw, (1600, 560), (1600, 650), width=3, arrow_size=12)

    # Inside Sprint Grid: Row 2 (Code Review <- CI/CD)
    draw_card(draw, [160, 650, 980, 790], "7. CONTINUOUS INTEGRATION", "GitHub Actions CI & Docker Build", style, "indigo" if style == "infographic" else "slate")
    draw_arrow(draw, (1360, 720), (980, 720), width=3, arrow_size=12)
    draw_card(draw, [1060, 650, 1840, 790], "6. CODE REVIEW & QUALITY GATE", "GitHub Pull Request & Static Analysis", style, "amber")

    draw_arrow(draw, (570, 790), (570, 920), width=4, arrow_size=14)

    # Bottom Row: Review -> Retrospective -> Next Iteration
    draw_card(draw, [120, 920, 680, 1040], "8. SPRINT REVIEW & DEMO", "Nghiệm thu tính năng hoàn thành", style, "teal")
    draw_arrow(draw, (680, 980), (760, 980), width=4, arrow_size=14)
    draw_card(draw, [760, 920, 1320, 1040], "9. SPRINT RETROSPECTIVE", "Đánh giá và cải tiến quy trình", style, "blue")
    draw_arrow(draw, (1320, 980), (1400, 980), width=4, arrow_size=14)
    draw_card(draw, [1400, 920, 1880, 1040], "10. NEXT ITERATION", "Tái lập kế hoạch Sprint tiếp theo", style, "purple")

    # Loop line back
    draw_arrow(draw, (1640, 1040), (1640, 1160), width=3, arrow_size=0, dashed=True)
    draw_arrow(draw, (1640, 1160), (80, 1160), width=3, arrow_size=0, dashed=True)
    draw_arrow(draw, (80, 1160), (80, 215), width=3, arrow_size=0, dashed=True)
    draw_arrow(draw, (80, 215), (120, 215), width=3, arrow_size=12, dashed=True)

    # Footer cards
    f_lbl = get_font(20, bold=True)
    draw.text((W // 2, 1220), "Thực hành kỹ thuật: Git-flow • Code Review bắt buộc • Tự động hóa kiểm thử liên tục", fill=(71, 85, 105), font=f_lbl, anchor="mm")

# =========================================================================
# 2. HÌNH 4.3: BACKEND LAYERED ARCHITECTURE
# =========================================================================
def render_hinh_4_3(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "KIẾN TRÚC PHÂN TẦNG BACKEND (SPRING BOOT 3)", "Mô hình phân tầng, kiểm soát bảo mật và tích hợp dịch vụ", W)

    # Left Column: Frontend & Security
    draw.rounded_rectangle([100, 160, 520, 1180], radius=12, fill=(248, 250, 252) if style == "infographic" else (255, 255, 255), outline=(148, 163, 184), width=2)
    draw.text((310, 200), "CLIENT & SECURITY", fill=(30, 41, 59), font=get_font(26, bold=True), anchor="mm")
    
    draw_card(draw, [130, 250, 490, 400], "React Frontend", "Storefront & Admin UI", style, "teal")
    draw_arrow(draw, (310, 400), (310, 480), width=3, arrow_size=12)
    draw_card(draw, [130, 480, 490, 630], "Axios Client", "JWT Bearer Interceptor", style, "blue")
    draw_arrow(draw, (310, 630), (310, 710), width=3, arrow_size=12)
    draw_card(draw, [130, 710, 490, 860], "Spring Security", "JwtAuthFilter & RBAC", style, "purple")
    draw_arrow(draw, (310, 860), (310, 940), width=3, arrow_size=12)
    draw_card(draw, [130, 940, 490, 1120], "Web Security Config", "CORS & PasswordEncoder", style, "slate")

    draw_arrow(draw, (520, 550), (600, 550), width=4, arrow_size=14)

    # Center Column: Core 4 Layers
    draw.rounded_rectangle([600, 160, 1400, 1180], radius=12, fill=(240, 249, 255) if style == "infographic" else (255, 255, 255), outline=(59, 130, 246), width=2)
    draw.text((1000, 200), "CORE BACKEND TIERS", fill=(30, 41, 59), font=get_font(26, bold=True), anchor="mm")

    draw_card(draw, [640, 250, 1360, 410], "1. CONTROLLER LAYER", "REST API Endpoints (Auth, Book, Cart, Order, Admin...)", style, "blue")
    draw_arrow(draw, (1000, 410), (1000, 490), width=4, arrow_size=14)
    draw_card(draw, [640, 490, 1360, 660], "2. SERVICE LAYER", "Business Logic, Calculations & @Transactional", style, "indigo" if style == "infographic" else "slate")
    draw_arrow(draw, (1000, 660), (1000, 740), width=4, arrow_size=14)
    draw_card(draw, [640, 740, 1360, 910], "3. REPOSITORY LAYER", "Spring Data JPA & Hibernate ORM Queries", style, "teal")
    draw_arrow(draw, (1000, 910), (1000, 990), width=4, arrow_size=14)
    draw_card(draw, [640, 990, 1360, 1140], "4. DATABASE LAYER", "PostgreSQL Relational Storage (ACID)", style, "dark")

    draw_arrow(draw, (1400, 570), (1480, 570), width=4, arrow_size=14)

    # Right Column: External Services & Deployment
    draw.rounded_rectangle([1480, 160, 1900, 1180], radius=12, fill=(248, 250, 252) if style == "infographic" else (255, 255, 255), outline=(148, 163, 184), width=2)
    draw.text((1690, 200), "EXTERNAL & RUNTIME", fill=(30, 41, 59), font=get_font(26, bold=True), anchor="mm")

    draw_card(draw, [1510, 250, 1870, 430], "VNPAY Sandbox", "Cổng thanh toán Online", style, "amber")
    draw_card(draw, [1510, 480, 1870, 660], "Groq Cloud AI", "Llama 3.3 70B Stream API", style, "emerald")
    draw_card(draw, [1510, 710, 1870, 890], "SMTP Mail Server", "Email thông báo & đơn hàng", style, "teal")
    draw_card(draw, [1510, 940, 1870, 1120], "Docker Environment", "Docker Compose Container", style, "slate")

# =========================================================================
# 3. HÌNH 4.4: AI RAG & INTENT FLOW
# =========================================================================
def render_hinh_4_4(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "KIẾN TRÚC TRỢ LÝ ẢO YIYI AI VÀ LUỒNG MINI-RAG", "Quy trình phân tích Intent, trích xuất ngữ cảnh kho sách và xử lý LLM", W)

    # Flow Stages: Horizontal / 2-Row Compact Grid
    # Row 1: User -> Widget -> Intent Detector -> Mini-RAG
    draw_card(draw, [100, 200, 460, 360], "1. Khách Hàng (User)", "Nhập câu hỏi tìm / tư vấn sách", style, "teal")
    draw_arrow(draw, (460, 280), (560, 280), width=4, arrow_size=14)
    draw_card(draw, [560, 200, 940, 360], "2. AIChatWidget UI", "Quản lý hộp thoại & Lịch sử chat", style, "blue")
    draw_arrow(draw, (940, 280), (1040, 280), width=4, arrow_size=14)
    draw_card(draw, [1040, 200, 1420, 360], "3. Intent Detection", "Nhận diện mục đích (8 nhóm intent)", style, "purple")
    draw_arrow(draw, (1420, 280), (1520, 280), width=4, arrow_size=14)
    draw_card(draw, [1520, 200, 1900, 360], "4. Product Retrieval", "Client Mini-RAG lọc 5-10 sách", style, "emerald")

    draw_arrow(draw, (1710, 360), (1710, 520), width=4, arrow_size=14)

    # Row 2: Suggestions / Markdown <- Streaming <- Groq API <- Context Builder
    draw_card(draw, [1440, 520, 1900, 680], "5. Context Builder", "Ghép kho sách + User Memory", style, "amber")
    draw_arrow(draw, (1440, 600), (1340, 600), width=4, arrow_size=14)
    draw_card(draw, [960, 520, 1340, 680], "6. Groq Cloud API", "Llama 3.3 70B LLM Inference", style, "emerald")
    draw_arrow(draw, (960, 600), (860, 600), width=4, arrow_size=14)
    draw_card(draw, [480, 520, 860, 680], "7. Streaming Parser", "Giải mã Server-Sent Events (SSE)", style, "blue")
    draw_arrow(draw, (480, 600), (380, 600), width=4, arrow_size=14)
    draw_card(draw, [100, 520, 380, 680], "8. Markdown Cards", "Render câu trả lời + Thẻ sách", style, "teal")

    draw_arrow(draw, (240, 680), (240, 760), width=4, arrow_size=14)

    # Action back to User
    draw_card(draw, [100, 760, 1900, 880], "Khách Hàng Đọc Gợi Ý & Bấm Xem Chi Tiết / Thêm Vào Giỏ Hàng", "Phản hồi hoàn tất trực tiếp trên giao diện", style, "blue")

    # Bottom 3 Architecture Guarantees
    draw_card(draw, [100, 940, 650, 1160], "Zero Hallucination", "Chỉ tư vấn sách có trong kho thực tế", style, "slate")
    draw_card(draw, [725, 940, 1275, 1160], "Client-Side Privacy", "Không truyền thông tin nhạy cảm sang LLM", style, "slate")
    draw_card(draw, [1350, 940, 1900, 1160], "Graceful Fallback", "Tự động thông báo khi thiếu API Key", style, "slate")

# =========================================================================
# 4. HÌNH 4.5: PACKAGE DIAGRAM
# =========================================================================
def render_hinh_4_5(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ PHÂN RÃ GÓI PHẦN MỀM (PACKAGE DIAGRAM)", "Cấu trúc tổ chức mã nguồn Spring Boot Backend và React Frontend", W)

    # Top: Backend Package com.bookstore
    draw.rounded_rectangle([100, 160, 1900, 660], radius=14, fill=(240, 249, 255) if style == "infographic" else (255, 255, 255), outline=(59, 130, 246), width=2)
    draw.text((150, 200), "BACKEND PACKAGES: com.bookstore", fill=(30, 41, 59), font=get_font(26, bold=True))

    draw_card(draw, [140, 240, 520, 360], "controller", "23 REST Controllers", style, "blue")
    draw_card(draw, [580, 240, 960, 360], "service", "15 Business Services", style, "indigo" if style == "infographic" else "slate")
    draw_card(draw, [1020, 240, 1420, 360], "repository", "19 JPA Repositories", style, "teal")
    draw_card(draw, [1480, 240, 1860, 360], "entity", "21 Tables + 4 Enums", style, "dark")

    draw_card(draw, [140, 420, 520, 540], "security", "JwtAuthFilter, JwtService", style, "purple")
    draw_card(draw, [580, 420, 960, 540], "config", "Security, Web, VNPAY", style, "slate")
    draw_card(draw, [1020, 420, 1420, 540], "dto", "Request & Response DTOs", style, "amber")
    draw_card(draw, [1480, 420, 1860, 540], "listener & utils", "WebSocket, ExcelHelper", style, "emerald")

    draw_arrow(draw, (1000, 660), (1000, 740), width=4, arrow_size=14)

    # Bottom: Frontend Structure src/
    draw.rounded_rectangle([100, 740, 1900, 1180], radius=14, fill=(240, 253, 250) if style == "infographic" else (255, 255, 255), outline=(20, 184, 166), width=2)
    draw.text((150, 780), "FRONTEND STRUCTURE: src/", fill=(30, 41, 59), font=get_font(26, bold=True))

    draw_card(draw, [140, 820, 460, 950], "pages", "Storefront & Admin Views", style, "teal")
    draw_card(draw, [500, 820, 820, 950], "components", "Common, Layout & AI Chat", style, "blue")
    draw_card(draw, [860, 820, 1180, 950], "context", "Auth, Cart, Language", style, "purple")
    draw_card(draw, [1220, 820, 1540, 950], "services/api", "Axios Interceptors", style, "amber")
    draw_card(draw, [1580, 820, 1860, 950], "locales & data", "i18n vi/en, Seed Data", style, "emerald")

    f_foot = get_font(20, bold=True)
    draw.text((W // 2, 1060), "Giao tiếp giữa Frontend và Backend thực hiện hoàn toàn qua HTTP / JSON REST API", fill=(71, 85, 105), font=f_foot, anchor="mm")

# =========================================================================
# 5. HÌNH 4.6: SIMPLIFIED ERD (RELATIONSHIP VIEW)
# =========================================================================
def render_hinh_4_6(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ THỰC THỂ QUAN HỆ CƠ SỞ DỮ LIỆU (ERD CỐT LÕI)", "Mô hình quan hệ giữa các thực thể trọng yếu trong hệ thống YiYi Book", W)

    # Core Commerce Tables
    # users, addresses, carts, cart_items, orders, order_items, books, categories, reviews, coupons, point_transactions
    
    # 1. users
    draw_card(draw, [100, 180, 480, 360], "users", "PK: id | email, password, role", style, "purple")
    # 2. addresses
    draw_card(draw, [100, 440, 480, 580], "addresses", "PK: id | FK: user_id | city, street", style, "slate")
    # 3. carts
    draw_card(draw, [600, 180, 980, 320], "carts", "PK: id | FK: user_id (1-1)", style, "blue")
    # 4. cart_items
    draw_card(draw, [600, 400, 980, 580], "cart_items", "PK: id | FK: cart_id, book_id | quantity", style, "blue")
    # 5. books
    draw_card(draw, [1100, 180, 1480, 360], "books", "PK: id | FK: category_id | title, price", style, "emerald")
    # 6. categories
    draw_card(draw, [1600, 180, 1900, 320], "categories", "PK: id | name", style, "teal")
    # 7. orders
    draw_card(draw, [100, 680, 480, 880], "orders", "PK: id | FK: user_id | status, total", style, "amber")
    # 8. order_items
    draw_card(draw, [600, 680, 980, 860], "order_items", "PK: id | FK: order_id, book_id | price", style, "amber")
    # 9. reviews
    draw_card(draw, [1100, 460, 1480, 620], "reviews", "PK: id | FK: user_id, book_id | rating", style, "teal")
    # 10. coupons
    draw_card(draw, [1100, 720, 1480, 880], "coupons", "PK: id | code, discount_value", style, "purple")
    # 11. point_transactions
    draw_card(draw, [1550, 460, 1900, 640], "point_transactions", "PK: id | FK: user_id | value", style, "slate")
    # 12. user_rewards
    draw_card(draw, [1550, 720, 1900, 880], "user_rewards", "PK: id | FK: user_id, voucher_id", style, "emerald")

    # Connectors
    draw_arrow(draw, (290, 360), (290, 440), width=2, arrow_size=10) # users -> addresses
    draw_arrow(draw, (480, 250), (600, 250), width=2, arrow_size=10) # users -> carts
    draw_arrow(draw, (790, 320), (790, 400), width=2, arrow_size=10) # carts -> cart_items
    draw_arrow(draw, (1100, 270), (980, 450), width=2, arrow_size=10) # books -> cart_items
    draw_arrow(draw, (1600, 250), (1480, 250), width=2, arrow_size=10) # categories -> books
    draw_arrow(draw, (290, 360), (290, 680), width=2, arrow_size=10) # users -> orders
    draw_arrow(draw, (480, 770), (600, 770), width=2, arrow_size=10) # orders -> order_items
    draw_arrow(draw, (1100, 320), (980, 730), width=2, arrow_size=10) # books -> order_items
    draw_arrow(draw, (1290, 360), (1290, 460), width=2, arrow_size=10) # books -> reviews

    draw_card(draw, [100, 960, 1900, 1140], "Tổng Thể Lược Đồ: 21 Thực Thể Ánh Xạ PostgreSQL & 4 Miền Giá Trị Enums", "Bao gồm đầy đủ các bảng hỗ trợ: banners, contacts, site_settings, vat_invoices, notifications...", style, "slate")

# =========================================================================
# 6. HÌNH 4.7 & 4.8: LOGIN (CLASS & SEQUENCE)
# =========================================================================
def render_hinh_4_7_login_class(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ LỚP XÁC THỰC VÀ BẢO MẬT (LOGIN CLASS DIAGRAM)", "Cấu trúc các lớp tham gia luồng chứng thực và sinh JWT Bearer Token", W)

    draw_card(draw, [100, 200, 520, 440], "AuthController", "login(AuthRequest)\nregister(RegisterRequest)", style, "blue")
    draw_arrow(draw, (520, 320), (620, 320), width=4, arrow_size=14)

    draw_card(draw, [620, 180, 1080, 480], "AuthService", "login() : AuthResponse\nregister() : AuthResponse", style, "indigo" if style == "infographic" else "slate")
    draw_arrow(draw, (1080, 320), (1180, 320), width=4, arrow_size=14)

    draw_card(draw, [1180, 200, 1580, 440], "JwtService", "generateToken(User)\nisTokenValid(token)", style, "purple")
    draw_card(draw, [1640, 200, 1900, 440], "PasswordEncoder", "matches(raw, hash)", style, "slate")

    draw_arrow(draw, (850, 480), (850, 620), width=4, arrow_size=14)

    draw_card(draw, [620, 620, 1080, 840], "UserRepository", "findByEmail(email)\nexistsByEmail(email)", style, "teal")
    draw_arrow(draw, (850, 840), (850, 940), width=4, arrow_size=14)

    draw_card(draw, [400, 940, 820, 1160], "User (Entity)", "id, email, password, role", style, "dark")
    draw_card(draw, [920, 940, 1300, 1160], "Role (Enum)", "USER, ADMIN", style, "dark")

def render_hinh_4_7_login_seq(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ ĐĂNG NHẬP (LOGIN SEQUENCE DIAGRAM)", "Quy trình xác thực thông tin tài khoản và phản hồi JWT Bearer Token", W)

    # Lifelines: User | LoginUI | AuthController | AuthService | UserRepository | PasswordEncoder | JwtService
    actors = [
        (180, "User / Client"),
        (480, "Login UI (React)"),
        (800, "AuthController"),
        (1120, "AuthService"),
        (1440, "UserRepository"),
        (1760, "JwtService")
    ]

    for x, name in actors:
        draw_card(draw, [x - 120, 170, x + 120, 240], name, "", style, "blue")
        draw.line([(x, 240), (x, 1140)], fill=(148, 163, 184), width=2)

    # Messages
    msgs = [
        (180, 480, "1. Nhập email & password", 300),
        (480, 800, "2. POST /api/auth/login", 400),
        (800, 1120, "3. login(AuthRequest)", 500),
        (1120, 1440, "4. findByEmail(email)", 600),
        (1440, 1120, "5. Trả về User Entity", 700, True),
        (1120, 1760, "6. generateToken(User)", 800),
        (1760, 1120, "7. Trả về JWT Token", 900, True),
        (1120, 800, "8. AuthResponse {token, user}", 980, True),
        (800, 480, "9. HTTP 200 {token}", 1050, True),
        (480, 180, "10. Lưu AuthContext & Chuyển trang", 1110, True)
    ]

    f_msg = get_font(21, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

# =========================================================================
# 7. HÌNH 4.12: CHECKOUT (CLASS & SEQUENCE)
# =========================================================================
def render_hinh_4_12_checkout_class(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ LỚP ĐẶT HÀNG (CHECKOUT CLASS DIAGRAM)", "Cấu trúc các lớp tham gia luồng tạo đơn và kiểm tra giảm giá", W)

    draw_card(draw, [100, 200, 560, 440], "OrderController", "createOrder(OrderRequest)\ngetUserOrders()", style, "blue")
    draw_arrow(draw, (560, 320), (680, 320), width=4, arrow_size=14)

    draw_card(draw, [680, 180, 1260, 480], "OrderService", "createOrder() : Order\nvalidateStockAndCoupon()", style, "amber")
    draw_arrow(draw, (1260, 320), (1380, 320), width=4, arrow_size=14)

    draw_card(draw, [1380, 200, 1900, 440], "CouponService", "validateCoupon(code)\ncalculateDiscount()", style, "teal")

    draw_arrow(draw, (970, 480), (970, 600), width=4, arrow_size=14)

    draw_card(draw, [100, 600, 620, 840], "CartService", "getCart(), clearCart()", style, "blue")
    draw_card(draw, [680, 600, 1260, 840], "OrderRepository", "save(Order), findById()", style, "slate")
    draw_card(draw, [1340, 600, 1900, 840], "BookRepository", "updateStock(bookId, qty)", style, "emerald")

    draw_arrow(draw, (970, 840), (970, 940), width=4, arrow_size=14)

    draw_card(draw, [400, 940, 950, 1160], "Order (Entity)", "id, totalAmount, status, address", style, "dark")
    draw_card(draw, [1050, 940, 1600, 1160], "OrderItem (Entity)", "id, quantity, price", style, "dark")

def render_hinh_4_12_checkout_seq(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ ĐẶT HÀNG (CHECKOUT SEQUENCE DIAGRAM)", "Quy trình xác nhận giỏ hàng, áp mã giảm giá và tạo đơn hàng COD", W)

    actors = [
        (180, "Customer"),
        (500, "Checkout UI"),
        (840, "OrderController"),
        (1180, "OrderService"),
        (1520, "Coupon / Cart"),
        (1820, "Database")
    ]

    for x, name in actors:
        draw_card(draw, [x - 120, 170, x + 120, 240], name, "", style, "amber")
        draw.line([(x, 240), (x, 1140)], fill=(148, 163, 184), width=2)

    msgs = [
        (180, 500, "1. Chọn địa chỉ & Đặt hàng", 300),
        (500, 840, "2. POST /api/orders (COD)", 400),
        (840, 1180, "3. createOrder(OrderRequest)", 500),
        (1180, 1520, "4. validateCoupon() & checkStock()", 600),
        (1520, 1180, "5. Xác thực thành công", 700, True),
        (1180, 1820, "6. save(Order) & updateStock()", 800),
        (1820, 1180, "7. Đơn hàng đã tạo", 900, True),
        (1180, 1520, "8. clearCart(userId)", 970),
        (1180, 840, "9. Trả về Order DTO", 1040, True),
        (840, 500, "10. HTTP 201 Created", 1090, True),
        (500, 180, "11. Hiển thị thông báo thành công", 1130, True)
    ]

    f_msg = get_font(21, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

# =========================================================================
# 8. HÌNH 4.13: ONLINE PAYMENT (CLASS & SEQUENCE)
# =========================================================================
def render_hinh_4_13_payment_class(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ LỚP THANH TOÁN (PAYMENT CLASS DIAGRAM)", "Cấu trúc các lớp tích hợp cổng thanh toán trực tuyến VNPAY", W)

    draw_card(draw, [100, 200, 560, 440], "PaymentController", "createPaymentUrl(orderId)\nvnpayCallback(params)", style, "amber")
    draw_arrow(draw, (560, 320), (680, 320), width=4, arrow_size=14)

    draw_card(draw, [680, 180, 1260, 480], "PaymentService", "createVNPayUrl() : String\nprocessVNPayCallback() : boolean", style, "amber")
    draw_arrow(draw, (1260, 320), (1380, 320), width=4, arrow_size=14)

    draw_card(draw, [1380, 200, 1900, 440], "VNPayConfig", "vnp_PayUrl, vnp_TmnCode\nvnp_HashSecret, hmacSHA512()", style, "slate")

    draw_arrow(draw, (970, 480), (970, 620), width=4, arrow_size=14)

    draw_card(draw, [300, 620, 880, 860], "OrderService", "updatePaymentStatus(orderId)\nconfirmPaid()", style, "blue")
    draw_card(draw, [1060, 620, 1640, 860], "Order (Entity)", "paymentMethod, status, isPaid", style, "dark")

def render_hinh_4_13_payment_seq(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ THANH TOÁN ONLINE (PAYMENT SEQUENCE)", "Quy trình sinh URL chuyển hướng VNPAY và xử lý kết quả giao dịch", W)

    actors = [
        (180, "Customer"),
        (500, "Payment UI"),
        (840, "PaymentController"),
        (1180, "PaymentService"),
        (1520, "VNPAY Gateway"),
        (1820, "Order / DB")
    ]

    for x, name in actors:
        draw_card(draw, [x - 120, 170, x + 120, 240], name, "", style, "amber")
        draw.line([(x, 240), (x, 1140)], fill=(148, 163, 184), width=2)

    msgs = [
        (180, 500, "1. Chọn thanh toán VNPAY", 300),
        (500, 840, "2. GET /api/payment/vnpay-url", 400),
        (840, 1180, "3. createPaymentUrl(orderId)", 500),
        (1180, 840, "4. Trả về Payment URL (HMAC-SHA512)", 600, True),
        (840, 500, "5. Chuyển hướng trình duyệt", 700, True),
        (500, 1520, "6. Khách hàng thực hiện thanh toán", 790),
        (1520, 500, "7. Callback về Frontend Return URL", 880, True),
        (500, 840, "8. GET /api/payment/vnpay-callback", 960),
        (840, 1180, "9. verifyCallback(params)", 1020),
        (1180, 1820, "10. updatePaymentStatus(PAID)", 1070),
        (840, 500, "11. HTTP 200 OK (Thành công)", 1115, True)
    ]

    f_msg = get_font(21, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

# =========================================================================
# 9. HÌNH 4.14: ORDER STATE & RETURN SEQUENCE
# =========================================================================
def render_hinh_4_14_order_state(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TRẠNG THÁI ĐƠN HÀNG (ORDER STATE DIAGRAM)", "Các trạng thái vòng đời đơn hàng và nhánh xử lý đổi trả", W)

    # Main States: PENDING -> PROCESSING -> SHIPPING -> DELIVERED -> COMPLETED
    draw_card(draw, [100, 260, 400, 400], "PENDING", "Chờ xác nhận", style, "blue")
    draw_arrow(draw, (400, 330), (480, 330), width=4, arrow_size=14)
    draw_card(draw, [480, 260, 780, 400], "PROCESSING", "Đang xử lý / Đóng gói", style, "indigo" if style == "infographic" else "slate")
    draw_arrow(draw, (780, 330), (860, 330), width=4, arrow_size=14)
    draw_card(draw, [860, 260, 1160, 400], "SHIPPING", "Đang vận chuyển", style, "amber")
    draw_arrow(draw, (1160, 330), (1240, 330), width=4, arrow_size=14)
    draw_card(draw, [1240, 260, 1540, 400], "DELIVERED", "Đã giao hàng", style, "teal")
    draw_arrow(draw, (1540, 330), (1620, 330), width=4, arrow_size=14)
    draw_card(draw, [1620, 260, 1900, 400], "COMPLETED", "Hoàn tất đơn", style, "emerald")

    # Cancellation Branch
    draw_arrow(draw, (250, 400), (250, 540), width=3, arrow_size=12)
    draw_arrow(draw, (630, 400), (630, 540), width=3, arrow_size=12)
    draw_card(draw, [200, 540, 680, 680], "CANCELLED", "Đơn hàng đã hủy (Rollback tồn kho)", style, "dark")

    # Return & Refund Branch
    draw_arrow(draw, (1390, 400), (1390, 540), width=3, arrow_size=12)
    draw_card(draw, [1200, 540, 1680, 680], "RETURN_REQUESTED", "Khách gửi yêu cầu đổi trả", style, "amber")
    
    draw_arrow(draw, (1440, 680), (1240, 800), width=3, arrow_size=12)
    draw_card(draw, [1000, 800, 1440, 940], "RETURN_REJECTED", "Từ chối yêu cầu đổi trả", style, "dark")

    draw_arrow(draw, (1440, 680), (1640, 800), width=3, arrow_size=12)
    draw_card(draw, [1460, 800, 1900, 940], "RETURN_APPROVED", "Chấp thuận đổi trả / Hoàn tiền", style, "emerald")

    draw_arrow(draw, (1680, 940), (1680, 1020), width=3, arrow_size=12)
    draw_card(draw, [1460, 1020, 1900, 1160], "REFUNDED", "Đã hoàn tiền cho khách hàng", style, "teal")

def render_hinh_4_14_order_seq(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ ĐỔI TRẢ ĐƠN HÀNG (ORDER RETURN SEQUENCE)", "Quy trình gửi yêu cầu hoàn trả và duyệt hồ sơ hoàn tiền", W)

    actors = [
        (200, "Customer"),
        (600, "Order UI"),
        (1000, "OrderController"),
        (1400, "OrderService"),
        (1800, "Database")
    ]

    for x, name in actors:
        draw_card(draw, [x - 140, 170, x + 140, 240], name, "", style, "teal")
        draw.line([(x, 240), (x, 1140)], fill=(148, 163, 184), width=2)

    msgs = [
        (200, 600, "1. Gửi yêu cầu đổi trả + Lý do", 320),
        (600, 1000, "2. POST /api/orders/{id}/return", 440),
        (1000, 1400, "3. requestReturn(ReturnRequest)", 560),
        (1400, 1800, "4. updateStatus(RETURN_REQUESTED)", 680),
        (1800, 1400, "5. Lưu bản ghi thành công", 800, True),
        (1400, 1000, "6. Trả về trạng thái cập nhật", 900, True),
        (1000, 600, "7. HTTP 200 OK", 990, True),
        (600, 200, "8. Hiển thị trạng thái Chờ Quản trị duyệt", 1080, True)
    ]

    f_msg = get_font(22, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 20), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

# =========================================================================
# 10. HÌNH 4.16: YIYI AI (COMPONENT & SEQUENCE)
# =========================================================================
def render_hinh_4_16_ai_component(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ THÀNH PHẦN TRỢ LÝ AI (AI COMPONENT DIAGRAM)", "Các module cấu thành hệ thống tư vấn thông minh YiYi AI", W)

    draw_card(draw, [100, 200, 550, 480], "AIChatWidget Component", "Quản lý hộp thoại, Lịch sử chat\nRender giao diện Markdown", style, "teal")
    draw_arrow(draw, (550, 340), (680, 340), width=4, arrow_size=14)

    draw_card(draw, [680, 200, 1220, 480], "Intent Classifier Engine", "Phân tích 8 nhóm ý định người dùng\n(Tìm sách, So sánh, Giá...)", style, "purple")
    draw_arrow(draw, (1220, 340), (1350, 340), width=4, arrow_size=14)

    draw_card(draw, [1350, 200, 1900, 480], "Client Mini-RAG Engine", "Lọc ngữ cảnh kho sách thực tế\n(Grounding Context Data)", style, "emerald")

    draw_arrow(draw, (1625, 480), (1625, 620), width=4, arrow_size=14)

    draw_card(draw, [100, 620, 650, 900], "User Memory Storage", "Lưu sở thích, xưng hô, hạng thành viên\n(LocalStorage Per-User)", style, "blue")
    draw_card(draw, [750, 620, 1250, 900], "Prompt Engineering", "Xây dựng System Prompt chống bịa đặt\n(Zero Hallucination Rule)", style, "amber")
    draw_card(draw, [1350, 620, 1900, 900], "Groq Cloud API Client", "Mô hình Llama 3.3 70B Versatile\nServer-Sent Events (SSE) Stream", style, "emerald")

    draw_card(draw, [100, 980, 1900, 1160], "Đặc Điểm Thiết Kế: Toàn bộ quá trình RAG diễn ra tại Client, không gây tải Database máy chủ", "", style, "slate")

def render_hinh_4_16_ai_seq(draw, style="infographic"):
    W, H = 2000, 1300
    draw_header(draw, "SƠ ĐỒ TUẦN TỰ TRỢ LÝ AI (AI SEQUENCE DIAGRAM)", "Quy trình tiếp nhận câu hỏi, trích xuất ngữ cảnh và phản hồi streaming", W)

    actors = [
        (200, "User"),
        (560, "AIChatWidget"),
        (960, "Intent Detector"),
        (1360, "Mini-RAG Engine"),
        (1760, "Groq Cloud LLM")
    ]

    for x, name in actors:
        draw_card(draw, [x - 140, 170, x + 140, 240], name, "", style, "emerald")
        draw.line([(x, 240), (x, 1140)], fill=(148, 163, 184), width=2)

    msgs = [
        (200, 560, "1. Nhập câu hỏi tư vấn sách", 300),
        (560, 960, "2. detectIntent(query)", 400),
        (960, 1360, "3. filterCatalog(intent, keywords)", 500),
        (1360, 560, "4. Trả về 5-10 tựa sách liên quan", 600, True),
        (560, 1760, "5. POST /chat/completions (Prompt + Context)", 720),
        (1760, 560, "6. Server-Sent Events (SSE) Streaming", 850, True),
        (560, 200, "7. Render chữ chạy theo thời gian thực", 970, True),
        (560, 200, "8. Hiển thị Thẻ gợi ý sản phẩm (Mua ngay)", 1070, True)
    ]

    f_msg = get_font(21, bold=True)
    for m in msgs:
        x_from, x_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=3, arrow_size=10, dashed=dashed)
        mid_x = (x_from + x_to) // 2
        draw.text((mid_x, y - 18), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

# Master render execution
def execute_all():
    diagrams = [
        ("Hinh_2.1_Agile_Scrum_Workflow_YiYi_Book", render_hinh_2_1),
        ("Hinh_4.3_Backend_Layered_Architecture", render_hinh_4_3),
        ("Hinh_4.4_AI_RAG_Intent_Flow_Architecture", render_hinh_4_4),
        ("Hinh_4.5_Package_Diagram_YiYi_Book", render_hinh_4_5),
        ("Hinh_4.6_ERD_Database_YiYi_Book", render_hinh_4_6),
        ("Hinh_4.7_Class_Diagram_Login_Auth", render_hinh_4_7_login_class),
        ("Hinh_4.7_Sequence_Diagram_Login_Auth", render_hinh_4_7_login_seq),
        ("Hinh_4.12_Class_Diagram_Checkout_COD", render_hinh_4_12_checkout_class),
        ("Hinh_4.12_Sequence_Diagram_Checkout_COD", render_hinh_4_12_checkout_seq),
        ("Hinh_4.13_Class_Diagram_Payment_Online", render_hinh_4_13_payment_class),
        ("Hinh_4.13_Sequence_Diagram_Payment_Online", render_hinh_4_13_payment_seq),
        ("Hinh_4.14_Order_State_Diagram", render_hinh_4_14_order_state),
        ("Hinh_4.14_Order_Return_Sequence_Diagram", render_hinh_4_14_order_seq),
        ("Hinh_4.16_Component_Diagram_YiYi_AI", render_hinh_4_16_ai_component),
        ("Hinh_4.16_Sequence_Diagram_YiYi_AI", render_hinh_4_16_ai_seq)
    ]

    for fname, dfunc in diagrams:
        # Render Infographic Revised
        img_info = Image.new("RGB", (2000, 1300), (255, 255, 255))
        draw_info = ImageDraw.Draw(img_info)
        dfunc(draw_info, style="infographic")
        p_info = os.path.join(INFO_REV_DIR, fname + ".png")
        img_info.save(p_info, dpi=(300, 300))

        # Render Standard Revised
        img_std = Image.new("RGB", (2000, 1300), (255, 255, 255))
        draw_std = ImageDraw.Draw(img_std)
        dfunc(draw_std, style="standard")
        p_std = os.path.join(STD_REV_DIR, fname + ".png")
        img_std.save(p_std, dpi=(300, 300))

        # Write SVG vector stub
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1300" width="2000" height="1300">\n  <rect width="100%" height="100%" fill="#ffffff"/>\n  <!-- Vector source for {fname} -->\n</svg>'
        with open(os.path.join(INFO_REV_DIR, fname + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg_content)
        with open(os.path.join(STD_REV_DIR, fname + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg_content)

        print(f"Rendered: {fname}")

if __name__ == "__main__":
    execute_all()
    print("All revised technical diagrams generated successfully!")

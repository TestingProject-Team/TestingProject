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

def render_hinh_4_3():
    W, H = 2000, 1300
    # 1. Infographic
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_sub = get_font(18, bold=False)
    f_col = get_font(20, bold=True)
    f_box = get_font(17, bold=True)
    f_body = get_font(14, bold=False)

    draw.text((W//2, 50), "KIẾN TRÚC PHÂN TẦNG BACKEND SPRING BOOT 3 — YIYI BOOK", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 85), "Bố cục 3 cột chuẩn Enterprise: Presentation, Security, Business Service, Persistence & External Services", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # Column 1: LEFT (Frontend Client & Security)
    # Box 1.1: Frontend Client (Top)
    draw.rounded_rectangle([80, 130, 580, 520], radius=12, fill=(240, 249, 255), outline=(56, 189, 248), width=2)
    draw.rectangle([80, 130, 580, 175], fill=(2, 132, 199))
    draw.text((330, 152), "1. CLIENT INTERACTION (SPA)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((105, 195), "• React 18 SPA (Vite + Tailwind CSS v4)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 230), "• Axios HTTP Client + JWT Interceptors", fill=(15, 23, 42), font=f_body)
    draw.text((105, 265), "• SockJS & STOMP Client (Live Updates)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 300), "• Context: Auth, Cart, Lang, WebSocket", fill=(15, 23, 42), font=f_body)
    draw.text((105, 335), "• LocalStorage: JWT Token & Cart Cache", fill=(15, 23, 42), font=f_body)
    draw.text((105, 370), "• Responsive UI: Customer & Admin Portal", fill=(15, 23, 42), font=f_body)
    draw.text((105, 405), "• Client-side RAG Intent Router (AI)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 440), "• Port: 5173 (Dev) / Production Vercel", fill=(15, 23, 42), font=f_body)

    # Box 1.2: Security & Cross-Cutting (Bottom)
    draw.rounded_rectangle([80, 560, 580, 1160], radius=12, fill=(250, 245, 255), outline=(168, 85, 247), width=2)
    draw.rectangle([80, 560, 580, 605], fill=(126, 34, 206))
    draw.text((330, 582), "2. CROSS-CUTTING & SECURITY", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((105, 625), "• Spring Security 6.x Filter Chain", fill=(15, 23, 42), font=f_body)
    draw.text((105, 660), "• JwtAuthFilter (Bearer Token Validation)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 695), "• JwtService (HMAC-SHA256 Sign/Verify)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 730), "• Role-Based Access: USER, ADMIN", fill=(15, 23, 42), font=f_body)
    draw.text((105, 765), "• Password Encoding (BCrypt 10 rounds)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 800), "• Global CORS & WebMvcConfigurer", fill=(15, 23, 42), font=f_body)
    draw.text((105, 835), "• CacheFilter (HTTP Cache-Control Headers)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 870), "• Global Exception Handler & DTO Validation", fill=(15, 23, 42), font=f_body)
    draw.text((105, 905), "• WebSocket STOMP Security Handshake", fill=(15, 23, 42), font=f_body)
    draw.text((105, 940), "• Jackson JSON Serializer / Deserializer", fill=(15, 23, 42), font=f_body)

    # Column 2: CENTER (Core Backend Layers)
    # 2.1 Controller Layer
    draw.rounded_rectangle([640, 130, 1360, 370], radius=12, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.rectangle([640, 130, 1360, 175], fill=(5, 150, 105))
    draw.text((1000, 152), "3. REST CONTROLLER LAYER (23 CONTROLLERS)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((665, 195), "• AuthController, UserController, AdminUserController", fill=(15, 23, 42), font=f_body)
    draw.text((665, 225), "• BookController, CategoryController, BannerController", fill=(15, 23, 42), font=f_body)
    draw.text((665, 255), "• CartController, OrderController, PaymentController (VNPay/MoMo/ZaloPay)", fill=(15, 23, 42), font=f_body)
    draw.text((665, 285), "• ReviewController, AdminReviewController, RewardController, CouponController", fill=(15, 23, 42), font=f_body)
    draw.text((665, 315), "• WishlistController, AddressController, NotificationController, FileController", fill=(15, 23, 42), font=f_body)
    draw.text((665, 345), "• SiteSettingController, NewsletterController, ContactController, PingController", fill=(15, 23, 42), font=f_body)

    # 2.2 Service Layer
    draw.rounded_rectangle([640, 410, 1360, 650], radius=12, fill=(239, 246, 255), outline=(59, 130, 246), width=2)
    draw.rectangle([640, 410, 1360, 455], fill=(37, 99, 235))
    draw.text((1000, 432), "4. BUSINESS SERVICE LAYER (15 SERVICES)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((665, 475), "• AuthService: Đăng ký, đăng nhập JWT, BCrypt validation", fill=(15, 23, 42), font=f_body)
    draw.text((665, 505), "• OrderService: Xử lý giỏ, mã giảm giá, tính phí ship, tích lũy điểm thưởng Y-Point", fill=(15, 23, 42), font=f_body)
    draw.text((665, 535), "• BookService & CategoryService: Tra cứu sách, lọc đa tiêu chí, phân trang Pageable", fill=(15, 23, 42), font=f_body)
    draw.text((665, 565), "• CartService, CouponService, RewardService, ReviewService, UserService", fill=(15, 23, 42), font=f_body)
    draw.text((665, 595), "• WebSocketService: Broadcast thông báo realtime qua topic /topic/notifications", fill=(15, 23, 42), font=f_body)
    draw.text((665, 625), "• NotificationService, BannerService, ContactService, NewsletterService", fill=(15, 23, 42), font=f_body)

    # 2.3 Persistence Layer (Repository + JPA)
    draw.rounded_rectangle([640, 690, 1360, 910], radius=12, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.rectangle([640, 690, 1360, 735], fill=(217, 119, 6))
    draw.text((1000, 712), "5. PERSISTENCE & DATA ACCESS LAYER (18 REPOSITORIES)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((665, 755), "• Spring Data JPA Repositories (JpaRepository & JpaSpecificationExecutor)", fill=(15, 23, 42), font=f_body)
    draw.text((665, 785), "• UserRepository, BookRepository, OrderRepository, CartRepository", fill=(15, 23, 42), font=f_body)
    draw.text((665, 815), "• PointTransactionRepository, CouponRepository, ReviewRepository, AddressRepository", fill=(15, 23, 42), font=f_body)
    draw.text((665, 845), "• Hibernate ORM 6.x / Entity Lifecycle / Transaction Management (@Transactional)", fill=(15, 23, 42), font=f_body)
    draw.text((665, 875), "• HikariCP Connection Pool (Max: 10, Min-Idle: 5, Timeout: 20000ms)", fill=(15, 23, 42), font=f_body)

    # 2.4 Database Layer (Safe Margin > 60px)
    draw.rounded_rectangle([640, 950, 1360, 1160], radius=12, fill=(241, 245, 249), outline=(100, 116, 139), width=2)
    draw.rectangle([640, 950, 1360, 995], fill=(51, 65, 85))
    draw.text((1000, 972), "6. DATABASE STORAGE (POSTGRESQL 16)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((665, 1015), "• PostgreSQL 16 RDBMS (Relational Database)", fill=(15, 23, 42), font=f_body)
    draw.text((665, 1045), "• 21 Normalized Tables (users, books, orders, cart_items, reviews...)", fill=(15, 23, 42), font=f_body)
    draw.text((665, 1075), "• Foreign Keys, Cascade Constraints, Indexes trên username/email/category_id", fill=(15, 23, 42), font=f_body)
    draw.text((665, 1105), "• 4 Enums: Role, AuthProvider, DiscountType, ShippingStatus", fill=(15, 23, 42), font=f_body)
    draw.text((665, 1135), "• Local Docker Container & Supabase Cloud PostgreSQL", fill=(15, 23, 42), font=f_body)

    # Column 3: RIGHT (Gateways & Runtime)
    # Box 3.1: Gateways & AI Services
    draw.rounded_rectangle([1420, 130, 1920, 620], radius=12, fill=(255, 247, 237), outline=(249, 115, 22), width=2)
    draw.rectangle([1420, 130, 1920, 175], fill=(234, 88, 12))
    draw.text((1670, 152), "7. EXTERNAL GATEWAYS & AI", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((1445, 200), "• VNPay Sandbox Payment Gateway", fill=(15, 23, 42), font=f_body)
    draw.text((1465, 225), "(vnp_Command=pay, HMAC-SHA512)", fill=(100, 116, 139), font=f_body)
    draw.text((1445, 260), "• MoMo Payment Gateway API", fill=(15, 23, 42), font=f_body)
    draw.text((1465, 285), "(captureWallet, partnerCode)", fill=(100, 116, 139), font=f_body)
    draw.text((1445, 320), "• ZaloPay Payment Integration", fill=(15, 23, 42), font=f_body)
    draw.text((1465, 345), "(AppId, Key1, Key2, MAC Verify)", fill=(100, 116, 139), font=f_body)
    draw.text((1445, 380), "• Groq Cloud AI / OpenAI API", fill=(15, 23, 42), font=f_body)
    draw.text((1465, 405), "(Llama-3.3-70b-versatile, mini-RAG)", fill=(100, 116, 139), font=f_body)
    draw.text((1445, 440), "• Google OAuth2 / Social Login API", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 475), "• Cloudflare Images / Static CDN", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 510), "• RestTemplate HTTP Clients", fill=(15, 23, 42), font=f_body)

    # Box 3.2: Runtime & Deployment
    draw.rounded_rectangle([1420, 660, 1920, 1160], radius=12, fill=(243, 244, 246), outline=(107, 114, 128), width=2)
    draw.rectangle([1420, 660, 1920, 705], fill=(75, 85, 99))
    draw.text((1670, 682), "8. RUNTIME & DEPLOYMENT", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((1445, 730), "• Java OpenJDK 21 LTS Runtime", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 765), "• Embedded Apache Tomcat 10 Server", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 800), "• Port: 8080 (REST) / 8081 (Docker)", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 835), "• Docker Multi-stage Build & Compose", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 870), "• Render / Railway Backend Cloud", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 905), "• Vercel Frontend Serverless Edge", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 940), "• GitHub Actions CI/CD Pipeline", fill=(15, 23, 42), font=f_body)
    draw.text((1445, 975), "• SonarQube & SpotBugs Quality Gate", fill=(15, 23, 42), font=f_body)

    # Connectors between layers
    draw_arrow(draw, (580, 250), (640, 250), fill=(2, 132, 199), width=3, arrow_size=8)
    draw_arrow(draw, (640, 310), (580, 310), fill=(100, 116, 139), width=3, arrow_size=8, dashed=True)
    draw_arrow(draw, (1000, 370), (1000, 410), fill=(5, 150, 105), width=3, arrow_size=8)
    draw_arrow(draw, (1000, 650), (1000, 690), fill=(37, 99, 235), width=3, arrow_size=8)
    draw_arrow(draw, (1000, 910), (1000, 950), fill=(217, 119, 6), width=3, arrow_size=8)

    draw_arrow(draw, (1360, 280), (1420, 280), fill=(234, 88, 12), width=3, arrow_size=8)
    draw_arrow(draw, (1420, 340), (1360, 340), fill=(234, 88, 12), width=3, arrow_size=8, dashed=True)

    draw.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — Backend Layered Architecture (Spring Boot 3 + PostgreSQL 16)", fill=(148, 163, 184), font=f_body, anchor="mm")

    # 2. Standard Diagram
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 50), "HÌNH 4.3. KIẾN TRÚC PHÂN TẦNG BACKEND SPRING BOOT", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 85), "Standard UML / Enterprise Layered Architecture", fill=(80, 80, 80), font=f_sub, anchor="mm")

    for box, title, lines in [
        ([80, 130, 580, 520], "1. Client Interaction (SPA)", ["• React 18 SPA (Vite + Tailwind CSS v4)", "• Axios HTTP Client + JWT Interceptors", "• SockJS & STOMP Client (Live Updates)", "• Context: Auth, Cart, Lang, WebSocket", "• LocalStorage: JWT Token & Cart Cache", "• Responsive UI: Customer & Admin Portal", "• Client-side RAG Intent Router (AI)", "• Port: 5173 (Dev) / Production Vercel"]),
        ([80, 560, 580, 1160], "2. Cross-Cutting & Security", ["• Spring Security 6.x Filter Chain", "• JwtAuthFilter (Bearer Token Validation)", "• JwtService (HMAC-SHA256 Sign/Verify)", "• Role-Based Access: USER, ADMIN", "• Password Encoding (BCrypt 10 rounds)", "• Global CORS & WebMvcConfigurer", "• CacheFilter (HTTP Cache Headers)", "• Global Exception Handler & DTO Validation", "• WebSocket STOMP Security Handshake", "• Jackson JSON Serialization"]),
        ([640, 130, 1360, 370], "3. REST Controller Layer (23 Controllers)", ["• AuthController, UserController, AdminUserController", "• BookController, CategoryController, BannerController", "• CartController, OrderController, PaymentController", "• ReviewController, AdminReviewController, RewardController", "• WishlistController, AddressController, NotificationController", "• SiteSettingController, NewsletterController, ContactController"]),
        ([640, 410, 1360, 650], "4. Business Service Layer (15 Services)", ["• AuthService: Đăng ký, đăng nhập JWT, BCrypt", "• OrderService: Xử lý giỏ, giảm giá, ship, Y-Points", "• BookService & CategoryService: Lọc sách, phân trang", "• CartService, CouponService, RewardService, ReviewService", "• WebSocketService: Broadcast realtime qua STOMP", "• NotificationService, BannerService, ContactService"]),
        ([640, 690, 1360, 910], "5. Persistence Layer (18 Repositories)", ["• Spring Data JPA Repositories", "• UserRepository, BookRepository, OrderRepository", "• PointTransactionRepository, CouponRepository, ReviewRepository", "• Hibernate ORM 6.x / Transaction Management", "• HikariCP Connection Pool (Max: 10, Timeout: 20s)"]),
        ([640, 950, 1360, 1160], "6. Database Storage (PostgreSQL 16)", ["• PostgreSQL 16 Relational Database", "• 21 Normalized Tables (users, books, orders...)", "• Foreign Keys, Constraints, Indexes", "• 4 Enums: Role, AuthProvider, DiscountType, ShippingStatus", "• Docker Container & Supabase Cloud PostgreSQL"]),
        ([1420, 130, 1920, 620], "7. External Gateways & AI", ["• VNPay Sandbox Payment Gateway", "• MoMo Payment Gateway API", "• ZaloPay Payment Integration", "• Groq Cloud AI / OpenAI API (Llama-3.3-70b)", "• Google OAuth2 Social Login", "• Cloudflare Images / Static CDN", "• RestTemplate HTTP Clients"]),
        ([1420, 660, 1920, 1160], "8. Runtime & Deployment", ["• Java OpenJDK 21 LTS Runtime", "• Embedded Apache Tomcat 10 Server", "• Port: 8080 (REST) / 8081 (Docker)", "• Docker Multi-stage Build & Compose", "• Render / Railway Backend Cloud", "• Vercel Frontend Serverless Edge", "• GitHub Actions CI/CD Pipeline", "• SonarQube & SpotBugs Quality Gate"])
    ]:
        draw_s.rectangle(box, fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        draw_s.rectangle([box[0], box[1], box[2], box[1]+35], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
        draw_s.text((box[0]+15, box[1]+18), title, fill=(0, 0, 0), font=f_box, anchor="lm")
        y_c = box[1] + 55
        for l in lines:
            draw_s.text((box[0]+15, y_c), l, fill=(0, 0, 0), font=f_body)
            y_c += 28

    draw_arrow(draw_s, (580, 250), (640, 250), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (640, 310), (580, 310), fill=(0, 0, 0), width=2, arrow_size=8, dashed=True)
    draw_arrow(draw_s, (1000, 370), (1000, 410), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1000, 650), (1000, 690), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1000, 910), (1000, 950), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1360, 280), (1420, 280), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1420, 340), (1360, 340), fill=(0, 0, 0), width=2, arrow_size=8, dashed=True)

    draw_s.text((W//2, 1275), "Safe Margin: 60px | Technical Standard Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    p_info = os.path.join(INFO_DIR, "Hinh_4.3_Backend_Layered_Architecture.png")
    p_std = os.path.join(STD_DIR, "Hinh_4.3_Backend_Layered_Architecture.png")
    img.save(p_info, "PNG", dpi=(300, 300))
    img_std.save(p_std, "PNG", dpi=(300, 300))

    svg_info = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
        <rect width="100%" height="100%" fill="#F8FAFC"/>
        <text x="{W//2}" y="50" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#0F172A" text-anchor="middle">KIẾN TRÚC PHÂN TẦNG BACKEND SPRING BOOT 3 — YIYI BOOK</text>
        <text x="{W//2}" y="85" font-family="Arial, sans-serif" font-size="18" fill="#475569" text-anchor="middle">Bố cục 3 cột chuẩn Enterprise: Presentation, Security, Business Service, Persistence & External Services</text>
    </svg>'''
    with open(os.path.join(INFO_DIR, "Hinh_4.3_Backend_Layered_Architecture.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.3_Backend_Layered_Architecture.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.3 successfully.")

if __name__ == "__main__":
    render_hinh_4_3()

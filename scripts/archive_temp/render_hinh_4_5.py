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

def render_hinh_4_5():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_sub = get_font(18, bold=False)
    f_pkg_t = get_font(18, bold=True)
    f_body = get_font(14, bold=False)

    draw.text((W//2, 50), "SƠ ĐỒ PHÂN RÃ GÓI PHẦN MỀM HỆ THỐNG (PACKAGE DIAGRAM) — YIYI BOOK", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 85), "Phân rã module mã nguồn Spring Boot 3 Backend (com.bookstore.*) và React 18 Frontend SPA (src/*)", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # Group 1: FRONTEND PACKAGES (Top Row: 4 Boxes)
    draw.rounded_rectangle([80, 130, 1920, 480], radius=16, fill=(255, 255, 255), outline=(56, 189, 248), width=3)
    draw.rectangle([80, 130, 1920, 175], fill=(2, 132, 199))
    draw.text((1000, 152), "📦 FRONTEND MODULE STRUCTURE (src/*) — REACT 18 SPA", fill=(255, 255, 255), font=f_pkg_t, anchor="mm")

    # FE Sub-packages
    fe_pkgs = [
        ([110, 200, 520, 450], "📂 src/pages (32 Views)", ["• Home, Login, Register, Cart", "• Category, ProductDetail, Search", "• Checkout, OrderDetail, Orders", "• admin/AdminBooks, AdminOrders", "• admin/AdminUsers, AdminReviews", "• policies/FAQ, Terms, Return"]),
        ([550, 200, 970, 450], "📂 src/components (18 Comps)", ["• common/AIChatWidget (RAG Engine)", "• layout/Header, layout/Footer", "• home/HeroBanner, FlashSale", "• home/BestSellersByCategory", "• checkout/AddressModal", "• common/ScrollToTopButton"]),
        ([1000, 200, 1440, 450], "📂 src/context & data (State)", ["• AuthContext (User Session & Role)", "• CartContext (Cart State & Items)", "• LanguageContext (vi.js / en.js)", "• WebSocketContext (STOMP Broker)", "• data/provinces.json (63 Provinces)", "• utils/alert.js (SweetAlert2)"]),
        ([1470, 200, 1890, 450], "📂 src/locales & assets", ["• locales/vi.js (Vietnamese i18n)", "• locales/en.js (English i18n)", "• assets/hero.png, logo.png", "• assets/publishers/ (Fahasa, Nhã Nam)", "• App.jsx (Route Configuration)", "• main.jsx (Vite Mount Point)"])
    ]
    for b, t, ls in fe_pkgs:
        draw.rounded_rectangle(b, radius=10, fill=(240, 249, 255), outline=(186, 230, 253), width=2)
        draw.text((b[0]+15, b[1]+25), t, fill=(2, 132, 199), font=f_pkg_t)
        y_c = b[1] + 60
        for l in ls:
            draw.text((b[0]+15, y_c), l, fill=(15, 23, 42), font=f_body)
            y_c += 28

    # Group 2: BACKEND PACKAGES (Bottom Container: 6 Packages)
    draw.rounded_rectangle([80, 520, 1920, 1160], radius=16, fill=(255, 255, 255), outline=(99, 102, 241), width=3)
    draw.rectangle([80, 520, 1920, 565], fill=(79, 70, 229))
    draw.text((1000, 542), "📦 BACKEND MODULE STRUCTURE (com.bookstore.*) — SPRING BOOT 3 REST API", fill=(255, 255, 255), font=f_pkg_t, anchor="mm")

    be_pkgs = [
        ([110, 590, 680, 840], "📂 com.bookstore.controller (23)", ["• AuthController, UserController", "• BookController, CategoryController", "• CartController, OrderController", "• PaymentController, ReviewController", "• RewardController, CouponController", "• Admin*Controllers, WebSocket, Ping"]),
        ([720, 590, 1300, 840], "📂 com.bookstore.service (15)", ["• AuthService (JWT & BCrypt Validation)", "• OrderService (Cart, Points, Shipping)", "• BookService, CategoryService (Filter)", "• CartService, CouponService, RewardService", "• ReviewService, UserService, WebSocketService", "• NotificationService, BannerService, Contact"]),
        ([1340, 590, 1890, 840], "📂 com.bookstore.security & config (12)", ["• JwtAuthFilter, JwtService", "• SecurityConfig (SecurityFilterChain)", "• VNPayConfig, MoMoConfig, ZaloPayConfig", "• WebSocketConfig, WebConfig, CacheFilter", "• ApplicationConfig, DataSeeder, SpringContext", "• ExceptionHandler & DTO Validation"]),
        ([110, 870, 680, 1120], "📂 com.bookstore.entity (21 Classes, 4 Enums)", ["• User, Book, Category, Order, OrderItem", "• Cart, CartItem, Review, ReviewComment", "• PointTransaction, RewardVoucher, Coupon", "• Address, VatInvoice, Wishlist, Banner", "• Enums: Role, AuthProvider, DiscountType,", "  ShippingStatus"]),
        ([720, 870, 1300, 1120], "📂 com.bookstore.repository (18)", ["• UserRepository, BookRepository, OrderRepo", "• CartRepository, CartItemRepository", "• PointTransactionRepository, CouponRepo", "• ReviewRepository, AddressRepository", "• WishlistRepository, BannerRepository", "• Spring Data JPA & Specification Executor"]),
        ([1340, 870, 1890, 1120], "📂 com.bookstore.dto & utils (10)", ["• AuthRequest, AuthResponse, RegisterRequest", "• OrderRequest, CartRequest, ReturnRequest", "• ProfileUpdateRequest, ChangePasswordRequest", "• ExcelHelper (Apache POI Data Export)", "• WebSocketEntityListener (STOMP Events)", "• ResponseWrapper & ErrorDetails"])
    ]
    for b, t, ls in be_pkgs:
        draw.rounded_rectangle(b, radius=10, fill=(245, 243, 255), outline=(196, 181, 253), width=2)
        draw.text((b[0]+15, b[1]+25), t, fill=(109, 40, 217), font=f_pkg_t)
        y_c = b[1] + 60
        for l in ls:
            draw.text((b[0]+15, y_c), l, fill=(15, 23, 42), font=f_body)
            y_c += 28

    # Package Dependency Arrows
    draw_arrow(draw, (400, 480), (400, 520), fill=(2, 132, 199), width=3, arrow_size=8)
    draw_arrow(draw, (400, 840), (720, 715), fill=(79, 70, 229), width=2, arrow_size=6)
    draw_arrow(draw, (1010, 840), (1010, 870), fill=(79, 70, 229), width=2, arrow_size=6)
    draw_arrow(draw, (720, 995), (680, 995), fill=(79, 70, 229), width=2, arrow_size=6)

    draw.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — Package Decomposition Diagram", fill=(148, 163, 184), font=f_body, anchor="mm")

    # Standard Version
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 50), "HÌNH 4.5. SƠ ĐỒ PHÂN RÃ GÓI PHẦN MỀM HỆ THỐNG (PACKAGE DIAGRAM)", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 85), "Standard UML Package Specification Diagram", fill=(80, 80, 80), font=f_sub, anchor="mm")

    # Frontend Group
    draw_s.rectangle([80, 130, 1920, 480], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([80, 130, 1920, 175], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    draw_s.text((1000, 152), "FRONTEND MODULE STRUCTURE (src/*) — REACT 18 SPA", fill=(0, 0, 0), font=f_pkg_t, anchor="mm")

    for b, t, ls in fe_pkgs:
        draw_s.rectangle(b, fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw_s.text((b[0]+15, b[1]+25), t, fill=(0, 0, 0), font=f_pkg_t)
        y_c = b[1] + 60
        for l in ls:
            draw_s.text((b[0]+15, y_c), l, fill=(0, 0, 0), font=f_body)
            y_c += 28

    # Backend Group
    draw_s.rectangle([80, 520, 1920, 1160], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([80, 520, 1920, 565], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    draw_s.text((1000, 542), "BACKEND MODULE STRUCTURE (com.bookstore.*) — SPRING BOOT 3 REST API", fill=(0, 0, 0), font=f_pkg_t, anchor="mm")

    for b, t, ls in be_pkgs:
        draw_s.rectangle(b, fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw_s.text((b[0]+15, b[1]+25), t, fill=(0, 0, 0), font=f_pkg_t)
        y_c = b[1] + 60
        for l in ls:
            draw_s.text((b[0]+15, y_c), l, fill=(0, 0, 0), font=f_body)
            y_c += 28

    draw_arrow(draw_s, (400, 480), (400, 520), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (400, 840), (720, 715), fill=(0, 0, 0), width=2, arrow_size=6)
    draw_arrow(draw_s, (1010, 840), (1010, 870), fill=(0, 0, 0), width=2, arrow_size=6)
    draw_arrow(draw_s, (720, 995), (680, 995), fill=(0, 0, 0), width=2, arrow_size=6)

    draw_s.text((W//2, 1275), "Safe Margin: 60px | Technical Standard Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    p_info = os.path.join(INFO_DIR, "Hinh_4.5_Package_Diagram_YiYi_Book.png")
    p_std = os.path.join(STD_DIR, "Hinh_4.5_Package_Diagram_YiYi_Book.png")
    img.save(p_info, "PNG", dpi=(300, 300))
    img_std.save(p_std, "PNG", dpi=(300, 300))

    svg_info = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
        <rect width="100%" height="100%" fill="#F8FAFC"/>
        <text x="{W//2}" y="50" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#0F172A" text-anchor="middle">SƠ ĐỒ PHÂN RÃ GÓI PHẦN MỀM HỆ THỐNG (PACKAGE DIAGRAM)</text>
        <text x="{W//2}" y="85" font-family="Arial, sans-serif" font-size="18" fill="#475569" text-anchor="middle">Phân rã module mã nguồn Spring Boot 3 Backend và React 18 Frontend SPA</text>
    </svg>'''
    with open(os.path.join(INFO_DIR, "Hinh_4.5_Package_Diagram_YiYi_Book.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.5_Package_Diagram_YiYi_Book.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.5 successfully.")

if __name__ == "__main__":
    render_hinh_4_5()

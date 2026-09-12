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

def draw_header(draw, title, subtitle, W=2200):
    f_title = get_font(36, bold=True)
    f_sub = get_font(22, bold=False)
    draw.text((W // 2, 45), title, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W // 2, 90), subtitle, fill=(71, 85, 105), font=f_sub, anchor="mm")
    draw.line([(60, 120), (W - 60, 120)], fill=(203, 213, 225), width=2)

def draw_uml_box(draw, box, class_name, fields, methods, header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246)):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=box_bg, outline=border_color, width=2)
    
    hdr_h = 44
    draw.rounded_rectangle([x1, y1, x2, y1 + hdr_h], radius=8, fill=header_bg)
    draw.rectangle([x1, y1 + 10, x2, y1 + hdr_h], fill=header_bg)
    
    f_title = get_font(22, bold=True)
    f_body = get_font(17, bold=False)
    
    draw.text(((x1 + x2) // 2, y1 + hdr_h // 2), class_name, fill=(255, 255, 255), font=f_title, anchor="mm")
    
    curr_y = y1 + hdr_h + 12
    if fields:
        for f in fields:
            draw.text((x1 + 16, curr_y), f, fill=(15, 23, 42), font=f_body)
            curr_y += 24
        curr_y += 4
        draw.line([(x1, curr_y), (x2, curr_y)], fill=border_color, width=1)
        curr_y += 8
    
    if methods:
        for m in methods:
            draw.text((x1 + 16, curr_y), m, fill=(15, 23, 42), font=f_body)
            curr_y += 24

# =========================================================================
# 1. HÌNH 4.10a: CLASS DIAGRAM CHI TIẾT SÁCH & ĐÁNH GIÁ (PERFECT FIT)
# =========================================================================
def render_hinh_4_10a():
    W, H = 2200, 1400
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP CHI TIẾT SÁCH & ĐÁNH GIÁ (CLASS DIAGRAM) — YIYI BOOK", 
                "Cấu trúc các lớp Controller, Service, Repository và Entity tham gia luồng xem chi tiết sách & đánh giá", W)
    
    # ROW 1: CONTROLLERS (y: 150 -> 380) - 3 Columns
    draw_uml_box(draw, [60, 150, 720, 380], "BookController",
                 ["- bookService: BookService", "- categoryService: CategoryService"],
                 ["+ getBookById(Long id): ResponseEntity<BookDTO>",
                  "+ getFeaturedBooks(): ResponseEntity<List<BookDTO>>",
                  "+ getRecommendations(Long userId): ResponseEntity"],
                 header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_uml_box(draw, [780, 150, 1440, 380], "ReviewController",
                 ["- reviewService: ReviewService", "- authService: AuthService"],
                 ["+ getReviewsByBook(Long bookId): ResponseEntity",
                  "+ checkEligibility(Long bookId): ResponseEntity",
                  "+ createReview(ReviewRequest req): ResponseEntity"],
                 header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    draw_uml_box(draw, [1500, 150, 2140, 380], "ReviewCommentController",
                 ["- commentService: ReviewCommentService"],
                 ["+ getComments(Long reviewId): ResponseEntity",
                  "+ addComment(Long reviewId, req): ResponseEntity",
                  "+ deleteComment(Long commentId): ResponseEntity"],
                 header_bg=(124, 58, 237), box_bg=(250, 245, 255), border_color=(139, 92, 246))

    # ROW 2: SERVICES (y: 470 -> 720) - 2 Columns wide
    draw_uml_box(draw, [60, 470, 720, 720], "BookService",
                 ["- bookRepository: BookRepository", "- categoryRepository: CategoryRepository"],
                 ["+ getBookById(Long id): BookDTO",
                  "+ updateStock(Long bookId, Integer qty): void",
                  "+ searchBooks(String kw, Pageable page): Page<BookDTO>",
                  "+ getRelatedBooks(Long categoryId): List<BookDTO>"],
                 header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_uml_box(draw, [780, 470, 1440, 720], "ReviewService",
                 ["- reviewRepo: ReviewRepository", "- orderRepo: OrderRepository", "- userRepo: UserRepository"],
                 ["+ getReviewsByBookId(Long bookId): List<ReviewDTO>",
                  "+ checkUserEligibility(String username, Long bookId): boolean",
                  "+ createReview(String username, ReviewRequest req): ReviewDTO",
                  "+ calculateAverageRating(Long bookId): Double"],
                 header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # ROW 3: REPOSITORIES (y: 810 -> 1030) - 4 Columns
    draw_uml_box(draw, [60, 810, 540, 1030], "BookRepository <<Interface>>",
                 [],
                 ["+ findById(Long id): Optional<Book>",
                  "+ findByCategoryId(Long catId): List<Book>",
                  "+ findFirstByTitle(String title): Optional<Book>",
                  "+ findAll(Specification, Pageable): Page<Book>"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_uml_box(draw, [590, 810, 1130, 1030], "ReviewRepository <<Interface>>",
                 [],
                 ["+ findByBookIdOrderByCreatedAtDesc(id): List",
                  "+ countByUserIdAndBookId(uid, bid): Long",
                  "+ findByUserId(Long userId): List<Review>",
                  "+ calculateAvgRating(Long bookId): Double"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_uml_box(draw, [1180, 810, 1660, 1030], "ReviewCommentRepository",
                 [],
                 ["+ findByReviewIdOrderByCreatedAtAsc(rid): List",
                  "+ countByReviewId(Long reviewId): Long",
                  "+ deleteByReviewId(Long reviewId): void"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_uml_box(draw, [1710, 810, 2140, 1030], "OrderRepository <<Interface>>",
                 [],
                 ["+ countUserDeliveredPurchases(uid, bid): Long",
                  "+ findByUserIdOrderByCreatedAtDesc(uid): List",
                  "+ findById(Long id): Optional<Order>"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # ROW 4: ENTITIES (y: 1120 -> 1350) - 3 Columns
    draw_uml_box(draw, [60, 1120, 540, 1350], "Book <<Entity>>",
                 ["- id: Long", "- title: String", "- price: BigDecimal", "- stockQuantity: Integer", "- category: Category"],
                 ["+ getPrice(): BigDecimal", "+ setStockQuantity(int qty): void"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_uml_box(draw, [590, 1120, 1130, 1350], "Review <<Entity>>",
                 ["- id: Long", "- rating: Integer (1-5)", "- comment: String", "- user: User", "- book: Book"],
                 ["+ getRating(): Integer", "+ getComments(): List<ReviewComment>"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_uml_box(draw, [1180, 1120, 1660, 1350], "ReviewComment <<Entity>>",
                 ["- id: Long", "- content: String", "- user: User", "- review: Review", "- createdAt: LocalDateTime"],
                 ["+ getContent(): String", "+ setContent(String c): void"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    # Connecting Arrows
    draw_arrow(draw, (390, 380), (390, 470), fill=(37, 99, 235), width=4, arrow_size=12)
    draw_arrow(draw, (1110, 380), (1110, 470), fill=(13, 148, 136), width=4, arrow_size=12)
    
    draw_arrow(draw, (300, 720), (300, 810), fill=(37, 99, 235), width=4, arrow_size=12)
    draw_arrow(draw, (860, 720), (860, 810), fill=(13, 148, 136), width=4, arrow_size=12)
    draw_arrow(draw, (1300, 720), (1920, 810), fill=(13, 148, 136), width=3, arrow_size=12, dashed=True)

    draw_arrow(draw, (300, 1030), (300, 1120), fill=(71, 85, 105), width=3, arrow_size=10, dashed=True)
    draw_arrow(draw, (860, 1030), (860, 1120), fill=(71, 85, 105), width=3, arrow_size=10, dashed=True)
    draw_arrow(draw, (1420, 1030), (1420, 1120), fill=(71, 85, 105), width=3, arrow_size=10, dashed=True)

    # 1..n relation line between Review and ReviewComment
    draw.line([(1130, 1235), (1180, 1235)], fill=(30, 41, 59), width=3)
    f_rel = get_font(17, bold=True)
    draw.text((1155, 1215), "1..n", fill=(30, 41, 59), font=f_rel, anchor="mm")

    return img

# =========================================================================
# 2. HÌNH 4.7: CLASS DIAGRAM LOGIN & JWT AUTH (PERFECT FIT)
# =========================================================================
def render_hinh_4_7_class():
    W, H = 2200, 1350
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP XÁC THỰC VÀ BẢO MẬT (LOGIN & JWT AUTH CLASS DIAGRAM)", 
                "Cấu trúc các lớp tham gia chứng thực danh tính, kiểm tra mật khẩu BCrypt và sinh JWT Token", W)
    
    # Top Row: AuthController -> AuthService -> JwtService & PasswordEncoder
    draw_uml_box(draw, [80, 160, 680, 480], "AuthController",
                 ["- authService: AuthService"],
                 ["+ login(AuthRequest): ResponseEntity<AuthResponse>",
                  "+ register(RegisterRequest): ResponseEntity<String>",
                  "+ changePassword(req): ResponseEntity",
                  "+ forgotPassword(email): ResponseEntity"],
                 header_bg=(147, 51, 234), box_bg=(250, 245, 255), border_color=(168, 85, 247))

    draw_arrow(draw, (680, 320), (780, 320), fill=(147, 51, 234), width=4, arrow_size=14)

    draw_uml_box(draw, [780, 160, 1440, 520], "AuthService",
                 ["- userRepository: UserRepository",
                  "- passwordEncoder: PasswordEncoder",
                  "- jwtService: JwtService",
                  "- authenticationManager: AuthManager"],
                 ["+ authenticate(AuthRequest): AuthResponse",
                  "+ register(RegisterRequest): User",
                  "+ generateJwtToken(User user): String",
                  "+ validateCredentials(u, p): boolean"],
                 header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_arrow(draw, (1440, 260), (1540, 260), fill=(37, 99, 235), width=4, arrow_size=14)
    draw_uml_box(draw, [1540, 160, 2120, 400], "JwtService",
                 ["- secretKey: String", "- expiration: Long"],
                 ["+ generateToken(User user): String",
                  "+ extractUsername(String token): String",
                  "+ isTokenValid(token, user): boolean"],
                 header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    draw_arrow(draw, (1440, 420), (1540, 420), fill=(37, 99, 235), width=4, arrow_size=14)
    draw_uml_box(draw, [1540, 420, 2120, 620], "PasswordEncoder <<Interface>>",
                 [],
                 ["+ encode(rawPassword): String (BCrypt)",
                  "+ matches(raw, encoded): boolean"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Middle Row: UserRepository
    draw_arrow(draw, (1110, 520), (1110, 680), fill=(37, 99, 235), width=4, arrow_size=14)

    draw_uml_box(draw, [780, 680, 1440, 920], "UserRepository <<Interface>>",
                 [],
                 ["+ findByEmail(String email): Optional<User>",
                  "+ existsByEmail(String email): boolean",
                  "+ findByUsername(String username): Optional<User>"],
                 header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # Bottom Row: Entities
    draw_arrow(draw, (1110, 920), (1110, 1030), fill=(71, 85, 105), width=3, arrow_size=12, dashed=True)

    draw_uml_box(draw, [480, 1030, 1220, 1270], "User <<Entity>>",
                 ["- id: Long", "- email: String", "- password: String (BCrypt)", "- role: Role"],
                 ["+ getAuthorities(): Collection<GrantedAuthority>"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_uml_box(draw, [1300, 1030, 1840, 1270], "Role <<Enum>>",
                 ["ROLE_CUSTOMER (Khách hàng)", "ROLE_ADMIN (Quản trị viên)"],
                 [],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    return img

# =========================================================================
# 3. HÌNH 4.12: CLASS DIAGRAM CHECKOUT & COD (PERFECT FIT)
# =========================================================================
def render_hinh_4_12_class():
    W, H = 2200, 1350
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP ĐẶT HÀNG COD & GIẢM GIÁ (CHECKOUT CLASS DIAGRAM)", 
                "Cấu trúc các lớp tham gia luồng kiểm tra giỏ hàng, áp mã giảm giá, trừ tồn kho và tạo đơn hàng", W)
    
    # Controllers & Services Row 1
    draw_uml_box(draw, [80, 160, 680, 450], "OrderController",
                 ["- orderService: OrderService"],
                 ["+ createOrder(user, req): ResponseEntity",
                  "+ getMyOrders(user): ResponseEntity",
                  "+ getOrderById(id): ResponseEntity",
                  "+ cancelOrder(id): ResponseEntity"],
                 header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_arrow(draw, (680, 305), (780, 305), fill=(37, 99, 235), width=4, arrow_size=14)

    draw_uml_box(draw, [780, 160, 1460, 520], "OrderService (@Transactional)",
                 ["- orderRepo: OrderRepository",
                  "- cartService: CartService",
                  "- couponService: CouponService",
                  "- bookRepo: BookRepository"],
                 ["+ createOrder(username, req): Order",
                  "+ validateStockAndItems(cart): void",
                  "+ calculateFinalAmount(cart, coupon): double",
                  "+ updateOrderStatus(id, status): Order"],
                 header_bg=(217, 119, 6), box_bg=(255, 251, 235), border_color=(245, 158, 11))

    draw_arrow(draw, (1460, 305), (1560, 305), fill=(217, 119, 6), width=4, arrow_size=14)

    draw_uml_box(draw, [1560, 160, 2120, 450], "CouponService",
                 ["- couponRepository: CouponRepository"],
                 ["+ validateCoupon(code, total): Coupon",
                  "+ calculateDiscount(coupon, total): double",
                  "+ incrementUsageCount(coupon): void"],
                 header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # Repositories & Services Row 2
    draw_arrow(draw, (1120, 520), (1120, 660), fill=(217, 119, 6), width=4, arrow_size=14)

    draw_uml_box(draw, [80, 660, 680, 910], "CartService",
                 ["- cartRepo: CartRepository"],
                 ["+ getCartByUser(username): Cart",
                  "+ clearCart(username): void",
                  "+ validateCartItems(cart): boolean"],
                 header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_uml_box(draw, [780, 660, 1460, 910], "OrderRepository <<Interface>>",
                 [],
                 ["+ save(Order order): Order",
                  "+ findById(Long id): Optional<Order>",
                  "+ findByUserIdOrderByCreatedAtDesc(Long uid): List"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_uml_box(draw, [1560, 660, 2120, 910], "BookRepository <<Interface>>",
                 [],
                 ["+ findByIdWithLock(Long id): Optional<Book>",
                  "+ updateStockQuantity(Long id, int qty): int"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Entities Row 3
    draw_arrow(draw, (1120, 910), (1120, 1030), fill=(71, 85, 105), width=3, arrow_size=12, dashed=True)

    draw_uml_box(draw, [380, 1030, 1180, 1270], "Order <<Entity>>",
                 ["- id: Long", "- totalAmount: BigDecimal", "- status: OrderStatus", "- paymentMethod: PaymentMethod"],
                 ["+ getOrderItems(): List<OrderItem>", "+ setStatus(status): void"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_uml_box(draw, [1260, 1030, 1980, 1270], "OrderItem <<Entity>>",
                 ["- id: Long", "- book: Book", "- quantity: Integer", "- price: BigDecimal"],
                 ["+ getSubTotal(): BigDecimal"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    return img

# =========================================================================
# 4. HÌNH 4.13: CLASS DIAGRAM ONLINE PAYMENT VNPAY (PERFECT FIT)
# =========================================================================
def render_hinh_4_13_class():
    W, H = 2200, 1250
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP TÍCH HỢP CỔNG THANH TOÁN (ONLINE PAYMENT CLASS DIAGRAM)", 
                "Cấu trúc các lớp tích hợp cổng thanh toán trực tuyến VNPAY, sinh mã Checksum và xử lý Callback", W)
    
    draw_uml_box(draw, [80, 160, 680, 500], "PaymentController",
                 ["- paymentService: PaymentService", "- orderService: OrderService"],
                 ["+ createPaymentUrl(orderId): ResponseEntity",
                  "+ vnpayCallback(params): ResponseEntity",
                  "+ momoCallback(params): ResponseEntity",
                  "+ zalopayCallback(params): ResponseEntity"],
                 header_bg=(217, 119, 6), box_bg=(255, 251, 235), border_color=(245, 158, 11))

    draw_arrow(draw, (680, 330), (780, 330), fill=(217, 119, 6), width=4, arrow_size=14)

    draw_uml_box(draw, [780, 160, 1460, 520], "PaymentService",
                 ["- vnpayConfig: VNPayConfig", "- orderRepository: OrderRepository"],
                 ["+ createVNPayUrl(Order order, String ip): String",
                  "+ verifyVNPayCallback(Map<String,String>): boolean",
                  "+ processPaymentSuccess(Long orderId): void"],
                 header_bg=(217, 119, 6), box_bg=(255, 251, 235), border_color=(245, 158, 11))

    draw_arrow(draw, (1460, 330), (1560, 330), fill=(217, 119, 6), width=4, arrow_size=14)

    draw_uml_box(draw, [1560, 160, 2120, 500], "VNPayConfig",
                 ["- vnp_PayUrl, vnp_TmnCode: String", "- secretKey: String (Hash Secret)"],
                 ["+ hmacSHA512(key, data): String",
                  "+ getIpAddress(HttpServletRequest): String",
                  "+ hashAllFields(fields): String"],
                 header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Row 2: OrderService & Order Entity
    draw_arrow(draw, (1120, 520), (1120, 680), fill=(217, 119, 6), width=4, arrow_size=14)

    draw_uml_box(draw, [200, 680, 1020, 980], "OrderService (Payment Integration)",
                 ["- orderRepository: OrderRepository"],
                 ["+ updatePaymentStatus(orderId, status): void",
                  "+ confirmPaid(Long orderId): Order",
                  "+ handlePaymentFailure(Long orderId): void"],
                 header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_arrow(draw, (1020, 830), (1160, 830), fill=(37, 99, 235), width=4, arrow_size=14)

    draw_uml_box(draw, [1160, 680, 1980, 980], "Order (Payment State Entity)",
                 ["- id: Long", "- paymentMethod: PaymentMethod", "- isPaid: boolean", "- paidAt: LocalDateTime", "- status: OrderStatus"],
                 ["+ setPaid(boolean paid): void", "+ setPaidAt(LocalDateTime time): void"],
                 header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    return img

def render_all_perfect_class_diagrams():
    tasks = [
        ("Hinh_4.10a_Class_Diagram_BookDetail_Review", render_hinh_4_10a),
        ("Hinh_4.7_Class_Diagram_Login_Auth", render_hinh_4_7_class),
        ("Hinh_4.12_Class_Diagram_Checkout_COD", render_hinh_4_12_class),
        ("Hinh_4.13_Class_Diagram_Payment_Online", render_hinh_4_13_class),
    ]
    for name, fn in tasks:
        img = fn()
        for out_dir in [INFO_REV_DIR, STD_REV_DIR, INFO_DIR, STD_DIR]:
            out_p = os.path.join(out_dir, name + ".png")
            img.save(out_p, dpi=(300, 300))
            print(f"Saved perfect fit diagram: {out_p}")

if __name__ == "__main__":
    render_all_perfect_class_diagrams()

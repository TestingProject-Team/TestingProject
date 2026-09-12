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

from render_high_visibility_diagrams import get_font, draw_arrow, draw_header, draw_class_box_large
from render_large_text_diagrams import draw_large_card

# =========================================================================
# 1. HÌNH 4.7: CLASS DIAGRAM LOGIN & AUTH
# =========================================================================
def render_hinh_4_7_class():
    W, H = 2000, 1250
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP XÁC THỰC VÀ BẢO MẬT (LOGIN & JWT AUTH CLASS DIAGRAM)", 
                "Cấu trúc các lớp tham gia chứng thực danh tính, kiểm tra mật khẩu BCrypt và sinh JWT Token", W)
    
    # Top Row: AuthController -> AuthService -> JwtService & PasswordEncoder
    draw_class_box_large(draw, [80, 180, 600, 480], "AuthController",
                         ["- authService: AuthService"],
                         ["+ login(AuthRequest): ResponseEntity",
                          "+ register(RegisterRequest): ResponseEntity",
                          "+ changePassword(req): ResponseEntity",
                          "+ forgotPassword(email): ResponseEntity"],
                         header_bg=(147, 51, 234), box_bg=(250, 245, 255), border_color=(168, 85, 247))

    draw_arrow(draw, (600, 330), (700, 330), fill=(147, 51, 234), width=5, arrow_size=16)

    draw_class_box_large(draw, [700, 160, 1300, 520], "AuthService",
                         ["- userRepository: UserRepository",
                          "- passwordEncoder: PasswordEncoder",
                          "- jwtService: JwtService",
                          "- authenticationManager: AuthManager"],
                         ["+ authenticate(AuthRequest): AuthResponse",
                          "+ register(RegisterRequest): User",
                          "+ generateJwtToken(User user): String",
                          "+ validateCredentials(u, p): boolean"],
                         header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_arrow(draw, (1300, 280), (1400, 280), fill=(37, 99, 235), width=4, arrow_size=14)
    draw_class_box_large(draw, [1400, 180, 1920, 420], "JwtService",
                         ["- secretKey: String", "- expiration: Long"],
                         ["+ generateToken(User user): String",
                          "+ extractUsername(String token): String",
                          "+ isTokenValid(token, user): boolean"],
                         header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    draw_arrow(draw, (1300, 440), (1400, 440), fill=(37, 99, 235), width=4, arrow_size=14)
    draw_class_box_large(draw, [1400, 440, 1920, 640], "PasswordEncoder <<Interface>>",
                         [],
                         ["+ encode(rawPassword): String (BCrypt)",
                          "+ matches(raw, encoded): boolean"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Bottom Row: UserRepository -> User Entity & Role Enum
    draw_arrow(draw, (1000, 520), (1000, 680), fill=(37, 99, 235), width=5, arrow_size=16)

    draw_class_box_large(draw, [700, 680, 1300, 920], "UserRepository <<Interface>>",
                         [],
                         ["+ findByEmail(String email): Optional<User>",
                          "+ existsByEmail(String email): boolean",
                          "+ findByUsername(String username): Optional<User>"],
                         header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    draw_arrow(draw, (1000, 920), (1000, 1000), fill=(71, 85, 105), width=4, arrow_size=14, dashed=True)

    draw_class_box_large(draw, [400, 1000, 1100, 1220], "User <<Entity>>",
                         ["- id: Long", "- email: String", "- password: String (Hashed)", "- role: Role"],
                         ["+ getAuthorities(): Collection<GrantedAuthority>"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_class_box_large(draw, [1200, 1000, 1700, 1220], "Role <<Enum>>",
                         ["ROLE_CUSTOMER (Khách hàng)", "ROLE_ADMIN (Quản trị viên)"],
                         [],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    return img

# =========================================================================
# 2. HÌNH 4.12: CLASS DIAGRAM CHECKOUT & COD
# =========================================================================
def render_hinh_4_12_class():
    W, H = 2000, 1250
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP ĐẶT HÀNG COD & GIẢM GIÁ (CHECKOUT CLASS DIAGRAM)", 
                "Cấu trúc các lớp tham gia luồng kiểm tra giỏ hàng, áp mã giảm giá, trừ tồn kho và tạo đơn hàng", W)
    
    # Controllers & Services Row
    draw_class_box_large(draw, [80, 180, 600, 460], "OrderController",
                         ["- orderService: OrderService"],
                         ["+ createOrder(user, req): ResponseEntity",
                          "+ getMyOrders(user): ResponseEntity",
                          "+ getOrderById(id): ResponseEntity",
                          "+ cancelOrder(id): ResponseEntity"],
                         header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_arrow(draw, (600, 320), (700, 320), fill=(37, 99, 235), width=5, arrow_size=16)

    draw_class_box_large(draw, [700, 160, 1320, 520], "OrderService (@Transactional)",
                         ["- orderRepo: OrderRepository",
                          "- cartService: CartService",
                          "- couponService: CouponService",
                          "- bookRepo: BookRepository"],
                         ["+ createOrder(username, req): Order",
                          "+ validateStockAndItems(cart): void",
                          "+ calculateFinalAmount(cart, coupon): double",
                          "+ updateOrderStatus(id, status): Order"],
                         header_bg=(217, 119, 6), box_bg=(255, 251, 235), border_color=(245, 158, 11))

    draw_arrow(draw, (1320, 320), (1420, 320), fill=(217, 119, 6), width=5, arrow_size=16)

    draw_class_box_large(draw, [1420, 180, 1920, 460], "CouponService",
                         ["- couponRepository: CouponRepository"],
                         ["+ validateCoupon(code, total): Coupon",
                          "+ calculateDiscount(coupon, total): double",
                          "+ incrementUsageCount(coupon): void"],
                         header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # Repositories & Services Row 2
    draw_arrow(draw, (1010, 520), (1010, 640), fill=(217, 119, 6), width=5, arrow_size=16)

    draw_class_box_large(draw, [80, 640, 600, 880], "CartService",
                         ["- cartRepo: CartRepository"],
                         ["+ getCartByUser(username): Cart",
                          "+ clearCart(username): void",
                          "+ validateCartItems(cart): boolean"],
                         header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_class_box_large(draw, [680, 640, 1340, 880], "OrderRepository <<Interface>>",
                         [],
                         ["+ save(Order order): Order",
                          "+ findById(Long id): Optional<Order>",
                          "+ findByUserIdOrderByCreatedAtDesc(Long uid): List"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_class_box_large(draw, [1420, 640, 1920, 880], "BookRepository <<Interface>>",
                         [],
                         ["+ findByIdWithLock(Long id): Optional<Book>",
                          "+ updateStockQuantity(Long id, int qty): int"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Entities Row 3
    draw_arrow(draw, (1010, 880), (1010, 980), fill=(71, 85, 105), width=4, arrow_size=14, dashed=True)

    draw_class_box_large(draw, [300, 980, 1050, 1210], "Order <<Entity>>",
                         ["- id: Long", "- totalAmount: BigDecimal", "- status: OrderStatus", "- paymentMethod: PaymentMethod"],
                         ["+ getOrderItems(): List<OrderItem>", "+ setStatus(status): void"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_class_box_large(draw, [1150, 980, 1800, 1210], "OrderItem <<Entity>>",
                         ["- id: Long", "- book: Book", "- quantity: Integer", "- price: BigDecimal"],
                         ["+ getSubTotal(): BigDecimal"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    return img

# =========================================================================
# 3. HÌNH 4.13: CLASS DIAGRAM ONLINE PAYMENT (VNPAY)
# =========================================================================
def render_hinh_4_13_class():
    W, H = 2000, 1250
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP TÍCH HỢP CỔNG THANH TOÁN (ONLINE PAYMENT CLASS DIAGRAM)", 
                "Cấu trúc các lớp tích hợp cổng thanh toán trực tuyến VNPAY, sinh mã Checksum và xử lý Callback", W)
    
    draw_class_box_large(draw, [80, 180, 620, 520], "PaymentController",
                         ["- paymentService: PaymentService", "- orderService: OrderService"],
                         ["+ createPaymentUrl(orderId): ResponseEntity",
                          "+ vnpayCallback(params): ResponseEntity",
                          "+ momoCallback(params): ResponseEntity",
                          "+ zalopayCallback(params): ResponseEntity"],
                         header_bg=(217, 119, 6), box_bg=(255, 251, 235), border_color=(245, 158, 11))

    draw_arrow(draw, (620, 350), (720, 350), fill=(217, 119, 6), width=5, arrow_size=16)

    draw_class_box_large(draw, [720, 160, 1340, 540], "PaymentService",
                         ["- vnpayConfig: VNPayConfig", "- orderRepository: OrderRepository"],
                         ["+ createVNPayUrl(Order order, String ip): String",
                          "+ verifyVNPayCallback(Map<String,String>): boolean",
                          "+ processPaymentSuccess(Long orderId): void"],
                         header_bg=(217, 119, 6), box_bg=(255, 251, 235), border_color=(245, 158, 11))

    draw_arrow(draw, (1340, 350), (1440, 350), fill=(217, 119, 6), width=5, arrow_size=16)

    draw_class_box_large(draw, [1440, 180, 1920, 520], "VNPayConfig",
                         ["- vnp_PayUrl, vnp_TmnCode: String", "- secretKey: String (Hash Secret)"],
                         ["+ hmacSHA512(key, data): String",
                          "+ getIpAddress(HttpServletRequest): String",
                          "+ hashAllFields(fields): String"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Row 2: OrderService & Order Entity
    draw_arrow(draw, (1030, 540), (1030, 680), fill=(217, 119, 6), width=5, arrow_size=16)

    draw_class_box_large(draw, [200, 680, 950, 960], "OrderService (Payment Integration)",
                         ["- orderRepository: OrderRepository"],
                         ["+ updatePaymentStatus(orderId, status): void",
                          "+ confirmPaid(Long orderId): Order",
                          "+ handlePaymentFailure(Long orderId): void"],
                         header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_arrow(draw, (950, 820), (1080, 820), fill=(37, 99, 235), width=5, arrow_size=16)

    draw_class_box_large(draw, [1080, 680, 1820, 960], "Order (Payment State Entity)",
                         ["- id: Long", "- paymentMethod: PaymentMethod", "- isPaid: boolean", "- paidAt: LocalDateTime", "- status: OrderStatus"],
                         ["+ setPaid(boolean paid): void", "+ setPaidAt(LocalDateTime time): void"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    return img

def render_and_save_all_classes():
    print("Generating large text Class Diagrams for 4.7, 4.12, 4.13...")
    tasks = [
        ("Hinh_4.7_Class_Diagram_Login_Auth", render_hinh_4_7_class),
        ("Hinh_4.12_Class_Diagram_Checkout_COD", render_hinh_4_12_class),
        ("Hinh_4.13_Class_Diagram_Payment_Online", render_hinh_4_13_class),
    ]
    for name, fn in tasks:
        img = fn()
        for out_dir in [INFO_REV_DIR, STD_REV_DIR, INFO_DIR, STD_DIR]:
            out_p = os.path.join(out_dir, name + ".png")
            img.save(out_p, dpi=(300, 300))
            print(f"  -> Saved large text diagram: {out_p}")

if __name__ == "__main__":
    render_and_save_all_classes()

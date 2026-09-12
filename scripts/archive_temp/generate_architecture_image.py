import os
from PIL import Image, ImageDraw, ImageFont

# Khởi tạo kích thước ảnh HD (3200 x 1800) - Tỉ lệ chuẩn 16:9 sắc nét cho báo cáo
WIDTH = 3200
HEIGHT = 1800
BG_COLOR = (248, 250, 252) # Slate 50

img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Font loading
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

font_title = get_font(52, bold=True)
font_subtitle = get_font(28, bold=False)
font_col_header = get_font(32, bold=True)
font_box_title = get_font(26, bold=True)
font_body = get_font(22, bold=False)
font_caption = get_font(30, bold=True)

# 1. Header
title_text = "HỆ THỐNG YIYI BOOK — SYSTEM ARCHITECTURE"
draw.text((WIDTH // 2, 70), title_text, fill=(15, 23, 42), font=font_title, anchor="mm")

sub_text = "Multi-tier Client-Server Architecture: React 18 SPA | Spring Boot 3 REST | PostgreSQL 16 | External Cloud Services"
draw.text((WIDTH // 2, 130), sub_text, fill=(100, 116, 139), font=font_subtitle, anchor="mm")

# 2. Định nghĩa các cột chính (5 Cột Ngang)
MARGIN_X = 60
TOP_Y = 200
BOTTOM_Y = 1350
COL_GAP = 35
NUM_COLS = 5
TOTAL_AVAILABLE_W = WIDTH - (2 * MARGIN_X) - (COL_GAP * (NUM_COLS - 1))
COL_W = TOTAL_AVAILABLE_W // NUM_COLS

columns_meta = [
    {
        "title": "1. FRONTEND LAYER",
        "subtitle": "React 18 + Vite SPA",
        "header_bg": (2, 132, 199),     # Sky blue
        "col_bg": (240, 249, 255),
        "border_color": (186, 230, 253),
        "cards": [
            {
                "title": "📱 Customer Portal",
                "items": ["• Home, Book Listing, Filter", "• Cart, Checkout, Order Tracking", "• User Profile, Member Rewards", "• Reviews, Rating, FlashSale"]
            },
            {
                "title": "🛡️ Admin Portal",
                "items": ["• Book & Category Management", "• Order Processing & Status Flow", "• Coupon & Reward Voucher Mgmt", "• Review Moderation, Site Settings"]
            },
            {
                "title": "⚙️ Core Client Services",
                "items": ["• Auth, Cart, Lang Context (i18n)", "• Axios Interceptors (JWT Bearer)", "• YiYi AI Mini-RAG & Intent Engine"]
            }
        ]
    },
    {
        "title": "SECURITY & CONFIG",
        "subtitle": "Spring Security & Gateways",
        "header_bg": (217, 119, 6),     # Amber
        "col_bg": (254, 243, 199),
        "border_color": (253, 230, 138),
        "cards": [
            {
                "title": "🔒 Spring Security 6",
                "items": ["• Stateless Session Management", "• Role-Based Access Control (RBAC)", "• PreAuthorize (USER / ADMIN)"]
            },
            {
                "title": "🔑 JWT Auth Filter",
                "items": ["• JwtAuthFilter Request Intercept", "• JwtService: Token Gen & Verify", "• Claims Extraction (Username, Role)"]
            },
            {
                "title": "📡 WebSocket & STOMP",
                "items": ["• Real-time Notification Broker", "• Live Order Status Update"]
            },
            {
                "title": "⚙️ System Configurations",
                "items": ["• CORS Policy & WebMvcConfig", "• CacheFilter (Response Caching)", "• HikariCP Connection Pool (10)"]
            }
        ]
    },
    {
        "title": "2. BACKEND API LAYER",
        "subtitle": "23 Spring REST Controllers",
        "header_bg": (5, 150, 105),     # Emerald
        "col_bg": (236, 253, 245),
        "border_color": (167, 243, 208),
        "cards": [
            {
                "title": "🔑 Auth & User (4 APIs)",
                "items": ["• AuthController (Login/Register/OTP)", "• UserController, AddressController", "• AdminUserController"]
            },
            {
                "title": "📚 Catalogue (4 APIs)",
                "items": ["• BookController, CategoryController", "• BannerController, FileController"]
            },
            {
                "title": "🛒 Commerce (4 APIs)",
                "items": ["• CartController, OrderController", "• WishlistController", "• VatInvoiceController"]
            },
            {
                "title": "💳 Pay & Community (11 APIs)",
                "items": ["• PaymentController (VNPay/MoMo/Zalo)", "• ReviewController, AdminReviewCtrl", "• RewardController, AdminRewardCtrl", "• Coupon, Notice, Newsletter, Contact"]
            }
        ]
    },
    {
        "title": "3. BUSINESS SERVICES",
        "subtitle": "15 Core Domain Services",
        "header_bg": (22, 163, 74),     # Green
        "col_bg": (240, 253, 244),
        "border_color": (187, 247, 208),
        "cards": [
            {
                "title": "👤 Auth & Identity Services",
                "items": ["• AuthService (JWT, Hash Pass, OTP)", "• UserService (Profile, Membership)", "• AddressService"]
            },
            {
                "title": "📚 Catalogue & Content Services",
                "items": ["• BookService (Stock, Price, Search)", "• CategoryService, BannerService", "• SiteSettingService"]
            },
            {
                "title": "🛒 Commerce & Order Services",
                "items": ["• CartService (Persistent Cart)", "• OrderService (@Transactional)", "• CouponService, RewardService"]
            },
            {
                "title": "💬 Interaction & System Services",
                "items": ["• ReviewService, ContactService", "• NotificationService, Newsletter", "• WebSocketService (Push Notification)"]
            }
        ]
    },
    {
        "title": "4. PERSISTENCE & DB",
        "subtitle": "Spring Data JPA & Postgres",
        "header_bg": (124, 58, 237),    # Violet
        "col_bg": (245, 243, 255),
        "border_color": (221, 214, 254),
        "cards": [
            {
                "title": "🗄️ 19 JPA Repositories",
                "items": ["• UserRepository, BookRepository", "• OrderRepository, CartRepository", "• CategoryRepository, ReviewRepo", "• CouponRepo, RewardVoucherRepo", "• PointTransactionRepository, ..."]
            },
            {
                "title": "📋 25 Relational Entities",
                "items": ["• User, Role, AuthProvider, Address", "• Book, Category, Banner, Review", "• Order, OrderItem, Cart, CartItem", "• Coupon, RewardVoucher, SiteSetting"]
            },
            {
                "title": "🐘 5. PostgreSQL 16 Database",
                "items": ["• Relational ACID Data Storage", "• Supabase Cloud / Docker Container", "• HikariCP Pool Manager (10 conns)"]
            }
        ]
    }
]

# Vẽ các cột
for idx, col in enumerate(columns_meta):
    cx = MARGIN_X + idx * (COL_W + COL_GAP)
    cy = TOP_Y
    
    # Khung cột
    draw.rounded_rectangle([cx, cy, cx + COL_W, BOTTOM_Y], radius=16, fill=col["col_bg"], outline=col["border_color"], width=3)
    
    # Header cột
    HEADER_H = 80
    draw.rounded_rectangle([cx, cy, cx + COL_W, cy + HEADER_H], radius=16, fill=col["header_bg"])
    # Vá phần bo góc dưới của header
    draw.rectangle([cx, cy + HEADER_H - 16, cx + COL_W, cy + HEADER_H], fill=col["header_bg"])
    
    draw.text((cx + COL_W // 2, cy + 28), col["title"], fill=(255, 255, 255), font=font_col_header, anchor="mm")
    draw.text((cx + COL_W // 2, cy + 60), col["subtitle"], fill=(241, 245, 249), font=get_font(20, bold=False), anchor="mm")
    
    # Vẽ các card con bên trong cột
    num_cards = len(col["cards"])
    AVAILABLE_CARD_H = BOTTOM_Y - (cy + HEADER_H) - 25
    CARD_GAP = 16
    CARD_H = (AVAILABLE_CARD_H - (CARD_GAP * (num_cards - 1))) // num_cards
    
    card_y = cy + HEADER_H + 15
    for card in col["cards"]:
        card_x = cx + 14
        card_w = COL_W - 28
        
        # Card background
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + CARD_H], radius=12, fill=(255, 255, 255), outline=col["border_color"], width=2)
        
        # Card title
        draw.text((card_x + 16, card_y + 24), card["title"], fill=(30, 41, 59), font=font_box_title, anchor="lm")
        
        # Card items
        item_y = card_y + 55
        for item in card["items"]:
            draw.text((card_x + 16, item_y), item, fill=(71, 85, 105), font=font_body, anchor="lm")
            item_y += 30
            
        card_y += CARD_H + CARD_GAP

# 3. Vẽ các mũi tên luồng liên kết giữa các cột chính
def draw_arrow(x1, y1, x2, y2, label=""):
    draw.line([x1, y1, x2, y2], fill=(14, 116, 144), width=5)
    # Đầu mũi tên
    arrow_size = 12
    draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size//2), (x2 - arrow_size, y2 + arrow_size//2)], fill=(14, 116, 144))
    if label:
        draw.text(((x1 + x2)//2, y1 - 18), label, fill=(14, 116, 144), font=get_font(18, bold=True), anchor="mm")

# Liên kết ngang giữa 5 cột
arrow_y = TOP_Y + 40
for idx in range(NUM_COLS - 1):
    ax1 = MARGIN_X + (idx + 1) * COL_W + idx * COL_GAP + 2
    ax2 = ax1 + COL_GAP - 4
    # Vẽ biểu tượng mũi tên kết nối
    draw.line([ax1, arrow_y, ax2, arrow_y], fill=(255, 255, 255), width=4)
    draw.polygon([(ax2, arrow_y), (ax2 - 10, arrow_y - 6), (ax2 - 10, arrow_y + 6)], fill=(255, 255, 255))

# 4. TẦNG TÍCH HỢP NGOÀI (6. EXTERNAL INTEGRATION LAYER) - Khung dưới cùng
EXT_Y = 1400
EXT_H = 260
draw.rounded_rectangle([MARGIN_X, EXT_Y, WIDTH - MARGIN_X, EXT_Y + EXT_H], radius=16, fill=(253, 242, 248), outline=(244, 114, 182), width=3)

# Header tầng External
draw.rounded_rectangle([MARGIN_X, EXT_Y, MARGIN_X + 420, EXT_Y + 50], radius=12, fill=(219, 39, 119))
draw.text((MARGIN_X + 210, EXT_Y + 25), "6. EXTERNAL INTEGRATION LAYER", fill=(255, 255, 255), font=get_font(24, bold=True), anchor="mm")

# 4 Hộp dịch vụ bên ngoài
ext_services = [
    {
        "icon": "🤖",
        "title": "Groq Cloud AI (Llama 3.3 70B)",
        "desc": "Mini-RAG, Intent Detection Engine, SSE Streaming response"
    },
    {
        "icon": "💳",
        "title": "Payment Gateways & VietQR",
        "desc": "VNPay, MoMo, ZaloPay, Dynamic VietQR payment processing"
    },
    {
        "icon": "📧",
        "title": "Email Services (Resend / SMTP)",
        "desc": "Transactional OTP emails, Marketing Newsletters"
    },
    {
        "icon": "🚀",
        "title": "Cloud Infrastructure & DevOps",
        "desc": "Vercel (FE) | Render (BE) | Docker Compose | Supabase DB"
    }
]

EXT_BOX_GAP = 30
EXT_BOX_W = (WIDTH - (2 * MARGIN_X) - 60 - (EXT_BOX_GAP * 3)) // 4
for i, ext in enumerate(ext_services):
    eb_x = MARGIN_X + 30 + i * (EXT_BOX_W + EXT_BOX_GAP)
    eb_y = EXT_Y + 70
    eb_h = EXT_H - 95
    
    draw.rounded_rectangle([eb_x, eb_y, eb_x + EXT_BOX_W, eb_y + eb_h], radius=12, fill=(255, 255, 255), outline=(249, 168, 212), width=2)
    draw.text((eb_x + 20, eb_y + 35), f"{ext['icon']}  {ext['title']}", fill=(157, 23, 77), font=get_font(22, bold=True), anchor="lm")
    draw.text((eb_x + 20, eb_y + 75), ext["desc"], fill=(71, 85, 105), font=get_font(18, bold=False), anchor="lm")

# Caption dưới cùng
caption_text = "Hình 4.1. System Architecture của YiYi Book (Kiến trúc phân tầng mở rộng đa dịch vụ)"
draw.text((WIDTH // 2, HEIGHT - 60), caption_text, fill=(30, 41, 59), font=font_caption, anchor="mm")

# Lưu ảnh ra thư mục docs/ và thư mục gốc
out_path = "docs/Hinh_4.1_System_Architecture_YiYi_Book.png"
img.save(out_path, "PNG", dpi=(300, 300))
img.save("Hinh_4.1_System_Architecture_YiYi_Book.png", "PNG", dpi=(300, 300))
print("Successfully generated image at:", out_path)

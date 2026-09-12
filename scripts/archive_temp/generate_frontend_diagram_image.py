import os
from PIL import Image, ImageDraw, ImageFont

# Khởi tạo kích thước ảnh HD (3200 x 1800) - Tỉ lệ 16:9 chuẩn báo cáo
WIDTH = 3200
HEIGHT = 1800
BG_COLOR = (248, 250, 252) # Slate 50

img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

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

font_title = get_font(50, bold=True)
font_subtitle = get_font(26, bold=False)
font_layer_header = get_font(28, bold=True)
font_box_title = get_font(24, bold=True)
font_body = get_font(20, bold=False)
font_caption = get_font(30, bold=True)

# 1. Header
title_text = "KIẾN TRÚC FRONTEND COMPONENT & ROUTE TREE"
draw.text((WIDTH // 2, 65), title_text, fill=(15, 23, 42), font=font_title, anchor="mm")

sub_text = "React 18 SPA | State Providers | Client Layout & Admin Layout | Route Hierarchy | Reusable UI"
draw.text((WIDTH // 2, 120), sub_text, fill=(100, 116, 139), font=font_subtitle, anchor="mm")

# 2. Tầng 1: Global Context Providers (Ngang trên cùng)
CTX_Y = 175
CTX_H = 150
MARGIN_X = 60
draw.rounded_rectangle([MARGIN_X, CTX_Y, WIDTH - MARGIN_X, CTX_Y + CTX_H], radius=14, fill=(240, 249, 255), outline=(186, 230, 253), width=3)
draw.rounded_rectangle([MARGIN_X, CTX_Y, MARGIN_X + 400, CTX_Y + 45], radius=10, fill=(2, 132, 199))
draw.text((MARGIN_X + 200, CTX_Y + 22), "1. GLOBAL CONTEXT PROVIDERS (STATE)", fill=(255, 255, 255), font=get_font(22, bold=True), anchor="mm")

providers = [
    {"title": "🌐 LanguageProvider", "desc": "i18n Context (vi/en switch, local dictionary)"},
    {"title": "🔐 AuthProvider", "desc": "JWT State, Current User, Role-based Access, OTP"},
    {"title": "🛒 CartProvider", "desc": "Cart persistence, items count, subtotal, voucher"},
    {"title": "📡 WebSocketProvider", "desc": "STOMP connection, realtime push notifications"}
]

CTX_BOX_W = (WIDTH - (2 * MARGIN_X) - 60 - (25 * 3)) // 4
for i, p in enumerate(providers):
    px = MARGIN_X + 30 + i * (CTX_BOX_W + 25)
    py = CTX_Y + 58
    ph = CTX_H - 75
    draw.rounded_rectangle([px, py, px + CTX_BOX_W, py + ph], radius=10, fill=(255, 255, 255), outline=(186, 230, 253), width=2)
    draw.text((px + 16, py + 22), p["title"], fill=(3, 105, 161), font=font_box_title, anchor="lm")
    draw.text((px + 16, py + 52), p["desc"], fill=(71, 85, 105), font=font_body, anchor="lm")

# 3. Tầng 2: BrowserRouter & Layouts (2 Khung Lớn Song Song: Client Layout vs Admin Layout)
MAIN_Y = 355
MAIN_H = 880
SPLIT_W = (WIDTH - (2 * MARGIN_X) - 40) // 2

# === KHUNG TRÁI: CLIENT LAYOUT ===
CL_X = MARGIN_X
draw.rounded_rectangle([CL_X, MAIN_Y, CL_X + SPLIT_W, MAIN_Y + MAIN_H], radius=16, fill=(240, 253, 244), outline=(187, 247, 208), width=3)
draw.rounded_rectangle([CL_X, MAIN_Y, CL_X + 480, MAIN_Y + 50], radius=12, fill=(22, 163, 74))
draw.text((CL_X + 240, MAIN_Y + 25), "2. CLIENT LAYOUT (/ - Customer Routes)", fill=(255, 255, 255), font=font_layer_header, anchor="mm")

# Header & Navigation UI inside Client Layout
draw.rounded_rectangle([CL_X + 25, MAIN_Y + 68, CL_X + SPLIT_W - 25, MAIN_Y + 145], radius=10, fill=(255, 255, 255), outline=(187, 247, 208), width=2)
draw.text((CL_X + 45, MAIN_Y + 92), "🧩 Layout Frame: Header (MegaMenu, SearchBar, MiniCart) + Footer (Links, Policy, Social)", fill=(22, 101, 52), font=get_font(22, bold=True), anchor="lm")
draw.text((CL_X + 45, MAIN_Y + 124), "Overlay Widgets: <AIChatWidget /> (Groq Llama 3.3 70B AI) + <ScrollToTopButton />", fill=(71, 85, 105), font=font_body, anchor="lm")

# 3 Nhóm Route Client
client_route_groups = [
    {
        "title": "🛍️ Core Commerce Pages (E-Commerce Flow)",
        "routes": [
            "• / : Home (HeroBanner, FlashSale, BestSellerRank, ComboTrending)",
            "• /category/:categoryId : Category (Dynamic filters, Price, Rating)",
            "• /book/:id : ProductDetail (Image gallery, Stock, Nested reviews)",
            "• /cart : Cart (Voucher selection, Point redemption, Quantity)",
            "• /checkout : Checkout (AddressModal, Province select, Payment)",
            "• /payment-result & /order-success/:id : Order completion & QR status"
        ]
    },
    {
        "title": "👤 Account & Orders Pages",
        "routes": [
            "• /login & /register : Authentication, OTP Verification, Firebase",
            "• /profile : User profile, Address management, AI Preference training",
            "• /orders & /orders/:id : Order history & 5-step status tracking",
            "• /notifications : Realtime notification inbox (STOMP WebSockets)",
            "• /coupons & /flash-sale : Voucher wallet & Flash sale events"
        ]
    },
    {
        "title": "📜 Policy & Information Pages (Lazy Loaded)",
        "routes": [
            "• /about, /new-books, /used-books, /promotions",
            "• /terms, /privacy, /payment-privacy, /returns, /warranty",
            "• /shipping, /faq, /contact"
        ]
    }
]

cg_y = MAIN_Y + 165
for cg in client_route_groups:
    cg_h = 220
    draw.rounded_rectangle([CL_X + 25, cg_y, CL_X + SPLIT_W - 25, cg_y + cg_h], radius=12, fill=(255, 255, 255), outline=(187, 247, 208), width=2)
    draw.text((CL_X + 45, cg_y + 28), cg["title"], fill=(21, 128, 61), font=font_box_title, anchor="lm")
    
    ry = cg_y + 60
    for r in cg["routes"]:
        draw.text((CL_X + 45, ry), r, fill=(51, 65, 85), font=font_body, anchor="lm")
        ry += 25
    cg_y += cg_h + 15

# === KHUNG PHẢI: ADMIN LAYOUT ===
AL_X = MARGIN_X + SPLIT_W + 40
draw.rounded_rectangle([AL_X, MAIN_Y, AL_X + SPLIT_W, MAIN_Y + MAIN_H], radius=16, fill=(254, 243, 199), outline=(253, 230, 138), width=3)
draw.rounded_rectangle([AL_X, MAIN_Y, AL_X + 480, MAIN_Y + 50], radius=12, fill=(217, 119, 6))
draw.text((AL_X + 240, MAIN_Y + 25), "3. ADMIN LAYOUT (/admin/* - Admin Portal)", fill=(255, 255, 255), font=font_layer_header, anchor="mm")

# Admin Frame Info
draw.rounded_rectangle([AL_X + 25, MAIN_Y + 68, AL_X + SPLIT_W - 25, MAIN_Y + 145], radius=10, fill=(255, 255, 255), outline=(253, 230, 138), width=2)
draw.text((AL_X + 45, MAIN_Y + 92), "🛡️ Layout Frame: AdminSidebar + AdminHeader + Role-based Route Guard (ROLE_ADMIN)", fill=(180, 83, 9), font=get_font(22, bold=True), anchor="lm")
draw.text((AL_X + 45, MAIN_Y + 124), "All admin pages are Lazy-Loaded (Suspense + <PageLoader />) to optimize initial bundle", fill=(71, 85, 105), font=font_body, anchor="lm")

# 3 Nhóm Admin Routes
admin_route_groups = [
    {
        "title": "📊 Dashboard & Catalogue Management",
        "routes": [
            "• /admin/dashboard : Business analytics, revenue, recent orders chart",
            "• /admin/books : Book catalog CRUD, bulk stock, multi-image upload",
            "• /admin/featured-books : Manage homepage featured book rankings",
            "• /admin/categories : Hierarchical category & slug management",
            "• /admin/banners : Hero & promotional banner carousel manager"
        ]
    },
    {
        "title": "📦 Operations, Orders & Customers",
        "routes": [
            "• /admin/orders : Order approval, fulfillment status, refund request",
            "• /admin/users : User accounts, RBAC role assignment, rank tiers",
            "• /admin/reviews : Review moderation, report handling, comment replies",
            "• /admin/contacts : Customer contact inquiries & ticket resolution"
        ]
    },
    {
        "title": "🎫 Marketing, Rewards & Settings",
        "routes": [
            "• /admin/coupons : Discount coupon codes, expiry, min-order limits",
            "• /admin/rewards : Y-Point reward voucher catalog configuration",
            "• /admin/notifications : Broadcast & targeted push notifications",
            "• /admin/newsletter : Subscriber list & newsletter email campaign",
            "• /admin/settings : Site identity, payment keys, footer configuration"
        ]
    }
]

ag_y = MAIN_Y + 165
for ag in admin_route_groups:
    ag_h = 220
    draw.rounded_rectangle([AL_X + 25, ag_y, AL_X + SPLIT_W - 25, ag_y + ag_h], radius=12, fill=(255, 255, 255), outline=(253, 230, 138), width=2)
    draw.text((AL_X + 45, ag_y + 28), ag["title"], fill=(180, 83, 9), font=font_box_title, anchor="lm")
    
    ry = ag_y + 60
    for r in ag["routes"]:
        draw.text((AL_X + 45, ry), r, fill=(51, 65, 85), font=font_body, anchor="lm")
        ry += 25
    ag_y += ag_h + 15

# 4. Tầng 3: Reusable Component Library & Utilities (Khung dưới cùng)
COMP_Y = 1260
COMP_H = 430
draw.rounded_rectangle([MARGIN_X, COMP_Y, WIDTH - MARGIN_X, COMP_Y + COMP_H], radius=16, fill=(245, 243, 255), outline=(221, 214, 254), width=3)
draw.rounded_rectangle([MARGIN_X, COMP_Y, MARGIN_X + 460, COMP_Y + 48], radius=12, fill=(124, 58, 237))
draw.text((MARGIN_X + 230, COMP_Y + 24), "4. REUSABLE UI COMPONENTS & UTILITIES", fill=(255, 255, 255), font=font_layer_header, anchor="mm")

comp_blocks = [
    {
        "title": "🏠 Home Widgets (components/home)",
        "items": [
            "• HeroBanner (Promotion slider)",
            "• FlashSale (Countdown clock)",
            "• BestSellerRank (Rankings)",
            "• BestSellersByCategory (Tabs)",
            "• ComboTrending & QuickLinks",
            "• PartnerBrands & Suggestions"
        ]
    },
    {
        "title": "🤖 AI & Shared UI (components/common)",
        "items": [
            "• AIChatWidget (Mini-RAG Engine)",
            "• Intro (Branding splash screen)",
            "• AddressModal (Province select)",
            "• ScrollToTop & ScrollToTopBtn",
            "• SwiperNavButtons (Sliders)",
            "• PageLoader (Suspense spinner)"
        ]
    },
    {
        "title": "🛠️ Utilities & Assets (utils & data)",
        "items": [
            "• alert.js (Toast & Modal alerts)",
            "• provinces.json (34 VN Provinces)",
            "• Axios Instance (JWT headers)",
            "• vi.js / en.js (Locales dictionary)",
            "• Anti-inspect & Anti-copy guards",
            "• Tailwind CSS v4 styling rules"
        ]
    }
]

COMP_BOX_W = (WIDTH - (2 * MARGIN_X) - 60 - (30 * 2)) // 3
for i, cb in enumerate(comp_blocks):
    cb_x = MARGIN_X + 30 + i * (COMP_BOX_W + 30)
    cb_y = COMP_Y + 68
    cb_h = COMP_H - 95
    
    draw.rounded_rectangle([cb_x, cb_y, cb_x + COMP_BOX_W, cb_y + cb_h], radius=12, fill=(255, 255, 255), outline=(221, 214, 254), width=2)
    draw.text((cb_x + 20, cb_y + 28), cb["title"], fill=(109, 40, 217), font=font_box_title, anchor="lm")
    
    iy = cb_y + 65
    for item in cb["items"]:
        draw.text((cb_x + 20, iy), item, fill=(51, 65, 85), font=font_body, anchor="lm")
        iy += 38

# Caption
caption_text = "Hình 4.2. Cấu trúc Frontend component và route của YiYi Book"
draw.text((WIDTH // 2, HEIGHT - 35), caption_text, fill=(30, 41, 59), font=font_caption, anchor="mm")

# Xuất ảnh
out_path = "docs/Hinh_4.2_Frontend_Component_Route_YiYi_Book.png"
img.save(out_path, "PNG", dpi=(300, 300))
img.save("Hinh_4.2_Frontend_Component_Route_YiYi_Book.png", "PNG", dpi=(300, 300))
print("Successfully generated image at:", out_path)

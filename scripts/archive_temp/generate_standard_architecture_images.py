import os
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# HÌNH 1: SYSTEM ARCHITECTURE (GIỐNG 100% STYLE ẢNH MẪU 1)
# ==============================================================================
W1, H1 = 2600, 1900
img1 = Image.new("RGBA", (W1, H1), (255, 255, 255))
draw1 = ImageDraw.Draw(img1)

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

f_main_title = get_font(42, bold=True)
f_box_header = get_font(30, bold=False)
f_box_title = get_font(34, bold=True)
f_label = get_font(24, bold=False)
f_caption = get_font(32, bold=True)
f_tech_title = get_font(38, bold=True)
f_thirdparty_title = get_font(36, bold=False)

# 1. Khung lớn bao quanh Hệ thống chính (Main System Box)
SYS_X1, SYS_Y1 = 150, 120
SYS_X2, SYS_Y2 = 2450, 1120

# Vẽ khung lớn
draw1.rectangle([SYS_X1, SYS_Y1, SYS_X2, SYS_Y2], outline=(120, 120, 120), width=3)
# Tên hệ thống trên đỉnh
draw1.text(((SYS_X1 + SYS_X2)//2, SYS_Y1 + 55), "YiYi Book Online Bookstore Management System", fill=(0, 0, 0), font=f_main_title, anchor="mm")

# 2. Khung Client-side
CS_X1, CS_Y1 = 240, 320
CS_X2, CS_Y2 = 720, 940
draw1.rectangle([CS_X1, CS_Y1, CS_X2, CS_Y2], outline=(140, 140, 140), width=2)
draw1.text(((CS_X1 + CS_X2)//2, CS_Y1 + 45), "Client-side", fill=(0, 0, 0), font=f_box_header, anchor="mm")

# Khung Web Application bên trong Client-side
WA_X1, WA_Y1 = 280, 500
WA_X2, WA_Y2 = 680, 890
draw1.rectangle([WA_X1, WA_Y1, WA_X2, WA_Y2], outline=(140, 140, 140), width=2)
draw1.text(((WA_X1 + WA_X2)//2, WA_Y1 + 35), "Web Application", fill=(0, 0, 0), font=get_font(26, bold=False), anchor="mm")

# Logo / Chữ REACT / VITE
draw1.text(((WA_X1 + WA_X2)//2, WA_Y1 + 180), "⚛  React.js", fill=(8, 126, 164), font=f_tech_title, anchor="mm")
draw1.text(((WA_X1 + WA_X2)//2, WA_Y1 + 240), "(React 18 + Vite SPA)", fill=(100, 116, 139), font=get_font(22, bold=False), anchor="mm")

# 3. Khung Server-side
SS_X1, SS_Y1 = 1100, 240
SS_X2, SS_Y2 = 1860, 1030
draw1.rectangle([SS_X1, SS_Y1, SS_X2, SS_Y2], outline=(140, 140, 140), width=2)
draw1.text(((SS_X1 + SS_X2)//2, SS_Y1 + 45), "Server-side", fill=(0, 0, 0), font=f_box_header, anchor="mm")

# Khung Rest API bên trong Server-side
API_X1, API_Y1 = 1180, 390
API_X2, API_Y2 = 1780, 930
draw1.rectangle([API_X1, API_Y1, API_X2, API_Y2], outline=(140, 140, 140), width=2)
draw1.text(((API_X1 + API_X2)//2, API_Y1 + 40), "Rest API", fill=(0, 0, 0), font=get_font(28, bold=False), anchor="mm")

# Box Spring Boot màu xanh lá chuẩn giống ảnh mẫu
SB_X1, SB_Y1 = 1240, 500
SB_X2, SB_Y2 = 1720, 830
draw1.rectangle([SB_X1, SB_Y1, SB_X2, SB_Y2], fill=(109, 179, 63), outline=(90, 150, 50), width=2)
# Chữ Spring Boot
draw1.text(((SB_X1 + SB_X2)//2, SB_Y1 + 120), "🍃  spring", fill=(255, 255, 255), font=get_font(44, bold=True), anchor="mm")
draw1.text(((SB_X1 + SB_X2)//2, SB_Y1 + 190), "Boot 3", fill=(255, 255, 255), font=get_font(40, bold=True), anchor="mm")
draw1.text(((SB_X1 + SB_X2)//2, SB_Y1 + 260), "(Java 17 / REST)", fill=(240, 255, 240), font=get_font(22, bold=False), anchor="mm")

# 4. Hình trụ Database (PostgreSQL) bên phải
DB_X = 2120
DB_Y = 540
DB_W = 200
DB_H = 260

# Vẽ hình trụ DB
draw1.ellipse([DB_X - DB_W//2, DB_Y - 40, DB_X + DB_W//2, DB_Y + 40], outline=(100, 100, 100), width=3, fill=(250, 250, 250))
draw1.rectangle([DB_X - DB_W//2, DB_Y, DB_X + DB_W//2, DB_Y + DB_H], fill=(250, 250, 250))
draw1.line([DB_X - DB_W//2, DB_Y, DB_X - DB_W//2, DB_Y + DB_H], fill=(100, 100, 100), width=3)
draw1.line([DB_X + DB_W//2, DB_Y, DB_X + DB_W//2, DB_Y + DB_H], fill=(100, 100, 100), width=3)
draw1.ellipse([DB_X - DB_W//2, DB_Y + DB_H - 40, DB_X + DB_W//2, DB_Y + DB_H + 40], outline=(100, 100, 100), width=3, fill=(250, 250, 250))
# Header DB
draw1.ellipse([DB_X - DB_W//2, DB_Y - 40, DB_X + DB_W//2, DB_Y + 40], outline=(100, 100, 100), width=3, fill=(250, 250, 250))

# Logo / Chữ PostgreSQL
draw1.text((DB_X, DB_Y + 110), "🐘", fill=(51, 103, 145), font=get_font(50, bold=True), anchor="mm")
draw1.text((DB_X, DB_Y + 180), "PostgreSQL", fill=(51, 103, 145), font=get_font(26, bold=True), anchor="mm")

# 5. Các mũi tên liên kết giữa Client -> Server và Server -> DB
def draw_line_arrow(x1, y1, x2, y2, dashed=False, label="", label_y_offset=-18):
    if dashed:
        # Vẽ nét đứt
        dash_len = 12
        space_len = 8
        total_len = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        ux = (x2 - x1) / total_len
        uy = (y2 - y1) / total_len
        curr = 0
        while curr < total_len:
            end_dash = min(curr + dash_len, total_len)
            draw1.line([x1 + curr*ux, y1 + curr*uy, x1 + end_dash*ux, y1 + end_dash*uy], fill=(80, 80, 80), width=2)
            curr += dash_len + space_len
    else:
        draw1.line([x1, y1, x2, y2], fill=(80, 80, 80), width=2)
        
    # Mũi tên tại (x2, y2)
    # Xác định góc
    if x2 > x1:
        draw1.polygon([(x2, y2), (x2 - 12, y2 - 6), (x2 - 12, y2 + 6)], fill=(80, 80, 80))
    elif x2 < x1:
        draw1.polygon([(x2, y2), (x2 + 12, y2 - 6), (x2 + 12, y2 + 6)], fill=(80, 80, 80))
    elif y2 > y1:
        draw1.polygon([(x2, y2), (x2 - 6, y2 - 12), (x2 + 6, y2 - 12)], fill=(80, 80, 80))
    elif y2 < y1:
        draw1.polygon([(x2, y2), (x2 - 6, y2 + 12), (x2 + 6, y2 + 12)], fill=(80, 80, 80))
        
    if label:
        draw1.text(((x1 + x2)//2, (y1 + y2)//2 + label_y_offset), label, fill=(50, 50, 50), font=f_label, anchor="mm")

# Mũi tên Client -> Server (HTTP Request: nét liền)
draw_line_arrow(680, 600, 1180, 600, dashed=False, label="HTTP Request", label_y_offset=-20)
# Mũi tên Server -> Client (HTTP Response: nét đứt)
draw_line_arrow(1180, 680, 680, 680, dashed=True, label="HTTP Response", label_y_offset=22)

# Mũi tên Server -> DB (Query: nét liền)
draw_line_arrow(1780, 600, 2020, 600, dashed=False, label="Query", label_y_offset=-20)
# Mũi tên DB -> Server (Returned value: nét đứt)
draw_line_arrow(2020, 680, 1780, 680, dashed=True, label="Returned value", label_y_offset=22)


# 6. Khung Third-parties phía dưới (Khung xám dài)
TP_X1, TP_Y1 = 350, 1300
TP_X2, TP_Y2 = 2250, 1620
draw1.rectangle([TP_X1, TP_Y1, TP_X2, TP_Y2], outline=(120, 120, 120), width=3)
draw1.text(((TP_X1 + TP_X2)//2, TP_Y1 + 45), "Third-parties", fill=(0, 0, 0), font=f_thirdparty_title, anchor="mm")

# Các logo / box trong Third-parties
third_boxes = [
    {"title": "🤖 Groq AI", "sub": "Llama 3.3 70B", "color": (249, 115, 22)},
    {"title": "WEBSOCKETS", "sub": "STOMP Push", "color": (234, 179, 8)},
    {"title": "🐳 DOCKER", "sub": "Container", "color": (2, 132, 199)},
    {"title": "💳 PAYMENT", "sub": "VNPay / MoMo / Zalo", "color": (225, 29, 72)},
    {"title": "📧 EMAIL", "sub": "Resend / SMTP", "color": (79, 70, 229)}
]

TP_INNER_W = (TP_X2 - TP_X1 - 100 - (30 * 4)) // 5
for i, tb in enumerate(third_boxes):
    bx = TP_X1 + 50 + i * (TP_INNER_W + 30)
    by = TP_Y1 + 90
    bw = TP_INNER_W
    bh = 190
    draw1.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, outline=(200, 200, 200), width=2, fill=(255, 255, 255))
    draw1.text((bx + bw//2, by + 75), tb["title"], fill=tb["color"], font=get_font(28, bold=True), anchor="mm")
    draw1.text((bx + bw//2, by + 130), tb["sub"], fill=(100, 116, 139), font=get_font(22, bold=False), anchor="mm")

# Mũi tên giữa Server-side và Third-parties
# Server -> Third-parties (Send Request: nét liền)
draw1.line([1600, 1030, 1600, 1300], fill=(80, 80, 80), width=2)
draw1.polygon([(1600, 1300), (1594, 1288), (1606, 1288)], fill=(80, 80, 80))
draw1.text((1600 + 100, 1165), "Send Request", fill=(50, 50, 50), font=f_label, anchor="lm")

# Third-parties -> Server (Return Value: nét đứt)
# Vẽ nét đứt từ 1380 lên
dash_len = 12
space_len = 8
curr = 1300
while curr > 1030:
    end_dash = max(curr - dash_len, 1030)
    draw1.line([1380, curr, 1380, end_dash], fill=(80, 80, 80), width=2)
    curr -= dash_len + space_len
draw1.polygon([(1380, 1030), (1374, 1042), (1386, 1042)], fill=(80, 80, 80))
draw1.text((1380 - 20, 1165), "Return Value", fill=(50, 50, 50), font=f_label, anchor="rm")

# Chú thích cuối ảnh
draw1.text((W1 // 2, 1780), "1.1 System Architecture", fill=(0, 0, 0), font=f_caption, anchor="mm")

# Lưu ảnh 1
out1 = "docs/Figure_1.1_System_Architecture_YiYi_Book.png"
img1.save(out1, "PNG", dpi=(300, 300))
img1.save("Figure_1.1_System_Architecture_YiYi_Book.png", "PNG", dpi=(300, 300))
print("Saved Figure 1.1 at:", out1)


# ==============================================================================
# HÌNH 2: BACKEND ARCHITECTURE (GIỐNG 100% STYLE ẢNH MẪU 2)
# ==============================================================================
W2, H2 = 2600, 2000
img2 = Image.new("RGBA", (W2, H2), (255, 255, 255))
draw2 = ImageDraw.Draw(img2)

# Khung vàng to: SPRING BOOT APPLICATION
APP_X1, APP_Y1 = 520, 120
APP_X2, APP_Y2 = 2380, 1500

# Header vàng
draw2.rounded_rectangle([APP_X1, APP_Y1, APP_X2, APP_Y2], radius=6, outline=(220, 190, 100), width=2, fill=(255, 255, 255))
draw2.rectangle([APP_X1, APP_Y1, APP_X2, APP_Y1 + 75], fill=(254, 243, 199))
draw2.line([APP_X1, APP_Y1 + 75, APP_X2, APP_Y1 + 75], fill=(220, 190, 100), width=2)
draw2.text(((APP_X1 + APP_X2)//2, APP_Y1 + 38), "SPRING BOOT APPLICATION", fill=(0, 0, 0), font=get_font(32, bold=True), anchor="mm")

INNER_W = APP_X2 - APP_X1 - 80
INNER_X = APP_X1 + 40

# --- 1. Controller Layer (Xanh lá) ---
L1_Y1 = APP_Y1 + 120
L1_H = 190
L1_Y2 = L1_Y1 + L1_H

draw2.rectangle([INNER_X, L1_Y1, INNER_X + INNER_W, L1_Y2], outline=(134, 239, 172), width=2, fill=(240, 253, 244))
draw2.rectangle([INNER_X, L1_Y1, INNER_X + INNER_W, L1_Y1 + 50], fill=(220, 252, 231))
draw2.line([INNER_X, L1_Y1 + 50, INNER_X + INNER_W, L1_Y1 + 50], fill=(134, 239, 172), width=2)
draw2.text((INNER_X + INNER_W//2, L1_Y1 + 25), "Controller Layer", fill=(0, 0, 0), font=get_font(26, bold=True), anchor="mm")

# 5 hộp Controller
ctrl_names = ["AuthController", "BookController", "OrderController", "CartController", "PaymentController", "..."]
c_gap = 18
c_w = (INNER_W - 40 - (c_gap * (len(ctrl_names)-1))) // len(ctrl_names)
for i, name in enumerate(ctrl_names):
    cx = INNER_X + 20 + i * (c_w + c_gap)
    cy = L1_Y1 + 70
    draw2.rounded_rectangle([cx, cy, cx + c_w, cy + 90], radius=8, outline=(74, 222, 128), width=2, fill=(255, 255, 255))
    draw2.text((cx + c_w//2, cy + 45), name, fill=(22, 101, 52), font=get_font(21, bold=True if name!="..." else False), anchor="mm")

# Mũi tên xám trỏ xuống từ Controller -> Service
ARR1_Y1 = L1_Y2
ARR1_Y2 = ARR1_Y1 + 50
draw2.line([INNER_X + INNER_W//2, ARR1_Y1, INNER_X + INNER_W//2, ARR1_Y2], fill=(100, 100, 100), width=4)
draw2.polygon([(INNER_X + INNER_W//2, ARR1_Y2), (INNER_X + INNER_W//2 - 10, ARR1_Y2 - 12), (INNER_X + INNER_W//2 + 10, ARR1_Y2 - 12)], fill=(100, 100, 100))

# --- 2. Service Layer (Business Logic) (Xanh dương) ---
L2_Y1 = ARR1_Y2
L2_H = 190
L2_Y2 = L2_Y1 + L2_H

draw2.rectangle([INNER_X, L2_Y1, INNER_X + INNER_W, L2_Y2], outline=(147, 197, 253), width=2, fill=(239, 246, 255))
draw2.rectangle([INNER_X, L2_Y1, INNER_X + INNER_W, L2_Y1 + 50], fill=(219, 234, 254))
draw2.line([INNER_X, L2_Y1 + 50, INNER_X + INNER_W, L2_Y1 + 50], fill=(147, 197, 253), width=2)
draw2.text((INNER_X + INNER_W//2, L2_Y1 + 25), "Service Layer (Business Logic)", fill=(0, 0, 0), font=get_font(26, bold=True), anchor="mm")

# 5 hộp Service
svc_names = ["AuthService", "BookService", "OrderService", "CartService", "UserService", "..."]
for i, name in enumerate(svc_names):
    cx = INNER_X + 20 + i * (c_w + c_gap)
    cy = L2_Y1 + 70
    draw2.rounded_rectangle([cx, cy, cx + c_w, cy + 90], radius=8, outline=(96, 165, 250), width=2, fill=(255, 255, 255))
    draw2.text((cx + c_w//2, cy + 45), name, fill=(30, 64, 175), font=get_font(21, bold=True if name!="..." else False), anchor="mm")

# Mũi tên xám trỏ xuống từ Service -> Repository
ARR2_Y1 = L2_Y2
ARR2_Y2 = ARR2_Y1 + 50
draw2.line([INNER_X + INNER_W//2, ARR2_Y1, INNER_X + INNER_W//2, ARR2_Y2], fill=(100, 100, 100), width=4)
draw2.polygon([(INNER_X + INNER_W//2, ARR2_Y2), (INNER_X + INNER_W//2 - 10, ARR2_Y2 - 12), (INNER_X + INNER_W//2 + 10, ARR2_Y2 - 12)], fill=(100, 100, 100))

# --- 3. Repository Layer (JPA/Hibernate) (Tím) ---
L3_Y1 = ARR2_Y2
L3_H = 190
L3_Y2 = L3_Y1 + L3_H

draw2.rectangle([INNER_X, L3_Y1, INNER_X + INNER_W, L3_Y2], outline=(216, 180, 254), width=2, fill=(250, 245, 255))
draw2.rectangle([INNER_X, L3_Y1, INNER_X + INNER_W, L3_Y1 + 50], fill=(243, 232, 255))
draw2.line([INNER_X, L3_Y1 + 50, INNER_X + INNER_W, L3_Y1 + 50], fill=(216, 180, 254), width=2)
draw2.text((INNER_X + INNER_W//2, L3_Y1 + 25), "Repository Layer (JPA/Hibernate)", fill=(0, 0, 0), font=get_font(26, bold=True), anchor="mm")

# 5 hộp Repo
repo_names = ["UserRepository", "BookRepository", "OrderRepository", "CartRepository", "CategoryRepository", "..."]
for i, name in enumerate(repo_names):
    cx = INNER_X + 20 + i * (c_w + c_gap)
    cy = L3_Y1 + 70
    draw2.rounded_rectangle([cx, cy, cx + c_w, cy + 90], radius=8, outline=(192, 132, 252), width=2, fill=(255, 255, 255))
    draw2.text((cx + c_w//2, cy + 45), name, fill=(107, 33, 168), font=get_font(20, bold=True if name!="..." else False), anchor="mm")

# --- 4. Hai khối bên dưới: Security & Config vs Scheduled Jobs & Realtime ---
BOTTOM_ROW_Y = L3_Y2 + 50
BOTTOM_ROW_H = 190
HALF_W = (INNER_W - 30) // 2

# Khối Security & Config (Đỏ / Hồng nhạt)
SEC_X = INNER_X
draw2.rectangle([SEC_X, BOTTOM_ROW_Y, SEC_X + HALF_W, BOTTOM_ROW_Y + BOTTOM_ROW_H], outline=(252, 165, 165), width=2, fill=(254, 242, 242))
draw2.rectangle([SEC_X, BOTTOM_ROW_Y, SEC_X + HALF_W, BOTTOM_ROW_Y + 50], fill=(254, 226, 226))
draw2.line([SEC_X, BOTTOM_ROW_Y + 50, SEC_X + HALF_W, BOTTOM_ROW_Y + 50], fill=(252, 165, 165), width=2)
draw2.text((SEC_X + HALF_W//2, BOTTOM_ROW_Y + 25), "Security & Config", fill=(0, 0, 0), font=get_font(24, bold=True), anchor="mm")

sec_sub = ["JWT Filter", "SecurityConfig", "WebMvcConfig / Cors"]
s_gap = 14
s_w = (HALF_W - 30 - (s_gap * (len(sec_sub)-1))) // len(sec_sub)
for i, sname in enumerate(sec_sub):
    sx = SEC_X + 15 + i * (s_w + s_gap)
    sy = BOTTOM_ROW_Y + 70
    draw2.rounded_rectangle([sx, sy, sx + s_w, sy + 85], radius=8, outline=(248, 113, 113), width=2, fill=(255, 255, 255))
    draw2.text((sx + s_w//2, sy + 42), sname, fill=(153, 27, 27), font=get_font(20, bold=True), anchor="mm")

# Khối Scheduled Jobs & Realtime (Cam nhạt)
JOB_X = INNER_X + HALF_W + 30
draw2.rectangle([JOB_X, BOTTOM_ROW_Y, JOB_X + HALF_W, BOTTOM_ROW_Y + BOTTOM_ROW_H], outline=(253, 186, 116), width=2, fill=(255, 247, 237))
draw2.rectangle([JOB_X, BOTTOM_ROW_Y, JOB_X + HALF_W, BOTTOM_ROW_Y + 50], fill=(254, 237, 213))
draw2.line([JOB_X, BOTTOM_ROW_Y + 50, JOB_X + HALF_W, BOTTOM_ROW_Y + 50], fill=(253, 186, 116), width=2)
draw2.text((JOB_X + HALF_W//2, BOTTOM_ROW_Y + 25), "Scheduled Jobs & Realtime", fill=(0, 0, 0), font=get_font(24, bold=True), anchor="mm")

job_sub = ["OrderAutoApprovedJob", "WebSocketBroker", "DataSeeder"]
for i, jname in enumerate(job_sub):
    jx = JOB_X + 15 + i * (s_w + s_gap)
    jy = BOTTOM_ROW_Y + 70
    draw2.rounded_rectangle([jx, jy, jx + s_w, jy + 85], radius=8, outline=(251, 146, 60), width=2, fill=(255, 255, 255))
    draw2.text((jx + s_w//2, jy + 42), jname, fill=(154, 52, 18), font=get_font(19, bold=True), anchor="mm")

# --- 5. Các khối bên ngoài (Bên Trái) ---
# Groq AI Cloud Messaging / API
EXT1_X1, EXT1_Y1 = 120, 520
EXT1_X2, EXT1_Y2 = 420, 640
draw2.rounded_rectangle([EXT1_X1, EXT1_Y1, EXT1_X2, EXT1_Y2], radius=12, outline=(251, 191, 36), width=2, fill=(254, 243, 199))
draw2.text(((EXT1_X1+EXT1_X2)//2, EXT1_Y1 + 40), "Groq AI Cloud", fill=(180, 83, 9), font=get_font(24, bold=True), anchor="mm")
draw2.text(((EXT1_X1+EXT1_X2)//2, EXT1_Y1 + 80), "(Llama 3.3 70B)", fill=(100, 116, 139), font=get_font(20, bold=False), anchor="mm")

# Mũi tên nét đứt 2 chiều <---> nối với Service Layer
def draw_double_dash(x1, y1, x2, y2):
    dash_len = 10
    space_len = 6
    curr = x1
    while curr < x2:
        end = min(curr + dash_len, x2)
        draw2.line([curr, y1, end, y1], fill=(100, 100, 100), width=2)
        curr += dash_len + space_len
    # 2 đầu mũi tên
    draw2.polygon([(x1, y1), (x1 + 10, y1 - 6), (x1 + 10, y1 + 6)], fill=(100, 100, 100))
    draw2.polygon([(x2, y1), (x2 - 10, y1 - 6), (x2 - 10, y1 + 6)], fill=(100, 100, 100))

draw_double_dash(EXT1_X2, (EXT1_Y1+EXT1_Y2)//2, APP_X1, (EXT1_Y1+EXT1_Y2)//2)

# Payment Gateways (VNPay / MoMo)
EXT2_X1, EXT2_Y1 = 120, 740
EXT2_X2, EXT2_Y2 = 420, 860
draw2.rounded_rectangle([EXT2_X1, EXT2_Y1, EXT2_X2, EXT2_Y2], radius=12, outline=(248, 113, 113), width=2, fill=(254, 226, 226))
draw2.text(((EXT2_X1+EXT2_X2)//2, EXT2_Y1 + 40), "Payment Gateways", fill=(153, 27, 27), font=get_font(22, bold=True), anchor="mm")
draw2.text(((EXT2_X1+EXT2_X2)//2, EXT2_Y1 + 80), "(VNPay / MoMo / Zalo)", fill=(100, 116, 139), font=get_font(19, bold=False), anchor="mm")

draw_double_dash(EXT2_X2, (EXT2_Y1+EXT2_Y2)//2, APP_X1, (EXT2_Y1+EXT2_Y2)//2)

# --- 6. Database (PostgreSQL) bên dưới ---
DB2_X = (APP_X1 + APP_X2) // 2
DB2_Y = 1680
DB2_W = 280
DB2_H = 130

draw2.ellipse([DB2_X - DB2_W//2, DB2_Y - 25, DB2_X + DB2_W//2, DB2_Y + 25], outline=(100, 100, 100), width=2, fill=(250, 250, 250))
draw2.rectangle([DB2_X - DB2_W//2, DB2_Y, DB2_X + DB2_W//2, DB2_Y + DB2_H], fill=(250, 250, 250))
draw2.line([DB2_X - DB2_W//2, DB2_Y, DB2_X - DB2_W//2, DB2_Y + DB2_H], fill=(100, 100, 100), width=2)
draw2.line([DB2_X + DB2_W//2, DB2_Y, DB2_X + DB2_W//2, DB2_Y + DB2_H], fill=(100, 100, 100), width=2)
draw2.ellipse([DB2_X - DB2_W//2, DB2_Y + DB2_H - 25, DB2_X + DB2_W//2, DB2_Y + DB2_H + 25], outline=(100, 100, 100), width=2, fill=(250, 250, 250))
draw2.ellipse([DB2_X - DB2_W//2, DB2_Y - 25, DB2_X + DB2_W//2, DB2_Y + 25], outline=(100, 100, 100), width=2, fill=(250, 250, 250))

draw2.text((DB2_X, DB2_Y + 65), "Database (PostgreSQL)", fill=(30, 41, 59), font=get_font(24, bold=True), anchor="mm")

# Mũi tên 2 chiều dọc giữa App và Database
draw2.line([DB2_X, APP_Y2, DB2_X, DB2_Y - 25], fill=(100, 100, 100), width=3)
draw2.polygon([(DB2_X, APP_Y2), (DB2_X - 8, APP_Y2 + 12), (DB2_X + 8, APP_Y2 + 12)], fill=(100, 100, 100))
draw2.polygon([(DB2_X, DB2_Y - 25), (DB2_X - 8, DB2_Y - 37), (DB2_X + 8, DB2_Y - 37)], fill=(100, 100, 100))

# Caption ảnh 2
draw2.text((W2 // 2, 1920), "Figure 1.1.1. Backend Architecture", fill=(0, 0, 0), font=get_font(30, bold=False), anchor="mm")

# Lưu ảnh 2
out2 = "docs/Figure_1.1.1_Backend_Architecture_YiYi_Book.png"
img2.save(out2, "PNG", dpi=(300, 300))
img2.save("Figure_1.1.1_Backend_Architecture_YiYi_Book.png", "PNG", dpi=(300, 300))
print("Saved Figure 1.1.1 at:", out2)

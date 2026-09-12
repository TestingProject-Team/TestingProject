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

def render_hinh_4_7():
    W, H = 2000, 1300
    # -------------------------------------------------------------
    # HÌNH 4.7: LOGIN CLASS & SEQUENCE DIAGRAM
    # -------------------------------------------------------------
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(30, bold=True)
    f_sub = get_font(17, bold=False)
    f_hdr = get_font(18, bold=True)
    f_box = get_font(15, bold=True)
    f_body = get_font(13, bold=False)

    draw.text((W//2, 45), "SƠ ĐỒ LỚP VÀ TUẦN TỰ XÁC THỰC JWT (LOGIN & AUTHENTICATION) — YIYI BOOK", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 75), "Thiết kế Class Diagram chi tiết và Sequence Flow đăng nhập, kiểm tra mật khẩu BCrypt, sinh Bearer Token", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # LEFT PANEL: CLASS DIAGRAM (x: 80 -> 900)
    draw.rounded_rectangle([80, 110, 900, 1180], radius=14, fill=(255, 255, 255), outline=(139, 92, 246), width=2)
    draw.rectangle([80, 110, 900, 155], fill=(124, 58, 237))
    draw.text((490, 132), "CLASS DIAGRAM: AUTHENTICATION SUBSYSTEM", fill=(255, 255, 255), font=f_hdr, anchor="mm")

    # Class 1: AuthController
    draw.rounded_rectangle([110, 175, 480, 420], radius=8, fill=(250, 245, 255), outline=(168, 85, 247), width=1)
    draw.rectangle([110, 175, 480, 210], fill=(147, 51, 234))
    draw.text((295, 192), "AuthController", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((120, 220), "- authService: AuthService", fill=(15, 23, 42), font=f_body)
    draw.line([(110, 245), (480, 245)], fill=(168, 85, 247), width=1)
    draw.text((120, 255), "+ login(AuthRequest): AuthResponse\n+ register(RegisterRequest): String\n+ changePassword(req): ResponseEntity\n+ forgotPassword(email): ResponseEntity", fill=(15, 23, 42), font=f_body)

    # Class 2: AuthService
    draw.rounded_rectangle([520, 175, 870, 440], radius=8, fill=(239, 246, 255), outline=(59, 130, 246), width=1)
    draw.rectangle([520, 175, 870, 210], fill=(37, 99, 235))
    draw.text((695, 192), "AuthService", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((530, 220), "- userRepo: UserRepository\n- passEncoder: PasswordEncoder\n- jwtService: JwtService\n- authManager: AuthManager", fill=(15, 23, 42), font=f_body)
    draw.line([(520, 305), (870, 305)], fill=(59, 130, 246), width=1)
    draw.text((530, 315), "+ authenticate(req): AuthResponse\n+ register(req): User\n+ generateJwtToken(user): String\n+ validateCredentials(u, p): boolean", fill=(15, 23, 42), font=f_body)

    # Class 3: JwtService
    draw.rounded_rectangle([110, 460, 480, 680], radius=8, fill=(254, 243, 199), outline=(245, 158, 11), width=1)
    draw.rectangle([110, 460, 480, 495], fill=(217, 119, 6))
    draw.text((295, 477), "JwtService", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((120, 505), "- SECRET_KEY: String\n- EXPIRATION_TIME: long (24h)", fill=(15, 23, 42), font=f_body)
    draw.line([(110, 550), (480, 550)], fill=(245, 158, 11), width=1)
    draw.text((120, 560), "+ generateToken(UserDetails): String\n+ extractUsername(token): String\n+ extractRole(token): String\n+ isTokenValid(token, User): boolean\n+ isTokenExpired(token): boolean", fill=(15, 23, 42), font=f_body)

    # Class 4: JwtAuthFilter
    draw.rounded_rectangle([520, 460, 870, 680], radius=8, fill=(236, 253, 245), outline=(16, 185, 129), width=1)
    draw.rectangle([520, 460, 870, 495], fill=(5, 150, 105))
    draw.text((695, 477), "JwtAuthFilter", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((530, 505), "- jwtService: JwtService\n- userDetailsService: UserDetailsSvc", fill=(15, 23, 42), font=f_body)
    draw.line([(520, 550), (870, 550)], fill=(16, 185, 129), width=1)
    draw.text((530, 560), "# doFilterInternal(req, res, chain)\n- extractBearerToken(req): String\n- setSecurityContext(auth): void", fill=(15, 23, 42), font=f_body)

    # Class 5: User (Entity) & Role (Enum)
    draw.rounded_rectangle([110, 710, 480, 940], radius=8, fill=(241, 245, 249), outline=(100, 116, 139), width=1)
    draw.rectangle([110, 710, 480, 745], fill=(51, 65, 85))
    draw.text((295, 727), "User (Entity)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((120, 755), "- id: Long [PK]\n- username: String [UK]\n- password: String\n- role: Role (USER, ADMIN)\n- yPoints: Integer\n- totalSpent: Double", fill=(15, 23, 42), font=f_body)
    draw.line([(110, 885), (480, 885)], fill=(100, 116, 139), width=1)
    draw.text((120, 895), "+ getAuthorities(): Collection\n+ isAccountNonExpired(): boolean", fill=(15, 23, 42), font=f_body)

    # Class 6: UserRepository
    draw.rounded_rectangle([520, 710, 870, 940], radius=8, fill=(241, 245, 249), outline=(100, 116, 139), width=1)
    draw.rectangle([520, 710, 870, 745], fill=(51, 65, 85))
    draw.text((695, 727), "UserRepository (Interface)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((530, 755), "<<extends JpaRepository<User, Long>>>", fill=(100, 116, 139), font=f_body)
    draw.line([(520, 785), (870, 785)], fill=(100, 116, 139), width=1)
    draw.text((530, 800), "+ findByUsername(name): Optional<User>\n+ findByEmail(email): Optional<User>\n+ existsByUsername(name): boolean\n+ existsByEmail(email): boolean\n+ countByRole(role): long", fill=(15, 23, 42), font=f_body)

    # DTOs box
    draw.rounded_rectangle([110, 970, 870, 1150], radius=8, fill=(255, 241, 242), outline=(244, 63, 94), width=1)
    draw.text((490, 995), "DTO Models: AuthRequest(username, password) | AuthResponse(token, user, role, expiresAt)", fill=(190, 18, 60), font=f_box, anchor="mm")
    draw.text((130, 1025), "• AuthRequest: Payload chứa thông tin đăng nhập của người dùng gửi từ giao diện React.", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1055), "• AuthResponse: Payload trả về JWT Bearer Token, thông tin người dùng cơ bản và quyền hạn (USER/ADMIN).", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1085), "• Bảo mật: Mật khẩu lưu trữ trong Database được băm bằng BCrypt 10 rounds, không lưu plaintext.", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1115), "• JWT Header: HS256, Claims bao gồm subject (username), role và expiration time (86400s).", fill=(15, 23, 42), font=f_body)

    # RIGHT PANEL: SEQUENCE DIAGRAM (x: 940 -> 1920)
    draw.rounded_rectangle([940, 110, 1920, 1180], radius=14, fill=(255, 255, 255), outline=(59, 130, 246), width=2)
    draw.rectangle([940, 110, 1920, 155], fill=(37, 99, 235))
    draw.text((1430, 132), "SEQUENCE FLOW: USER LOGIN & JWT AUTHENTICATION", fill=(255, 255, 255), font=f_hdr, anchor="mm")

    seq_actors = [
        ("User (Client)", 1010, (13, 148, 136)),
        ("Login.jsx (UI)", 1190, (2, 132, 199)),
        ("AuthController", 1380, (147, 51, 234)),
        ("AuthService", 1560, (37, 99, 235)),
        ("UserRepository", 1720, (51, 65, 85)),
        ("JwtService", 1860, (217, 119, 6))
    ]
    for title, x, col in seq_actors:
        draw.rounded_rectangle([x-65, 175, x+65, 215], radius=6, fill=col)
        draw.text((x, 195), title, fill=(255, 255, 255), font=f_box, anchor="mm")
        draw.line([(x, 215), (x, 1130)], fill=(203, 213, 225), width=2)
        draw.rounded_rectangle([x-65, 1130, x+65, 1160], radius=6, fill=col)
        draw.text((x, 1145), title, fill=(255, 255, 255), font=f_body, anchor="mm")

    seq_msgs = [
        (1010, 1190, "1. Nhập username, password & click 'Đăng nhập'", 250, False, (15, 23, 42)),
        (1190, 1380, "2. POST /api/auth/login (AuthRequest)", 320, False, (147, 51, 234)),
        (1380, 1560, "3. authenticate(AuthRequest)", 390, False, (37, 99, 235)),
        (1560, 1720, "4. findByUsername(username)", 460, False, (51, 65, 85)),
        (1720, 1560, "5. Trả về Optional<User>", 530, True, (51, 65, 85)),
        (1560, 1560, "6. BCrypt.matches(password, user.getPassword())", 600, False, (37, 99, 235)), # Self
        (1560, 1860, "7. generateToken(user) với Claims: role, userId", 670, False, (217, 119, 6)),
        (1860, 1560, "8. Trả về signed JWT String", 740, True, (217, 119, 6)),
        (1560, 1380, "9. Trả về AuthResponse(token, user, role)", 810, True, (37, 99, 235)),
        (1380, 1190, "10. HTTP 200 OK + JSON AuthResponse", 880, True, (147, 51, 234)),
        (1190, 1190, "11. Lưu token vào LocalStorage & Cập nhật AuthContext", 950, False, (2, 132, 199)), # Self
        (1190, 1010, "12. Render toast thông báo & chuyển hướng (Home / Admin)", 1020, True, (13, 148, 136)),
        (1190, 1380, "13. [Subsequent Requests] Gửi Header: Bearer <Token>", 1080, False, (100, 116, 139))
    ]

    for x1, x2, text, y, is_dashed, col in seq_msgs:
        if x1 == x2:
            draw.line([(x1, y-12), (x1+35, y-12), (x1+35, y+12), (x1, y+12)], fill=col, width=2)
            draw_arrow(draw, (x1+35, y+12), (x1, y+12), fill=col, width=2, arrow_size=5)
            draw.text((x1+42, y), text, fill=col, font=f_body, anchor="lm")
        else:
            draw_arrow(draw, (x1, y), (x2, y), fill=col, width=2, arrow_size=7, dashed=is_dashed)
            draw.text(((x1+x2)//2, y-12), text, fill=col, font=f_body, anchor="mm")

    draw.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — Authentication Class & Sequence Diagram (JWT + BCrypt)", fill=(148, 163, 184), font=f_body, anchor="mm")

    # Standard Version
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 45), "HÌNH 4.7. SƠ ĐỒ LỚP VÀ TUẦN TỰ XÁC THỰC JWT (LOGIN)", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 75), "Standard UML Class & Sequence Diagram Specification", fill=(80, 80, 80), font=f_sub, anchor="mm")

    # Class Panel Standard
    draw_s.rectangle([80, 110, 900, 1180], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([80, 110, 900, 155], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    draw_s.text((490, 132), "CLASS DIAGRAM: AUTHENTICATION SUBSYSTEM", fill=(0, 0, 0), font=f_hdr, anchor="mm")

    for b, t, lines in [
        ([110, 175, 480, 420], "AuthController", ["- authService: AuthService", "---", "+ login(AuthRequest): AuthResponse", "+ register(RegisterRequest): String", "+ changePassword(req): ResponseEntity", "+ forgotPassword(email): ResponseEntity"]),
        ([520, 175, 870, 440], "AuthService", ["- userRepo: UserRepository", "- passEncoder: PasswordEncoder", "- jwtService: JwtService", "---", "+ authenticate(req): AuthResponse", "+ register(req): User", "+ generateJwtToken(user): String", "+ validateCredentials(u, p): boolean"]),
        ([110, 460, 480, 680], "JwtService", ["- SECRET_KEY: String", "- EXPIRATION_TIME: long", "---", "+ generateToken(UserDetails): String", "+ extractUsername(token): String", "+ extractRole(token): String", "+ isTokenValid(token, User): boolean"]),
        ([520, 460, 870, 680], "JwtAuthFilter", ["- jwtService: JwtService", "- userDetailsService: UserDetailsSvc", "---", "# doFilterInternal(req, res, chain)", "- extractBearerToken(req): String", "- setSecurityContext(auth): void"]),
        ([110, 710, 480, 940], "User (Entity)", ["- id: Long [PK]", "- username: String [UK]", "- password: String", "- role: Role (USER, ADMIN)", "---", "+ getAuthorities(): Collection", "+ isAccountNonExpired(): boolean"]),
        ([520, 710, 870, 940], "UserRepository (Interface)", ["<<extends JpaRepository>>", "---", "+ findByUsername(name): Optional<User>", "+ findByEmail(email): Optional<User>", "+ existsByUsername(name): boolean"])
    ]:
        draw_s.rectangle(b, fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw_s.rectangle([b[0], b[1], b[2], b[1]+30], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
        draw_s.text((b[0]+10, b[1]+15), t, fill=(0, 0, 0), font=f_box, anchor="lm")
        y_c = b[1] + 45
        for l in lines:
            if l == "---":
                draw_s.line([(b[0], y_c-5), (b[2], y_c-5)], fill=(0, 0, 0), width=1)
            else:
                draw_s.text((b[0]+10, y_c), l, fill=(0, 0, 0), font=f_body)
                y_c += 24

    draw_s.rectangle([110, 970, 870, 1150], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    draw_s.text((490, 995), "DTO Models: AuthRequest | AuthResponse", fill=(0, 0, 0), font=f_box, anchor="mm")
    draw_s.text((130, 1025), "• AuthRequest: Payload chứa thông tin đăng nhập của người dùng gửi từ giao diện React.", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 1055), "• AuthResponse: Payload trả về JWT Bearer Token, thông tin người dùng cơ bản và quyền hạn.", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 1085), "• Bảo mật: Mật khẩu lưu trữ trong Database được băm bằng BCrypt 10 rounds.", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 1115), "• JWT Header: HS256, Claims bao gồm subject (username), role và expiration time.", fill=(0, 0, 0), font=f_body)

    # Sequence Panel Standard
    draw_s.rectangle([940, 110, 1920, 1180], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([940, 110, 1920, 155], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    draw_s.text((1430, 132), "SEQUENCE FLOW: USER LOGIN & JWT AUTHENTICATION", fill=(0, 0, 0), font=f_hdr, anchor="mm")

    for title, x, _ in seq_actors:
        draw_s.rectangle([x-65, 175, x+65, 215], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
        draw_s.text((x, 195), title, fill=(0, 0, 0), font=f_box, anchor="mm")
        draw_s.line([(x, 215), (x, 1130)], fill=(0, 0, 0), width=1)
        draw_s.rectangle([x-65, 1130, x+65, 1160], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
        draw_s.text((x, 1145), title, fill=(0, 0, 0), font=f_body, anchor="mm")

    for x1, x2, text, y, is_dashed, _ in seq_msgs:
        if x1 == x2:
            draw_s.line([(x1, y-12), (x1+35, y-12), (x1+35, y+12), (x1, y+12)], fill=(0, 0, 0), width=1)
            draw_arrow(draw_s, (x1+35, y+12), (x1, y+12), fill=(0, 0, 0), width=1, arrow_size=5)
            draw_s.text((x1+42, y), text, fill=(0, 0, 0), font=f_body, anchor="lm")
        else:
            draw_arrow(draw_s, (x1, y), (x2, y), fill=(0, 0, 0), width=1, arrow_size=7, dashed=is_dashed)
            draw_s.text(((x1+x2)//2, y-12), text, fill=(0, 0, 0), font=f_body, anchor="mm")

    draw_s.text((W//2, 1275), "Safe Margin: 60px | Technical Standard Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    p_info = os.path.join(INFO_DIR, "Hinh_4.7_Class_Sequence_Diagram_Login_Auth.png")
    p_std = os.path.join(STD_DIR, "Hinh_4.7_Class_Sequence_Diagram_Login_Auth.png")
    img.save(p_info, "PNG", dpi=(300, 300))
    img_std.save(p_std, "PNG", dpi=(300, 300))

    svg_info = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
        <rect width="100%" height="100%" fill="#F8FAFC"/>
        <text x="{W//2}" y="45" font-family="Arial, sans-serif" font-size="30" font-weight="bold" fill="#0F172A" text-anchor="middle">SƠ ĐỒ LỚP VÀ TUẦN TỰ XÁC THỰC JWT (LOGIN & AUTHENTICATION) — YIYI BOOK</text>
        <text x="{W//2}" y="75" font-family="Arial, sans-serif" font-size="17" fill="#475569" text-anchor="middle">Thiết kế Class Diagram chi tiết và Sequence Flow đăng nhập, kiểm tra mật khẩu BCrypt, sinh Bearer Token</text>
    </svg>'''
    with open(os.path.join(INFO_DIR, "Hinh_4.7_Class_Sequence_Diagram_Login_Auth.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.7_Class_Sequence_Diagram_Login_Auth.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.7 (Login Class & Sequence) successfully.")

if __name__ == "__main__":
    render_hinh_4_7()

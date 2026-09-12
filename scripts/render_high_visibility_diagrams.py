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

def draw_state_box(draw, box, title, sub="", color_type="blue", r=12):
    x1, y1, x2, y2 = box
    color_map = {
        "blue":    ((239, 246, 255), (37, 99, 235),  (30, 64, 175),  (29, 78, 216)),
        "indigo":  ((238, 242, 255), (79, 70, 229),  (49, 46, 129),  (67, 56, 202)),
        "purple":  ((250, 245, 255), (147, 51, 234), (107, 33, 168), (126, 34, 206)),
        "amber":   ((255, 251, 235), (217, 119, 6),  (146, 64, 14),  (180, 83, 9)),
        "teal":    ((240, 253, 250), (13, 148, 136), (17, 94, 89),   (15, 118, 110)),
        "emerald": ((240, 253, 244), (16, 185, 129), (22, 101, 52),  (5, 150, 105)),
        "dark":    ((241, 245, 249), (71, 85, 105),  (15, 23, 42),   (51, 65, 85)),
        "red":     ((254, 242, 242), (220, 38, 38),  (153, 27, 27),  (185, 28, 28))
    }
    bg, border, text_c, sub_c = color_map.get(color_type, color_map["blue"])
    
    # Rounded box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=bg, outline=border, width=3)
    
    cx = (x1 + x2) // 2
    f_t = get_font(28, bold=True)
    f_s = get_font(21, bold=False)
    
    if sub:
        draw.text((cx, y1 + 40), title, fill=text_c, font=f_t, anchor="mm")
        draw.line([(x1 + 20, y1 + 70), (x2 - 20, y1 + 70)], fill=border, width=2)
        draw.text((cx, y1 + 102), sub, fill=sub_c, font=f_s, anchor="mm")
    else:
        cy = (y1 + y2) // 2
        draw.text((cx, cy), title, fill=text_c, font=f_t, anchor="mm")

def draw_class_box_large(draw, box, class_name, fields, methods, header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246)):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=box_bg, outline=border_color, width=3)
    
    hdr_h = 48
    draw.rounded_rectangle([x1, y1, x2, y1 + hdr_h], radius=10, fill=header_bg)
    draw.rectangle([x1, y1 + 15, x2, y1 + hdr_h], fill=header_bg)
    
    f_t = get_font(24, bold=True)
    f_b = get_font(19, bold=False)
    
    draw.text(((x1 + x2) // 2, y1 + hdr_h // 2), class_name, fill=(255, 255, 255), font=f_t, anchor="mm")
    
    curr_y = y1 + hdr_h + 14
    if fields:
        for f in fields:
            draw.text((x1 + 18, curr_y), f, fill=(15, 23, 42), font=f_b)
            curr_y += 28
        curr_y += 6
        draw.line([(x1, curr_y), (x2, curr_y)], fill=border_color, width=2)
        curr_y += 12
    
    if methods:
        for m in methods:
            draw.text((x1 + 18, curr_y), m, fill=(15, 23, 42), font=f_b)
            curr_y += 28

def draw_sequence_diagram_base(draw, title, sub, actors, msgs, W=2000, H=1300):
    draw_header(draw, title, sub, W)
    
    # Calculate lifeline X coords
    num_actors = len(actors)
    margin_x = 100
    spacing = (W - 2 * margin_x) // (num_actors - 1) if num_actors > 1 else 0
    
    f_act = get_font(25, bold=True)
    f_msg = get_font(24, bold=True)
    
    actor_x_coords = []
    for i, (name, col_type) in enumerate(actors):
        x = margin_x + i * spacing
        actor_x_coords.append(x)
        
        # Actor header card
        w_card = min(spacing - 20, 240)
        h_card = 80
        x1, y1, x2, y2 = x - w_card // 2, 160, x + w_card // 2, 160 + h_card
        
        draw_state_box(draw, [x1, y1, x2, y2], name, "", col_type, r=10)
        # Lifeline vertical line
        draw.line([(x, y2), (x, H - 70)], fill=(148, 163, 184), width=3)
    
    # Draw messages
    for m in msgs:
        idx_from, idx_to, text, y = m[0], m[1], m[2], m[3]
        dashed = m[4] if len(m) > 4 else False
        
        x_from = actor_x_coords[idx_from]
        x_to = actor_x_coords[idx_to]
        
        draw_arrow(draw, (x_from, y), (x_to, y), fill=(30, 41, 59), width=4, arrow_size=14, dashed=dashed)
        
        mid_x = (x_from + x_to) // 2
        # Text above arrow
        draw.text((mid_x, y - 22), text, fill=(15, 23, 42), font=f_msg, anchor="mm")

# =========================================================================
# 1. HÌNH 4.14: SƠ ĐỒ TRẠNG THÁI ĐƠN HÀNG (ORDER STATE DIAGRAM) - FULL SIZE
# =========================================================================
def render_hinh_4_14_order_state():
    W, H = 2000, 1100
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ TRẠNG THÁI ĐƠN HÀNG (ORDER STATE DIAGRAM)", 
                "Vòng đời chuyển đổi trạng thái đơn hàng và các nhánh hủy đơn, đổi trả hoàn tiền", W)
    
    # Row 1: Main Flow (Y: 180 -> 330)
    # Box width 320, height 140
    states_row1 = [
        (60,  "PENDING", "Chờ xác nhận đơn", "blue"),
        (450, "PROCESSING", "Đang đóng gói xử lý", "indigo"),
        (840, "SHIPPING", "Đang giao hàng", "amber"),
        (1230, "DELIVERED", "Đã giao thành công", "teal"),
        (1620, "COMPLETED", "Hoàn tất đơn hàng", "emerald")
    ]
    
    for x, title, sub, col in states_row1:
        draw_state_box(draw, [x, 180, x + 320, 330], title, sub, col)
    
    # Arrows row 1
    draw_arrow(draw, (380, 255), (450, 255), width=5, arrow_size=16)
    draw_arrow(draw, (770, 255), (840, 255), width=5, arrow_size=16)
    draw_arrow(draw, (1160, 255), (1230, 255), width=5, arrow_size=16)
    draw_arrow(draw, (1550, 255), (1620, 255), width=5, arrow_size=16)
    
    # Row 2: Cancellation Branch (Y: 440 -> 590)
    draw_arrow(draw, (220, 330), (220, 440), width=4, arrow_size=16)
    draw_arrow(draw, (610, 330), (610, 440), width=4, arrow_size=16)
    
    draw_state_box(draw, [140, 440, 690, 590], "CANCELLED", "Đơn hàng đã hủy (Hoàn trả tồn kho)", "red")
    
    # Row 2: Return Requested Branch (Y: 440 -> 590)
    draw_arrow(draw, (1390, 330), (1390, 440), width=4, arrow_size=16)
    draw_state_box(draw, [1180, 440, 1720, 590], "RETURN_REQUESTED", "Khách gửi yêu cầu đổi trả / hoàn tiền", "amber")
    
    # Row 3: Return Result Branch (Y: 700 -> 850)
    draw_arrow(draw, (1340, 590), (1050, 700), width=4, arrow_size=16)
    draw_state_box(draw, [840, 700, 1320, 850], "RETURN_REJECTED", "Từ chối yêu cầu đổi trả", "dark")
    
    draw_arrow(draw, (1560, 590), (1650, 700), width=4, arrow_size=16)
    draw_state_box(draw, [1440, 700, 1920, 850], "RETURN_APPROVED", "Chấp thuận đổi trả / Hoàn tiền", "emerald")
    
    # Row 4: Refunded (Y: 920 -> 1060)
    draw_arrow(draw, (1680, 850), (1680, 920), width=4, arrow_size=16)
    draw_state_box(draw, [1440, 920, 1920, 1060], "REFUNDED", "Đã hoàn tiền vào tài khoản khách", "teal")
    
    return img

# =========================================================================
# 2. HÌNH 4.10a: SƠ ĐỒ LỚP CHI TIẾT SÁCH VÀ ĐÁNH GIÁ (CLASS DIAGRAM) - CLEAR FONT
# =========================================================================
def render_hinh_4_10a():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SƠ ĐỒ LỚP CHI TIẾT SÁCH & ĐÁNH GIÁ (CLASS DIAGRAM)", 
                "Cấu trúc các lớp Controller, Service, Repository và Entity tham gia luồng xem chi tiết sách & đánh giá", W)
    
    # Row 1: Controllers (Y: 160 -> 390)
    draw_class_box_large(draw, [80, 160, 680, 390], "BookController",
                         ["- bookService: BookService", "- categoryService: CategoryService"],
                         ["+ getBookById(Long id): ResponseEntity<BookDTO>",
                          "+ getFeaturedBooks(): ResponseEntity<List<BookDTO>>",
                          "+ getRecommendations(Long userId): ResponseEntity<List<BookDTO>>"],
                         header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_class_box_large(draw, [740, 160, 1340, 390], "ReviewController",
                         ["- reviewService: ReviewService", "- authService: AuthService"],
                         ["+ getReviewsByBook(Long bookId): ResponseEntity<List<ReviewDTO>>",
                          "+ checkEligibility(Long bookId): ResponseEntity<EligibilityDTO>",
                          "+ createReview(ReviewRequest req): ResponseEntity<ReviewDTO>"],
                         header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    draw_class_box_large(draw, [1400, 160, 1920, 390], "ReviewCommentController",
                         ["- commentService: ReviewCommentService"],
                         ["+ getComments(Long reviewId): ResponseEntity<List<CommentDTO>>",
                          "+ addComment(Long reviewId, CommentReq req): ResponseEntity",
                          "+ deleteComment(Long commentId): ResponseEntity"],
                         header_bg=(124, 58, 237), box_bg=(250, 245, 255), border_color=(139, 92, 246))

    # Row 2: Services (Y: 470 -> 700)
    draw_class_box_large(draw, [80, 470, 680, 700], "BookService",
                         ["- bookRepository: BookRepository", "- categoryRepository: CategoryRepository"],
                         ["+ getBookById(Long id): BookDTO",
                          "+ updateStock(Long bookId, Integer qty): void",
                          "+ searchBooks(String kw, Pageable page): Page<BookDTO>",
                          "+ getRelatedBooks(Long categoryId): List<BookDTO>"],
                         header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    draw_class_box_large(draw, [740, 470, 1340, 700], "ReviewService",
                         ["- reviewRepo: ReviewRepository", "- orderRepo: OrderRepository", "- userRepo: UserRepository"],
                         ["+ getReviewsByBookId(Long bookId): List<ReviewDTO>",
                          "+ checkUserEligibility(String username, Long bookId): boolean",
                          "+ createReview(String username, ReviewRequest req): ReviewDTO",
                          "+ calculateAverageRating(Long bookId): Double"],
                         header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # Row 3: Repositories (Y: 770 -> 980)
    draw_class_box_large(draw, [80, 770, 500, 980], "BookRepository <<Interface>>",
                         [],
                         ["+ findById(Long id): Optional<Book>",
                          "+ findByCategoryId(Long catId): List<Book>",
                          "+ findFirstByTitle(String title): Optional<Book>",
                          "+ findAll(Specification, Pageable): Page<Book>"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_class_box_large(draw, [550, 770, 1060, 980], "ReviewRepository <<Interface>>",
                         [],
                         ["+ findByBookIdOrderByCreatedAtDesc(Long id): List<Review>",
                          "+ countByUserIdAndBookId(Long uid, Long bid): Long",
                          "+ findByUserId(Long userId): List<Review>",
                          "+ calculateAvgRating(Long bookId): Double"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_class_box_large(draw, [1110, 770, 1500, 980], "ReviewCommentRepository",
                         [],
                         ["+ findByReviewIdOrderByCreatedAtAsc(Long rid): List",
                          "+ countByReviewId(Long reviewId): Long",
                          "+ deleteByReviewId(Long reviewId): void"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    draw_class_box_large(draw, [1550, 770, 1920, 980], "OrderRepository <<Interface>>",
                         [],
                         ["+ countUserDeliveredPurchases(Long uid, Long bid): Long",
                          "+ findByUserIdOrderByCreatedAtDesc(Long uid): List",
                          "+ findById(Long id): Optional<Order>"],
                         header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # Row 4: Entities (Y: 1050 -> 1260)
    draw_class_box_large(draw, [80, 1050, 500, 1260], "Book <<Entity>>",
                         ["- id: Long", "- title: String", "- price: BigDecimal", "- stockQuantity: Integer", "- category: Category"],
                         ["+ getPrice(): BigDecimal", "+ setStockQuantity(int qty): void"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_class_box_large(draw, [550, 1050, 1060, 1260], "Review <<Entity>>",
                         ["- id: Long", "- rating: Integer (1-5)", "- comment: String", "- user: User", "- book: Book"],
                         ["+ getRating(): Integer", "+ getComments(): List<ReviewComment>"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    draw_class_box_large(draw, [1110, 1050, 1500, 1260], "ReviewComment <<Entity>>",
                         ["- id: Long", "- content: String", "- user: User", "- review: Review", "- createdAt: LocalDateTime"],
                         ["+ getContent(): String", "+ setContent(String c): void"],
                         header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    # Connecting Arrows
    draw_arrow(draw, (380, 390), (380, 470), fill=(37, 99, 235), width=4, arrow_size=12)
    draw_arrow(draw, (1040, 390), (1040, 470), fill=(13, 148, 136), width=4, arrow_size=12)
    
    draw_arrow(draw, (290, 700), (290, 770), fill=(37, 99, 235), width=4, arrow_size=12)
    draw_arrow(draw, (810, 700), (810, 770), fill=(13, 148, 136), width=4, arrow_size=12)
    draw_arrow(draw, (1200, 700), (1730, 770), fill=(13, 148, 136), width=3, arrow_size=12, dashed=True)

    draw_arrow(draw, (290, 980), (290, 1050), fill=(71, 85, 105), width=3, arrow_size=10, dashed=True)
    draw_arrow(draw, (810, 980), (810, 1050), fill=(71, 85, 105), width=3, arrow_size=10, dashed=True)
    draw_arrow(draw, (1300, 980), (1300, 1050), fill=(71, 85, 105), width=3, arrow_size=10, dashed=True)

    draw.line([(1060, 1155), (1110, 1155)], fill=(30, 41, 59), width=4)
    f_rel = get_font(18, bold=True)
    draw.text((1085, 1130), "1..n", fill=(30, 41, 59), font=f_rel, anchor="mm")
    
    return img

# =========================================================================
# 3. HÌNH 4.10b: SƠ ĐỒ TUẦN TỰ CHI TIẾT SÁCH & ĐÁNH GIÁ (SEQUENCE DIAGRAM)
# =========================================================================
def render_hinh_4_10b():
    W, H = 2000, 1250
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    actors = [
        ("Customer", "blue"),
        ("Product UI", "teal"),
        ("BookController", "blue"),
        ("BookService", "indigo"),
        ("ReviewController", "teal"),
        ("PostgreSQL DB", "dark")
    ]
    
    msgs = [
        (0, 1, "1. Nhấn chọn tựa sách cụ thể", 280),
        (1, 2, "2. GET /api/books/{id}", 360),
        (2, 3, "3. getBookById(id)", 440),
        (3, 5, "4. SELECT * FROM books WHERE id = ?", 520),
        (5, 1, "5. HTTP 200 — Thông tin chi tiết sách (JSON)", 600, True),
        (1, 4, "6. GET /api/reviews/book/{bookId}", 680),
        (4, 5, "7. findByBookIdOrderByCreatedAtDesc(bookId)", 760),
        (5, 1, "8. HTTP 200 — Danh sách Đánh giá (JSON)", 840, True),
        (1, 4, "9. GET /api/reviews/check-eligibility/{bookId}", 920),
        (4, 5, "10. countUserDeliveredPurchases() & countReview()", 1000),
        (5, 1, "11. Phản hồi quyền đánh giá: {eligible: true/false}", 1080, True),
        (1, 0, "12. Render giao diện Chi tiết Sách & Form Đánh giá", 1160, True)
    ]
    
    draw_sequence_diagram_base(draw, "SƠ ĐỒ TUẦN TỰ XEM CHI TIẾT SÁCH & ĐÁNH GIÁ (SEQUENCE DIAGRAM)", 
                               "Quy trình truy vấn thông tin sách, danh sách nhận xét cộng đồng và kiểm tra quyền viết đánh giá", 
                               actors, msgs, W, H)
    return img

# =========================================================================
# 4. HÌNH 4.11: SƠ ĐỒ TUẦN TỰ THAO TÁC GIỎ HÀNG (CART SEQUENCE DIAGRAM)
# =========================================================================
def render_hinh_4_11():
    W, H = 2000, 1250
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    actors = [
        ("Customer", "blue"),
        ("Cart UI (React)", "teal"),
        ("CartController", "blue"),
        ("CartService", "indigo"),
        ("CartRepository", "purple"),
        ("PostgreSQL DB", "dark")
    ]
    
    msgs = [
        (0, 1, "1. Nhấn 'Thêm vào giỏ' / Cập nhật số lượng", 280),
        (1, 2, "2. POST /api/cart {bookId, quantity}", 360),
        (2, 3, "3. addToCart(username, CartRequest)", 440),
        (3, 4, "4. findByUserId() & bookRepo.findById()", 520),
        (4, 5, "5. SELECT * FROM carts, books WHERE id = ?", 600),
        (5, 3, "6. Trả về thực thể Cart & Book tồn kho", 680, True),
        (3, 4, "7. Kiểm tra tồn kho & Thêm CartItem (@Transactional)", 760),
        (4, 5, "8. cartRepository.save(cart) — INSERT/UPDATE", 840),
        (5, 3, "9. Xác nhận lưu dữ liệu giỏ hàng thành công", 920, True),
        (3, 2, "10. Trả về Cart Entity mới nhất", 1000, True),
        (2, 1, "11. HTTP 200 OK — Cart DTO", 1080, True),
        (1, 0, "12. Cập nhật Badge số lượng & Tổng tiền giỏ hàng", 1160, True)
    ]
    
    draw_sequence_diagram_base(draw, "SƠ ĐỒ TUẦN TỰ THAO TÁC GIỎ HÀNG (CART MANAGEMENT)", 
                               "Quy trình thêm sách vào giỏ, cập nhật số lượng, kiểm tra tồn kho và đồng bộ dữ liệu giỏ hàng", 
                               actors, msgs, W, H)
    return img

# =========================================================================
# 5. HÌNH 4.8: SƠ ĐỒ TUẦN TỰ XEM DANH MỤC VÀ DANH SÁCH SÁCH
# =========================================================================
def render_hinh_4_8():
    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    actors = [
        ("Customer", "blue"),
        ("Storefront UI", "teal"),
        ("BookController", "blue"),
        ("BookService", "indigo"),
        ("BookRepository", "purple"),
        ("PostgreSQL DB", "dark")
    ]
    
    msgs = [
        (0, 1, "1. Truy cập Trang chủ / Khám phá sách", 280),
        (1, 2, "2. GET /api/categories & GET /api/books", 370),
        (2, 3, "3. getAllCategories() & getAllBooks()", 460),
        (3, 4, "4. findAll() / findByCategoryId()", 550),
        (4, 5, "5. SELECT * FROM categories, books WHERE active = true", 640),
        (5, 4, "6. Trả về tập thực thể Category & Book", 730, True),
        (4, 3, "7. Chuyển đổi sang List<BookDTO>", 820, True),
        (3, 2, "8. Trả về danh sách DTO đã đóng gói", 910, True),
        (2, 1, "9. HTTP 200 OK (JSON Data)", 1000, True),
        (1, 0, "10. Render danh mục thể loại & Lưới sách nổi bật", 1090, True)
    ]
    
    draw_sequence_diagram_base(draw, "SƠ ĐỒ TUẦN TỰ XEM DANH MỤC VÀ DANH SÁCH SÁCH", 
                               "Quy trình tải cây danh mục thể loại và truy vấn danh sách sách hiển thị trên giao diện", 
                               actors, msgs, W, H)
    return img

# =========================================================================
# 6. HÌNH 4.9: SƠ ĐỒ TUẦN TỰ TÌM KIẾM VÀ LỌC SÁCH
# =========================================================================
def render_hinh_4_9():
    W, H = 2000, 1200
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    actors = [
        ("Customer", "blue"),
        ("Search UI", "teal"),
        ("BookController", "blue"),
        ("BookService", "indigo"),
        ("BookRepository", "purple"),
        ("PostgreSQL DB", "dark")
    ]
    
    msgs = [
        (0, 1, "1. Nhập từ khóa & Chọn bộ lọc (giá, thể loại, sắp xếp)", 280),
        (1, 2, "2. GET /api/books?search=...&category=...&minPrice=...", 370),
        (2, 3, "3. searchBooks(Specification, Pageable)", 460),
        (3, 4, "4. findAll(Specification spec, Pageable p)", 550),
        (4, 5, "5. SELECT * FROM books WHERE title LIKE ... AND price BETWEEN ...", 640),
        (5, 4, "6. Trả về trang thực thể Page<Book>", 730, True),
        (4, 3, "7. Ánh xạ dữ liệu sang Page<BookDTO>", 820, True),
        (3, 2, "8. Trả về phân trang kết quả tìm kiếm", 910, True),
        (2, 1, "9. HTTP 200 OK — Page<BookDTO>", 1000, True),
        (1, 0, "10. Hiển thị danh sách kết quả & Thanh phân trang", 1090, True)
    ]
    
    draw_sequence_diagram_base(draw, "SƠ ĐỒ TUẦN TỰ TÌM KIẾM VÀ LỌC SÁCH NÂNG CAO", 
                               "Quy trình xử lý truy vấn tìm kiếm theo từ khóa và lọc kết hợp đa tiêu chí", 
                               actors, msgs, W, H)
    return img

def render_all_high_visibility_diagrams():
    diagram_functions = [
        ("Hinh_4.14_Order_State_Diagram", render_hinh_4_14_order_state),
        ("Hinh_4.10a_Class_Diagram_BookDetail_Review", render_hinh_4_10a),
        ("Hinh_4.10b_Sequence_Diagram_BookDetail_Review", render_hinh_4_10b),
        ("Hinh_4.11_Sequence_Diagram_Cart_Management", render_hinh_4_11),
        ("Hinh_4.8_Sequence_Diagram_Product_List", render_hinh_4_8),
        ("Hinh_4.9_Sequence_Diagram_Search_Filter", render_hinh_4_9),
    ]
    
    for name, func in diagram_functions:
        img = func()
        for out_dir in [INFO_REV_DIR, STD_REV_DIR, INFO_DIR, STD_DIR]:
            out_path = os.path.join(out_dir, name + ".png")
            img.save(out_path, dpi=(300, 300))
            print(f"Saved large readable diagram: {out_path}")

if __name__ == "__main__":
    render_all_high_visibility_diagrams()

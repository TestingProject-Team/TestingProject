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

def render_class_box(draw, box, class_name, fields, methods, header_bg=(59, 130, 246), box_bg=(248, 250, 252), border_color=(148, 163, 184)):
    x1, y1, x2, y2 = box
    # Rounded box background
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=box_bg, outline=border_color, width=2)
    # Header box for class name
    hdr_h = 36
    draw.rectangle([x1, y1, x2, y1 + hdr_h], fill=header_bg)
    # Re-draw top rounded corners cleanly or fill
    draw.rounded_rectangle([x1, y1, x2, y1 + hdr_h], radius=8, fill=header_bg)
    draw.rectangle([x1, y1 + 10, x2, y1 + hdr_h], fill=header_bg)
    
    f_title = get_font(16, bold=True)
    f_body = get_font(13, bold=False)
    
    draw.text(((x1 + x2) // 2, y1 + hdr_h // 2), class_name, fill=(255, 255, 255), font=f_title, anchor="mm")
    
    curr_y = y1 + hdr_h + 10
    if fields:
        for f in fields:
            draw.text((x1 + 14, curr_y), f, fill=(15, 23, 42), font=f_body)
            curr_y += 20
        curr_y += 4
        draw.line([(x1, curr_y), (x2, curr_y)], fill=border_color, width=1)
        curr_y += 8
    
    if methods:
        for m in methods:
            draw.text((x1 + 14, curr_y), m, fill=(15, 23, 42), font=f_body)
            curr_y += 20

def render_hinh_4_10a(style="infographic"):
    W, H = 2000, 1300
    bg_color = (248, 250, 252) if style == "infographic" else (255, 255, 255)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)

    f_title = get_font(30, bold=True)
    f_sub = get_font(18, bold=False)

    # Title header
    draw.text((W // 2, 45), "SƠ ĐỒ LỚP CHI TIẾT SÁCH & ĐÁNH GIÁ (CLASS DIAGRAM) — YIYI BOOK", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W // 2, 80), "Cấu trúc phân tầng lớp Controller, Service, Repository và Entity tham gia luồng xem chi tiết sách & đánh giá", fill=(71, 85, 105), font=f_sub, anchor="mm")
    draw.line([(80, 110), (W - 80, 110)], fill=(226, 232, 240), width=2)

    # =========================================================================
    # ROW 1: CONTROLLERS (y: 140 -> 360)
    # =========================================================================
    # 1. BookController
    render_class_box(draw, [100, 140, 680, 360], "BookController",
                     ["- bookService: BookService", "- categoryService: CategoryService"],
                     ["+ getBookById(Long id): ResponseEntity<BookDTO>",
                      "+ getFeaturedBooks(): ResponseEntity<List<BookDTO>>",
                      "+ getRecommendations(Long userId): ResponseEntity<List<BookDTO>>"],
                     header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    # 2. ReviewController
    render_class_box(draw, [740, 140, 1320, 360], "ReviewController",
                     ["- reviewService: ReviewService", "- authService: AuthService"],
                     ["+ getReviewsByBook(Long bookId): ResponseEntity<List<ReviewDTO>>",
                      "+ checkEligibility(Long bookId): ResponseEntity<EligibilityDTO>",
                      "+ createReview(ReviewRequest req): ResponseEntity<ReviewDTO>"],
                     header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # 3. ReviewCommentController
    render_class_box(draw, [1380, 140, 1900, 360], "ReviewCommentController",
                     ["- commentService: ReviewCommentService"],
                     ["+ getComments(Long reviewId): ResponseEntity<List<CommentDTO>>",
                      "+ addComment(Long reviewId, CommentReq req): ResponseEntity",
                      "+ deleteComment(Long commentId): ResponseEntity"],
                     header_bg=(124, 58, 237), box_bg=(250, 245, 255), border_color=(139, 92, 246))

    # =========================================================================
    # ROW 2: SERVICES (y: 440 -> 680)
    # =========================================================================
    # 1. BookService
    render_class_box(draw, [100, 440, 680, 680], "BookService",
                     ["- bookRepository: BookRepository", "- categoryRepository: CategoryRepository"],
                     ["+ getBookById(Long id): BookDTO",
                      "+ updateStock(Long bookId, Integer qty): void",
                      "+ searchBooks(String kw, Pageable page): Page<BookDTO>",
                      "+ getRelatedBooks(Long categoryId): List<BookDTO>"],
                     header_bg=(37, 99, 235), box_bg=(239, 246, 255), border_color=(59, 130, 246))

    # 2. ReviewService
    render_class_box(draw, [740, 440, 1320, 680], "ReviewService",
                     ["- reviewRepo: ReviewRepository", "- orderRepo: OrderRepository", "- userRepo: UserRepository"],
                     ["+ getReviewsByBookId(Long bookId): List<ReviewDTO>",
                      "+ checkUserEligibility(String username, Long bookId): boolean",
                      "+ createReview(String username, ReviewRequest req): ReviewDTO",
                      "+ calculateAverageRating(Long bookId): Double"],
                     header_bg=(13, 148, 136), box_bg=(240, 253, 250), border_color=(20, 184, 166))

    # =========================================================================
    # ROW 3: REPOSITORIES (y: 760 -> 960)
    # =========================================================================
    # 1. BookRepository
    render_class_box(draw, [100, 760, 520, 960], "BookRepository <<Interface>>",
                     [],
                     ["+ findById(Long id): Optional<Book>",
                      "+ findByCategoryId(Long catId): List<Book>",
                      "+ findFirstByTitle(String title): Optional<Book>",
                      "+ findAll(Specification spec, Pageable p): Page<Book>"],
                     header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # 2. ReviewRepository
    render_class_box(draw, [560, 760, 1060, 960], "ReviewRepository <<Interface>>",
                     [],
                     ["+ findByBookIdOrderByCreatedAtDesc(Long id): List<Review>",
                      "+ countByUserIdAndBookId(Long uid, Long bid): Long",
                      "+ findByUserId(Long userId): List<Review>",
                      "+ calculateAvgRating(Long bookId): Double"],
                     header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # 3. ReviewCommentRepository
    render_class_box(draw, [1100, 760, 1500, 960], "ReviewCommentRepository <<Interface>>",
                     [],
                     ["+ findByReviewIdOrderByCreatedAtAsc(Long rid): List",
                      "+ countByReviewId(Long reviewId): Long",
                      "+ deleteByReviewId(Long reviewId): void"],
                     header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # 4. OrderRepository
    render_class_box(draw, [1540, 760, 1900, 960], "OrderRepository <<Interface>>",
                     [],
                     ["+ countUserDeliveredPurchases(Long uid, Long bid): Long",
                      "+ findByUserIdOrderByCreatedAtDesc(Long uid): List",
                      "+ findById(Long id): Optional<Order>"],
                     header_bg=(71, 85, 105), box_bg=(248, 250, 252), border_color=(100, 116, 139))

    # =========================================================================
    # ROW 4: ENTITIES (y: 1040 -> 1240)
    # =========================================================================
    # 1. Book Entity
    render_class_box(draw, [100, 1040, 520, 1240], "Book <<Entity>>",
                     ["- id: Long", "- title: String", "- price: BigDecimal", "- stockQuantity: Integer", "- category: Category"],
                     ["+ getPrice(): BigDecimal", "+ setStockQuantity(int qty): void"],
                     header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    # 2. Review Entity
    render_class_box(draw, [560, 1040, 1060, 1240], "Review <<Entity>>",
                     ["- id: Long", "- rating: Integer (1-5)", "- comment: String", "- user: User", "- book: Book"],
                     ["+ getRating(): Integer", "+ getComments(): List<ReviewComment>"],
                     header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    # 3. ReviewComment Entity
    render_class_box(draw, [1100, 1040, 1500, 1240], "ReviewComment <<Entity>>",
                     ["- id: Long", "- content: String", "- user: User", "- review: Review", "- createdAt: LocalDateTime"],
                     ["+ getContent(): String", "+ setContent(String c): void"],
                     header_bg=(30, 41, 59), box_bg=(241, 245, 249), border_color=(71, 85, 105))

    # =========================================================================
    # CONNECTING ARROWS
    # =========================================================================
    # Controller -> Service (Solid arrow)
    draw_arrow(draw, (390, 360), (390, 440), fill=(37, 99, 235), width=3, arrow_size=10)
    draw_arrow(draw, (1030, 360), (1030, 440), fill=(13, 148, 136), width=3, arrow_size=10)

    # Service -> Repositories (Solid arrow)
    draw_arrow(draw, (310, 680), (310, 760), fill=(37, 99, 235), width=3, arrow_size=10)
    draw_arrow(draw, (810, 680), (810, 760), fill=(13, 148, 136), width=3, arrow_size=10)
    draw_arrow(draw, (1150, 680), (1720, 760), fill=(13, 148, 136), width=2, arrow_size=10, dashed=True)

    # Repository -> Entity (Dashed arrow)
    draw_arrow(draw, (310, 960), (310, 1040), fill=(71, 85, 105), width=2, arrow_size=8, dashed=True)
    draw_arrow(draw, (810, 960), (810, 1040), fill=(71, 85, 105), width=2, arrow_size=8, dashed=True)
    draw_arrow(draw, (1300, 960), (1300, 1040), fill=(71, 85, 105), width=2, arrow_size=8, dashed=True)

    # Review -> ReviewComment relationship (1..n)
    draw.line([(1060, 1140), (1100, 1140)], fill=(30, 41, 59), width=3)
    f_rel = get_font(14, bold=True)
    draw.text((1080, 1120), "1..n", fill=(30, 41, 59), font=f_rel, anchor="mm")

    return img

def main():
    print("Generating newly designed Hinh 4.10a Class Diagram without text overlapping...")
    for style, out_dir in [("infographic", INFO_REV_DIR), ("standard", STD_REV_DIR), ("infographic", INFO_DIR), ("standard", STD_DIR)]:
        img = render_hinh_4_10a(style)
        out_path = os.path.join(out_dir, "Hinh_4.10a_Class_Diagram_BookDetail_Review.png")
        img.save(out_path, dpi=(300, 300))
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()

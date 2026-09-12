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

def render_hinh_4_12():
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(30, bold=True)
    f_sub = get_font(17, bold=False)
    f_hdr = get_font(18, bold=True)
    f_box = get_font(15, bold=True)
    f_body = get_font(13, bold=False)

    draw.text((W//2, 45), "SƠ ĐỒ LỚP VÀ TUẦN TỰ ĐẶT HÀNG COD & GIẢM GIÁ (CHECKOUT) — YIYI BOOK", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 75), "Class Diagram xử lý đơn hàng, tính toán Coupon, miễn phí vận chuyển, tích lũy Y-Points và Sequence Flow", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # LEFT PANEL: CLASS DIAGRAM (x: 80 -> 900)
    draw.rounded_rectangle([80, 110, 900, 1180], radius=14, fill=(255, 255, 255), outline=(37, 99, 235), width=2)
    draw.rectangle([80, 110, 900, 155], fill=(37, 99, 235))
    draw.text((490, 132), "CLASS DIAGRAM: ORDER & CHECKOUT SUBSYSTEM", fill=(255, 255, 255), font=f_hdr, anchor="mm")

    # OrderController
    draw.rounded_rectangle([110, 175, 480, 410], radius=8, fill=(239, 246, 255), outline=(59, 130, 246), width=1)
    draw.rectangle([110, 175, 480, 210], fill=(37, 99, 235))
    draw.text((295, 192), "OrderController", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((120, 220), "- orderService: OrderService", fill=(15, 23, 42), font=f_body)
    draw.line([(110, 245), (480, 245)], fill=(59, 130, 246), width=1)
    draw.text((120, 255), "+ createOrder(user, req): Order\n+ getMyOrders(user): List<Order>\n+ getOrderById(id): Order\n+ cancelOrder(id): ResponseEntity\n+ requestReturn(id, req): Order", fill=(15, 23, 42), font=f_body)

    # OrderService
    draw.rounded_rectangle([520, 175, 870, 450], radius=8, fill=(236, 253, 245), outline=(16, 185, 129), width=1)
    draw.rectangle([520, 175, 870, 210], fill=(5, 150, 105))
    draw.text((695, 192), "OrderService", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((530, 220), "- orderRepo: OrderRepository\n- userRepo: UserRepository\n- bookRepo: BookRepository\n- couponService: CouponService\n- pointTxRepo: PointTxRepo", fill=(15, 23, 42), font=f_body)
    draw.line([(520, 320), (870, 320)], fill=(16, 185, 129), width=1)
    draw.text((530, 330), "+ createOrder(u, req): Order\n- updatePointsAndSpent(u, total)\n+ applyCoupon(code, total): double\n+ processCOD(order): Order", fill=(15, 23, 42), font=f_body)

    # Order & OrderItem Entities
    draw.rounded_rectangle([110, 470, 480, 710], radius=8, fill=(254, 243, 199), outline=(245, 158, 11), width=1)
    draw.rectangle([110, 470, 480, 505], fill=(217, 119, 6))
    draw.text((295, 487), "Order & OrderItem (Entities)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((120, 515), "Order:\n- id: Long [PK] | user: User [FK]\n- totalAmount: Double | status: String\n- paymentMethod: 'COD' / 'VNPAY'\n- items: List<OrderItem> [1-N]\nOrderItem:\n- id: Long | book: Book | quantity | price", fill=(15, 23, 42), font=f_body)

    # Coupon & PointTransaction
    draw.rounded_rectangle([520, 470, 870, 710], radius=8, fill=(255, 247, 237), outline=(249, 115, 22), width=1)
    draw.rectangle([520, 470, 870, 505], fill=(234, 88, 12))
    draw.text((695, 487), "Coupon & PointTransaction", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((530, 515), "Coupon:\n- code: String [UK] | discountValue\n- discountType: FIXED / PERCENTAGE\n- minOrderAmount | maxDiscountAmount\nPointTransaction:\n- action: 'EARN_ORDER' / 'REDEEM'\n- transactionValue | newBalance", fill=(15, 23, 42), font=f_body)

    # Repositories Box
    draw.rounded_rectangle([110, 730, 870, 940], radius=8, fill=(241, 245, 249), outline=(100, 116, 139), width=1)
    draw.rectangle([110, 730, 870, 765], fill=(51, 65, 85))
    draw.text((490, 747), "Persistence Repositories (Spring Data JPA)", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((130, 775), "• OrderRepository: findByUserId(userId, Pageable), countByStatus(status), sumTotalRevenue()", fill=(15, 23, 42), font=f_body)
    draw.text((130, 805), "• CartRepository & CartItemRepository: findByUserId, deleteByCartIdAndBookIdIn(cartId, bookIds)", fill=(15, 23, 42), font=f_body)
    draw.text((130, 835), "• CouponRepository: findByCodeAndIsActiveTrue(code), decrementUsageLimit(code)", fill=(15, 23, 42), font=f_body)
    draw.text((130, 865), "• PointTransactionRepository: save(earnTx), findByUserIdOrderByCreatedAtDesc(userId)", fill=(15, 23, 42), font=f_body)
    draw.text((130, 895), "• UserRepository: save(user.totalSpent, user.yPoints, user.accumulatedPoints)", fill=(15, 23, 42), font=f_body)

    # Summary Box
    draw.rounded_rectangle([110, 960, 870, 1150], radius=8, fill=(245, 243, 255), outline=(139, 92, 246), width=1)
    draw.text((490, 985), "Quy tắc nghiệp vụ Đặt hàng & Khuyến mãi COD", fill=(109, 40, 217), font=f_box, anchor="mm")
    draw.text((130, 1015), "1. Trạng thái khởi tạo đơn COD là 'PENDING' ngay sau khi tạo bản ghi đơn hàng thành công.", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1045), "2. Tích điểm thưởng Y-Point tự động theo tỷ lệ hạng thành viên (0.5% Bạc -> 2% Kim Cương).", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1075), "3. Thưởng đơn hàng đầu tiên (isFirstOrder): Tặng thêm 20,000 Y-Points + Coupon FREESHIP 30K.", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1105), "4. Tự động dọn dẹp các sản phẩm đã thanh toán khỏi CartItem trong giỏ hàng người dùng.", fill=(15, 23, 42), font=f_body)

    # RIGHT PANEL: SEQUENCE FLOW (x: 940 -> 1920)
    draw.rounded_rectangle([940, 110, 1920, 1180], radius=14, fill=(255, 255, 255), outline=(16, 185, 129), width=2)
    draw.rectangle([940, 110, 1920, 155], fill=(5, 150, 105))
    draw.text((1430, 132), "SEQUENCE FLOW: COD CHECKOUT & COUPON DISCOUNT", fill=(255, 255, 255), font=f_hdr, anchor="mm")

    seq_actors = [
        ("Customer", 1010, (13, 148, 136)),
        ("Checkout.jsx (UI)", 1180, (2, 132, 199)),
        ("OrderController", 1360, (37, 99, 235)),
        ("OrderService", 1540, (5, 150, 105)),
        ("Coupon & Cart Svc", 1720, (234, 88, 12)),
        ("Database / JPA", 1870, (51, 65, 85))
    ]
    for title, x, col in seq_actors:
        draw.rounded_rectangle([x-65, 175, x+65, 215], radius=6, fill=col)
        draw.text((x, 195), title, fill=(255, 255, 255), font=f_box, anchor="mm")
        draw.line([(x, 215), (x, 1130)], fill=(203, 213, 225), width=2)
        draw.rounded_rectangle([x-65, 1130, x+65, 1160], radius=6, fill=col)
        draw.text((x, 1145), title, fill=(255, 255, 255), font=f_body, anchor="mm")

    seq_msgs = [
        (1010, 1180, "1. Chọn sản phẩm, áp mã giảm giá & click 'Đặt hàng COD'", 250, False, (15, 23, 42)),
        (1180, 1360, "2. POST /api/orders (OrderRequest, Bearer JWT)", 315, False, (37, 99, 235)),
        (1360, 1540, "3. createOrder(username, OrderRequest)", 380, False, (5, 150, 105)),
        (1540, 1720, "4. validateCoupon(code) & calculateFinalPrice()", 445, False, (234, 88, 12)),
        (1720, 1540, "5. Coupon OK -> Trả về tổng tiền đã chiết khấu", 510, True, (234, 88, 12)),
        (1540, 1870, "6. save(Order entity status='PENDING', OrderItems)", 575, False, (51, 65, 85)),
        (1870, 1540, "7. Đã lưu đơn hàng vào bảng 'orders' & 'order_items'", 640, True, (51, 65, 85)),
        (1540, 1720, "8. cartService.removePurchasedItems(cartId, bookIds)", 705, False, (234, 88, 12)),
        (1540, 1870, "9. updatePointsAndSpent(user, total) -> save(PointTx)", 770, False, (51, 65, 85)),
        (1540, 1360, "10. Trả về Order entity hoàn chỉnh", 835, True, (5, 150, 105)),
        (1360, 1180, "11. HTTP 200 OK + Order JSON DTO", 900, True, (37, 99, 235)),
        (1180, 1180, "12. Cập nhật CartContext (xóa badge) & chuyển hướng", 965, False, (2, 132, 199)), # Self
        (1180, 1010, "13. Chuyển sang /order-success/{id} hiển thị mã đơn", 1030, True, (13, 148, 136)),
        (1010, 1180, "14. [Optional] Xem tiến trình tại /orders", 1085, False, (100, 116, 139))
    ]

    for x1, x2, text, y, is_dashed, col in seq_msgs:
        if x1 == x2:
            draw.line([(x1, y-12), (x1+35, y-12), (x1+35, y+12), (x1, y+12)], fill=col, width=2)
            draw_arrow(draw, (x1+35, y+12), (x1, y+12), fill=col, width=2, arrow_size=5)
            draw.text((x1+42, y), text, fill=col, font=f_body, anchor="lm")
        else:
            draw_arrow(draw, (x1, y), (x2, y), fill=col, width=2, arrow_size=7, dashed=is_dashed)
            draw.text(((x1+x2)//2, y-12), text, fill=col, font=f_body, anchor="mm")

    draw.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — COD Checkout Class & Sequence Diagram", fill=(148, 163, 184), font=f_body, anchor="mm")

    # Standard Version
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 45), "HÌNH 4.12. SƠ ĐỒ LỚP VÀ TUẦN TỰ ĐẶT HÀNG COD & GIẢM GIÁ (CHECKOUT)", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 75), "Standard UML Class & Sequence Diagram Specification", fill=(80, 80, 80), font=f_sub, anchor="mm")

    draw_s.rectangle([80, 110, 900, 1180], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([80, 110, 900, 155], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    draw_s.text((490, 132), "CLASS DIAGRAM: ORDER & CHECKOUT SUBSYSTEM", fill=(0, 0, 0), font=f_hdr, anchor="mm")

    for b, t, lines in [
        ([110, 175, 480, 410], "OrderController", ["- orderService: OrderService", "---", "+ createOrder(user, req): Order", "+ getMyOrders(user): List<Order>", "+ getOrderById(id): Order", "+ cancelOrder(id): ResponseEntity"]),
        ([520, 175, 870, 450], "OrderService", ["- orderRepo: OrderRepository", "- userRepo: UserRepository", "- bookRepo: BookRepository", "- couponService: CouponService", "---", "+ createOrder(u, req): Order", "- updatePointsAndSpent(u, total)", "+ applyCoupon(code, total): double"]),
        ([110, 470, 480, 710], "Order & OrderItem (Entities)", ["Order: - id: Long [PK] | user: User", "- totalAmount: Double | status: String", "- paymentMethod: 'COD' / 'VNPAY'", "---", "OrderItem: - id: Long | book: Book", "- quantity: Integer | price: Double"]),
        ([520, 470, 870, 710], "Coupon & PointTransaction", ["Coupon: - code: String [UK]", "- discountValue | discountType", "---", "PointTransaction: - action", "- transactionValue | newBalance"])
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

    draw_s.rectangle([110, 730, 870, 940], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    draw_s.text((490, 755), "Persistence Repositories (Spring Data JPA)", fill=(0, 0, 0), font=f_box, anchor="mm")
    draw_s.text((130, 785), "• OrderRepository: findByUserId, countByStatus, sumTotalRevenue", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 815), "• CartRepository & CartItemRepository: findByUserId, deleteByCartId", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 845), "• CouponRepository: findByCodeAndIsActiveTrue, decrementUsageLimit", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 875), "• PointTransactionRepository: save(earnTx), findByUserId", fill=(0, 0, 0), font=f_body)

    draw_s.rectangle([110, 960, 870, 1150], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    draw_s.text((490, 985), "Quy tắc nghiệp vụ Đặt hàng & Khuyến mãi COD", fill=(0, 0, 0), font=f_box, anchor="mm")
    draw_s.text((130, 1015), "1. Trạng thái khởi tạo đơn COD là 'PENDING' ngay sau khi tạo bản ghi.", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 1045), "2. Tích điểm thưởng Y-Point tự động theo tỷ lệ hạng thành viên (0.5% -> 2%).", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 1075), "3. Thưởng đơn đầu: +20,000 Y-Points + Coupon FREESHIP 30K.", fill=(0, 0, 0), font=f_body)
    draw_s.text((130, 1105), "4. Tự động dọn dẹp các sản phẩm đã mua khỏi CartItem.", fill=(0, 0, 0), font=f_body)

    # Sequence Standard
    draw_s.rectangle([940, 110, 1920, 1180], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([940, 110, 1920, 155], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
    draw_s.text((1430, 132), "SEQUENCE FLOW: COD CHECKOUT & COUPON DISCOUNT", fill=(0, 0, 0), font=f_hdr, anchor="mm")

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

    p_info = os.path.join(INFO_DIR, "Hinh_4.12_Class_Sequence_Diagram_Checkout_COD.png")
    p_std = os.path.join(STD_DIR, "Hinh_4.12_Class_Sequence_Diagram_Checkout_COD.png")
    img.save(p_info, "PNG", dpi=(300, 300))
    img_std.save(p_std, "PNG", dpi=(300, 300))

    svg_info = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
        <rect width="100%" height="100%" fill="#F8FAFC"/>
        <text x="{W//2}" y="45" font-family="Arial, sans-serif" font-size="30" font-weight="bold" fill="#0F172A" text-anchor="middle">SƠ ĐỒ LỚP VÀ TUẦN TỰ ĐẶT HÀNG COD & GIẢM GIÁ (CHECKOUT) — YIYI BOOK</text>
        <text x="{W//2}" y="75" font-family="Arial, sans-serif" font-size="17" fill="#475569" text-anchor="middle">Class Diagram xử lý đơn hàng, tính toán Coupon, miễn phí vận chuyển, tích lũy Y-Points và Sequence Flow</text>
    </svg>'''
    with open(os.path.join(INFO_DIR, "Hinh_4.12_Class_Sequence_Diagram_Checkout_COD.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.12_Class_Sequence_Diagram_Checkout_COD.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.12 (Checkout COD) successfully.")

if __name__ == "__main__":
    render_hinh_4_12()

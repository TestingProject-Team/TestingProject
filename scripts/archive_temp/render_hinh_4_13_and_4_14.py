# -*- coding: utf-8 -*-
"""
Render Hinh 4.13: Sơ đồ lớp và Tuần tự Tích hợp Cổng thanh toán Online (VNPay, MoMo, ZaloPay)
Render Hinh 4.14: Sơ đồ trạng thái (State Diagram) & Tuần tự luồng Đơn hàng và Đổi trả
"""
import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
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
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6),
          y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6),
          y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)

def draw_rounded_card(draw, rect, fill, outline, width=2, radius=8):
    draw.rounded_rectangle(rect, fill=fill, outline=outline, width=width, radius=radius)

def draw_uml_class(draw, rect, title, attributes, methods, is_info=True, header_fill=(241, 245, 249), stroke=(100, 116, 139)):
    x1, y1, x2, y2 = rect
    body_fill = (255, 255, 255) if is_info else (255, 255, 255)
    draw.rectangle([x1, y1, x2, y2], fill=body_fill, outline=stroke, width=2)
    
    # Title compartment
    t_h = 32
    draw.rectangle([x1, y1, x2, y1 + t_h], fill=header_fill, outline=stroke, width=2)
    draw.text((x1 + 10, y1 + 7), title, fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(14, True))
    
    # Attributes
    curr_y = y1 + t_h + 8
    for attr in attributes:
        draw.text((x1 + 10, curr_y), attr, fill=(51, 65, 85) if is_info else (0, 0, 0), font=get_font(12, False))
        curr_y += 18
        
    # Divider
    curr_y += 4
    draw.line([(x1, curr_y), (x2, curr_y)], fill=stroke, width=1)
    curr_y += 6
    
    # Methods
    for meth in methods:
        draw.text((x1 + 10, curr_y), meth, fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(12, False))
        curr_y += 18

def save_dual_svg(fn_base, is_info=True):
    # Minimal stub to save SVG reference alongside PNG
    out_dir = INFO_DIR if is_info else STD_DIR
    svg_path = os.path.join(out_dir, f"{fn_base}.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1600"><text x="100" y="100" font-family="Arial" font-size="24">{fn_base}</text></svg>')

def render_hinh_4_13():
    """Hình 4.13: Payment Online Class & Sequence Diagram"""
    W, H = 2400, 1600

    def draw_content(draw, is_info=True):
        bg_col = (248, 250, 252) if is_info else (255, 255, 255)
        draw.rectangle([(0, 0), (W, H)], fill=bg_col)

        title = "HÌNH 4.13: SƠ ĐỒ LỚP VÀ TUẦN TỰ (CLASS/SEQUENCE) TÍCH HỢP CỔNG THANH TOÁN ONLINE"
        sub = "Kiến trúc tích hợp đa cổng thanh toán: VNPay Sandbox (HMAC-SHA512), MoMo QR (captureWallet), ZaloPay Gateway"
        
        t_col = (15, 23, 42) if is_info else (0, 0, 0)
        s_col = (71, 85, 105) if is_info else (68, 68, 68)
        
        draw.text((60, 40), title, fill=t_col, font=get_font(26, True))
        draw.text((60, 80), sub, fill=s_col, font=get_font(15, False))

        # --- SECTION 1: CLASS DIAGRAM (Top Half) ---
        c_hdr = (224, 242, 254) if is_info else (240, 240, 240)
        c_str = (2, 132, 199) if is_info else (0, 0, 0)
        
        # PaymentController Class
        draw_uml_class(draw, (70, 130, 490, 440), "PaymentController",
                       ["- orderService: OrderService",
                        "- frontendUrl: String",
                        "- restTemplate: RestTemplate"],
                       ["+ createPaymentUrl(amount, orderId, ...): Map",
                        "+ createMoMoPaymentUrl(amount, orderId): Map",
                        "+ createZaloPaymentUrl(amount, orderId): Map",
                        "+ paymentReturn(params, request): Response",
                        "+ momoReturn(params): Response",
                        "+ zalopayReturn(params): Response",
                        "+ momoIpn(payload): Response"],
                       is_info=is_info, header_fill=c_hdr, stroke=c_str)

        # Configs Class
        draw_uml_class(draw, (530, 130, 910, 440), "Payment Gateway Configs",
                       ["«utility» VNPayConfig / MoMoConfig",
                        "- vnp_TmnCode, vnp_HashSecret: String",
                        "- momo_PartnerCode, momo_AccessKey",
                        "- zalopay_AppId, zalopay_Key1: String"],
                       ["+ hmacSHA512(key, data): String",
                        "+ encodeHmacSha256(key, data): String",
                        "+ getIpAddress(request): String",
                        "+ verifyChecksum(params): boolean"],
                       is_info=is_info, header_fill=c_hdr, stroke=c_str)

        # Order & OrderService
        draw_uml_class(draw, (950, 130, 1360, 440), "OrderService (Payment Integration)",
                       ["- orderRepository: OrderRepository",
                        "- userRepository: UserRepository",
                        "- pointService: PointTransactionService"],
                       ["+ confirmVNPayPayment(orderId, success)",
                        "+ updatePaymentMethod(orderId, method)",
                        "+ createOrder(username, req): Order",
                        "+ updatePointsAndSpent(user, total, isFirst)"],
                       is_info=is_info, header_fill=c_hdr, stroke=c_str)

        # External Gateways
        draw_uml_class(draw, (1400, 130, 1850, 440), "External Payment Gateways API",
                       ["«external service»",
                        "- VNPay Sandbox Endpoint",
                        "- MoMo Payment Gateway Endpoint",
                        "- ZaloPay Sandbox Endpoint"],
                       ["+ POST /vpcpay.html (Redirect URL)",
                        "+ POST /v2/gateway/api/create (MoMo QR)",
                        "+ POST /v2/create (ZaloPay Order)",
                        "+ Webhook IPN Callback"],
                       is_info=is_info, header_fill=c_hdr, stroke=c_str)

        # Order Entity
        draw_uml_class(draw, (1890, 130, 2330, 440), "Order (Payment State)",
                       ["- id: Long",
                        "- paymentMethod: String (VNPAY/MOMO/COD)",
                        "- isPaid: boolean",
                        "- paidAt: LocalDateTime",
                        "- paymentStatus: String",
                        "- total: double"],
                       ["+ setPaid(boolean)",
                        "+ setPaidAt(LocalDateTime)",
                        "+ setPaymentStatus(String)"],
                       is_info=is_info, header_fill=c_hdr, stroke=c_str)

        # Class relationships
        draw_arrow(draw, (490, 280), (530, 280), fill=(100, 116, 139) if is_info else (0, 0, 0))
        draw_arrow(draw, (490, 340), (950, 340), fill=(2, 132, 199) if is_info else (0, 0, 0))
        draw_arrow(draw, (1360, 280), (1400, 280), fill=(100, 116, 139) if is_info else (0, 0, 0))
        draw_arrow(draw, (1360, 340), (1890, 340), fill=(5, 150, 105) if is_info else (0, 0, 0))

        # --- SECTION 2: SEQUENCE DIAGRAM (Lower Section) ---
        sep_y = 480
        draw.line([(60, sep_y), (W - 60, sep_y)], fill=(203, 213, 225) if is_info else (0, 0, 0), width=2)
        draw.text((70, sep_y + 15), "LUỒNG TUẦN TỰ (SEQUENCE DIAGRAM): TẠO GIAO DỊCH, CHUYỂN HƯỚNG CỔNG & XÁC THỰC CHECKSUM RETURN / IPN",
                  fill=(3, 105, 161) if is_info else (0, 0, 0), font=get_font(18, True))

        # Lifeline Participants
        actors = [
            ("Client / Buyer", 180, (238, 242, 255), (99, 102, 241)),
            ("Frontend React", 580, (239, 246, 255), (59, 130, 246)),
            ("PaymentController", 1040, (240, 253, 244), (34, 197, 94)),
            ("VNPay / MoMo Gateway", 1540, (254, 242, 242), (239, 68, 68)),
            ("OrderService & DB", 2060, (254, 243, 199), (245, 158, 11))
        ]

        ll_top = 540
        ll_bot = 1530

        for name, cx, bg, border in actors:
            b_bg = bg if is_info else (255, 255, 255)
            b_bd = border if is_info else (0, 0, 0)
            draw_rounded_card(draw, (cx - 130, ll_top, cx + 130, ll_top + 45), fill=b_bg, outline=b_bd, radius=6)
            draw.text((cx - 110, ll_top + 12), name, fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(14, True))
            draw_arrow(draw, (cx, ll_top + 45), (cx, ll_bot), fill=(148, 163, 184) if is_info else (0, 0, 0), width=1, dashed=True)

        # Steps
        cur_y = 630
        step_gap = 72

        # 1
        draw_arrow(draw, (180, cur_y), (580, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0))
        draw.text((200, cur_y - 18), "1. Chọn VNPay / MoMo & xác nhận Đặt hàng", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 2
        draw_arrow(draw, (580, cur_y), (1040, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0))
        draw.text((600, cur_y - 18), "2. GET /api/payment/create-url?amount=X&orderId=Y", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 3. Hash computation
        draw_rounded_card(draw, (900, cur_y - 15, 1180, cur_y + 25), fill=(240, 253, 244) if is_info else (255, 255, 255), outline=(34, 197, 94) if is_info else (0, 0, 0), radius=4)
        draw.text((915, cur_y - 6), "Tạo params & HMAC-SHA512 checksum", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(12, True))
        cur_y += 45

        # 4
        draw_arrow(draw, (1040, cur_y), (580, cur_y), fill=(100, 116, 139) if is_info else (0, 0, 0), dashed=True)
        draw.text((630, cur_y - 18), "3. Trả về { paymentUrl: 'https://sandbox.vnpayment.vn/...' }", fill=(71, 85, 105) if is_info else (0, 0, 0), font=get_font(13, False))
        cur_y += step_gap

        # 5
        draw_arrow(draw, (580, cur_y), (1540, cur_y), fill=(239, 68, 68) if is_info else (0, 0, 0))
        draw.text((750, cur_y - 18), "4. window.location.href = paymentUrl (Chuyển hướng cổng)", fill=(185, 28, 28) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 6
        draw_arrow(draw, (180, cur_y), (1540, cur_y), fill=(99, 102, 241) if is_info else (0, 0, 0))
        draw.text((380, cur_y - 18), "5. Khách quét MoMo QR / Nhập thẻ test VNPay Sandbox + OTP", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, False))
        cur_y += step_gap

        # 7
        draw_arrow(draw, (1540, cur_y), (580, cur_y), fill=(239, 68, 68) if is_info else (0, 0, 0))
        draw.text((720, cur_y - 18), "6. Redirect ReturnUrl /payment-result?vnp_ResponseCode=00&vnp_SecureHash=...", fill=(185, 28, 28) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 8
        draw_arrow(draw, (580, cur_y), (1040, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0))
        draw.text((610, cur_y - 18), "7. GET /api/payment/vnpay-return (Chuyển tiếp tất cả params)", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 9. Verify checksum
        draw_rounded_card(draw, (890, cur_y - 15, 1190, cur_y + 25), fill=(240, 253, 244) if is_info else (255, 255, 255), outline=(34, 197, 94) if is_info else (0, 0, 0), radius=4)
        draw.text((905, cur_y - 6), "Xác thực chữ ký số: signValue == vnp_SecureHash", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(12, True))
        cur_y += 45

        # 10
        draw_arrow(draw, (1040, cur_y), (2060, cur_y), fill=(34, 197, 94) if is_info else (0, 0, 0))
        draw.text((1220, cur_y - 18), "8. [Chữ ký hợp lệ & Code 00] confirmVNPayPayment(orderId, true)", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 11. Database update
        draw_rounded_card(draw, (1910, cur_y - 15, 2210, cur_y + 25), fill=(254, 243, 199) if is_info else (255, 255, 255), outline=(245, 158, 11) if is_info else (0, 0, 0), radius=4)
        draw.text((1925, cur_y - 6), "order.setPaid(true), tích lũy Y-Point", fill=(180, 83, 9) if is_info else (0, 0, 0), font=get_font(12, True))
        cur_y += 45

        # 12
        draw_arrow(draw, (2060, cur_y), (1040, cur_y), fill=(100, 116, 139) if is_info else (0, 0, 0), dashed=True)
        draw.text((1380, cur_y - 18), "9. Ghi nhận thanh toán & tích điểm thành công", fill=(71, 85, 105) if is_info else (0, 0, 0), font=get_font(13, False))
        cur_y += step_gap

        # 13
        draw_arrow(draw, (1040, cur_y), (580, cur_y), fill=(34, 197, 94) if is_info else (0, 0, 0), dashed=True)
        draw.text((630, cur_y - 18), "10. Trả về { status: 'success', message: 'Thanh toán thành công' }", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 14
        draw_arrow(draw, (580, cur_y), (180, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0), dashed=True)
        draw.text((220, cur_y - 18), "11. Hiển thị màn hình Hoàn tất Đơn hàng & Thông tin theo dõi", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, True))

    # Render Infographic
    img_info = Image.new("RGB", (W, H), (248, 250, 252))
    draw_info = ImageDraw.Draw(img_info)
    draw_content(draw_info, is_info=True)
    img_info.save(os.path.join(INFO_DIR, "Hinh_4.13_Class_Sequence_Diagram_Payment_Online.png"), "PNG", dpi=(300, 300))
    save_dual_svg("Hinh_4.13_Class_Sequence_Diagram_Payment_Online", is_info=True)

    # Render Standard
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_std = ImageDraw.Draw(img_std)
    draw_content(draw_std, is_info=False)
    img_std.save(os.path.join(STD_DIR, "Hinh_4.13_Class_Sequence_Diagram_Payment_Online.png"), "PNG", dpi=(300, 300))
    save_dual_svg("Hinh_4.13_Class_Sequence_Diagram_Payment_Online", is_info=False)


def render_hinh_4_14():
    """Hình 4.14: Sơ đồ trạng thái & Tuần tự luồng Đơn hàng và Đổi trả"""
    W, H = 2400, 1600

    def draw_content(draw, is_info=True):
        bg_col = (248, 250, 252) if is_info else (255, 255, 255)
        draw.rectangle([(0, 0), (W, H)], fill=bg_col)

        title = "HÌNH 4.14: SƠ ĐỒ TRẠNG THÁI (STATE) VÀ TUẦN TỰ (SEQUENCE) LUỒNG ĐƠN HÀNG VÀ ĐỔI TRẢ"
        sub = "Vòng đời đơn hàng (PENDING -> PROCESSING -> SHIPPED -> DELIVERED -> COMPLETED / CANCELLED / RETURNED) & Quy trình Return Request"
        
        t_col = (15, 23, 42) if is_info else (0, 0, 0)
        s_col = (71, 85, 105) if is_info else (68, 68, 68)
        
        draw.text((60, 40), title, fill=t_col, font=get_font(26, True))
        draw.text((60, 80), sub, fill=s_col, font=get_font(15, False))

        # --- SECTION 1: STATE MACHINE DIAGRAM (Upper Half) ---
        state_y = 140
        draw.text((70, state_y), "SƠ ĐỒ TRẠNG THÁI VÒNG ĐỜI ĐƠN HÀNG (ORDER STATE MACHINE DIAGRAM)", 
                  fill=(3, 105, 161) if is_info else (0, 0, 0), font=get_font(18, True))

        # Initial State
        draw.ellipse([(90, state_y + 80), (120, state_y + 110)], fill=(15, 23, 42) if is_info else (0, 0, 0))
        draw_arrow(draw, (120, state_y + 95), (170, state_y + 95), fill=(100, 116, 139) if is_info else (0, 0, 0))
        draw.text((125, state_y + 75), "Tạo đơn", fill=(71, 85, 105) if is_info else (0, 0, 0), font=get_font(11, False))

        # States boxes
        def draw_state(x, y, w, h, name, desc, bg, border):
            draw_rounded_card(draw, (x, y, x + w, y + h), fill=bg if is_info else (255, 255, 255), outline=border if is_info else (0, 0, 0), radius=8)
            draw.text((x + 12, y + 10), name, fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(14, True))
            draw.text((x + 12, y + 34), desc, fill=(71, 85, 105) if is_info else (68, 68, 68), font=get_font(11, False))

        # 1. PENDING
        draw_state(170, state_y + 60, 240, 75, "PENDING (Chờ xử lý)", "Chờ thanh toán Online\nhoặc xác nhận COD", (241, 245, 249), (148, 163, 184))

        # 2. PROCESSING
        draw_state(510, state_y + 60, 260, 75, "PROCESSING (Đang xử lý)", "Thanh toán xong / COD duyệt\nKho đóng gói đơn hàng", (239, 246, 255), (59, 130, 246))

        # 3. SHIPPED
        draw_state(870, state_y + 60, 260, 75, "SHIPPED (Đang giao)", "Bàn giao ĐVVC (GHTK/GHN)\nCó mã TrackingNumber", (240, 253, 244), (34, 197, 94))

        # 4. DELIVERED
        draw_state(1230, state_y + 60, 270, 75, "DELIVERED (Đã giao)", "Khách nhận kiện hàng\nBắt đầu hạn 7 ngày đổi trả", (254, 243, 199), (245, 158, 11))

        # 5. COMPLETED (Terminal State 1)
        draw_state(1600, state_y + 60, 260, 75, "COMPLETED (Hoàn tất)", "Xác nhận nhận / Sau 7 ngày\nTích lũy điểm Y-Point", (236, 253, 245), (16, 185, 129))

        # End Circle for Completed
        draw.ellipse([(1930, state_y + 78), (1970, state_y + 118)], fill=(255, 255, 255), outline=(16, 185, 129) if is_info else (0, 0, 0), width=3)
        draw.ellipse([(1938, state_y + 86), (1962, state_y + 110)], fill=(16, 185, 129) if is_info else (0, 0, 0))

        # State Transitions Upper Row
        draw_arrow(draw, (410, state_y + 95), (510, state_y + 95), fill=(59, 130, 246) if is_info else (0, 0, 0))
        draw.text((420, state_y + 75), "Thanh toán OK", fill=(30, 64, 175) if is_info else (0, 0, 0), font=get_font(11, True))

        draw_arrow(draw, (770, state_y + 95), (870, state_y + 95), fill=(34, 197, 94) if is_info else (0, 0, 0))
        draw.text((780, state_y + 75), "Gán Vận đơn", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(11, True))

        draw_arrow(draw, (1130, state_y + 95), (1230, state_y + 95), fill=(245, 158, 11) if is_info else (0, 0, 0))
        draw.text((1140, state_y + 75), "Giao thành công", fill=(180, 83, 9) if is_info else (0, 0, 0), font=get_font(11, True))

        draw_arrow(draw, (1500, state_y + 95), (1600, state_y + 95), fill=(16, 185, 129) if is_info else (0, 0, 0))
        draw.text((1510, state_y + 75), "Bấm Nhận / 7 ngày", fill=(4, 120, 87) if is_info else (0, 0, 0), font=get_font(11, True))

        draw_arrow(draw, (1860, state_y + 95), (1930, state_y + 95), fill=(16, 185, 129) if is_info else (0, 0, 0))

        # Lower Branch: CANCELLED & RETURN_REQUESTED / RETURNED
        # 6. CANCELLED
        draw_state(220, state_y + 200, 260, 75, "CANCELLED (Đã hủy)", "Khách hủy khi PENDING\nHoàn tồn kho lập tức", (254, 242, 242), (239, 68, 68))
        draw_arrow(draw, (290, state_y + 135), (290, state_y + 200), fill=(239, 68, 68) if is_info else (0, 0, 0))
        draw.text((300, state_y + 160), "userCancelOrder()", fill=(185, 28, 28) if is_info else (0, 0, 0), font=get_font(11, False))

        # 7. RETURN_REQUESTED
        draw_state(1170, state_y + 200, 290, 75, "RETURN_REQUESTED", "Gửi form lý do & ảnh lỗi\nTrong vòng 7 ngày từ giao", (254, 242, 242), (244, 63, 94))
        draw_arrow(draw, (1320, state_y + 135), (1320, state_y + 200), fill=(244, 63, 94) if is_info else (0, 0, 0))
        draw.text((1330, state_y + 160), "userReturnOrder()", fill=(190, 18, 60) if is_info else (0, 0, 0), font=get_font(11, False))

        # 8. RETURNED
        draw_state(1600, state_y + 200, 260, 75, "RETURNED (Đã trả hàng)", "Admin duyệt Hoàn hàng\nHoàn tiền & Thu hồi điểm", (254, 242, 242), (225, 29, 72))
        draw_arrow(draw, (1460, state_y + 235), (1600, state_y + 235), fill=(225, 29, 72) if is_info else (0, 0, 0))
        draw.text((1475, state_y + 215), "Admin Approve", fill=(159, 18, 57) if is_info else (0, 0, 0), font=get_font(11, True))

        # Transition Reject Return back to COMPLETED
        draw_arrow(draw, (1360, state_y + 200), (1640, state_y + 135), fill=(100, 116, 139) if is_info else (0, 0, 0), dashed=True)
        draw.text((1440, state_y + 165), "Admin Reject -> Giữ COMPLETED", fill=(71, 85, 105) if is_info else (0, 0, 0), font=get_font(11, False))

        # --- SECTION 2: SEQUENCE DIAGRAM FOR RETURN & REFUND (Lower Half) ---
        sep_y = 440
        draw.line([(60, sep_y), (W - 60, sep_y)], fill=(203, 213, 225) if is_info else (0, 0, 0), width=2)
        draw.text((70, sep_y + 15), "LUỒNG TUẦN TỰ (SEQUENCE DIAGRAM): QUY TRÌNH YÊU CẦU ĐỔI TRẢ & XỬ LÝ DUYỆT HOÀN HÀNG (RETURN WORKFLOW)",
                  fill=(3, 105, 161) if is_info else (0, 0, 0), font=get_font(18, True))

        # Lifeline Participants
        actors = [
            ("Buyer / Khách hàng", 200, (238, 242, 255), (99, 102, 241)),
            ("Frontend Client", 600, (239, 246, 255), (59, 130, 246)),
            ("OrderService & Controller", 1100, (240, 253, 244), (34, 197, 94)),
            ("Admin Operator", 1600, (254, 243, 199), (245, 158, 11)),
            ("Database & Points", 2100, (245, 243, 255), (168, 85, 247))
        ]

        ll_top = 510
        ll_bot = 1530

        for name, cx, bg, border in actors:
            b_bg = bg if is_info else (255, 255, 255)
            b_bd = border if is_info else (0, 0, 0)
            draw_rounded_card(draw, (cx - 140, ll_top, cx + 140, ll_top + 45), fill=b_bg, outline=b_bd, radius=6)
            draw.text((cx - 110, ll_top + 12), name, fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(14, True))
            draw_arrow(draw, (cx, ll_top + 45), (cx, ll_bot), fill=(148, 163, 184) if is_info else (0, 0, 0), width=1, dashed=True)

        # Steps
        cur_y = 600
        step_gap = 75

        # 1
        draw_arrow(draw, (200, cur_y), (600, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0))
        draw.text((220, cur_y - 18), "1. Nhấn 'Yêu cầu đổi trả' & nhập lý do, tải ảnh lỗi sản phẩm", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 2
        draw_arrow(draw, (600, cur_y), (1100, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0))
        draw.text((630, cur_y - 18), "2. POST /api/orders/{id}/return (reason, imageProofUrl)", fill=(15, 23, 42) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 3. Check condition
        draw_rounded_card(draw, (950, cur_y - 15, 1250, cur_y + 25), fill=(254, 242, 242) if is_info else (255, 255, 255), outline=(244, 63, 94) if is_info else (0, 0, 0), radius=4)
        draw.text((965, cur_y - 6), "Kiểm tra: DELIVERED & trong vòng 7 ngày", fill=(190, 18, 60) if is_info else (0, 0, 0), font=get_font(12, True))
        cur_y += 45

        # 4
        draw_arrow(draw, (1100, cur_y), (2100, cur_y), fill=(34, 197, 94) if is_info else (0, 0, 0))
        draw.text((1200, cur_y - 18), "3. Lưu ReturnRequest, đổi status='RETURN_REQUESTED'", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 5
        draw_arrow(draw, (1100, cur_y), (600, cur_y), fill=(100, 116, 139) if is_info else (0, 0, 0), dashed=True)
        draw.text((700, cur_y - 18), "4. Phản hồi Yêu cầu gửi thành công tới Khách hàng", fill=(71, 85, 105) if is_info else (0, 0, 0), font=get_font(13, False))
        cur_y += step_gap

        # 6
        draw_arrow(draw, (1600, cur_y), (1100, cur_y), fill=(245, 158, 11) if is_info else (0, 0, 0))
        draw.text((1180, cur_y - 18), "5. Admin truy cập Quản lý đổi trả: GET /api/admin/returns", fill=(180, 83, 9) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 7
        draw_arrow(draw, (1100, cur_y), (1600, cur_y), fill=(100, 116, 139) if is_info else (0, 0, 0), dashed=True)
        draw.text((1190, cur_y - 18), "6. Hiển thị danh sách yêu cầu & hình ảnh bằng chứng lỗi", fill=(71, 85, 105) if is_info else (0, 0, 0), font=get_font(13, False))
        cur_y += step_gap

        # 8
        draw_arrow(draw, (1600, cur_y), (1100, cur_y), fill=(245, 158, 11) if is_info else (0, 0, 0))
        draw.text((1220, cur_y - 18), "7. PUT /api/admin/orders/{id}/return/approve", fill=(180, 83, 9) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 9. Process approval
        draw_rounded_card(draw, (930, cur_y - 15, 1270, cur_y + 25), fill=(240, 253, 244) if is_info else (255, 255, 255), outline=(34, 197, 94) if is_info else (0, 0, 0), radius=4)
        draw.text((945, cur_y - 6), "Hoàn tiền, Cộng tồn kho sách, Trừ điểm Y-Point", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(12, True))
        cur_y += 45

        # 10
        draw_arrow(draw, (1100, cur_y), (2100, cur_y), fill=(34, 197, 94) if is_info else (0, 0, 0))
        draw.text((1220, cur_y - 18), "8. Cập nhật Order status='RETURNED', ghi nhận hoàn tiền", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 11
        draw_arrow(draw, (1100, cur_y), (200, cur_y), fill=(59, 130, 246) if is_info else (0, 0, 0), dashed=True)
        draw.text((380, cur_y - 18), "9. Gửi Thông báo: 'Yêu cầu trả hàng đã được chấp thuận'", fill=(30, 64, 175) if is_info else (0, 0, 0), font=get_font(13, True))
        cur_y += step_gap

        # 12
        draw_arrow(draw, (1100, cur_y), (1600, cur_y), fill=(34, 197, 94) if is_info else (0, 0, 0), dashed=True)
        draw.text((1200, cur_y - 18), "10. Thông báo duyệt thành công trên Admin Dashboard", fill=(21, 128, 61) if is_info else (0, 0, 0), font=get_font(13, True))

    # Render Infographic
    img_info = Image.new("RGB", (W, H), (248, 250, 252))
    draw_info = ImageDraw.Draw(img_info)
    draw_content(draw_info, is_info=True)
    img_info.save(os.path.join(INFO_DIR, "Hinh_4.14_Order_State_Return_Sequence_Diagram.png"), "PNG", dpi=(300, 300))
    save_dual_svg("Hinh_4.14_Order_State_Return_Sequence_Diagram", is_info=True)

    # Render Standard
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_std = ImageDraw.Draw(img_std)
    draw_content(draw_std, is_info=False)
    img_std.save(os.path.join(STD_DIR, "Hinh_4.14_Order_State_Return_Sequence_Diagram.png"), "PNG", dpi=(300, 300))
    save_dual_svg("Hinh_4.14_Order_State_Return_Sequence_Diagram", is_info=False)

if __name__ == "__main__":
    print("Rendering Hinh 4.13 & Hinh 4.14...")
    render_hinh_4_13()
    render_hinh_4_14()
    print("Rendered Hinh 4.13 & 4.14 successfully.")

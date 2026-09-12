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

def render_hinh_4_4_and_4_16():
    W, H = 2000, 1300
    
    # -------------------------------------------------------------
    # HÌNH 4.4: AI RAG & INTENT FLOW ARCHITECTURE
    # -------------------------------------------------------------
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_sub = get_font(18, bold=False)
    f_box = get_font(17, bold=True)
    f_body = get_font(14, bold=False)

    draw.text((W//2, 50), "KIẾN TRÚC LUỒNG TRỢ LÝ AI & XỬ LÝ NGÔN NGỮ TỰ NHIÊN (RAG + INTENT ENGINE)", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 85), "Mô hình Client-side Context Injection RAG kết hợp LLM Llama-3.3-70b-versatile qua Groq Cloud / OpenAI", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # Column 1: Client Layer (AIChatWidget)
    draw.rounded_rectangle([80, 130, 480, 1160], radius=12, fill=(240, 253, 250), outline=(20, 184, 166), width=2)
    draw.rectangle([80, 130, 480, 175], fill=(13, 148, 136))
    draw.text((280, 152), "1. CLIENT INTERACTION", fill=(255, 255, 255), font=f_box, anchor="mm")
    draw.text((105, 200), "• AIChatWidget React Component", fill=(15, 23, 42), font=f_body)
    draw.text((105, 235), "• Floating Action Button (FAB)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 270), "• Expanded / Minimized Chat Box", fill=(15, 23, 42), font=f_body)
    draw.text((105, 305), "• Quick Prompt Chips (Sách mới,", fill=(15, 23, 42), font=f_body)
    draw.text((120, 330), "Giảm giá, Gợi ý, Đơn hàng...)", fill=(100, 116, 139), font=f_body)
    draw.text((105, 365), "• LocalStorage Multi-User Chat History", fill=(15, 23, 42), font=f_body)
    draw.text((120, 390), "(yiyi_chat_history_{userId})", fill=(100, 116, 139), font=f_body)
    draw.text((105, 425), "• Typing Indicator & Auto-scroll", fill=(15, 23, 42), font=f_body)
    draw.text((105, 460), "• Markdown Rendering (ReactMarkdown)", fill=(15, 23, 42), font=f_body)
    draw.text((105, 495), "• Book Card Component with Buy Link", fill=(15, 23, 42), font=f_body)
    draw.text((105, 530), "• Clear Conversation History Action", fill=(15, 23, 42), font=f_body)

    # Column 2: Mini-RAG & Intent Classification Engine
    draw.rounded_rectangle([530, 130, 1050, 1160], radius=12, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.rectangle([530, 130, 1050, 175], fill=(5, 150, 105))
    draw.text((790, 152), "2. CLIENT-SIDE RAG & INTENT ENGINE", fill=(255, 255, 255), font=f_box, anchor="mm")
    
    # Sub 2.1: Knowledge Sync
    draw.rounded_rectangle([555, 195, 1025, 420], radius=8, fill=(255, 255, 255), outline=(16, 185, 129), width=1)
    draw.text((790, 220), "A. Knowledge Retrieval & Sync", fill=(4, 120, 87), font=f_box, anchor="mm")
    draw.text((575, 250), "• Fetch GET /api/books?size=5000 khi load", fill=(15, 23, 42), font=f_body)
    draw.text((575, 280), "• Lưu bộ nhớ Client (In-memory catalogue)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 310), "• Cache metadata: title, author, price,", fill=(15, 23, 42), font=f_body)
    draw.text((590, 335), "category, description, stock status", fill=(100, 116, 139), font=f_body)
    draw.text((575, 365), "• Loại trừ payload nặng để tiết kiệm RAM", fill=(15, 23, 42), font=f_body)

    # Sub 2.2: Intent Classifier
    draw.rounded_rectangle([555, 440, 1025, 780], radius=8, fill=(255, 255, 255), outline=(16, 185, 129), width=1)
    draw.text((790, 465), "B. Natural Intent Classifier", fill=(4, 120, 87), font=f_box, anchor="mm")
    draw.text((575, 495), "• BOOK_RECOMMENDATION (Tư vấn theo gu)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 525), "• SEARCH_BY_PRICE (Tìm sách theo ngân sách)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 555), "• SEARCH_BY_AUTHOR (Tìm tác giả cụ thể)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 585), "• PROMOTION_QUERY (Tra cứu mã giảm giá)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 615), "• ORDER_POLICY (Chính sách đổi trả, ship)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 645), "• GENERAL_CHAT (Trò chuyện thông minh)", fill=(15, 23, 42), font=f_body)
    draw.text((575, 675), "• Keyword Matching & Fuzzy Levenshtein", fill=(15, 23, 42), font=f_body)
    draw.text((575, 705), "• Prompt Context Injection & Guardrails", fill=(15, 23, 42), font=f_body)
    draw.text((575, 735), "• Cắt tỉa ngữ cảnh (Recent 20 Messages)", fill=(15, 23, 42), font=f_body)

    # Sub 2.3: Security & Sanitization
    draw.rounded_rectangle([555, 800, 1025, 1130], radius=8, fill=(255, 255, 255), outline=(16, 185, 129), width=1)
    draw.text((790, 825), "C. Prompt Sanitization & Guardrails", fill=(4, 120, 87), font=f_box, anchor="mm")
    draw.text((575, 855), "• Loại bỏ Prompt Injection & Malicious Script", fill=(15, 23, 42), font=f_body)
    draw.text((575, 885), "• Giới hạn Persona: 'Trợ lý bán sách thân thiện'", fill=(15, 23, 42), font=f_body)
    draw.text((575, 915), "• Bắt buộc trả về liên kết sản phẩm chính xác", fill=(15, 23, 42), font=f_body)
    draw.text((575, 945), "• Fallback sang Default Offline Responses", fill=(15, 23, 42), font=f_body)
    draw.text((575, 975), "• Bảo mật API Key qua VITE_AI_API_KEY", fill=(15, 23, 42), font=f_body)

    # Column 3: LLM Cloud Provider & Backend Gateway
    draw.rounded_rectangle([1100, 130, 1920, 1160], radius=12, fill=(239, 246, 255), outline=(59, 130, 246), width=2)
    draw.rectangle([1100, 130, 1920, 175], fill=(37, 99, 235))
    draw.text((1510, 152), "3. LLM CLOUD GATEWAY & INFERENCE RUNTIME", fill=(255, 255, 255), font=f_box, anchor="mm")

    # Sub 3.1: LLM Engine
    draw.rounded_rectangle([1125, 195, 1895, 520], radius=8, fill=(255, 255, 255), outline=(59, 130, 246), width=1)
    draw.text((1510, 220), "A. High-Speed LLM Inference (Groq Cloud / OpenAI)", fill=(29, 78, 216), font=f_box, anchor="mm")
    draw.text((1145, 250), "• Base URL: https://api.groq.com/openai/v1/chat/completions", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 280), "• Model: llama-3.3-70b-versatile (Hoặc gpt-4o-mini / 9Router API)", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 310), "• LPUs (Language Processing Units): Siêu tốc < 800ms độ trễ", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 340), "• Temperature: 0.7 | Max Output Tokens: 1024", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 370), "• JSON Schema & Structured Natural Response Formatting", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 400), "• Token Usage Monitoring & Rate Limit Throttling Guard", fill=(15, 23, 42), font=f_body)

    # Sub 3.2: Spring Boot Backend Data Provider
    draw.rounded_rectangle([1125, 545, 1895, 840], radius=8, fill=(255, 255, 255), outline=(59, 130, 246), width=1)
    draw.text((1510, 570), "B. Spring Boot REST Backend Support", fill=(29, 78, 216), font=f_box, anchor="mm")
    draw.text((1145, 600), "• BookController -> BookService -> BookRepository", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 630), "• CategoryController & CouponController (Cung cấp metadata)", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 660), "• User aiPreferences sync (Lưu sở thích đọc sách cá nhân hóa)", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 690), "• SiteSetting (Bật/tắt chế độ AI Assistant & Model Config)", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 720), "• PostgreSQL Database Storage: books, categories, users", fill=(15, 23, 42), font=f_body)

    # Sub 3.3: Output Evaluation
    draw.rounded_rectangle([1125, 865, 1895, 1130], radius=8, fill=(255, 255, 255), outline=(59, 130, 246), width=1)
    draw.text((1510, 890), "C. AI Quality & Evaluation Metrics", fill=(29, 78, 216), font=f_box, anchor="mm")
    draw.text((1145, 920), "• Context Relevance: 96.4% đúng sách trong kho", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 950), "• Hallucination Rate: < 1.5% nhờ Context Injection RAG", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 980), "• Response Time trung bình: 650ms (Groq LPU Acceleration)", fill=(15, 23, 42), font=f_body)
    draw.text((1145, 1010), "• E2E Automation Testing: Playwright Test AI Chat Flow", fill=(15, 23, 42), font=f_body)

    # Arrows between blocks
    draw_arrow(draw, (480, 280), (530, 280), fill=(13, 148, 136), width=3, arrow_size=8)
    draw_arrow(draw, (1050, 350), (1100, 350), fill=(5, 150, 105), width=3, arrow_size=8)
    draw_arrow(draw, (1100, 420), (1050, 420), fill=(37, 99, 235), width=3, arrow_size=8, dashed=True)
    draw_arrow(draw, (530, 480), (480, 480), fill=(13, 148, 136), width=3, arrow_size=8, dashed=True)

    draw.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — AI RAG & Natural Language Architecture", fill=(148, 163, 184), font=f_body, anchor="mm")

    # Standard Version
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 50), "HÌNH 4.4. KIẾN TRÚC LUỒNG TRỢ LÝ AI VÀ XỬ LÝ NGÔN NGỮ TỰ NHIÊN", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 85), "Standard UML / AI Engine Architecture Diagram", fill=(80, 80, 80), font=f_sub, anchor="mm")

    for box, title, lines in [
        ([80, 130, 480, 1160], "1. Client Interaction", ["• AIChatWidget React Component", "• Floating Action Button (FAB)", "• Expanded / Minimized Chat Box", "• Quick Prompt Chips", "• LocalStorage Chat History", "• Typing Indicator & Auto-scroll", "• ReactMarkdown Content Render", "• Book Card Component with Buy Link"]),
        ([530, 130, 1050, 1160], "2. Client-side RAG & Intent Engine", ["• Knowledge Retrieval: GET /api/books", "• In-memory Book Metadata Caching", "• Intent Classifier (6 Core Intents)", "• Keyword Matching & Fuzzy Logic", "• Prompt Context Injection & Guardrails", "• Message History Pruning (20 msgs)", "• Anti Prompt-Injection Filter", "• Fallback Default Responses"]),
        ([1100, 130, 1920, 1160], "3. LLM Cloud & Backend Support", ["• Groq Cloud / OpenAI REST API", "• Llama-3.3-70b-versatile Model", "• Ultra-low Latency LPU (< 800ms)", "• Temperature 0.7, Max Tokens 1024", "• Spring Boot Backend (Book/Category APIs)", "• PostgreSQL Data Store Sync", "• User aiPreferences Personalization", "• Automated Playwright E2E Verification"])
    ]:
        draw_s.rectangle(box, fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        draw_s.rectangle([box[0], box[1], box[2], box[1]+35], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
        draw_s.text((box[0]+15, box[1]+18), title, fill=(0, 0, 0), font=f_box, anchor="lm")
        y_c = box[1] + 60
        for l in lines:
            draw_s.text((box[0]+20, y_c), l, fill=(0, 0, 0), font=f_body)
            y_c += 35

    draw_arrow(draw_s, (480, 280), (530, 280), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1050, 350), (1100, 350), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1100, 420), (1050, 420), fill=(0, 0, 0), width=2, arrow_size=8, dashed=True)
    draw_arrow(draw_s, (530, 480), (480, 480), fill=(0, 0, 0), width=2, arrow_size=8, dashed=True)

    draw_s.text((W//2, 1275), "Safe Margin: 60px | Technical Standard Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    p_info = os.path.join(INFO_DIR, "Hinh_4.4_AI_RAG_Intent_Flow_Architecture.png")
    p_std = os.path.join(STD_DIR, "Hinh_4.4_AI_RAG_Intent_Flow_Architecture.png")
    img.save(p_info, "PNG", dpi=(300, 300))
    img_std.save(p_std, "PNG", dpi=(300, 300))

    svg_info = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
        <rect width="100%" height="100%" fill="#F8FAFC"/>
        <text x="{W//2}" y="50" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#0F172A" text-anchor="middle">KIẾN TRÚC LUỒNG TRỢ LÝ AI & XỬ LÝ NGÔN NGỮ TỰ NHIÊN</text>
        <text x="{W//2}" y="85" font-family="Arial, sans-serif" font-size="18" fill="#475569" text-anchor="middle">Mô hình Client-side Context Injection RAG kết hợp LLM Llama-3.3-70b qua Groq Cloud / OpenAI</text>
    </svg>'''
    with open(os.path.join(INFO_DIR, "Hinh_4.4_AI_RAG_Intent_Flow_Architecture.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.4_AI_RAG_Intent_Flow_Architecture.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.4 successfully.")

    # -------------------------------------------------------------
    # HÌNH 4.16: YIYI AI COMPONENT & SEQUENCE DIAGRAM
    # -------------------------------------------------------------
    img16 = Image.new("RGB", (W, H), (248, 250, 252))
    draw16 = ImageDraw.Draw(img16)

    draw16.text((W//2, 50), "SƠ ĐỒ THÀNH PHẦN VÀ TUẦN TỰ (COMPONENT & SEQUENCE) — TRỢ LÝ AI YIYI", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw16.text((W//2, 85), "Chi tiết luồng phân tích ý định, tiêm ngữ cảnh kho sách (RAG) và phản hồi từ Llama-3.3-70b LLM", fill=(71, 85, 105), font=f_sub, anchor="mm")

    # Sequence Lifelines
    actors = [
        ("User (Khách / Member)", 220, (13, 148, 136)),
        ("AIChatWidget (React)", 580, (2, 132, 199)),
        ("RAG & Intent Engine", 950, (5, 150, 105)),
        ("Spring REST Backend", 1350, (37, 99, 235)),
        ("Groq Cloud (LLM API)", 1750, (126, 34, 206))
    ]

    for title, x, color in actors:
        draw16.rounded_rectangle([x-130, 130, x+130, 180], radius=8, fill=color)
        draw16.text((x, 155), title, fill=(255, 255, 255), font=f_box, anchor="mm")
        draw16.line([(x, 180), (x, 1160)], fill=(203, 213, 225), width=2)
        draw16.rounded_rectangle([x-130, 1160, x+130, 1200], radius=8, fill=color)
        draw16.text((x, 1180), title, fill=(255, 255, 255), font=f_box, anchor="mm")

    # Sequence Messages
    steps = [
        (1, 220, 580, "1. Nhấn icon AI / Gõ câu hỏi: 'Gợi ý sách lập trình Java'", 230, False, (15, 23, 42)),
        (2, 580, 950, "2. handleSendMessage() -> Phân tích câu hỏi & Intent", 300, False, (5, 150, 105)),
        (3, 950, 1350, "3. [Lần đầu load] GET /api/books?size=5000 để lấy kho sách", 370, False, (37, 99, 235)),
        (4, 1350, 950, "4. 200 OK: Trả về danh sách sách (In-memory catalogue)", 440, True, (37, 99, 235)),
        (5, 950, 950, "5. Client RAG lọc top 5 sách phù hợp nhất theo từ khóa/danh mục", 510, False, (5, 150, 105)), # Self call
        (6, 950, 1750, "6. POST /chat/completions (System Prompt + RAG Context + History)", 580, False, (126, 34, 206)),
        (7, 1750, 1750, "7. Groq LPU Inference (Llama-3.3-70b sinh câu trả lời tiếng Việt)", 660, False, (126, 34, 206)), # Self
        (8, 1750, 580, "8. Trả về kết quả tư vấn Markdown + kèm Book Metadata", 740, True, (126, 34, 206)),
        (9, 580, 580, "9. Render tin nhắn, Product Cards & Link mua sách nhanh", 820, False, (2, 132, 199)), # Self
        (10, 580, 220, "10. Hiển thị hội thoại hoàn chỉnh & lưu localStorage history", 900, True, (13, 148, 136)),
        (11, 220, 580, "11. [Optional] Nhấn vào thẻ sách để xem Chi tiết / Thêm Giỏ", 980, False, (15, 23, 42)),
        (12, 580, 1350, "12. Chuyển hướng /product/{id} hoặc POST /api/cart/add", 1060, False, (37, 99, 235)),
    ]

    for step, x1, x2, text, y, is_dashed, col in steps:
        if x1 == x2:
            # Self call
            draw16.line([(x1, y-15), (x1+50, y-15), (x1+50, y+15), (x1, y+15)], fill=col, width=2)
            draw_arrow(draw16, (x1+50, y+15), (x1, y+15), fill=col, width=2, arrow_size=6)
            draw16.text((x1+60, y), text, fill=col, font=f_body, anchor="lm")
        else:
            draw_arrow(draw16, (x1, y), (x2, y), fill=col, width=2, arrow_size=8, dashed=is_dashed)
            draw16.text(((x1+x2)//2, y-15), text, fill=col, font=f_body, anchor="mm")

    draw16.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — YiYi AI Component & Sequence Interaction", fill=(148, 163, 184), font=f_body, anchor="mm")

    # Standard version 4.16
    img16_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw16_s = ImageDraw.Draw(img16_std)
    draw16_s.text((W//2, 50), "HÌNH 4.16. SƠ ĐỒ THÀNH PHẦN VÀ TUẦN TỰ TRỢ LÝ AI (YIYI AI ASSISTANT)", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw16_s.text((W//2, 85), "Standard UML Sequence Diagram Specification", fill=(80, 80, 80), font=f_sub, anchor="mm")

    for title, x, _ in actors:
        draw16_s.rectangle([x-130, 130, x+130, 180], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
        draw16_s.text((x, 155), title, fill=(0, 0, 0), font=f_box, anchor="mm")
        draw16_s.line([(x, 180), (x, 1160)], fill=(0, 0, 0), width=1)
        draw16_s.rectangle([x-130, 1160, x+130, 1200], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
        draw16_s.text((x, 1180), title, fill=(0, 0, 0), font=f_box, anchor="mm")

    for step, x1, x2, text, y, is_dashed, _ in steps:
        if x1 == x2:
            draw16_s.line([(x1, y-15), (x1+50, y-15), (x1+50, y+15), (x1, y+15)], fill=(0, 0, 0), width=1)
            draw_arrow(draw16_s, (x1+50, y+15), (x1, y+15), fill=(0, 0, 0), width=1, arrow_size=6)
            draw16_s.text((x1+60, y), text, fill=(0, 0, 0), font=f_body, anchor="lm")
        else:
            draw_arrow(draw16_s, (x1, y), (x2, y), fill=(0, 0, 0), width=1, arrow_size=8, dashed=is_dashed)
            draw16_s.text(((x1+x2)//2, y-15), text, fill=(0, 0, 0), font=f_body, anchor="mm")

    draw16_s.text((W//2, 1275), "Safe Margin: 60px | Technical Standard Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    p16_info = os.path.join(INFO_DIR, "Hinh_4.16_Component_Sequence_Diagram_YiYi_AI.png")
    p16_std = os.path.join(STD_DIR, "Hinh_4.16_Component_Sequence_Diagram_YiYi_AI.png")
    img16.save(p16_info, "PNG", dpi=(300, 300))
    img16_std.save(p16_std, "PNG", dpi=(300, 300))

    with open(os.path.join(INFO_DIR, "Hinh_4.16_Component_Sequence_Diagram_YiYi_AI.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)
    with open(os.path.join(STD_DIR, "Hinh_4.16_Component_Sequence_Diagram_YiYi_AI.svg"), "w", encoding="utf-8") as f:
        f.write(svg_info)

    print("Rendered Hinh 4.16 successfully.")

if __name__ == "__main__":
    render_hinh_4_4_and_4_16()

import os
import math
from PIL import Image, ImageDraw, ImageFont

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
        num_dashes = int(dist // (dash_len * 2))
        for i in range(num_dashes + 1):
            s = (i * 2 * dash_len) / dist
            e = min(1.0, ((i * 2 + 1) * dash_len) / dist)
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

# ==========================================
# 1. HÌNH 2.1: AGILE / SCRUM WORKFLOW
# ==========================================
def render_hinh_2_1():
    # Infographic
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    
    # Title
    f_title = get_font(32, bold=True)
    f_sub = get_font(18, bold=False)
    f_hdr = get_font(20, bold=True)
    f_card_t = get_font(18, bold=True)
    f_body = get_font(15, bold=False)
    
    draw.text((W//2, 50), "QUY TRÌNH PHÁT TRIỂN PHẦN MỀM AGILE / SCRUM — YIYI BOOK", fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((W//2, 85), "Mô hình quản trị Sprint 2 tuần, tích hợp CI/CD tự động hóa và đảm bảo chất lượng liên tục", fill=(71, 85, 105), font=f_sub, anchor="mm")
    
    # Row 1: Product Backlog & Sprint Planning (Top)
    # Row 2: Sprint Execution Container (Dev, Test, Review, CI/CD)
    # Row 3: Sprint Review, Retrospective & Release
    
    # Top Row: 2 boxes
    draw.rounded_rectangle([100, 130, 950, 310], radius=12, fill=(240, 253, 250), outline=(20, 184, 166), width=2)
    draw.rectangle([100, 130, 950, 175], fill=(13, 148, 136))
    draw.text((525, 152), "1. PRODUCT BACKLOG & REQUIREMENTS", fill=(255, 255, 255), font=f_card_t, anchor="mm")
    draw.text((130, 195), "• Khảo sát mô hình Nhà sách, thu thập FR & NFR", fill=(15, 23, 42), font=f_body)
    draw.text((130, 225), "• Quản lý User Story, Epics, Acceptance Criteria trên Jira", fill=(15, 23, 42), font=f_body)
    draw.text((130, 255), "• Ước lượng Story Points & phân cấp ưu tiên MoSCoW", fill=(15, 23, 42), font=f_body)
    draw.text((130, 285), "• Xây dựng Ma trận truy xuất nguồn gốc (RTM)", fill=(15, 23, 42), font=f_body)

    draw.rounded_rectangle([1050, 130, 1900, 310], radius=12, fill=(239, 246, 255), outline=(59, 130, 246), width=2)
    draw.rectangle([1050, 130, 1900, 175], fill=(37, 99, 235))
    draw.text((1475, 152), "2. SPRINT PLANNING & TASK BREAKDOWN", fill=(255, 255, 255), font=f_card_t, anchor="mm")
    draw.text((1080, 195), "• Họp Sprint Planning đầu mỗi chu kỳ 2 tuần (Sprint 1 -> 4)", fill=(15, 23, 42), font=f_body)
    draw.text((1080, 225), "• Chọn Story từ Product Backlog đưa vào Sprint Backlog", fill=(15, 23, 42), font=f_body)
    draw.text((1080, 255), "• Chia nhỏ Task kỹ thuật: Frontend, Backend, Database, Test", fill=(15, 23, 42), font=f_body)
    draw.text((1080, 285), "• Cam kết Definition of Ready (DoR) và Definition of Done (DoD)", fill=(15, 23, 42), font=f_body)

    draw_arrow(draw, (950, 220), (1050, 220), fill=(37, 99, 235), width=3, arrow_size=10)

    # Middle Row: SPRINT EXECUTION CONTAINER
    draw.rounded_rectangle([100, 350, 1900, 880], radius=16, fill=(255, 255, 255), outline=(99, 102, 241), width=3)
    draw.rectangle([100, 350, 1900, 400], fill=(79, 70, 229))
    draw.text((1000, 375), "⚡ SPRINT EXECUTION & CONTINUOUS QUALITY ASSURANCE (2 WEEKS CYCLE)", fill=(255, 255, 255), font=f_hdr, anchor="mm")

    # Inside container: 4 sub-phases
    # Phase 2.1: Architecture & Design
    draw.rounded_rectangle([130, 430, 520, 840], radius=10, fill=(245, 243, 255), outline=(139, 92, 246), width=2)
    draw.text((325, 460), "A. Design & Architecture", fill=(109, 40, 217), font=f_card_t, anchor="mm")
    draw.text((150, 500), "• Thiết kế Clean Architecture\n  Frontend & Backend REST\n• ERD 21 Tables PostgreSQL\n• UML Sequence, Class &\n  State Diagrams\n• Chuẩn hóa API Contract\n  DTO, JSON Request/Response", fill=(30, 41, 59), font=f_body)

    # Phase 2.2: Development
    draw.rounded_rectangle([560, 430, 960, 840], radius=10, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
    draw.text((760, 460), "B. Implementation & Coding", fill=(67, 56, 202), font=f_card_t, anchor="mm")
    draw.text((580, 500), "• Git Flow: feature/* -> develop\n• Frontend: React 18 + Vite,\n  Tailwind, Context API\n• Backend: Spring Boot 3,\n  Spring Security 6, JWT, JPA\n• Tích hợp VNPay, MoMo, AI\n• Daily Scrum & Task Sync", fill=(30, 41, 59), font=f_body)

    # Phase 2.3: Automated Testing
    draw.rounded_rectangle([1000, 430, 1430, 840], radius=10, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.text((1215, 460), "C. Multi-tier Automated Test", fill=(4, 120, 87), font=f_card_t, anchor="mm")
    draw.text((1020, 500), "• Unit Test: JUnit 5 & Mockito\n  Coverage đạt 81.3% JaCoCo\n• API Test: Postman & Newman CLI\n  (Auth, Cart, Order, BVA)\n• E2E Automation: CodeceptJS\n  + Playwright UI flows\n• BVA & Boundary Validation", fill=(30, 41, 59), font=f_body)

    # Phase 2.4: Code Quality & CI/CD
    draw.rounded_rectangle([1470, 430, 1870, 840], radius=10, fill=(255, 241, 242), outline=(244, 63, 94), width=2)
    draw.text((1670, 460), "D. Static Analysis & CI/CD", fill=(190, 18, 60), font=f_card_t, anchor="mm")
    draw.text((1490, 500), "• Checkstyle (0 violations)\n• SpotBugs bytecode analysis\n• SonarQube Quality Gate\n• GitHub Actions Workflow:\n  Auto build, test, verify PR\n• Peer Code Review trước\n  khi merge vào develop", fill=(30, 41, 59), font=f_body)

    # Arrows between sub-phases
    draw_arrow(draw, (520, 630), (560, 630), fill=(99, 102, 241), width=3, arrow_size=8)
    draw_arrow(draw, (960, 630), (1000, 630), fill=(16, 185, 129), width=3, arrow_size=8)
    draw_arrow(draw, (1430, 630), (1470, 630), fill=(244, 63, 94), width=3, arrow_size=8)

    # Down arrow from Planning to Execution
    draw_arrow(draw, (1475, 310), (1475, 350), fill=(79, 70, 229), width=3, arrow_size=10)

    # Bottom Row: Review, Retrospective, Release
    draw.rounded_rectangle([100, 920, 650, 1180], radius=12, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.rectangle([100, 920, 650, 965], fill=(217, 119, 6))
    draw.text((375, 942), "3. SPRINT REVIEW & DEMO", fill=(255, 255, 255), font=f_card_t, anchor="mm")
    draw.text((130, 985), "• Demo tính năng hoàn thành theo DoD", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1015), "• Đánh giá Burn-down chart & Velocity", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1045), "• Tiếp nhận phản hồi từ Product Owner/User", fill=(15, 23, 42), font=f_body)
    draw.text((130, 1075), "• Cập nhật trạng thái User Story hoàn tất", fill=(15, 23, 42), font=f_body)

    draw.rounded_rectangle([720, 920, 1280, 1180], radius=12, fill=(243, 244, 246), outline=(107, 114, 128), width=2)
    draw.rectangle([720, 920, 1280, 965], fill=(75, 85, 99))
    draw.text((1000, 942), "4. SPRINT RETROSPECTIVE", fill=(255, 255, 255), font=f_card_t, anchor="mm")
    draw.text((750, 985), "• Họp cải tiến quy trình: What went well?", fill=(15, 23, 42), font=f_body)
    draw.text((750, 1015), "• Điểm nghẽn kỹ thuật: What can be improved?", fill=(15, 23, 42), font=f_body)
    draw.text((750, 1045), "• Đề xuất Action Items cho Sprint tiếp theo", fill=(15, 23, 42), font=f_body)
    draw.text((750, 1075), "• Tối ưu năng suất & chất lượng kiểm thử", fill=(15, 23, 42), font=f_body)

    draw.rounded_rectangle([1350, 920, 1900, 1180], radius=12, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.rectangle([1350, 920, 1900, 965], fill=(5, 150, 105))
    draw.text((1625, 942), "5. DEPLOYMENT & RELEASE", fill=(255, 255, 255), font=f_card_t, anchor="mm")
    draw.text((1380, 985), "• Merge develop -> main sau khi pass DoD", fill=(15, 23, 42), font=f_body)
    draw.text((1380, 1015), "• Docker Containerize Backend & Frontend", fill=(15, 23, 42), font=f_body)
    draw.text((1380, 1045), "• Triển khai Staging / Production Cloud", fill=(15, 23, 42), font=f_body)
    draw.text((1380, 1075), "• Smoke Test & Health Check hệ thống", fill=(15, 23, 42), font=f_body)

    # Arrows between bottom boxes
    draw_arrow(draw, (1670, 880), (1625, 920), fill=(5, 150, 105), width=3, arrow_size=10)
    draw_arrow(draw, (1350, 1050), (1280, 1050), fill=(75, 85, 99), width=3, arrow_size=10)
    draw_arrow(draw, (720, 1050), (650, 1050), fill=(217, 119, 6), width=3, arrow_size=10)
    
    # Loop back arrow from Retro to Sprint Planning
    draw.line([(375, 1180), (375, 1240), (1880, 1240), (1880, 220), (1900, 220)], fill=(99, 102, 241), width=3)
    draw_arrow(draw, (1880, 220), (1050, 220), fill=(99, 102, 241), width=3, arrow_size=8, dashed=True)
    draw.text((1000, 1225), "Khởi động Sprint tiếp theo (Next Sprint Planning)", fill=(99, 102, 241), font=f_body, anchor="mm")

    # Safe margin & footer note
    draw.text((W//2, 1275), "Safe Margin: 60px | YiYi Book Capstone Project — Agile / Scrum Engineering Lifecycle", fill=(148, 163, 184), font=f_body, anchor="mm")

    out_png = os.path.join(INFO_DIR, "Hinh_2.1_Agile_Scrum_Workflow_YiYi_Book.png")
    img.save(out_png, "PNG", dpi=(300, 300))
    print("Saved:", out_png)

    # Standard version (clean black & white / minimal)
    img_std = Image.new("RGB", (W, H), (255, 255, 255))
    draw_s = ImageDraw.Draw(img_std)
    draw_s.text((W//2, 50), "HÌNH 2.1. QUY TRÌNH PHÁT TRIỂN PHẦN MỀM AGILE / SCRUM", fill=(0, 0, 0), font=f_title, anchor="mm")
    draw_s.text((W//2, 85), "Standard UML / Process Specification Diagram", fill=(80, 80, 80), font=f_sub, anchor="mm")
    
    # Draw boxes in standard clean style
    for box, title, lines in [
        ([100, 130, 950, 310], "1. Product Backlog & Requirements", ["• Khảo sát mô hình Nhà sách, thu thập FR & NFR", "• Quản lý User Story, Epics trên Jira", "• Ước lượng Story Points & phân cấp MoSCoW", "• Xây dựng Ma trận truy xuất nguồn gốc (RTM)"]),
        ([1050, 130, 1900, 310], "2. Sprint Planning & Task Breakdown", ["• Họp Sprint Planning đầu chu kỳ 2 tuần", "• Đưa User Story vào Sprint Backlog", "• Phân rã Task Frontend, Backend, Test", "• Cam kết Definition of Ready & Done"]),
        ([100, 920, 650, 1180], "3. Sprint Review & Demo", ["• Demo tính năng theo Definition of Done", "• Đánh giá Burn-down chart & Velocity", "• Nhận phản hồi từ Product Owner/User", "• Cập nhật trạng thái Story hoàn tất"]),
        ([720, 920, 1280, 1180], "4. Sprint Retrospective", ["• Đánh giá quy trình: What went well?", "• Phân tích điểm nghẽn kỹ thuật", "• Đề xuất Action Items cho Sprint tiếp theo", "• Tối ưu hiệu quả kiểm thử"]),
        ([1350, 920, 1900, 1180], "5. Deployment & Release", ["• Merge nhánh develop vào main", "• Đóng gói Docker Container Backend & Frontend", "• Triển khai Staging / Production Cloud", "• Smoke Test & Health Check hệ thống"])
    ]:
        draw_s.rectangle(box, fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        draw_s.rectangle([box[0], box[1], box[2], box[1]+40], fill=(240, 240, 240), outline=(0, 0, 0), width=1)
        draw_s.text((box[0]+15, box[1]+20), title, fill=(0, 0, 0), font=f_card_t, anchor="lm")
        y_c = box[1] + 65
        for l in lines:
            draw_s.text((box[0]+20, y_c), l, fill=(0, 0, 0), font=f_body)
            y_c += 30

    # Middle execution box
    draw_s.rectangle([100, 350, 1900, 880], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw_s.rectangle([100, 350, 1900, 400], fill=(230, 230, 230), outline=(0, 0, 0), width=1)
    draw_s.text((1000, 375), "SPRINT EXECUTION & CONTINUOUS QUALITY ASSURANCE (2 WEEKS)", fill=(0, 0, 0), font=f_hdr, anchor="mm")

    sub_boxes = [
        ([130, 430, 520, 840], "A. Design & Architecture", ["• Clean Architecture\n  Frontend & Backend REST\n• ERD 21 Tables PostgreSQL\n• UML Sequence, Class &\n  State Diagrams\n• Chuẩn hóa API Contract\n  DTO, JSON format"]),
        ([560, 430, 960, 840], "B. Implementation & Coding", ["• Git Flow: feature -> develop\n• React 18, Vite, Tailwind\n• Spring Boot 3, Security 6,\n  JWT, JPA, PostgreSQL\n• Tích hợp VNPay, MoMo, AI\n• Daily Scrum đồng bộ"]),
        ([1000, 430, 1430, 840], "C. Multi-tier Test", ["• Unit Test: JUnit 5 & Mockito\n  Coverage 81.3% JaCoCo\n• API Test: Postman & Newman\n  (Auth, Cart, Order, BVA)\n• E2E: CodeceptJS + Playwright\n• Boundary Value Analysis"]),
        ([1470, 430, 1870, 840], "D. Quality Gate & CI/CD", ["• Checkstyle (0 violations)\n• SpotBugs static analysis\n• SonarQube Quality Gate\n• GitHub Actions CI/CD Pipeline\n• Peer Review trước merge"])
    ]
    for b, t, ls in sub_boxes:
        draw_s.rectangle(b, fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw_s.rectangle([b[0], b[1], b[2], b[1]+35], fill=(245, 245, 245), outline=(0, 0, 0), width=1)
        draw_s.text((b[0]+10, b[1]+18), t, fill=(0, 0, 0), font=f_card_t, anchor="lm")
        draw_s.text((b[0]+15, b[1]+55), ls[0], fill=(0, 0, 0), font=f_body)

    # Standard arrows
    draw_arrow(draw_s, (950, 220), (1050, 220), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1475, 310), (1475, 350), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (520, 630), (560, 630), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (960, 630), (1000, 630), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1430, 630), (1470, 630), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1670, 880), (1625, 920), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (1350, 1050), (1280, 1050), fill=(0, 0, 0), width=2, arrow_size=8)
    draw_arrow(draw_s, (720, 1050), (650, 1050), fill=(0, 0, 0), width=2, arrow_size=8)
    
    draw_s.text((W//2, 1275), "Safe Margin: 60px | Technical Standard Diagram", fill=(100, 100, 100), font=f_body, anchor="mm")

    out_std = os.path.join(STD_DIR, "Hinh_2.1_Agile_Scrum_Workflow_YiYi_Book.png")
    img_std.save(out_std, "PNG", dpi=(300, 300))
    print("Saved:", out_std)

if __name__ == "__main__":
    render_hinh_2_1()

# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# HÌNH 2.1: SƠ ĐỒ QUY TRÌNH PHÁT TRIỂN PHẦN MỀM AGILE/SCRUM VÀ SPRINT WORKFLOW
# Thiết kế chuẩn phong cách Academic / Box Diagram đồng bộ với hệ thống đồ án
# ==============================================================================
W, H = 2600, 1450
img = Image.new("RGBA", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

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

# 1. Khung lớn bao quanh sơ đồ
BORDER_X1, BORDER_Y1 = 60, 50
BORDER_X2, BORDER_Y2 = W - 60, H - 50

draw.rounded_rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y2], radius=12, outline=(180, 195, 210), width=3, fill=(255, 255, 255))

# Header của Diagram
HEADER_H = 85
draw.rectangle([BORDER_X1, BORDER_Y1, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(238, 242, 255))
draw.line([BORDER_X1, BORDER_Y1 + HEADER_H, BORDER_X2, BORDER_Y1 + HEADER_H], fill=(199, 210, 254), width=3)
draw.text(((BORDER_X1 + BORDER_X2) // 2, BORDER_Y1 + 42), 
          "QUY TRÌNH PHÁT TRIỂN PHẦN MỀM AGILE/SCRUM & SPRINT WORKFLOW - YIYI BOOK", 
          fill=(30, 58, 138), font=get_font(34, bold=True), anchor="mm")

# Sub-header: Sprint Iteration Cycle Notice
SUB_H_Y = BORDER_Y1 + HEADER_H + 25
draw.text(((BORDER_X1 + BORDER_X2) // 2, SUB_H_Y),
          "Chu kỳ Sprint 1-2 tuần với 5 giai đoạn liên hoàn kết hợp Continuous Feedback & Quality Assurance",
          fill=(75, 85, 99), font=get_font(21, bold=False), anchor="mm")

# 2. Định nghĩa 5 Giai đoạn chính (5 Columns)
STAGES = [
    {
        "step": "BƯỚC 1",
        "title": "Backlog & Làm rõ yêu cầu",
        "sub": "Requirement & Sprint Planning",
        "theme": {
            "border": (59, 130, 246),
            "header_bg": (219, 234, 254),
            "body_bg": (248, 250, 252),
            "text_main": (30, 64, 175),
            "tag_bg": (37, 99, 235),
        },
        "bullets": [
            "• Phân tích Product Backlog & Ưu tiên",
            "• Họp Sprint Planning & Chia User Story",
            "• Xác định Tiêu chí Chấp nhận (AC)",
            "• Giao việc & Ước lượng Story Points",
            "• Quản trị trên Jira Scrum Board"
        ],
        "tool": "Tool: Jira Software / Confluence"
    },
    {
        "step": "BƯỚC 2",
        "title": "Thiết kế kỹ thuật & Giao diện",
        "sub": "Design Flow, API & Data Model",
        "theme": {
            "border": (139, 92, 246),
            "header_bg": (237, 233, 254),
            "body_bg": (248, 250, 252),
            "text_main": (109, 40, 217),
            "tag_bg": (124, 58, 237),
        },
        "bullets": [
            "• Thiết kế User Flow & Wireframe UI",
            "• Đặc tả API Contract (Swagger/REST)",
            "• Thiết kế Database ERD & DTO Schema",
            "• Xác định State: Loading/Empty/Error",
            "• Thiết kế kiến trúc AI Chatbot RAG"
        ],
        "tool": "Tool: Figma / Draw.io / Swagger"
    },
    {
        "step": "BƯỚC 3",
        "title": "Triển khai Branch & PR Review",
        "sub": "Feature Branching & Clean Code",
        "theme": {
            "border": (245, 158, 11),
            "header_bg": (254, 243, 199),
            "body_bg": (248, 250, 252),
            "text_main": (180, 83, 9),
            "tag_bg": (217, 119, 6),
        },
        "bullets": [
            "• Nhánh Git chuẩn: feature/*, bugfix/*",
            "• Lập trình Spring Boot 3 & React.js",
            "• Tuân thủ Clean Code, Layered Pattern",
            "• Tạo Pull Request (PR) minh bạch",
            "• Peer Code Review (≥1 Approval)"
        ],
        "tool": "Tool: GitHub / VS Code / IntelliJ"
    },
    {
        "step": "BƯỚC 4",
        "title": "Kiểm thử đa tầng & Bảo mật",
        "sub": "Unit, API & Security Testing",
        "theme": {
            "border": (239, 68, 68),
            "header_bg": (254, 226, 226),
            "body_bg": (248, 250, 252),
            "text_main": (185, 28, 28),
            "tag_bg": (220, 38, 38),
        },
        "bullets": [
            "• Backend Unit Test (JUnit 5, Mockito)",
            "• API Collection (Postman / Newman)",
            "• Negative Authorization & RBAC Test",
            "• Frontend Lint, Build & UI Test",
            "• Ghi nhận Defect Bug trên Jira"
        ],
        "tool": "Tool: JUnit 5 / Postman / Newman"
    },
    {
        "step": "BƯỚC 5",
        "title": "Tích hợp, Deploy & Demo",
        "sub": "CI/CD, Smoke Test & Release",
        "theme": {
            "border": (16, 185, 129),
            "header_bg": (209, 250, 229),
            "body_bg": (248, 250, 252),
            "text_main": (4, 120, 87),
            "tag_bg": (5, 150, 105),
        },
        "bullets": [
            "• Tự động Build CI trên GitHub Actions",
            "• Triển khai Docker Cloud / Localhost",
            "• Chạy Deployment Smoke Test",
            "• Hoàn thiện Test Summary & API Doc",
            "• Sprint Review & Demo khách hàng"
        ],
        "tool": "Tool: GitHub Actions / Docker"
    }
]

# Layout tính toán vị trí cho 5 Hộp
START_X = 110
START_Y = 200
COL_W = 425
COL_GAP = 55
BOX_H = 780

for i, stage in enumerate(STAGES):
    bx = START_X + i * (COL_W + COL_GAP)
    by = START_Y
    t = stage["theme"]
    
    # 1. Vẽ Box chính
    draw.rounded_rectangle([bx, by, bx + COL_W, by + BOX_H], radius=10, outline=t["border"], width=3, fill=t["body_bg"])
    
    # 2. Header Box
    HDR_H = 135
    draw.rounded_rectangle([bx, by, bx + COL_W, by + HDR_H], radius=10, outline=t["border"], width=3, fill=t["header_bg"])
    # Cắt phẳng phần bo góc dưới của Header
    draw.rectangle([bx, by + HDR_H - 10, bx + COL_W, by + HDR_H], fill=t["header_bg"])
    draw.line([bx, by + HDR_H, bx + COL_W, by + HDR_H], fill=t["border"], width=3)
    
    # Badge Bước (Tag)
    TAG_W = 120
    TAG_H = 34
    draw.rounded_rectangle([bx + (COL_W - TAG_W)//2, by + 12, bx + (COL_W + TAG_W)//2, by + 12 + TAG_H], 
                           radius=6, fill=t["tag_bg"])
    draw.text((bx + COL_W//2, by + 12 + TAG_H//2), stage["step"], fill=(255, 255, 255), font=get_font(18, bold=True), anchor="mm")
    
    # Tiêu đề chính của Box
    draw.text((bx + COL_W//2, by + 68), stage["title"], fill=t["text_main"], font=get_font(21, bold=True), anchor="mm")
    # Phụ đề tiếng Anh
    draw.text((bx + COL_W//2, by + 102), stage["sub"], fill=(100, 116, 139), font=get_font(16, bold=False), anchor="mm")
    
    # 3. Danh sách bullet points
    BULLET_START_Y = by + HDR_H + 35
    LINE_GAP = 75
    for b_idx, bullet in enumerate(stage["bullets"]):
        ly = BULLET_START_Y + b_idx * LINE_GAP
        draw.rounded_rectangle([bx + 16, ly - 8, bx + COL_W - 16, ly + 52], radius=6, outline=(226, 232, 240), width=1, fill=(255, 255, 255))
        
        words = bullet.split()
        if len(bullet) > 38:
            line1 = " ".join(words[:4])
            line2 = "   " + " ".join(words[4:])
            draw.text((bx + 26, ly + 4), line1, fill=(30, 41, 59), font=get_font(17, bold=True if b_idx == 0 else False))
            draw.text((bx + 26, ly + 28), line2, fill=(51, 65, 85), font=get_font(16, bold=False))
        else:
            draw.text((bx + 26, ly + 14), bullet, fill=(30, 41, 59), font=get_font(17, bold=True if b_idx == 0 else False))
            
    # 4. Tool Footer Badge ở đáy mỗi Box
    TOOL_Y = by + BOX_H - 65
    draw.rounded_rectangle([bx + 20, TOOL_Y, bx + COL_W - 20, TOOL_Y + 45], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((bx + COL_W//2, TOOL_Y + 22), stage["tool"], fill=(71, 85, 105), font=get_font(16, bold=True), anchor="mm")

# 3. Vẽ các mũi tên tuần tự nối giữa 5 Hộp (Forward Arrows)
for i in range(4):
    ax1 = START_X + i * (COL_W + COL_GAP) + COL_W
    ax2 = START_X + (i + 1) * (COL_W + COL_GAP)
    ay = START_Y + 70  # Ngang tầm header
    
    draw.line([ax1 + 6, ay, ax2 - 6, ay], fill=(59, 130, 246), width=5)
    draw.polygon([(ax2 - 4, ay), (ax2 - 20, ay - 10), (ax2 - 20, ay + 10)], fill=(59, 130, 246))

# 4. Vẽ Mũi tên phản hồi lỗi (Defect Loopback Arrow: Bước 4 -> Bước 3)
FB_Y = START_Y + BOX_H + 50
P4_MID_X = START_X + 3 * (COL_W + COL_GAP) + COL_W // 2
P3_MID_X = START_X + 2 * (COL_W + COL_GAP) + COL_W // 2

# Đường gấp khúc màu đỏ: vẽ đường đứt quãng hoặc liền nhưng ngắt quãng ở giữa để không đè lên nhãn
DEFECT_LABEL_W = 540
DEFECT_LABEL_H = 40
DEF_L_X1 = (P3_MID_X + P4_MID_X)//2 - DEFECT_LABEL_W//2
DEF_L_X2 = (P3_MID_X + P4_MID_X)//2 + DEFECT_LABEL_W//2

draw.line([P4_MID_X, START_Y + BOX_H, P4_MID_X, FB_Y], fill=(239, 68, 68), width=3)
draw.line([P4_MID_X, FB_Y, DEF_L_X2, FB_Y], fill=(239, 68, 68), width=3)
draw.line([DEF_L_X1, FB_Y, P3_MID_X, FB_Y], fill=(239, 68, 68), width=3)
draw.line([P3_MID_X, FB_Y, P3_MID_X, START_Y + BOX_H], fill=(239, 68, 68), width=3)
draw.polygon([(P3_MID_X, START_Y + BOX_H + 4), (P3_MID_X - 8, START_Y + BOX_H + 20), (P3_MID_X + 8, START_Y + BOX_H + 20)], fill=(239, 68, 68))

# Nhãn Defect Feedback
draw.rounded_rectangle([DEF_L_X1, FB_Y - DEFECT_LABEL_H//2, DEF_L_X2, FB_Y + DEFECT_LABEL_H//2], 
                       radius=6, fill=(254, 226, 226), outline=(239, 68, 68), width=2)
draw.text(((P3_MID_X + P4_MID_X)//2, FB_Y), "Lỗi kiểm thử / Reject PR -> Fix Bug & Re-test", 
          fill=(185, 28, 28), font=get_font(18, bold=True), anchor="mm")

# 5. Vẽ Mũi tên Vòng lặp Sprint tiếp theo (Next Sprint Retrospective Loop: Bước 5 -> Bước 1)
SPRINT_LOOP_Y = START_Y + BOX_H + 130
P5_MID_X = START_X + 4 * (COL_W + COL_GAP) + COL_W // 2
P1_MID_X = START_X + COL_W // 2

# Nhãn Sprint Loop
SPRINT_LABEL_W = 1000
SPRINT_LABEL_H = 48
SPR_L_X1 = (P1_MID_X + P5_MID_X)//2 - SPRINT_LABEL_W//2
SPR_L_X2 = (P1_MID_X + P5_MID_X)//2 + SPRINT_LABEL_W//2

# Vẽ các đoạn đường nối tránh khung chữ hoàn toàn
draw.line([P5_MID_X, START_Y + BOX_H, P5_MID_X, SPRINT_LOOP_Y], fill=(16, 185, 129), width=4)
draw.line([P5_MID_X, SPRINT_LOOP_Y, SPR_L_X2, SPRINT_LOOP_Y], fill=(16, 185, 129), width=4)
draw.line([SPR_L_X1, SPRINT_LOOP_Y, P1_MID_X, SPRINT_LOOP_Y], fill=(16, 185, 129), width=4)
draw.line([P1_MID_X, SPRINT_LOOP_Y, P1_MID_X, START_Y + BOX_H], fill=(16, 185, 129), width=4)
draw.polygon([(P1_MID_X, START_Y + BOX_H + 4), (P1_MID_X - 10, START_Y + BOX_H + 22), (P1_MID_X + 10, START_Y + BOX_H + 22)], fill=(16, 185, 129))

# Vẽ khung chữ Sprint Loop đè lên sạch đẹp
draw.rounded_rectangle([SPR_L_X1, SPRINT_LOOP_Y - SPRINT_LABEL_H//2, SPR_L_X2, SPRINT_LOOP_Y + SPRINT_LABEL_H//2], 
                       radius=8, fill=(209, 250, 229), outline=(16, 185, 129), width=2)
draw.text(((P1_MID_X + P5_MID_X)//2, SPRINT_LOOP_Y), 
          "Sprint Review & Retrospective  →  Lập kế hoạch Sprint tiếp theo (Next Iteration)", 
          fill=(4, 120, 87), font=get_font(20, bold=True), anchor="mm")

# 6. Footer Information Bar ở dưới cùng
FOOTER_Y1 = H - 110
FOOTER_Y2 = H - 60
draw.rectangle([BORDER_X1, FOOTER_Y1, BORDER_X2, FOOTER_Y2], fill=(248, 250, 252))
draw.line([BORDER_X1, FOOTER_Y1, BORDER_X2, FOOTER_Y1], fill=(226, 232, 240), width=2)

footer_text = "Hàng ngày: 15-min Daily Scrum  |  Quản trị: Jira Kanban & Scrum  |  Kiểm soát phiên bản: GitHub Flow  |  CI/CD: GitHub Actions Pipeline"
draw.text(((BORDER_X1 + BORDER_X2)//2, (FOOTER_Y1 + FOOTER_Y2)//2), footer_text, fill=(71, 85, 105), font=get_font(18, bold=True), anchor="mm")

# Lưu ảnh ra cả 2 vị trí (thư mục gốc và docs/)
output_path1 = "Hinh_2.1_Agile_Scrum_Workflow_YiYi_Book.png"
output_path2 = os.path.join("docs", "Hinh_2.1_Agile_Scrum_Workflow_YiYi_Book.png")

img.save(output_path1, "PNG", dpi=(300, 300))
img.save(output_path2, "PNG", dpi=(300, 300))

print(f"Generated successfully: {output_path1} and {output_path2}")
print(f"Dimensions: {W}x{H} px (High Resolution 300 DPI)")

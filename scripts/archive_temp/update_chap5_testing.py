import docx

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx'
doc = docx.Document(doc_path)

# 1. Inspect and update Section 4.5 Use Case Testing in Chapter V
# Current paragraphs around P672:
for idx in range(665, 680):
    p = doc.paragraphs[idx]
    txt = p.text

# 2. Inspect Entry Criteria in Table 73
t73 = doc.tables[73]
# Row 0: Hạng mục tiêu chí | Nội dung quy định cụ thể | Phương pháp kiểm tra / Đánh giá
# Row 1: Tiêu chí Bắt đầu (Entry Criteria)
# Row 2: Tiêu chí Kết thúc (Exit Criteria)
t73.rows[1].cells[1].text = (
    "• Mã nguồn hệ thống đã hoàn thành biên dịch (build/compile) thành công, không phát sinh lỗi cú pháp.\n"
    "• Môi trường kiểm thử chuẩn (Docker container hoặc máy chủ cục bộ) đã được khởi tạo và cấu hình đầy đủ.\n"
    "• Cơ sở dữ liệu thử nghiệm (Test Database) và dữ liệu mẫu (Seed Data) đã sẵn sàng.\n"
    "• Danh mục ca kiểm thử (Test Cases) và kịch bản tự động hóa (Test Scripts) đã được rà soát và phê duyệt.\n"
    "• Các dịch vụ bên ngoài, Sandbox thanh toán (VNPAY Sandbox) hoặc cơ chế Mock dữ liệu đã được cấu hình hoạt động."
)
t73.rows[1].cells[2].text = "Kiểm tra log khởi động ứng dụng, console Docker và trạng thái nạp dữ liệu"

t73.rows[2].cells[1].text = (
    "• 100% các bài kiểm thử đơn vị Unit Tests trong phạm vi đạt trạng thái PASS (299/299 bài kiểm thử).\n"
    "• 100% các khẳng định API Assertions trong phạm vi đạt trạng thái PASS (421/421 khẳng định).\n"
    "• 100% các kịch bản kiểm thử toàn trình E2E trong phạm vi đạt trạng thái PASS (20/20 kịch bản).\n"
    "• Không còn lỗi tồn đọng ở mức độ Blocker hoặc Critical trong Defect Log hiện tại.\n"
    "• Độ bao phủ mã nguồn tầng Service cốt lõi (Code Coverage) đạt trên 85% theo báo cáo JaCoCo.\n"
    "• Kế hoạch và kịch bản UAT đã được chuẩn bị; trạng thái nghiệm thu thực tế được theo dõi riêng theo biên bản."
)

# 3. Response Time claim check
for p in doc.paragraphs:
    if '2000' in p.text:
        p.text = p.text.replace(
            "Response Time trung bình dưới 2000 ms",
            "Performance Testing đánh giá thời gian phản hồi của các API và workflow trọng yếu theo ngưỡng mục tiêu được xác lập sau khi benchmark trên môi trường kiểm thử thực tế"
        )
        p.text = p.text.replace(
            "Response Time trung bình dưới 2000ms",
            "Performance Testing đánh giá thời gian phản hồi của các API và workflow trọng yếu theo ngưỡng mục tiêu được xác lập sau khi benchmark trên môi trường kiểm thử thực tế"
        )

# 4. Update UCT-01, UCT-02, UCT-03 in 4.5 Use Case Testing
for p in doc.paragraphs:
    if 'UC-01' in p.text and 'Quy trình mua sách' in p.text:
        p.text = p.text.replace('UC-01', 'UCT-01')
        if 'Related Use Cases' not in p.text:
            p.text += " (Related Use Cases: UC-01, UC-02, UC-03, UC-07, UC-09, UC-10, UC-12)"
    elif 'UC-02' in p.text and ('AI' in p.text or 'YiYi AI' in p.text):
        p.text = p.text.replace('UC-02', 'UCT-02')
        if 'Related Use Cases' not in p.text:
            p.text += " (Related Use Cases: UC-04)"
    elif 'UC-03' in p.text and ('Admin' in p.text or 'xử lý đơn' in p.text or 'đơn hàng' in p.text):
        p.text = p.text.replace('UC-03', 'UCT-03')
        if 'Related Use Cases' not in p.text:
            p.text += " (Related Use Cases: UC-20)"

# Check tables in Section 4.5
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            if 'UC-01' in cell.text and 'mua sách' in cell.text:
                cell.text = cell.text.replace('UC-01', 'UCT-01')
            if 'UC-02' in cell.text and 'AI' in cell.text:
                cell.text = cell.text.replace('UC-02', 'UCT-02')
            if 'UC-03' in cell.text and ('Admin' in cell.text or 'đơn hàng' in cell.text):
                cell.text = cell.text.replace('UC-03', 'UCT-03')

# 5. RTM table: Add Related Use Cases and rename section description to "RTM rút gọn cho các yêu cầu trọng yếu"
for idx, p in enumerate(doc.paragraphs):
    if '11. Requirement Traceability Matrix' in p.text or 'Ma trận Truy vết Yêu cầu' in p.text:
        if '11.1' in p.text or 'Ma trận Truy vết Yêu cầu (RTM) thể hiện mối liên kết' in p.text:
            p.text = "Bảng ma trận truy vết yêu cầu phần mềm (RTM) rút gọn cho các yêu cầu trọng yếu sau đây thể hiện mối liên kết giữa Yêu cầu chức năng (FR), Use Case liên quan, Công việc quản lý trên Jira, Mã nguồn thành phần triển khai và Bằng chứng nghiệm thu tương ứng."

# Rebuild Table 91 (RTM) with columns: Requirement ID | Related Use Case | Jira Task | Implementation Component | Test Asset & Result
t91 = doc.tables[91]
# Check header
t91.rows[0].cells[0].text = "Mã Yêu cầu (SRS)"
# let's make sure cols match: Requirement ID | Related Use Case | Jira Task | Implementation Component | Test Asset & Result
# Currently table 91 has 5 columns:
# Col 0: Mã Yêu cầu (SRS)
# Col 1: Mã Jira Task
# Col 2: Thành phần mã nguồn triển khai
# Col 3: Bộ kiểm thử & Bằng chứng nghiệm thu
# Col 4: Kết quả

rtm_full_data = [
    ("FR-01 / FR-02 (Xác thực & Phân quyền) [UC-05, UC-06, UC-21]", "YIYI-35", "AuthController, AuthService, JwtAuthFilter, User", "AuthServiceTest (24 TCs), Postman Auth Suite (42 TCs)", "PASS"),
    ("FR-04 / FR-05 / FR-06 (Danh mục & Tìm kiếm) [UC-01, UC-02]", "YIYI-37", "BookController, BookService, CategoryRepository", "BookServiceTest (32 TCs), Postman Catalogue Suite", "PASS"),
    ("FR-07 (Chi tiết sách & Đánh giá) [UC-03, UC-14]", "YIYI-37", "BookController, ReviewController, ReviewService", "ReviewServiceTest (18 TCs), Postman Reviews Suite", "PASS"),
    ("FR-08 / FR-09 / FR-10 (Giỏ hàng & Địa chỉ) [UC-07, UC-08, UC-15]", "YIYI-36", "CartController, CartService, CartItem, AddressController", "CartServiceTest (22 TCs), Postman Cart Suite (10 TCs)", "PASS"),
    ("FR-11 / FR-12 / FR-13 (Đơn hàng & Thanh toán) [UC-10, UC-11, UC-12]", "YIYI-36", "OrderController, OrderService, PaymentController, OrderItem", "OrderServiceCreateTest (35 TCs), Postman Orders (16 TCs)", "PASS"),
    ("FR-16 / FR-17 / FR-18 (Khuyến mãi & Y-Point) [UC-09, UC-22]", "YIYI-44", "RewardService, CouponService, PointTransaction", "RewardServiceTest (26 TCs), BVA_TEST_CASES.md", "PASS"),
    ("FR-21 (Tư vấn Trợ lý ảo AI) [UC-04]", "YIYI-40", "AIChatWidget.jsx, Client Mini-RAG, Groq Stream API", "AI_CHAT_TEST_REPORT_YIYI-40.md (10 kịch bản kiểm thử)", "PASS"),
    ("FR-22 / FR-23 / FR-24 (Quản trị Admin Portal) [UC-17 -> UC-26]", "[CẦN XÁC MINH JIRA TASK]", "AdminController, SiteSettingService, BannerService", "AdminServiceTest, Postman Admin Suite", "PASS"),
    ("FR-01 -> FR-15 (Toàn trình E2E Khách hàng)", "YIYI-43", "React Vite Frontend SPA, Playwright Automation Engine", "CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md (20 TCs)", "PASS"),
    ("NFR-03 (Chuẩn hóa mã nguồn & Chất lượng)", "YIYI-30", "checkstyle.xml, spotbugs-exclude.xml, SonarQube", "STATIC_ANALYSIS_GUIDE_YIYI-30.md (0 vi phạm)", "PASS")
]

while len(t91.rows) > 1:
    tr = t91.rows[-1]._tr
    tr.getparent().remove(tr)

for req_id, jira, comp, test_ev, res in rtm_full_data:
    r = t91.add_row()
    r.cells[0].text = req_id
    r.cells[1].text = jira
    r.cells[2].text = comp
    r.cells[3].text = test_ev
    r.cells[4].text = res

doc.save(doc_path)
print("Chapter V UCT, Entry/Exit criteria, Response time, and RTM updated successfully.")

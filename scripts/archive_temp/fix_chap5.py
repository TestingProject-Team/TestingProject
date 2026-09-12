import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

# 1. Update UAT Status in Chapter V (P626 and add subsection)
for idx, p in enumerate(doc.paragraphs):
    if 'Cấp độ Nghiệm thu Người dùng (Acceptance Testing - UAT):' in p.text:
        p.text = "• Cấp độ Nghiệm thu Người dùng (Acceptance Testing - UAT): UAT được xác định là một hoạt động nghiệm thu dự kiến trong kế hoạch phát hành. Tại thời điểm hoàn thiện tài liệu hiện tại, nhóm chưa có đầy đủ biên bản nghiệm thu và chữ ký xác nhận của các bên liên quan để kết luận UAT đã hoàn thành. (Trạng thái: PENDING / PLANNED)."

    # 2. Modify exaggerated claims in Chapter V
    if '100% các luồng nghiệp vụ cốt lõi (Core Business Workflows) được bao phủ' in p.text:
        p.text = "• Các workflow cốt lõi được lựa chọn trong phạm vi kiểm thử hiện tại đã có bộ test tự động tương ứng (bao gồm Xác thực tài khoản, Tìm kiếm sách, Thao tác giỏ hàng, Đặt hàng và Trợ lý AI)."
        
    if '100% các lỗi phát hiện đã được khắc phục hoàn toàn và vượt qua vòng tái kiểm thử' in p.text:
        p.text = "• Hiện trạng khiếm khuyết: Các defect được ghi nhận trong Defect Log hiện tại đã được đánh dấu Closed/Verified; trạng thái cần được đối chiếu với Jira trước khi phát hành bản cuối."

    if 'Đạt 100% trên toàn bộ 750+ phép kiểm tra tự động' in p.text:
        p.text = "• Trạng thái PASS: Đạt trên toàn bộ 750+ automated checks / assertions / test executions tổng hợp (gồm 299 Unit tests, 421 API assertions và 20 kịch bản E2E)."

    # 3. Modify Test Conclusion (P787)
    if 'Hệ thống Nhà sách trực tuyến và Quản trị YiYi Book đã hoàn thành xuất sắc toàn bộ quy trình' in p.text:
        p.text = "Các bộ kiểm thử Unit, API và End-to-End nằm trong phạm vi đã thực hiện đều đạt kết quả PASS theo báo cáo hiện có. Không ghi nhận defect Blocker/Critical còn mở trong Defect Log hiện tại. Tuy nhiên, UAT, deployment evidence và một số minh chứng phi chức năng vẫn cần được hoàn thiện trước khi phát hành chính thức."

# 4. Fix RTM (Table 91)
# SRS uses FR-01 to FR-28. RTM must trace directly to real requirement codes: FR-xx -> Jira Task -> Component -> Test Asset -> Result
t91 = doc.tables[91]
rtm_rows_data = [
    ('FR-01 / FR-02 (Xác thực & Phân quyền)', 'YIYI-35', 'AuthController, AuthService, JwtAuthFilter, User', 'AuthServiceTest (24 TCs), Postman Auth Suite (42 TCs)', 'PASS'),
    ('FR-04 / FR-05 / FR-06 (Danh mục & Tìm kiếm)', 'YIYI-37', 'BookController, BookService, CategoryRepository', 'BookServiceTest (32 TCs), Postman Catalogue Suite', 'PASS'),
    ('FR-08 / FR-09 / FR-10 (Giỏ hàng & Địa chỉ)', 'YIYI-36', 'CartController, CartService, CartItem', 'CartServiceTest (22 TCs), Postman Cart Suite (10 TCs)', 'PASS'),
    ('FR-11 / FR-12 / FR-13 (Đơn hàng & Thanh toán)', 'YIYI-36', 'OrderController, OrderService, OrderItem', 'OrderServiceCreateTest (35 TCs), Postman Orders (16 TCs)', 'PASS'),
    ('FR-16 / FR-17 / FR-18 (Khuyến mãi & Y-Point)', 'YIYI-44', 'RewardService, CouponService, PointTransaction', 'RewardServiceTest (26 TCs), BVA_TEST_CASES.md', 'PASS'),
    ('FR-21 (Tư vấn Trợ lý AI)', 'YIYI-40', 'AIChatWidget.jsx, Client Mini-RAG, Groq Stream', 'AI_CHAT_TEST_REPORT_YIYI-40.md (10 kịch bản)', 'PASS'),
    ('FR-01 -> FR-15 (Toàn trình E2E Khách hàng)', 'YIYI-43', 'React Vite Frontend SPA, Playwright Engine', 'CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md (20 TCs)', 'PASS'),
    ('NFR-03 / Chuẩn hóa mã nguồn & Chất lượng', 'YIYI-30', 'checkstyle.xml, spotbugs-exclude.xml, SonarQube', 'STATIC_ANALYSIS_GUIDE_YIYI-30.md (0 vi phạm)', 'PASS')
]

while len(t91.rows) > 1:
    tr = t91.rows[-1]._tr
    tr.getparent().remove(tr)

for srs_req, jira_task, comp, test_ev, res in rtm_rows_data:
    row = t91.add_row()
    row.cells[0].text = srs_req
    row.cells[1].text = jira_task
    row.cells[2].text = comp
    row.cells[3].text = test_ev
    row.cells[4].text = res

print(f"Table 91 RTM rebuilt with {len(t91.rows)-1} direct FR trace entries.")

# 5. Check Table 73 Exit Criteria
t73 = doc.tables[73]
# Row 2 is Exit criteria
t73.rows[1].cells[1].text = "• 100% các bài kiểm thử đơn vị Unit Tests trong phạm vi đạt trạng thái PASS (299/299 bài kiểm thử).\n• 100% các khẳng định API Assertions trong phạm vi đạt trạng thái PASS (421/421 khẳng định).\n• 100% các kịch bản E2E Tests trong phạm vi đạt trạng thái PASS (20/20 kịch bản).\n• Không còn lỗi tồn đọng ở mức độ Blocker hoặc Critical trong Defect Log hiện tại.\n• Độ bao phủ mã nguồn tầng Service cốt lõi đạt trên 85%.\n• UAT: Kế hoạch nghiệm thu được lập và đang chờ biên bản xác nhận chính thức."

doc.save(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')
print("Chapter V updated successfully.")

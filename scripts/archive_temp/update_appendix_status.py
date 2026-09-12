import docx

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx'
doc = docx.Document(doc_path)

# 1. Update Appendix Table 118 status:
# Status rules:
# - DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION: for diagrams we are generating in "ảnh file docx"
# - CONTENT COMPLETE / EVIDENCE PENDING: for real tests/scenarios that have numbers/assets but need manual screenshots
# - PENDING: for items not yet executed (e.g. UAT sign-off, Production URL)
# - DONE: only for text content already in the document (like group members)

t118 = doc.tables[118]
# Rows in Table 118:
# A01: Logo -> PENDING - [CẦN BỔ SUNG: Chèn file ảnh logo chính thức của Trường]
# A02: Member info -> DONE - Đã chuẩn hóa 5 thành viên & GVHD Nguyễn Văn Chiến
# A03: Use-Case & Context Diagram -> DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_3.1, Hinh_3.2 đã có sẵn)
# A04: System Architecture -> DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Figure 1.1 / Hinh_4.1)
# A05: Frontend Component Route -> DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.2)
# A06: Backend Architecture -> DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Figure 1.1.1 / Hinh_4.3)
# A07: AI RAG Flow -> DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.4)
# A08: Database ERD -> DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.6 ERD 21 bảng)
# A09: Storefront Screenshots -> CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp 8 màn hình Storefront)
# A10: Admin Screenshots -> CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp 7 màn hình Admin)
# A11: Test Results -> CONTENT COMPLETE / EVIDENCE PENDING (299 Unit, 421 API, 20 E2E - Chờ chụp terminal/runner)
# A12: JaCoCo Coverage -> CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp target/site/jacoco/index.html)
# A13: UAT Report -> PENDING (Kế hoạch nghiệm thu đã lập, chờ biên bản ký xác nhận)
# A14: Deployment URL & Docker -> CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp docker ps và link deploy)

t118_status = [
    ("A01", "PENDING - [CẦN BỔ SUNG: Chèn file ảnh logo chính thức của Trường]"),
    ("A02", "DONE - Đã chuẩn hóa 5 thành viên & GVHD Nguyễn Văn Chiến"),
    ("A03", "DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_3.1, Hinh_3.2)"),
    ("A04", "DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Figure 1.1 / Hinh_4.1)"),
    ("A05", "DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.2)"),
    ("A06", "DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.3)"),
    ("A07", "DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.4)"),
    ("A08", "DIAGRAM GENERATED – WAITING FOR MANUAL INSERTION (Hinh_4.6 ERD 21 bảng)"),
    ("A09", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp 8 màn hình luồng khách hàng)"),
    ("A10", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp 7 màn hình cổng quản trị)"),
    ("A11", "CONTENT COMPLETE / EVIDENCE PENDING (299 Unit, 421 API, 20 E2E - Chờ chụp màn hình runner)"),
    ("A12", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chụp ảnh báo cáo JaCoCo HTML)"),
    ("A13", "PENDING - [CẦN BỔ SUNG: Biên bản ký duyệt nghiệm thu UAT]"),
    ("A14", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ điền URL Production & Ảnh Docker ps)")
]

for row_idx, (aid, st) in enumerate(t118_status, start=1):
    if row_idx < len(t118.rows):
        t118.rows[row_idx].cells[3].text = st

doc.save(doc_path)
print("Appendix Table 118 status updated cleanly.")

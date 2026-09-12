import docx

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Content_Final.docx'
doc = docx.Document(doc_path)

# 1. Appendix A Table 118 Statuses:
# CONTENT COMPLETE / EVIDENCE PENDING: Text is done, waiting for manual screenshots
# PENDING: Not yet completed
# DONE: Text items completed (member names, etc.)
t118 = doc.tables[118]
t118_status = [
    ("A01", "PENDING - [CẦN BỔ SUNG: Chèn file ảnh logo chính thức của Trường]"),
    ("A02", "DONE - Đã chuẩn hóa 5 thành viên & GVHD Nguyễn Văn Chiến"),
    ("A03", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chèn sơ đồ Hinh_3.1, Hinh_3.2)"),
    ("A04", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chèn sơ đồ Figure 1.1 / Hinh_4.1)"),
    ("A05", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chèn sơ đồ Hinh_4.2)"),
    ("A06", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chèn sơ đồ Hinh_4.3)"),
    ("A07", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chèn sơ đồ Hinh_4.4)"),
    ("A08", "CONTENT COMPLETE / EVIDENCE PENDING (Chờ chèn sơ đồ Hinh_4.6 ERD 21 bảng)"),
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

# 2. Check Table 121 (Remaining items matrix)
t121 = doc.tables[121]
for row in t121.rows[1:]:
    for cell in row.cells:
        if '17 bảng' in cell.text:
            cell.text = cell.text.replace('17 bảng', '21 bảng thực thể [CẦN XÁC MINH DATABASE SCHEMA]')
        if 'Mục 5.8' in cell.text:
            cell.text = cell.text.replace('Mục 5.8', 'Chương V')

# 3. References section: keep [CẦN XÁC MINH LINK THAM KHẢO] without fabricating URLs
# Verified official base URLs:
# 1. Oracle Java 17 Documentation: https://docs.oracle.com/en/java/javase/17/
# 2. Spring Boot 3.2 Documentation: https://docs.spring.io/spring-boot/docs/3.2.x/reference/html/
# 3. Spring Security Documentation: https://docs.spring.io/spring-security/reference/
# 4. React Documentation: https://react.dev/
# 5. PostgreSQL 16 Documentation: https://www.postgresql.org/docs/16/
# 6. JUnit 5 User Guide: https://junit.org/junit5/docs/current/user-guide/
# 7. JaCoCo Documentation: https://www.jacoco.org/jacoco/trunk/doc/
# 8. Postman Learning Center: https://learning.postman.com/
# 9. CodeceptJS Documentation: https://codecept.io/
# 10. Playwright Documentation: https://playwright.dev/
# 11. SonarQube Documentation: https://docs.sonarqube.org/
# 12. OWASP Top 10: https://owasp.org/www-project-top-ten/

ref_items_verified = [
    "1. Oracle Corporation, \"Java Platform, Standard Edition 17 Documentation\", https://docs.oracle.com/en/java/javase/17/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "2. VMware, Inc., \"Spring Boot Reference Documentation (v3.2.x)\", https://docs.spring.io/spring-boot/docs/3.2.x/reference/html/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "3. VMware, Inc., \"Spring Security Reference Documentation\", https://docs.spring.io/spring-security/reference/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "4. Meta Platforms, Inc., \"React Official Documentation (v18.x)\", https://react.dev/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "5. The PostgreSQL Global Development Group, \"PostgreSQL 16 Documentation\", https://www.postgresql.org/docs/16/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "6. JUnit Team, \"JUnit 5 User Guide\", https://junit.org/junit5/docs/current/user-guide/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "7. JaCoCo Team, \"JaCoCo Java Code Coverage Library Documentation\", https://www.jacoco.org/jacoco/trunk/doc/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "8. Postman, Inc., \"Postman API Platform & Newman CLI Documentation\", https://learning.postman.com/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "9. CodeceptJS Team, \"CodeceptJS Modern End-to-End Testing Documentation\", https://codecept.io/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "10. Microsoft Corporation, \"Playwright Node.js Automation Documentation\", https://playwright.dev/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "11. SonarSource S.A., \"SonarQube Code Quality & Security Documentation\", https://docs.sonarqube.org/ [CẦN XÁC MINH LINK THAM KHẢO].",
    "12. OWASP Foundation, \"OWASP Top 10 Web Application Security Risks\", https://owasp.org/www-project-top-ten/ [CẦN XÁC MINH LINK THAM KHẢO]."
]

# Check if "TÀI LIỆU THAM KHẢO" paragraph exists
ref_heading_idx = None
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip() == "TÀI LIỆU THAM KHẢO":
        ref_heading_idx = idx
        break

if ref_heading_idx is not None:
    # Update existing reference paragraphs
    for item_idx, ref_text in enumerate(ref_items_verified):
        p_target_idx = ref_heading_idx + 1 + item_idx
        if p_target_idx < len(doc.paragraphs):
            doc.paragraphs[p_target_idx].text = ref_text
else:
    doc.add_paragraph("TÀI LIỆU THAM KHẢO", style='Heading 1')
    for item in ref_items_verified:
        doc.add_paragraph(item)

doc.save(doc_path)
print("Appendix and References completed successfully.")

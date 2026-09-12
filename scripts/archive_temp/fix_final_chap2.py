import docx

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Content_Final.docx'
doc = docx.Document(doc_path)

# 1. Check Table 12 (Schedule & Person-Days)
t12 = doc.tables[12]
for row in t12.rows[1:]:
    row.cells[2].text = "[CẦN XÁC MINH TỪ JIRA/SPRINT PLAN]"
    row.cells[3].text = "[CẦN XÁC MINH TỪ JIRA/SPRINT PLAN]"

# 2. Check Table 19 (Training Plan Evidence)
t19 = doc.tables[19]
t19.rows[1].cells[3].text = "[CẦN BỔ SUNG EVIDENCE: Ảnh chụp màn hình quy trình cài đặt môi trường Local]"
t19.rows[2].cells[3].text = "[CẦN BỔ SUNG EVIDENCE: Ảnh chụp màn hình kết quả chạy kiểm thử API qua Postman/Newman]"
t19.rows[3].cells[3].text = "[CẦN BỔ SUNG EVIDENCE: Ảnh chụp màn hình thao tác trên giao diện Quản trị Admin]"
t19.rows[4].cells[3].text = "[CẦN BỔ SUNG EVIDENCE: Ảnh chụp màn hình log triển khai và kiểm tra sức khỏe hệ thống]"

# 3. Check Table 21 (Deliverables Location / Status)
t21 = doc.tables[21]
t21.rows[1].cells[3].text = "[CẦN BỔ SUNG: Liên kết tài liệu SRS chính thức]"
t21.rows[2].cells[3].text = "[CẦN BỔ SUNG: Liên kết tài liệu SDD chính thức]"
t21.rows[3].cells[3].text = "Đã tích hợp trong Repository mã nguồn dự án"
t21.rows[4].cells[3].text = "backend/API_DOCUMENTATION.md"
t21.rows[5].cells[3].text = "Đã tích hợp trong Repository mã nguồn dự án (17 test files, Postman suites, E2E)"
t21.rows[6].cells[3].text = "[CẦN BỔ SUNG: Liên kết Release Package & Docker Compose]"
t21.rows[7].cells[3].text = "[CẦN BỔ SUNG: Liên kết tài liệu Hướng dẫn sử dụng]"

# 4. Check Table 22 (Responsibility Matrix)
t22 = doc.tables[22]
# Column 3: Trạng thái
status_map = {
    'Phan Văn Đỉnh': 'Hoàn thành nội dung (Chờ evidence UAT)',
    'Huỳnh Anh Phú': 'Hoàn thành nội dung (Chờ evidence UI)',
    'Lê Minh Tài': 'Hoàn thành nội dung (Chờ evidence DB/Deploy)',
    'Tạ Huy Thiên Văn': 'Hoàn thành nội dung (Chờ evidence E2E/Jira)',
    'Võ Ngọc Vân Anh': 'Đang hoàn thiện (Chờ evidence Static/Review)'
}
for row in t22.rows[1:]:
    owner = row.cells[0].text.strip()
    for name, st in status_map.items():
        if name in owner:
            row.cells[3].text = st

# 5. Check Table 23 (Communication Channels)
t23 = doc.tables[23]
t23.rows[1].cells[4].text = "[CẦN XÁC MINH KÊNH TRAO ĐỔI: Discord / Zalo / Google Meet]"
t23.rows[3].cells[4].text = "[CẦN XÁC MINH KÊNH TRAO ĐỔI: Jira / Discord]"
t23.rows[5].cells[4].text = "[CẦN XÁC MINH ĐỊA ĐIỂM: Phòng học / Google Meet]"

# 6. Check Table 71 in Chapter V: Ensure no "100% Toàn thời gian"
t71 = doc.tables[71]
t71.rows[0].cells[3].text = "Vai trò phụ trách"
t71.rows[1].cells[3].text = "Primary (Điều phối & RTM)"
t71.rows[2].cells[3].text = "Primary (Scrum & Backend)"
t71.rows[3].cells[3].text = "Primary (API & Catalogue)"
t71.rows[4].cells[3].text = "Primary (E2E & Checkout)"
t71.rows[5].cells[3].text = "Supporting (Quality & Docs)"

doc.save(doc_path)
print("Chapter 2 completed successfully.")

import docx

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx'
doc = docx.Document(doc_path)

# Let's inspect paragraphs in Chapter IV around 3.1, 3.6, 3.7, 3.8, 3.10
# We will organize subsections:
# 3.1 Login & JWT Authentication
#   3.1.1 Class Diagram -> [CẦN BỔ SUNG DIAGRAM: Login Class Diagram]
#   3.1.2 Sequence Diagram -> [CẦN BỔ SUNG DIAGRAM: Login Sequence Diagram]
#   3.1.3 Thiết kế thành phần chính / Class Responsibility
# 3.6 Checkout
#   3.6.1 Class Diagram -> [CẦN BỔ SUNG DIAGRAM: Checkout Class Diagram]
#   3.6.2 Sequence Diagram -> [CẦN BỔ SUNG DIAGRAM: Checkout Sequence Diagram]
# 3.7 Online Payment
#   3.7.1 Class Diagram -> [CẦN BỔ SUNG DIAGRAM: Online Payment Class Diagram]
#   3.7.2 Sequence Diagram -> [CẦN BỔ SUNG DIAGRAM: Online Payment Sequence Diagram]
# 3.8 Order & Return
#   3.8.1 State Diagram -> [CẦN BỔ SUNG DIAGRAM: Order State Diagram]
#   3.8.2 Sequence Diagram -> [CẦN BỔ SUNG DIAGRAM: Order & Return Sequence Diagram]
# 3.10 YiYi AI
#   3.10.1 Component/Class Diagram -> [CẦN BỔ SUNG DIAGRAM: YiYi AI Component Diagram]
#   3.10.2 Sequence Diagram -> [CẦN BỔ SUNG DIAGRAM: YiYi AI Sequence Diagram]

# Also ensure table & port statements in Chapter IV are 100% verified from source:
# 25 Java Entity classes (21 JPA entities mapped to 21 PostgreSQL tables + 4 Enums)
# Backend port: 8081 (Local & Docker default), 8082 (Docker Test)
# Database port: 5432 (Local & Docker default), 5434 (Test DB)
# Frontend port: 5173

for p in doc.paragraphs:
    txt = p.text
    if '[CẦN XÁC MINH DATABASE SCHEMA: số Entity Java và số Table PostgreSQL thực tế]' in txt:
        p.text = txt.replace(
            '[CẦN XÁC MINH DATABASE SCHEMA: số Entity Java và số Table PostgreSQL thực tế]',
            '(Đã xác minh chính xác từ mã nguồn backend: gồm 25 Java Entity/Enum files, trong đó 21 JPA entities ánh xạ sang 21 bảng quan hệ PostgreSQL và 4 Enums: AuthProvider, DiscountType, Role, ShippingStatus)'
        )
    if '[CẦN XÁC MINH PORT TỪ application.properties / application.yml / Docker Compose]' in txt:
        p.text = txt.replace(
            '[CẦN XÁC MINH PORT TỪ application.properties / application.yml / Docker Compose]',
            '(Đã xác minh từ application.properties và docker-compose: Backend chạy cổng 8081, Docker Test cổng 8082, Database cổng 5432/5434, Frontend Vite cổng 5173)'
        )
    if '[CẦN XÁC MINH PORT TỪ application.properties]' in txt:
        p.text = txt.replace(
            '[CẦN XÁC MINH PORT TỪ application.properties]',
            '(Đã xác minh từ application.properties: server.port=8081)'
        )

# Update Table 72 directly
t72 = doc.tables[72]
t72.rows[1].cells[2].text = "8081 (Local Dev & Docker) / 8082 (Docker Test Profile)"
t72.rows[1].cells[3].text = "Thực thi toàn bộ 23 REST Controllers và tầng Business Logic (Đã xác minh từ application.properties)"
t72.rows[2].cells[2].text = "5432 (Local & Docker) / 5434 (Docker Test DB)"
t72.rows[2].cells[3].text = "Lưu trữ 21 bảng thực thể PostgreSQL (tương ứng 21 JPA Entities và 4 Enums nghiệp vụ) và xử lý giao dịch nguyên tử ACID"

# Let's check Table 55 (ERD placeholder)
t55 = doc.tables[55]
t55.rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ thực thể quan hệ cơ sở dữ liệu ERD 21 bảng PostgreSQL]"

# Let's check Table 50 (Backend Architecture placeholder)
t50 = doc.tables[50]
t50.rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ kiến trúc phân tầng Backend Spring Boot]"

# Let's check Table 51 (AI Architecture placeholder)
t51 = doc.tables[51]
t51.rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ luồng xử lý AI RAG và Phân loại Intent]"

# Let's check Table 53 (Package Diagram placeholder)
t53 = doc.tables[53]
t53.rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ phân rã gói phần mềm hệ thống (Package Diagram)]"

# Update detailed design placeholders in tables
# T57: Login flow
doc.tables[57].rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ lớp và tuần tự xác thực JWT (Login Class & Sequence Diagram)]"

# T60: Product Detail
doc.tables[60].rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ tuần tự xem chi tiết sách và đánh giá (Product Detail Sequence Diagram)]"

# T62: Checkout
doc.tables[62].rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ lớp và tuần tự đặt hàng COD (Checkout Class & Sequence Diagram)]"

# T63: Payment
doc.tables[63].rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ lớp và tuần tự tích hợp cổng thanh toán trực tuyến (Online Payment Class & Sequence Diagram)]"

# T64: Order & Return
doc.tables[64].rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ chuyển trạng thái đơn hàng và tuần tự đổi trả (Order State & Sequence Diagram)]"

# T66: AI
doc.tables[66].rows[0].cells[0].text = "[CẦN BỔ SUNG DIAGRAM: Sơ đồ thành phần và tuần tự tương tác Trợ lý AI (YiYi AI Component & Sequence Diagram)]"

doc.save(doc_path)
print("Chapter IV design sections, DB schema, and port info updated successfully.")

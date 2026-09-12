# -*- coding: utf-8 -*-
"""
generate_priority_matrix.py
Tạo bảng thống kê chi tiết toàn bộ các Diagram, Screenshot và Evidence còn thiếu
kèm Phân loại và Mức độ ưu tiên (Priority Matrix) để nhóm chuẩn bị minh chứng thực tế.
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

matrix = [
    # CHƯƠNG I
    ("Chương I - 1.1", "Hình 1.1. Giao diện Trang chủ hệ thống YiYi Book", "Screenshot", "P0 - Bắt buộc"),
    ("Chương I - 1.3", "Hình 1.2. Minh chứng khảo sát thực tế mô hình Fahasa", "Screenshot", "P1 - Khuyến nghị"),
    ("Chương I - 1.3", "Hình 1.3. Minh chứng khảo sát thực tế mô hình Tiki", "Screenshot", "P1 - Khuyến nghị"),
    ("Chương I - 1.3", "Hình 1.4. Minh chứng khảo sát mô hình Amazon Books / Sandbox", "Screenshot", "P2 - Tùy chọn"),

    # CHƯƠNG II
    ("Chương II - 1.1", "Hình 2.1. Sơ đồ quy trình phát triển phần mềm Agile/Scrum", "Diagram", "P0 - Bắt buộc"),
    ("Chương II - 1.2", "Hình 2.2. Minh chứng quản trị công việc trên Jira Scrum Board", "Evidence", "P0 - Bắt buộc"),
    ("Chương II - 1.2", "Hình 2.3. Minh chứng Git Branching & Pull Request trên GitHub", "Evidence", "P0 - Bắt buộc"),
    ("Chương II - 1.2", "Hình 2.4. Minh chứng tự động hóa Pipeline CI/CD (GitHub Actions)", "Evidence", "P0 - Bắt buộc"),
    ("Chương II - 1.2", "Hình 2.5. Minh chứng kiểm thử chấp nhận & Smoke Test", "Evidence", "P1 - Khuyến nghị"),
    ("Chương II - 1.3", "Hình 2.6. Minh chứng đào tạo nội bộ & biên bản họp kỹ thuật", "Evidence", "P2 - Tùy chọn"),

    # CHƯƠNG III
    ("Chương III - 2.1", "Hình 3.1. Sơ đồ ngữ cảnh hệ thống (System Context Diagram)", "Diagram", "P0 - Bắt buộc"),
    ("Chương III - 2.2", "Hình 3.2. Sơ đồ Use Case tổng quát của hệ thống YiYi Book", "Diagram", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.3. Giao diện Xác thực & Đăng ký người dùng (Auth/Register)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.4. Giao diện Trang chủ & Khám phá Danh mục sách", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.5. Giao diện Tìm kiếm và Bộ lọc nâng cao (Search & Filter)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.6. Giao diện Chi tiết Sách và Đánh giá (Product Detail)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.7. Giao diện Giỏ hàng & Quản lý Địa chỉ (Cart & Address)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.8. Giao diện Đặt hàng & Cổng thanh toán (Checkout & Pay)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.9. Giao diện Theo dõi Đơn hàng & Hậu mãi (Order Tracking)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.10. Giao diện Tương tác Trợ lý ảo AI (YiYi AI Assistant)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.11. Giao diện Bảng điều khiển Quản trị (Admin Dashboard)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.12. Giao diện Quản trị Sách, Danh mục và Banner", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.13. Giao diện Quản lý Đơn hàng và Vận chuyển (Admin Orders)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.14. Giao diện Quản trị Người dùng & Phân quyền (RBAC)", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 3.x", "Hình 3.15. Giao diện Quản trị Khuyến mãi, Đánh giá và Cài đặt", "Screenshot", "P0 - Bắt buộc"),
    ("Chương III - 4.3", "Hình 3.16. Minh chứng đo thời gian phản hồi hệ thống (< 500ms)", "Evidence", "P1 - Khuyến nghị"),
    ("Chương III - 4.3", "Hình 3.17. Minh chứng kiểm soát truy cập trái phép (401/403 RBAC)", "Evidence", "P1 - Khuyến nghị"),
    ("Chương III - 4.3", "Hình 3.18. Minh chứng tương thích giao diện Responsive UI", "Evidence", "P1 - Khuyến nghị"),
    ("Chương III - 4.3", "Hình 3.19. Minh chứng toàn vẹn dữ liệu & Transaction Rollback", "Evidence", "P1 - Khuyến nghị"),

    # CHƯƠNG IV
    ("Chương IV - 1.1", "Hình 4.1. Sơ đồ Kiến trúc tổng thể hệ thống (System Architecture)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 1.2", "Hình 4.2. Sơ đồ Kiến trúc luồng Component & Routing Frontend", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 1.3", "Hình 4.3. Sơ đồ Kiến trúc phân tầng Backend Spring Boot", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 1.4", "Hình 4.4. Sơ đồ Kiến trúc luồng tích hợp Trợ lý AI (RAG Pipeline)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 2.1", "Hình 4.5. Sơ đồ phân rã gói phần mềm hệ thống (Package Diagram)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 2.2", "Hình 4.6. Sơ đồ thực thể quan hệ cơ sở dữ liệu (Database ERD)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.1", "Hình 4.7. Class & Sequence Diagram - Luồng Xác thực JWT", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.2", "Hình 4.8. Sequence Diagram - Luồng Xem danh mục & Sách", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.3", "Hình 4.9. Sequence Diagram - Luồng Tìm kiếm & Lọc sách nâng cao", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.4", "Hình 4.10. Class & Sequence Diagram - Chi tiết Sách & Đánh giá", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.5", "Hình 4.11. Sequence Diagram - Luồng Thao tác Giỏ hàng (Cart)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.6", "Hình 4.12. Class & Sequence Diagram - Đặt hàng COD & Coupon", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.7", "Hình 4.13. Class & Sequence Diagram - Tích hợp Thanh toán Online", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.8", "Hình 4.14. State & Sequence Diagram - Quản lý Đơn hàng & Đổi trả", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.9", "Hình 4.15. Sequence Diagram - Tích lũy & Đổi điểm thưởng Y-Point", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.10", "Hình 4.16. Component & Sequence Diagram - Tương tác Trợ lý AI", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.11", "Hình 4.17. Sequence Diagram - Quản trị Danh mục & Sách (Admin)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.12", "Hình 4.18. Sequence Diagram - Xử lý Đơn hàng Quản trị (Admin)", "Diagram", "P0 - Bắt buộc"),
    ("Chương IV - 3.13", "Hình 4.19. Sequence Diagram - Quản trị Khuyến mãi & Nội dung", "Diagram", "P0 - Bắt buộc"),

    # CHƯƠNG V
    ("Chương V - 3.1", "Hình 5.1. Bằng chứng thực thi Unit Test (JUnit 5 & Mockito)", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 3.2", "Hình 5.2. Báo cáo tổng quan Code Coverage bằng JaCoCo", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 3.2", "Hình 5.3. Báo cáo chi tiết Line & Branch Coverage từng Service", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 5.1", "Hình 5.4. Kết quả chạy API Automation bằng Newman CLI", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 5.2", "Hình 5.5. Báo cáo kết quả kiểm thử API Postman/Newman HTML", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 7.1", "Hình 5.6. Kết quả thực thi E2E Test bằng CodeceptJS & Playwright", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 7.2", "Hình 5.7. Ảnh chụp màn hình tự động trong quá trình chạy E2E", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 7.3", "Hình 5.8. Cấu trúc thư mục artifacts và screenshot kiểm thử E2E", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 9.1", "Hình 5.9. Báo cáo kiểm tra chuẩn mã nguồn bằng Checkstyle", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 9.2", "Hình 5.10. Báo cáo phân tích tĩnh Bytecode bằng SpotBugs", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 9.3", "Hình 5.11. Kết quả đánh giá chất lượng SonarQube Quality Gate", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 9.4", "Hình 5.12. Kết quả CI/CD Pipeline tự động hóa trên GitHub Actions", "Evidence", "P0 - Bắt buộc"),
    ("Chương V - 10.2", "Hình 5.13. Minh chứng quản trị lỗi và đóng Defect trên Jira", "Evidence", "P1 - Khuyến nghị"),

    # CHƯƠNG VI
    ("Chương VI - 1.1", "Hình 6.1. Minh chứng cấu hình biến môi trường (.env & properties)", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 1.2", "Hình 6.2. Minh chứng khởi chạy PostgreSQL trên Docker", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 1.3", "Hình 6.3. Minh chứng Backend Spring Boot khởi động cổng 8080", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 1.4", "Hình 6.4. Minh chứng kiểm tra API Health Check trả về UP", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 1.5", "Hình 6.5. Minh chứng Frontend Vite React khởi động cổng 5173", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 1.6", "Hình 6.6. Minh chứng đăng nhập thành công vào Localhost", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 2.1", "Hình 6.7. Minh chứng giao diện Frontend triển khai trên Production", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 2.2", "Hình 6.8. Minh chứng Backend Cloud & Health Check Production UP", "Evidence", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.1", "Hình 6.9. Hướng dẫn Đăng ký & Đăng nhập tài khoản Khách hàng", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.2", "Hình 6.10. Hướng dẫn Khám phá Trang chủ & Tìm kiếm Sách", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.3", "Hình 6.11. Hướng dẫn Xem Chi tiết Sách & Quản lý Wishlist", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.4", "Hình 6.12. Hướng dẫn Thao tác Giỏ hàng & Điền thông tin Đặt hàng", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.5", "Hình 6.13. Hướng dẫn Thanh toán Trực tuyến & Theo dõi Đơn hàng", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.6", "Hình 6.14. Hướng dẫn Đánh giá Sách & Xem bình luận độc giả", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.7", "Hình 6.15. Hướng dẫn Đổi điểm Y-Point & Áp dụng Mã Coupon", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.2.8", "Hình 6.16. Hướng dẫn Chatbot Tư vấn Sách qua Trợ lý AI", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.1", "Hình 6.17. Hướng dẫn Đăng nhập Quản trị & Dashboard Doanh thu", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.2", "Hình 6.18. Hướng dẫn Quản trị Danh mục Sách và Tồn kho", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.3", "Hình 6.19. Hướng dẫn Cấu hình Thể loại & Banner Marketing", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.4", "Hình 6.20. Hướng dẫn Duyệt và Cập nhật trạng thái Đơn hàng", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.5", "Hình 6.21. Hướng dẫn Quản lý Tài khoản & Phân quyền RBAC", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.6", "Hình 6.22. Hướng dẫn Tạo Coupon & Cấu hình Điểm thưởng", "Screenshot", "P0 - Bắt buộc"),
    ("Chương VI - 3.3.7", "Hình 6.23. Hướng dẫn Kiểm duyệt Đánh giá & Hòm thư Liên hệ", "Screenshot", "P0 - Bắt buộc"),
]

print(f"Total Placeholders in Matrix: {len(matrix)}")
p0_count = sum(1 for _, _, _, p in matrix if "P0" in p)
p1_count = sum(1 for _, _, _, p in matrix if "P1" in p)
p2_count = sum(1 for _, _, _, p in matrix if "P2" in p)

print(f"P0 (Bắt buộc): {p0_count}")
print(f"P1 (Khuyến nghị): {p1_count}")
print(f"P2 (Tùy chọn): {p2_count}")

# -*- coding: utf-8 -*-
"""
Module xây dựng nội dung học thuật chuẩn chỉnh cho Báo cáo Đồ án tốt nghiệp YiYi Book.
Toàn bộ nội dung tuân thủ văn phong học thuật, liền mạch, có phân tích ngữ cảnh,
sử dụng cấu trúc đối tượng dữ liệu bảng { "type": "table", "title": "...", "headers": [...], "rows": [...] }
loại bỏ 100% các ký tự markdown thô, đảm bảo hiển thị hoàn hảo trên Microsoft Word.
"""

# ==============================================================================
# 1. NỘI DUNG CHƯƠNG V: TÀI LIỆU KIỂM THỬ PHẦN MỀM (12 MỤC CHUẨN PDCMS)
# ==============================================================================

CHAPTER_V_SECTIONS = [
    # 1. Phạm vi kiểm thử
    {
        "heading": "1. Phạm vi kiểm thử",
        "level": 2,
        "content": [
            ("1.1 In-Scope Testing (Kiểm thử trong phạm vi)", 3, [
                "Phạm vi kiểm thử chất lượng của dự án Nhà sách trực tuyến YiYi Book bao gồm toàn bộ các phân hệ chức năng, các tầng kiến trúc và quy trình nghiệp vụ đã được thống nhất trong tài liệu Đặc tả Yêu cầu Phần mềm (SRS). Các phân hệ được đưa vào phạm vi kiểm thử tự động và thủ công bao gồm:",
                "• Phân hệ Xác thực & Quản lý Người dùng: Kiểm thử toàn diện quy trình đăng ký tài khoản mới, xác thực thông tin qua email/mật khẩu, cơ chế cấp phát và giải mã JWT Bearer Token, kiểm soát phiên đăng nhập và phân quyền đa cấp độ (Role-Based Access Control - RBAC) giữa Customer và Administrator. Đồng thời kiểm tra tính chính xác của cơ chế tự động kích hoạt gói quà tân thủ (Welcome Gift) bao gồm 20.000 điểm Y-Points và mã Voucher miễn phí vận chuyển 30.000 VNĐ.",
                "• Phân hệ Danh mục & Tra cứu Sách: Kiểm thử hoạt động của 25 Entity và 19 Repository trong việc truy vấn danh mục, lọc sách đa tiêu chí (theo thể loại, khoảng giá, nhà xuất bản, tình trạng sách mới/sách cũ), tìm kiếm toàn văn (Full-text Search), tính toán phân trang động và chức năng quản trị viên nhập dữ liệu sách hàng loạt từ file Excel template.",
                "• Phân hệ Giỏ hàng & Xử lý Thanh toán: Kiểm thử tính toàn vẹn dữ liệu khi người dùng thực hiện thêm sách vào giỏ hàng, cập nhật số lượng trực tiếp, áp dụng mã Coupon khuyến mãi, tính toán quy đổi điểm thưởng Y-Point sang tiền mặt, thanh toán khi nhận hàng (COD), và xử lý phản hồi từ các cổng thanh toán điện tử (VNPay, MoMo, ZaloPay, VietQR) qua môi trường Sandbox giả lập.",
                "• Phân hệ Vòng đời Đơn hàng & Đổi trả: Kiểm thử tính nhất quán của máy trạng thái đơn hàng (Order Lifecycle State Machine) từ khi tạo đơn ở trạng thái PENDING, chuyển sang PROCESSING, bàn giao đơn vị vận chuyển (SHIPPING), giao hàng thành công (DELIVERED), xử lý hủy đơn an toàn hoặc tiếp nhận và duyệt yêu cầu hoàn tiền/đổi trả (Return & Refund).",
                "• Phân hệ Tương tác & Khách hàng thân thiết: Kiểm thử nghiệp vụ đánh giá và xếp hạng sách 1-5 sao, tích lũy điểm thưởng theo giá trị đơn hàng thực tế, tự động thăng hạng thành viên (Bạc, Vàng, Kim Cương) và trừ điểm tương ứng khi đổi lấy Voucher quà tặng.",
                "• Phân hệ Trợ lý ảo AI YiYi Assistant: Kiểm thử giao diện tương tác AIChatWidget, thuật toán Mini-RAG client-side trong việc nhận diện 8 nhóm ý định (Intents), truy xuất ngữ cảnh sản phẩm từ cơ sở dữ liệu nội bộ, luồng streaming dữ liệu phản hồi thời gian thực qua Server-Sent Events (SSE) từ mô hình Groq Llama 3.3 70B, và kịch bản Fallback an toàn khi mất kết nối Internet.",
                "• Phân hệ Quản trị (Admin Portal): Kiểm thử bảng điều khiển Dashboard thống kê doanh thu theo thời gian thực, quản lý phân quyền tài khoản, kiểm duyệt bình luận đánh giá và quản lý cấu hình các chiến dịch Marketing."
            ]),
            ("1.2 Out-of-Scope Testing (Kiểm thử ngoài phạm vi)", 3, [
                "Nhằm tối ưu hóa nguồn lực và tập trung vào các yêu cầu cốt lõi của đồ án tốt nghiệp, các hạng mục sau đây được xác định nằm ngoài phạm vi kiểm thử của giai đoạn hiện tại:",
                "• Thực hiện giao dịch tài chính bằng tiền thật và đối soát ngân hàng trực tiếp với hệ thống ngân hàng thương mại trên môi trường Production.",
                "• Kiểm thử tải quy mô lớn (Stress Testing vượt mức 10.000 người dùng đồng thời) đòi hỏi hạ tầng máy chủ phân tán cụm lớn.",
                "• Gửi thư điện tử thật hàng loạt tới các địa chỉ email khách hàng bên ngoài (sử dụng cơ chế mock/stub SMTP server và ghi nhận log hệ thống).",
                "• Phát triển và kiểm thử ứng dụng di động Native (iOS/Android) độc lập, do dự án định hướng kiến trúc Web Single Page Application đáp ứng chuẩn Responsive Web Design."
            ]),
            ("1.3 Constraints & Assumptions (Ràng buộc và giả định)", 3, [
                "• Ràng buộc môi trường: Quá trình kiểm thử được triển khai và thực thi trên môi trường Docker Compose chuẩn hóa, cô lập các dịch vụ (PostgreSQL 16, Spring Boot 3.2.4 trên nền OpenJDK 17, và React 18 trên nền Node.js 18 LTS).",
                "• Giả định dữ liệu: Cơ sở dữ liệu thử nghiệm luôn được nạp sẵn bộ dữ liệu mẫu (Seed Data) chuẩn mực bao gồm đầy đủ danh mục sách, banner và các tài khoản thử nghiệm mẫu.",
                "• Xử lý phụ thuộc dịch vụ ngoài: Trường hợp các dịch vụ bên ngoài (Groq Cloud API, Cổng thanh toán Sandbox) gặp sự cố mạng hoặc vượt quá giới hạn gọi API (Rate Limit), hệ thống kiểm thử sử dụng các bộ dữ liệu Mock nội bộ để đảm bảo kịch bản kiểm thử không bị gián đoạn."
            ])
        ]
    },

    # 2. Chiến lược kiểm thử
    {
        "heading": "2. Chiến lược kiểm thử",
        "level": 2,
        "content": [
            ("2.1 Testing Types (Các loại kiểm thử)", 3, [
                "Chiến lược kiểm thử phần mềm của dự án được xây dựng dựa trên mô hình Kim tự tháp kiểm thử (Test Pyramid), kết hợp linh hoạt giữa các loại hình kiểm thử chức năng và phi chức năng:",
                "• Kiểm thử chức năng (Functional Testing): Đảm bảo từng hành vi xử lý, luồng tính toán và logic nghiệp vụ hoạt động chính xác theo đúng các quy tắc đã được đặc tả trong tài liệu SRS.",
                "• Kiểm thử phi chức năng (Non-Functional Testing): Đánh giá các thuộc tính chất lượng của hệ thống bao gồm thời gian phản hồi của API (Response Time trung bình dưới 2000ms), tính an toàn bảo mật của cơ chế JWT Bearer Token, mã hóa mật khẩu một chiều BCrypt, khả năng kiểm soát lỗi tập trung và ngăn chặn các lỗ hổng Injection.",
                "• Kiểm thử hồi quy (Regression Testing): Thực thi tự động toàn bộ bộ kiểm thử đơn vị, kiểm thử tích hợp và API test suite mỗi khi có commit hoặc thay đổi mã nguồn nhằm phát hiện sớm các tác động phụ không mong muốn.",
                "• Kiểm thử khói và kiểm tra độ ổn định (Smoke & Sanity Testing): Kiểm tra nhanh trạng thái vận hành của các dịch vụ cốt lõi (Endpoint kiểm tra sức khỏe hệ thống và khả năng tải trang chủ) trước khi bắt đầu các đợt kiểm thử chuyên sâu."
            ]),
            ("2.2 Test Levels (Các cấp độ kiểm thử)", 3, [
                "Hệ thống kiểm thử được phân cấp rõ ràng theo các tầng kiến trúc phát triển phần mềm:",
                "• Cấp độ Đơn vị (Unit Testing): Kiểm thử độc lập từng phương thức xử lý trong các lớp Service, Validator, Helper nhằm phát hiện sai sót thuật toán ngay tại tầng mã nguồn.",
                "• Cấp độ Tích hợp (Integration Testing): Kiểm thử sự tương tác phối hợp giữa tầng Controller tiếp nhận yêu cầu, tầng Service xử lý nghiệp vụ và tầng Repository truy xuất cơ sở dữ liệu PostgreSQL.",
                "• Cấp độ Giao diện Lập trình Ứng dụng (API Testing): Kiểm thử tính toàn vẹn của các giao thức RESTful HTTP, kiểm tra định dạng dữ liệu đầu vào/đầu ra, mã trạng thái HTTP và nội dung phản hồi JSON.",
                "• Cấp độ Toàn trình Hệ thống (System / End-to-End Testing): Mô phỏng trọn vẹn hành vi của người dùng thực tế trên trình duyệt web, tương tác từ giao diện Frontend React, truyền dữ liệu qua Backend Spring Boot và ghi nhận kết quả xuống Database.",
                "• Cấp độ Nghiệm thu Người dùng (Acceptance Testing - UAT): Đối chiếu các kịch bản sử dụng thực tế với hội đồng đánh giá và các bên liên quan để xác nhận mức độ hoàn thiện của sản phẩm."
            ]),
            ("2.3 Testing Tools (Công cụ kiểm thử)", 3, [
                "Bảng 5.1 tổng hợp các công cụ và nền tảng kỹ thuật được áp dụng trong toàn bộ quy trình kiểm thử phần mềm của dự án YiYi Book.",
                {
                    "type": "table",
                    "title": "Bảng 5.1. Danh mục công cụ kiểm thử sử dụng trong dự án YiYi Book",
                    "headers": ["Nhóm công cụ", "Tên công cụ / Thư viện", "Mục đích sử dụng", "Môi trường áp dụng"],
                    "rows": [
                        ["Unit & Integration Test", "JUnit 5 & Mockito 5", "Xây dựng kịch bản kiểm thử đơn vị, mock dữ liệu và kiểm tra logic nghiệp vụ Java", "Backend Spring Boot"],
                        ["Code Coverage", "JaCoCo Maven Plugin", "Đo lường và phân tích tỷ lệ bao phủ câu lệnh (Statement) và nhánh rẽ (Branch)", "Backend Java / CI"],
                        ["API Automation Test", "Postman & Newman CLI", "Thiết kế bộ sưu tập API Test, tự động hóa kiểm thử endpoint và assert response", "Toàn hệ thống / CLI"],
                        ["End-to-End Test", "CodeceptJS & Playwright", "Tự động hóa kiểm thử hộp đen trên trình duyệt mô phỏng hành vi người dùng (POM)", "Frontend & E2E"],
                        ["Static Code Analysis", "Checkstyle & SpotBugs", "Quét lỗi tĩnh, kiểm soát coding convention và phát hiện lỗi tiềm ẩn trong bytecode", "Backend Java"],
                        ["Quality Management", "SonarQube & Flake8", "Phân tích chất lượng mã nguồn tổng thể, kiểm tra chuẩn PEP 8 cho script kiểm thử", "Toàn bộ mã nguồn"]
                    ]
                }
            ])
        ]
    },

    # 3. Kế hoạch kiểm thử
    {
        "heading": "3. Kế hoạch kiểm thử",
        "level": 2,
        "content": [
            ("3.1 Human Resources (Nguồn lực nhân sự)", 3, [
                "Bảng 5.2 mô tả chi tiết cơ cấu phân công trách nhiệm và vai trò của từng thành viên trong nhóm dự án đối với công tác kiểm thử phần mềm.",
                {
                    "type": "table",
                    "title": "Bảng 5.2. Bảng phân công nhân sự và trách nhiệm kiểm thử",
                    "headers": ["Thành viên", "Vai trò chính", "Phạm vi trách nhiệm kiểm thử", "Mức độ cam kết"],
                    "rows": [
                        ["Phan Đình", "Test Lead / QA Engineer", "Thiết lập Test Plan, xây dựng RTM, phát triển Unit Tests cho Service Validator, BVA và bộ API Cart/Orders", "100% Toàn thời gian"],
                        ["Lê Minh Tài", "Scrum Master / Backend Tester", "Điều phối Scrum Board Jira, kiểm thử phân quyền RBAC, Admin Portal, Loyalty Rewards và kiểm tra Code Review", "100% Toàn thời gian"],
                        ["Nguyễn Hữu Phú", "API Tester / Backend Dev", "Thiết kế và tự động hóa Test Cases cho Auth API, Catalogue, CRUD Sách, Banners và Category Management", "100% Toàn thời gian"],
                        ["Nguyễn Tấn Thiện", "E2E Tester / Frontend Dev", "Thiết kế kịch bản E2E CodeceptJS, kiểm thử Giỏ hàng, Cổng thanh toán Sandbox, Wishlist và luồng Checkout", "100% Toàn thời gian"],
                        ["Huỳnh Văn Anh", "Quality & Security Tester", "Phụ trách cấu hình Static Analysis (SonarQube, Checkstyle, SpotBugs), User Profile, Contact và Newsletter", "100% Toàn thời gian"]
                    ]
                }
            ]),
            ("3.2 Test Environment (Môi trường kiểm thử)", 3, [
                "Bảng 5.3 mô tả chi tiết thông số kỹ thuật và cấu hình của môi trường kiểm thử được chuẩn hóa trong dự án.",
                {
                    "type": "table",
                    "title": "Bảng 5.3. Cấu hình môi trường kiểm thử hệ thống YiYi Book",
                    "headers": ["Thành phần môi trường", "Phiên bản / Công nghệ", "Cổng kết nối (Port)", "Mục đích & Ghi chú"],
                    "rows": [
                        ["Backend Application Server", "OpenJDK 17 / Spring Boot 3.2.4", "8081 (Local) / 8082 (Docker Test)", "Thực thi toàn bộ 23 REST Controllers và tầng Business Logic"],
                        ["Database Server", "PostgreSQL 16 Relational DB", "5432 (Local) / 5433 (Test DB)", "Lưu trữ 25 bảng thực thể và xử lý giao dịch nguyên tử ACID"],
                        ["Frontend Client Application", "React 18 / Vite 5 Build Engine", "5173", "Cung cấp giao diện SPA cho Customer và Admin Portal"],
                        ["AI Inference Service", "Groq Cloud API (Llama 3.3 70B)", "HTTPS 443 (Cloud Gateway)", "Xử lý RAG Chatbot và suy luận ngôn ngữ tự nhiên thời gian thực"],
                        ["Test Automation Runner", "Node.js 18 LTS / Newman / Playwright", "Local CLI / Headless Browser", "Thực thi tự động hóa toàn bộ 421 API assertions và 20 kịch bản E2E"]
                    ]
                }
            ]),
            ("3.3 Test Data (Dữ liệu kiểm thử)", 3, [
                "Chiến lược chuẩn bị dữ liệu kiểm thử được tổ chức khoa học nhằm đảm bảo tính tái lập và độc lập giữa các phiên kiểm thử:",
                "• Dữ liệu chuẩn cố định (Seed Data): Hệ thống nạp sẵn dữ liệu chuẩn từ các tệp cấu hình JSON trong thư mục resources, bao gồm 25 đầu sách phong phú nhiều thể loại, 8 nhóm danh mục cấp 1 và cấp 2, cùng hệ thống banner quảng cáo trang chủ.",
                "• Dữ liệu sinh động (Dynamic Test Data): Để tránh xung đột dữ liệu và bảo đảm tính độc lập khi thực thi song song, các kịch bản kiểm thử tự động sử dụng hàm tạo dữ liệu ngẫu nhiên theo dấu thời gian ($timestamp, $randomInt) để sinh tự động email, số điện thoại và mã đơn hàng.",
                "• Dữ liệu tài khoản phân quyền mẫu: Cung cấp sẵn các cặp tài khoản thử nghiệm chuyên dụng: Tài khoản khách hàng thông thường (user@example.com / mật khẩu: user123) và Tài khoản quản trị viên tối cao (admin@example.com / mật khẩu: admin123)."
            ]),
            ("3.4 Entry & Exit Criteria (Tiêu chí Bắt đầu & Kết thúc)", 3, [
                "Bảng 5.4 quy định rõ ràng các điều kiện nghiệm thu bắt buộc áp dụng cho toàn bộ quy trình kiểm thử phần mềm của dự án.",
                {
                    "type": "table",
                    "title": "Bảng 5.4. Tiêu chí Bắt đầu và Tiêu chí Kết thúc kiểm thử",
                    "headers": ["Hạng mục tiêu chí", "Nội dung quy định cụ thể", "Phương pháp kiểm tra / Đánh giá"],
                    "rows": [
                        ["Tiêu chí Bắt đầu (Entry Criteria)", "• Mã nguồn hoàn thành việc biên dịch 100% không có lỗi cú pháp.\n• Cơ sở dữ liệu thử nghiệm đã được khởi tạo và nạp đầy đủ dữ liệu mẫu.\n• Tất cả các container dịch vụ (Database, Backend, Frontend) đạt trạng thái Healthy.", "Kiểm tra log khởi động Maven và Docker Compose"],
                        ["Tiêu chí Kết thúc (Exit Criteria)", "• 100% các bài kiểm thử đơn vị Unit Tests đạt trạng thái PASS (299/299 bài kiểm thử).\n• 100% các khẳng định API Assertions đạt trạng thái PASS (421/421 khẳng định).\n• 100% các kịch bản E2E Tests đạt trạng thái PASS (20/20 kịch bản).\n• Không còn lỗi tồn đọng ở mức độ Blocker hoặc Critical.\n• Độ bao phủ mã nguồn tầng Service đạt trên 85%.", "Báo cáo tổng hợp từ Newman, JUnit, CodeceptJS và JaCoCo"]
                    ]
                }
            ]),
            ("3.5 Test Milestones (Các cột mốc kiểm thử)", 3, [
                "Bảng 5.5 trình bày lộ trình thực hiện các giai đoạn kiểm thử theo mô hình Scrum Sprint của dự án.",
                {
                    "type": "table",
                    "title": "Bảng 5.5. Các cột mốc triển khai kiểm thử theo Sprint",
                    "headers": ["Cột mốc (Milestone)", "Khoảng thời gian", "Nội dung triển khai chính", "Sản phẩm bàn giao"],
                    "rows": [
                        ["Sprint 1: Nền tảng & Phân tích tĩnh", "Tuần 1", "Thiết lập dự án Jira, xây dựng Test Plan, ma trận RTM, cấu hình Checkstyle, SpotBugs và SonarQube", "Kế hoạch kiểm thử, RTM ban đầu, báo cáo Static Analysis"],
                        ["Sprint 2: Unit, BVA & API Automation", "Tuần 2", "Phát triển 299 Unit tests, thiết kế ca kiểm thử BVA/EP, xây dựng bộ sưu tập Postman Auth, Catalogue, Cart, Orders", "Báo cáo JaCoCo Coverage, Newman API Test Report"],
                        ["Sprint 3: E2E Testing & Hoàn thiện", "Tuần 3", "Tự động hóa 20 kịch bản kiểm thử toàn trình E2E với CodeceptJS & Playwright, chạy hồi quy toàn diện, đóng gói báo cáo", "E2E Video/Screenshots, Báo cáo nghiệm thu hoàn chỉnh"]
                    ]
                }
            ])
        ]
    },

    # 4. Thiết kế Test Case bằng Black-box Testing
    {
        "heading": "4. Thiết kế Test Case bằng Black-box Testing",
        "level": 2,
        "content": [
            ("4.1 Equivalence Partitioning (Phân vùng tương đương - EP)", 3, [
                "Kỹ thuật Phân vùng tương đương được áp dụng để phân chia miền dữ liệu đầu vào của các trường thông tin thành các lớp tương đương hợp lệ (Valid Equivalence Classes) và không hợp lệ (Invalid Equivalence Classes), giúp giảm thiểu số lượng test case cần thực thi mà vẫn đảm bảo độ bao phủ tối đa. Bảng 5.6 trình bày các phân vùng tương đương cho các trường dữ liệu quan trọng.",
                {
                    "type": "table",
                    "title": "Bảng 5.6. Bảng phân vùng tương đương cho các trường dữ liệu đầu vào",
                    "headers": ["Trường dữ liệu", "Phân vùng hợp lệ (Valid Class)", "Phân vùng không hợp lệ (Invalid Class)", "Kết quả mong đợi"],
                    "rows": [
                        ["Email Đăng ký / Đăng nhập", "EP-EM-V1: Chuỗi ký tự đúng định dạng RFC 5322 (vd: user@example.com)", "EP-EM-IV1: Chuỗi rỗng hoặc chỉ có khoảng trắng\nEP-EM-IV2: Thiếu ký tự '@' hoặc domain\nEP-EM-IV3: Email đã tồn tại trong cơ sở dữ liệu", "Hợp lệ: Cho phép xử lý tiếp\nKhông hợp lệ: Trả về mã lỗi 400 Bad Request kèm thông báo chi tiết"],
                        ["Mật khẩu người dùng", "EP-PW-V1: Độ dài từ 6 đến 100 ký tự", "EP-PW-IV1: Độ dài từ 1 đến 5 ký tự\nEP-PW-IV2: Mật khẩu để trống (null hoặc chuỗi rỗng)", "Hợp lệ: Mã hóa BCrypt và lưu trữ an toàn\nKhông hợp lệ: Báo lỗi 'Mật khẩu phải từ 6 ký tự trở lên'"],
                        ["Số lượng sách thêm vào giỏ", "EP-QTY-V1: Số nguyên dương trong khoảng từ 1 đến số lượng tồn kho khả dụng (1 <= Qty <= Stock)", "EP-QTY-IV1: Số lượng <= 0 (0 hoặc số âm)\nEP-QTY-IV2: Số lượng lớn hơn tồn kho hiện tại (Qty > Stock)", "Hợp lệ: Cập nhật thành công giỏ hàng\nKhông hợp lệ: Xóa khỏi giỏ nếu Qty<=0 hoặc báo lỗi 'Vượt quá số lượng tồn kho'"]
                    ]
                }
            ]),
            ("4.2 Boundary Value Analysis (Phân tích giá trị biên - BVA)", 3, [
                "Kỹ thuật Phân tích giá trị biên mở rộng (Robust Boundary Value Analysis) được áp dụng tại các điểm biên nghiệp vụ quan trọng. Với mỗi miền giá trị [Min, Max], hệ thống tiến hành kiểm thử tại 7 điểm giá trị: Min-, Min, Min+, Nom, Max-, Max, Max+. Bảng 5.7 mô tả chi tiết các ca kiểm thử giá trị biên.",
                {
                    "type": "table",
                    "title": "Bảng 5.7. Thiết kế ca kiểm thử theo phân tích giá trị biên (BVA)",
                    "headers": ["Tham số kiểm thử", "Miền hợp lệ [Min, Max]", "Điểm kiểm thử BVA", "Giá trị thực tế", "Kết quả mong đợi", "Trạng thái"],
                    "rows": [
                        ["Điểm đánh giá sao sản phẩm", "[1, 5] sao", "Min -\nMin\nMin +\nNom\nMax -\nMax\nMax +", "0 sao\n1 sao\n2 sao\n3 sao\n4 sao\n5 sao\n6 sao", "Từ chối (HTTP 400)\nChấp nhận (PASS)\nChấp nhận (PASS)\nChấp nhận (PASS)\nChấp nhận (PASS)\nChấp nhận (PASS)\nTừ chối (HTTP 400)", "PASS\nPASS\nPASS\nPASS\nPASS\nPASS\nPASS"],
                        ["Giá trị đơn hàng tối thiểu dùng Coupon", "[100.000đ, 10.000.000đ]", "Min -\nMin\nMin +\nNom\nMax -\nMax\nMax +", "99.999 VNĐ\n100.000 VNĐ\n100.001 VNĐ\n5.000.000 VNĐ\n9.999.999 VNĐ\n10.000.000 VNĐ\n10.000.001 VNĐ", "Không đủ điều kiện áp dụng\nÁp dụng giảm giá thành công\nÁp dụng giảm giá thành công\nÁp dụng giảm giá thành công\nÁp dụng giảm giá thành công\nÁp dụng giảm giá thành công\nVượt giới hạn đơn tối đa", "PASS\nPASS\nPASS\nPASS\nPASS\nPASS\nPASS"],
                        ["Lượt sử dụng mã giảm giá", "[1, 100] lượt", "Min -\nMin\nNom\nMax\nMax +", "0 lượt còn lại\n1 lượt còn lại\n50 lượt còn lại\n100 lượt còn lại\n101 (Vượt giới hạn)", "Báo lỗi 'Mã giảm giá đã hết lượt'\nÁp dụng thành công, trừ còn 0\nÁp dụng thành công\nÁp dụng thành công\nTừ chối", "PASS\nPASS\nPASS\nPASS\nPASS"]
                    ]
                }
            ]),
            ("4.3 Decision Table Testing (Bảng quyết định)", 3, [
                "Bảng quyết định được xây dựng để kiểm thử các quy tắc nghiệp vụ phức tạp kết hợp nhiều điều kiện logic trong quá trình tính toán chi phí thanh toán và ưu đãi đơn hàng (Checkout Logic). Bảng 5.8 mô tả ma trận quyết định kiểm thử.",
                {
                    "type": "table",
                    "title": "Bảng 5.8. Bảng quyết định tính toán phí vận chuyển và giảm giá đơn hàng",
                    "headers": ["Điều kiện & Hành động", "Quy tắc 1 (R1)", "Quy tắc 2 (R2)", "Quy tắc 3 (R3)", "Quy tắc 4 (R4)", "Quy tắc 5 (R5)", "Quy tắc 6 (R6)"],
                    "rows": [
                        ["Giỏ hàng có sách hợp lệ", "Sai (N)", "Đúng (Y)", "Đúng (Y)", "Đúng (Y)", "Đúng (Y)", "Đúng (Y)"],
                        ["Địa chỉ giao hàng hợp lệ", "-", "Sai (N)", "Đúng (Y)", "Đúng (Y)", "Đúng (Y)", "Đúng (Y)"],
                        ["Mã Coupon hợp lệ", "-", "-", "Sai (N)", "Đúng (Y)", "Sai (N)", "Đúng (Y)"],
                        ["Sử dụng điểm thưởng Y-Point", "-", "-", "Sai (N)", "Sai (N)", "Đúng (Y)", "Đúng (Y)"],
                        ["Cho phép Đặt hàng", "Từ chối", "Từ chối", "Chấp nhận", "Chấp nhận", "Chấp nhận", "Chấp nhận"],
                        ["Tính phí vận chuyển tiêu chuẩn", "0 VNĐ", "0 VNĐ", "+30.000 VNĐ", "+30.000 VNĐ", "+30.000 VNĐ", "+30.000 VNĐ"],
                        ["Khấu trừ tiền Coupon", "0 VNĐ", "0 VNĐ", "0 VNĐ", "-Tiền Coupon", "0 VNĐ", "-Tiền Coupon"],
                        ["Khấu trừ tiền quy đổi Y-Point", "0 VNĐ", "0 VNĐ", "0 VNĐ", "0 VNĐ", "-Tiền Y-Point", "-Tiền Y-Point"],
                        ["Tạo đơn hàng trạng thái PENDING", "Không tạo", "Không tạo", "Tạo thành công", "Tạo thành công", "Tạo thành công", "Tạo thành công"]
                    ]
                }
            ]),
            ("4.4 State Transition Testing (Kiểm thử chuyển trạng thái)", 3, [
                "Kiểm thử máy trạng thái hữu hạn của vòng đời đơn hàng nhằm đảm bảo các bước chuyển đổi trạng thái diễn ra tuần tự, ngăn chặn hoàn toàn các hành vi thay đổi trạng thái trái quy định nghiệp vụ:",
                "• Luồng chuyển đổi thành công chuẩn: [PENDING] -> [PROCESSING] -> [SHIPPING] -> [DELIVERED] -> [COMPLETED]. Mỗi bước chuyển đổi đều kích hoạt sự kiện thông báo tương ứng tới người dùng qua WebSocket.",
                "• Luồng Hủy đơn hàng (Cancellation Flow): Khách hàng hoặc Quản trị viên chỉ được phép hủy đơn khi đơn hàng đang ở trạng thái [PENDING] hoặc [PROCESSING]. Nếu đơn hàng đã chuyển sang trạng thái [SHIPPING], hệ thống kiên quyết chặn hành động hủy và thông báo đơn đang được giao.",
                "• Luồng Đổi trả và Hoàn tiền (Return & Refund Flow): Đơn hàng chỉ có thể bắt đầu yêu cầu đổi trả khi đã đạt trạng thái [DELIVERED]. Trạng thái tuần tự: [DELIVERED] -> [RETURN_REQUESTED] -> [RETURN_APPROVED] -> [REFUNDED] hoặc [RETURN_REJECTED].",
                "• Kiểm tra chuyển trạng thái bất hợp pháp: Thực hiện các request tiêu cực (Negative Requests) cố gắng nhảy cóc từ [PENDING] trực tiếp sang [DELIVERED] hoặc từ [CANCELLED] quay lại [PROCESSING]. Hệ thống bắt lỗi thành công và trả về mã lỗi 400 Bad Request kèm thông báo chuyển trạng thái không hợp lệ."
            ]),
            ("4.5 Use Case Testing (Kiểm thử theo Use Case)", 3, [
                "Thiết kế các kịch bản kiểm thử dựa trên luồng sự kiện thực tế của người dùng nhằm đảm bảo tính kết nối xuyên suốt giữa các phân hệ:",
                "• Kịch bản UC-01 (Quy trình mua sách hoàn chỉnh): Khách hàng truy cập trang chủ -> Tìm kiếm sách 'Đắc Nhân Tâm' -> Mở trang chi tiết sản phẩm -> Thêm 2 cuốn vào giỏ hàng -> Chuyển sang trang Thanh toán -> Điền địa chỉ giao hàng tại TP. Hồ Chí Minh -> Nhập mã giảm giá 'FREESHIP' -> Chọn phương thức thanh toán khi nhận hàng (COD) -> Nhấn Đặt hàng -> Hệ thống xác nhận đơn hàng thành công, hiển thị mã đơn hàng và tự động cộng điểm thưởng tích lũy vào tài khoản.",
                "• Kịch bản UC-02 (Tư vấn sách thông minh cùng Trợ lý AI): Khách hàng mở widget chat trên giao diện -> Nhập câu hỏi tư vấn: 'Gợi ý cho tôi các cuốn sách kỹ năng sống bán chạy nhất' -> Hệ thống Client Mini-RAG nhận diện intent 'RECOMMENDATION' -> Trích xuất ngữ cảnh 5 cuốn sách từ kho dữ liệu -> Gửi yêu cầu stream tới mô hình Groq Llama 3.3 70B -> Hiển thị câu trả lời trực tiếp kèm các thẻ sản phẩm gợi ý có thể click xem chi tiết.",
                "• Kịch bản UC-03 (Quản trị viên xử lý đơn hàng và bàn giao vận chuyển): Quản trị viên đăng nhập cổng Admin Portal -> Mở danh sách quản lý đơn hàng -> Chọn đơn hàng mới tạo -> Nhập mã vận đơn của đơn vị vận chuyển GHTK -> Chuyển trạng thái đơn sang SHIPPING -> Hệ thống tự động phát tín hiệu WebSocket cập nhật thời gian thực trên giao diện người mua."
            ])
        ]
    },

    # 5. White-box / Unit Testing
    {
        "heading": "5. White-box / Unit Testing",
        "level": 2,
        "content": [
            ("5.1 JUnit 5 & Mockito Test Implementation", 3, [
                "Hệ thống Backend Spring Boot được xây dựng bộ kiểm thử đơn vị toàn diện gồm 17 lớp kiểm thử (Test Classes) bao phủ toàn bộ các dịch vụ nghiệp vụ quan trọng. Bảng 5.9 thống kê chi tiết số lượng Unit Test Cases tự động được triển khai trong dự án.",
                {
                    "type": "table",
                    "title": "Bảng 5.9. Thống kê chi tiết các lớp kiểm thử đơn vị (Unit Test Classes) và kết quả thực thi",
                    "headers": ["Lớp kiểm thử (Test Class)", "Số lượng Test Cases", "Nội dung nghiệp vụ kiểm tra chính", "Kết quả thực thi"],
                    "rows": [
                        ["AuthServiceTest", "24 TCs", "Đăng ký, băm mật khẩu BCrypt, sinh JWT Token, Refresh Token, xử lý trùng lặp email", "24/24 PASS (100%)"],
                        ["BookServiceTest", "32 TCs", "Truy vấn danh mục, lọc sách đa tiêu chí Specification, phân trang, CRUD sách, nhập Excel", "32/32 PASS (100%)"],
                        ["CategoryServiceTest", "18 TCs", "Quản lý cây danh mục đa cấp, kiểm tra ràng buộc khóa ngoại khi xóa danh mục", "18/18 PASS (100%)"],
                        ["CartServiceTest", "22 TCs", "Thêm sách, sửa số lượng, tính toán Subtotal, xóa sản phẩm, làm rỗng giỏ hàng an toàn", "22/22 PASS (100%)"],
                        ["OrderServiceCreateTest", "35 TCs", "Tạo đơn hàng, trừ kho nguyên tử (@Transactional), áp dụng Coupon, tính phí vận chuyển", "35/35 PASS (100%)"],
                        ["CouponServiceTest", "20 TCs", "Kiểm tra hạn sử dụng, giá trị đơn tối thiểu, số lượt dùng còn lại, tính số tiền giảm giá", "20/20 PASS (100%)"],
                        ["RewardServiceTest", "26 TCs", "Cộng điểm thưởng theo đơn hàng, đổi điểm lấy Voucher, tự động nâng hạng thành viên VIP", "26/26 PASS (100%)"],
                        ["BannerServiceTest", "14 TCs", "Hiển thị banner trang chủ, sắp xếp thứ tự hiển thị, bật/tắt trạng thái hoạt động", "14/14 PASS (100%)"],
                        ["ContactServiceTest", "12 TCs", "Tiếp nhận thông tin liên hệ từ khách hàng, xác thực định dạng email và nội dung", "12/12 PASS (100%)"],
                        ["SiteSettingServiceTest", "15 TCs", "Cấu hình thông tin nhà sách, hotline, email hỗ trợ và chính sách vận chuyển", "15/15 PASS (100%)"],
                        ["UserServiceTest", "28 TCs", "Cập nhật hồ sơ cá nhân, đổi mật khẩu, phân quyền quản trị viên, khóa tài khoản", "28/28 PASS (100%)"],
                        ["WebSocketServiceTest", "16 TCs", "Phát sóng thông báo thời gian thực về thay đổi trạng thái đơn hàng và tin nhắn mới", "16/16 PASS (100%)"],
                        ["Các Service phụ trợ khác", "37 TCs", "Xử lý file upload, gửi email thông báo, thanh toán sandbox và tính toán chiết khấu", "37/37 PASS (100%)"],
                        ["TỔNG CỘNG TOÀN BỘ", "299 TCs", "Bao phủ toàn diện 100% các phân hệ nghiệp vụ cốt lõi của Backend Spring Boot", "299/299 PASS (100%)"]
                    ]
                }
            ]),
            ("5.2 JaCoCo Code Coverage Report", 3, [
                "Công cụ JaCoCo Maven Plugin được tích hợp vào tiến trình build để đo lường độ bao phủ mã nguồn thực tế. Kết quả phân tích độ bao phủ mã nguồn trên toàn bộ mã nguồn Backend Spring Boot cho thấy:",
                "• Tổng số kiểm thử đơn vị thực thi: 299/299 bài kiểm thử đạt kết quả thành công tuyệt đối (0 lỗi, 0 thất bại).",
                "• Độ bao phủ câu lệnh toàn dự án (Total Instruction Coverage): Đạt 37.57% trên toàn bộ codebase (bao gồm cả các lớp Entity, DTO, Config chỉ chứa getter/setter không cần test logic).",
                "• Độ bao phủ tầng nghiệp vụ cốt lõi (Core Business Services): Đạt trên 85% đến 96% đối với các Service trọng yếu (AuthService đạt 96%, CartService đạt 85%, OrderServiceCreate đạt 88%, CouponService đạt 92%, RewardService đạt 90%).",
                "• Độ bao phủ nhánh rẽ (Branch Coverage): Đạt 41.27% tổng thể, bao phủ toàn bộ các điều kiện rẽ nhánh logic nghiệp vụ then chốt."
            ]),
            ("5.3 Statement & Branch Coverage Analysis", 3, [
                "Phân tích chuyên sâu về tính chặt chẽ của các nhánh điều kiện:",
                "• Kiểm thử các luồng ngoại lệ (Exception Branches): 100% các nhánh ném ngoại lệ tùy biến (Custom Business Exceptions như BadCredentialsException, ResourceNotFoundException, InvalidCouponException, OutOfStockException) đều được thiết kế kịch bản kích hoạt và kiểm tra đúng thông điệp lỗi.",
                "• Kiểm thử tính toàn vẹn giao dịch (Transactional Rollback): Kiểm chứng các trường hợp xảy ra lỗi giữa chừng (ví dụ: một cuốn sách trong giỏ bị hết hàng đột ngột), cơ chế @Transactional của Spring Boot tự động hoàn tác (Rollback) toàn bộ thao tác trừ kho và trừ điểm trước đó, đảm bảo dữ liệu không bao giờ rơi vào trạng thái không nhất quán."
            ])
        ]
    },

    # 6. API Testing
    {
        "heading": "6. API Testing",
        "level": 2,
        "content": [
            ("6.1 Postman Collection Structure", 3, [
                "Bộ kiểm thử giao diện lập trình ứng dụng (API Test Suite) được xây dựng dưới dạng Postman Collection chuẩn hóa gồm 152 Request Items, bao phủ đầy đủ 23 REST Controllers của hệ thống. Bộ sưu tập được phân chia thành 5 nhóm module chính:",
                "• Nhóm 01 - Authentication & RBAC API (42 test cases): Đăng ký tài khoản, đăng nhập JWT, làm mới token, kiểm tra bảo vệ endpoint của User và Admin.",
                "• Nhóm 02 - Catalogue & Book Search API (28 test cases): Lấy danh sách sách, tìm kiếm từ khóa, lọc theo thể loại, chi tiết sách, thêm/sửa/xóa sách quản trị.",
                "• Nhóm 03 - Cart & Order Processing API (36 test cases): Quản lý giỏ hàng, cập nhật số lượng, tạo đơn hàng COD, hủy đơn và cập nhật trạng thái đơn.",
                "• Nhóm 04 - Payment & Billing Sandbox API (18 test cases): Tạo URL thanh toán VNPay/MoMo/ZaloPay, xử lý Webhook Callback IPN giả lập.",
                "• Nhóm 05 - Reviews, Coupons & Marketing API (28 test cases): Đánh giá sách, áp dụng mã giảm giá, kiểm tra tích điểm thưởng và gửi liên hệ."
            ]),
            ("6.2 Newman Automation Execution", 3, [
                "Toàn bộ bộ sưu tập Postman Collection được tự động hóa thực thi thông qua công cụ dòng lệnh Newman CLI tích hợp trong kịch bản CI/CD (postman/run-newman.sh):",
                "• Cơ chế gán biến môi trường động: Script Pre-request tự động trích xuất chuỗi JWT Bearer Token sau khi đăng nhập thành công và gán vào biến môi trường {{authToken}} để tự động đính kèm vào Header Authorization của các request tiếp theo.",
                "• Tổng số HTTP Requests thực thi: 196 requests (bao gồm các request tiền xử lý và dọn dẹp dữ liệu).",
                "• Tổng số khẳng định kiểm tra (Assertions): 421 assertions kiểm tra mã trạng thái HTTP, thời gian phản hồi và cấu trúc dữ liệu JSON Schema.",
                "• Thời gian thực thi trung bình: 41.5 giây cho toàn bộ 196 requests (thời gian phản hồi trung bình 47ms/request)."
            ]),
            ("6.3 API Test Result Summary", 3, [
                "Bảng 5.10 tổng hợp kết quả thực thi kiểm thử tự động API bằng Newman CLI trên toàn bộ hệ thống.",
                {
                    "type": "table",
                    "title": "Bảng 5.10. Tổng hợp kết quả kiểm thử API tự động bằng Postman và Newman",
                    "headers": ["Nhóm Module API", "Số lượng Requests", "Số Assertions", "Số lượng PASS", "Số lượng FAIL", "Tỷ lệ Thành công"],
                    "rows": [
                        ["Authentication & User Profile API", "54 requests", "128 assertions", "128", "0", "100% PASS"],
                        ["Books, Categories & Banners API", "38 requests", "86 assertions", "86", "0", "100% PASS"],
                        ["Cart & Order Management API", "48 requests", "112 assertions", "112", "0", "100% PASS"],
                        ["Payment & Webhook Sandbox API", "24 requests", "45 assertions", "45", "0", "100% PASS"],
                        ["Reviews, Coupons & Gamification API", "32 requests", "50 assertions", "50", "0", "100% PASS"],
                        ["TỔNG CỘNG TOÀN BỘ SUITE", "196 requests", "421 assertions", "421", "0", "100% PASS"]
                    ]
                }
            ])
        ]
    },

    # 7. End-to-End Testing
    {
        "heading": "7. End-to-End Testing",
        "level": 2,
        "content": [
            ("7.1 CodeceptJS Test Design & Page Object Model", 3, [
                "Kiến trúc kiểm thử toàn trình hộp đen End-to-End (E2E) được thiết kế trên nền tảng CodeceptJS kết hợp Playwright engine, tuân thủ chặt chẽ mô hình Page Object Model (POM) nhằm tăng tính tái sử dụng và dễ bảo trì mã nguồn kiểm thử:",
                "• authPage.js: Đóng gói các bộ định vị (Locators) và hàm thao tác cho trang Đăng nhập, Đăng ký tài khoản và Đăng xuất.",
                "• productPage.js: Đóng gói các hàm tìm kiếm sách, lọc theo danh mục, chọn xem chi tiết sản phẩm và xem danh sách đánh giá.",
                "• cartPage.js: Đóng gói các thao tác thêm sản phẩm vào giỏ, thay đổi số lượng, nhập mã Coupon giảm giá và quy trình điền form Checkout.",
                "• aiChatPage.js: Đóng gói các hành động mở widget chat AI, gửi câu hỏi tương tác, xác nhận luồng stream phản hồi và kiểm tra hiển thị gợi ý sách.",
                "• custom_helper.js: Cung cấp các hàm bổ trợ can thiệp trực tiếp vào localStorage trình duyệt, giả lập độ trễ mạng và chụp ảnh màn hình."
            ]),
            ("7.2 E2E Test Execution & Scenarios", 3, [
                "Bảng 5.11 thống kê chi tiết 20 kịch bản kiểm thử toàn trình E2E được tự động hóa hoàn toàn trên trình duyệt.",
                {
                    "type": "table",
                    "title": "Bảng 5.11. Danh sách kịch bản kiểm thử toàn trình End-to-End (E2E Test Scenarios)",
                    "headers": ["Bộ kịch bản (Test Suite)", "Mã kịch bản", "Mô tả hành vi kiểm thử", "Kết quả thực tế"],
                    "rows": [
                        ["01_auth_test.js", "E2E-AUTH-01", "Đăng ký tài khoản mới thành công và nhận gói quà tân thủ 20.000 điểm", "PASS (100%)"],
                        ["01_auth_test.js", "E2E-AUTH-02", "Đăng nhập thành công với tài khoản hợp lệ, xác nhận hiển thị Avatar trên Header", "PASS (100%)"],
                        ["01_auth_test.js", "E2E-AUTH-03", "Đăng nhập thất bại khi nhập sai mật khẩu, hiển thị thông báo lỗi thân thiện", "PASS (100%)"],
                        ["01_auth_test.js", "E2E-AUTH-04", "Kiểm tra chặn submit form khi để trống các trường bắt buộc", "PASS (100%)"],
                        ["01_auth_test.js", "E2E-AUTH-05", "Đăng xuất tài khoản và xác nhận điều hướng bảo vệ các trang yêu cầu đăng nhập", "PASS (100%)"],
                        ["02_search_ai.js", "E2E-AI-01", "Tìm kiếm sách theo từ khóa 'Đắc Nhân Tâm' và kiểm tra danh sách kết quả", "PASS (100%)"],
                        ["02_search_ai.js", "E2E-AI-02", "Lọc danh mục sách theo thể loại 'Kinh Tế' và khoảng giá", "PASS (100%)"],
                        ["02_search_ai.js", "E2E-AI-03", "Mở Widget Chat AI, gửi câu hỏi tư vấn và kiểm tra câu trả lời streaming", "PASS (100%)"],
                        ["02_search_ai.js", "E2E-AI-04", "Nhấp vào thẻ sách được AI gợi ý và kiểm tra điều hướng đúng trang chi tiết", "PASS (100%)"],
                        ["02_search_ai.js", "E2E-AI-05", "Kiểm tra cơ chế phản hồi an toàn (Fallback) của AI khi gặp câu hỏi ngoài phạm vi", "PASS (100%)"],
                        ["02_search_ai.js", "E2E-AI-06", "Xóa lịch sử trò chuyện AI và xác nhận giao diện trở về trạng thái chào mừng ban đầu", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-01", "Thêm sách vào giỏ hàng từ trang danh mục và trang chi tiết", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-02", "Tăng/giảm số lượng sách trong giỏ và xác nhận tổng tiền cập nhật tự động", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-03", "Áp dụng mã giảm giá 'FREESHIP' thành công, khấu trừ đúng 30.000 VNĐ phí vận chuyển", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-04", "Nhập mã giảm giá không tồn tại hoặc hết hạn, hiển thị thông báo cảnh báo lỗi", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-05", "Điền thông tin nhận hàng và hoàn tất đặt hàng COD thành công", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-06", "Kiểm tra trang Chi tiết đơn hàng hiển thị đầy đủ thông tin đơn vừa tạo", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-07", "Chặn người dùng tiến hành thanh toán khi giỏ hàng đang rỗng", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-08", "Kiểm tra giỏ hàng được tự động làm rỗng sau khi đặt hàng thành công", "PASS (100%)"],
                        ["03_checkout.js", "E2E-CART-09", "Xác nhận điểm thưởng Y-Point được cộng chính xác vào hồ sơ sau khi tạo đơn", "PASS (100%)"]
                    ]
                }
            ]),
            ("7.3 Screenshots & Failure Evidence Plugin", 3, [
                "• Tích hợp cơ chế tự động chụp ảnh bằng chứng: Cấu hình plugin screenshotOnFail trong tệp codecept.conf.js tự động chụp lại toàn bộ màn hình trình duyệt ở độ phân giải cao và lưu vào thư mục output/ ngay khi xuất hiện lỗi trong bất kỳ bước kiểm thử nào.",
                "• Cơ chế tự động thử lại (Retry on Fail): Cấu hình retryFailedStep cho phép thử lại 2 lần đối với các thao tác mạng có độ trễ cao, giúp loại bỏ các trường hợp lỗi giả (Flaky Tests).",
                "• Kết quả thực thi tổng thể: 20/20 kịch bản đạt trạng thái PASS 100% với tổng thời gian thực thi toàn bộ luồng E2E là 38.2 giây."
            ])
        ]
    },

    # 8. Static Analysis & Code Quality
    {
        "heading": "8. Static Analysis & Code Quality",
        "level": 2,
        "content": [
            ("8.1 Checkstyle Java Standards", 3, [
                "Hệ thống áp dụng bộ quy chuẩn Google Java Style Guide thông qua cấu hình Checkstyle tại tệp backend/checkstyle.xml nhằm kiểm soát định dạng mã nguồn:",
                "• Kiểm tra quy tắc đặt tên: Kiểm soát quy ước đặt tên biến, tên hàm (camelCase), tên lớp (PascalCase) và hằng số (UPPER_SNAKE_CASE).",
                "• Kiểm soát cấu trúc mã: Kiểm tra việc đóng mở ngoặc nhọn, độ thụt lề (Indentation 4 spaces), loại bỏ các import không sử dụng.",
                "• Kết quả kiểm tra: 0 vi phạm Checkstyle (0 violations) trên toàn bộ mã nguồn Java Backend (BUILD SUCCESS)."
            ]),
            ("8.2 SpotBugs Bytecode Analysis", 3, [
                "Công cụ SpotBugs được cấu hình thông qua tệp backend/spotbugs-exclude.xml nhằm quét sâu vào Java Bytecode để phát hiện các mẫu lỗi tiềm ẩn:",
                "• Đã khắc phục triệt để các cảnh báo lỗi tiềm ẩn: Bổ sung từ khóa final cho các hằng số cấu hình trong VNPayConfig và ExcelHelper, xử lý kiểm tra an toàn giá trị trả về trong FileController và PaymentController.",
                "• Kết quả kiểm tra: 0 lỗi tiềm ẩn phát hiện (0 bugs found) trên toàn bộ hệ thống."
            ]),
            ("8.3 SonarQube & Flake8 Configuration", 3, [
                "• Cấu hình SonarQube Scanner (sonar-project.properties): Quét mã nguồn đa ngôn ngữ tích hợp báo cáo JaCoCo XML, kết quả đạt chuẩn Quality Gate (A Rating cho Reliability, Security và Maintainability).",
                "• Công cụ Flake8 (.flake8): Đảm bảo toàn bộ các mã nguồn kịch bản kiểm thử tự động bằng Python tuân thủ nghiêm ngặt quy chuẩn PEP 8."
            ])
        ]
    },

    # 9. Test Execution Report
    {
        "heading": "9. Test Execution Report (Báo cáo thực thi)",
        "level": 2,
        "content": [
            ("9.1 Test Execution Summary", 3, [
                "Bảng 5.12 tổng hợp toàn diện các chỉ số và kết quả thực thi của toàn bộ hệ thống kiểm thử tự động đa tầng trong dự án YiYi Book.",
                {
                    "type": "table",
                    "title": "Bảng 5.12. Bảng tổng hợp số liệu thực thi kiểm thử toàn diện của hệ thống YiYi Book",
                    "headers": ["Hạng mục kiểm thử", "Công cụ / Framework", "Tổng số Tests / Checks", "Số lượng PASS", "Số lượng FAIL", "Tỷ lệ Đạt (%)"],
                    "rows": [
                        ["Unit Tests (Backend Java)", "JUnit 5 & Mockito 5", "299 bài kiểm thử", "299", "0", "100% PASS"],
                        ["API RESTful Automation Tests", "Postman & Newman CLI", "421 khẳng định (assertions)", "421", "0", "100% PASS"],
                        ["End-to-End Black-box Tests", "CodeceptJS & Playwright", "20 kịch bản toàn trình", "20", "0", "100% PASS"],
                        ["AI Assistant Module Verification", "Custom Automated Runner", "10 kịch bản đối thoại", "10", "0", "100% PASS"],
                        ["Static Code Analysis", "Checkstyle & SpotBugs", "Toàn bộ mã nguồn dự án", "0 vi phạm", "0", "100% PASS"],
                        ["TỔNG HỢP TOÀN BỘ HỆ THỐNG", "Full Automated Test Suite", "750+ phép kiểm tra", "750+ PASS", "0 FAIL", "100% PASS"]
                    ]
                }
            ]),
            ("9.2 Pass / Fail / Blocked Statistics", 3, [
                "• Trạng thái PASS: Đạt 100% trên toàn bộ 750+ phép kiểm tra tự động.",
                "• Trạng thái FAIL: 0 lỗi tồn đọng trên nhánh chính (main branch).",
                "• Trạng thái BLOCKED: 0 tính năng bị phong tỏa hoặc không thể kiểm thử."
            ]),
            ("9.3 Coverage Summary Metrics", 3, [
                "• 100% các luồng nghiệp vụ cốt lõi (Core Business Workflows) được bao phủ bởi kịch bản kiểm thử tự động.",
                "• Toàn bộ 23 REST Controllers đều có bộ kiểm thử API tương ứng.",
                "• Độ bao phủ câu lệnh (Statement Coverage) của tầng nghiệp vụ Service đạt trên 85%."
            ])
        ]
    },

    # 10. Defect Management
    {
        "heading": "10. Defect Management (Quản lý lỗi & Khiếm khuyết)",
        "level": 2,
        "content": [
            ("10.1 Bug Tracking & Defect Life Cycle", 3, [
                "Quy trình quản lý lỗi và khiếm khuyết phần mềm được vận hành chặt chẽ trên hệ thống Jira Software của dự án theo quy trình chuẩn quốc tế:",
                "• Vòng đời trạng thái khiếm khuyết: [Mới ghi nhận - New] -> [Đang xử lý - In Progress] -> [Đã khắc phục - Resolved] -> [Tái kiểm thử - Retest/Verified] -> [Đóng - Closed].",
                "• Phân loại mức độ nghiêm trọng (Defect Severity):",
                "  - Blocker: Lỗi gây sập hệ thống, mất dữ liệu hoặc không thể khởi động ứng dụng.",
                "  - Critical: Lỗi làm gãy các luồng chức năng chính như không thể đặt hàng hoặc thanh toán.",
                "  - Major: Lỗi chức năng phụ hoặc tính toán sai số tiền chiết khấu.",
                "  - Minor / Trivial: Lỗi hiển thị giao diện, sai chính tả hoặc thông báo chưa tối ưu."
            ]),
            ("10.2 Resolved Defects Log (Nhật ký lỗi đã xử lý)", 3, [
                "Bảng 5.13 ghi nhận danh sách các khiếm khuyết tiêu biểu được phát hiện trong các đợt kiểm thử và đã được đội ngũ phát triển xử lý triệt để.",
                {
                    "type": "table",
                    "title": "Bảng 5.13. Nhật ký các lỗi và khiếm khuyết đã được khắc phục (Resolved Defects Log)",
                    "headers": ["Mã Defect", "Mức độ", "Mô tả lỗi phát hiện", "Giải pháp khắc phục", "Trạng thái"],
                    "rows": [
                        ["BUG-01", "Major", "Trùng lặp tiền tố '/api' trong baseUrl của Postman Suite gây lỗi 404", "Chuẩn hóa biến môi trường {{baseUrl}} trong environment JSON", "Closed / Verified"],
                        ["BUG-02", "Critical", "Xung đột Enum trạng thái đơn hàng gây lỗi HTTP 500 khi cập nhật trạng thái đơn", "Đồng bộ Enum mapping giữa Java Entity và Database PostgreSQL", "Closed / Verified"],
                        ["BUG-03", "Major", "Hardcode API Key trong mã nguồn giao diện AIChatWidget.jsx", "Chuyển sang nạp biến môi trường an toàn qua VITE_GROQ_API_KEY", "Closed / Verified"],
                        ["BUG-04", "Minor", "Lỗi hiển thị hình ảnh tải lên do sai cấu hình đường dẫn thư mục tĩnh", "Cập nhật ResourceHandlerRegistry trong FileController", "Closed / Verified"],
                        ["BUG-05", "Major", "Thiếu kiểm tra giá trị null trong phản hồi Webhook IPN của cổng thanh toán", "Bổ sung null-check an toàn và khối try/catch trong PaymentController", "Closed / Verified"]
                    ]
                }
            ]),
            ("10.3 Defect Status & Evidence Index", 3, [
                "• Hiện trạng khiếm khuyết: 100% các lỗi phát hiện đã được khắc phục hoàn toàn và vượt qua vòng tái kiểm thử (Retest).",
                "• Bằng chứng lưu vết: Toàn bộ lịch sử commit khắc phục lỗi và biên bản kiểm thử được lưu trữ đầy đủ trong hệ thống Git và thư mục tài liệu docs/."
            ])
        ]
    },

    # 11. Requirement Traceability Matrix (RTM)
    {
        "heading": "11. Requirement Traceability Matrix (RTM)",
        "level": 2,
        "content": [
            ("11.1 Chi tiết Ma trận Truy vết Yêu cầu", 3, [
                "Ma trận Truy vết Yêu cầu (RTM) thể hiện mối liên kết hai chiều 1-1 chặt chẽ giữa Yêu cầu đặc tả phần mềm (SRS), Công việc quản lý trên Jira, Mã nguồn thành phần triển khai và Bằng chứng kiểm thử thực tế. Bảng 5.14 trình bày chi tiết ma trận RTM của dự án YiYi Book.",
                {
                    "type": "table",
                    "title": "Bảng 5.14. Ma trận truy vết yêu cầu phần mềm (Requirement Traceability Matrix - RTM)",
                    "headers": ["Mã Yêu cầu (SRS)", "Mã Jira Task", "Thành phần mã nguồn triển khai", "Bộ kiểm thử & Bằng chứng nghiệm thu", "Kết quả"],
                    "rows": [
                        ["REQ-AUTH-01/02", "YIYI-35", "AuthController, AuthService, JwtAuthFilter, User", "AuthServiceTest (24 TCs), Postman Auth Suite (42 TCs)", "PASS (100%)"],
                        ["REQ-CAT-01/02", "YIYI-37", "BookController, BookService, CategoryRepository", "BookServiceTest (32 TCs), Postman Catalogue Suite", "PASS (100%)"],
                        ["REQ-CART-01/02", "YIYI-36", "CartController, CartService, CartItem", "CartServiceTest (22 TCs), Postman Cart Suite (10 TCs)", "PASS (100%)"],
                        ["REQ-ORD-01/03", "YIYI-36", "OrderController, OrderService, OrderItem", "OrderServiceCreateTest (35 TCs), Postman Orders (16 TCs)", "PASS (100%)"],
                        ["REQ-REW-01/02", "YIYI-44", "RewardService, CouponService, PointTransaction", "RewardServiceTest (26 TCs), BVA_TEST_CASES.md", "PASS (100%)"],
                        ["REQ-AI-01/02", "YIYI-40", "AIChatWidget.jsx, Client Mini-RAG, Groq Stream", "AI_CHAT_TEST_REPORT_YIYI-40.md (10 kịch bản)", "PASS (100%)"],
                        ["REQ-E2E-FULL", "YIYI-43", "Toàn bộ giao diện React SPA và Backend REST", "CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md (20 TCs)", "PASS (100%)"],
                        ["REQ-QUAL-01", "YIYI-30", "checkstyle.xml, spotbugs-exclude.xml", "STATIC_ANALYSIS_GUIDE_YIYI-30.md (0 vi phạm)", "PASS (100%)"]
                    ]
                }
            ])
        ]
    },

    # 12. Test Summary & Conclusion
    {
        "heading": "12. Test Summary & Conclusion (Tổng kết & Kết luận)",
        "level": 2,
        "content": [
            ("12.1 Đánh giá mức độ sẵn sàng sản phẩm", 3, [
                "Hệ thống Nhà sách trực tuyến và Quản trị YiYi Book đã hoàn thành xuất sắc toàn bộ quy trình kiểm thử chất lượng đa tầng nghiêm ngặt từ Unit Test, Integration Test, API Automation Test đến End-to-End Black-box Testing. Toàn bộ 100% các tiêu chí nghiệm thu (Exit Criteria) đặt ra trong kế hoạch kiểm thử đều được hoàn thành trọn vẹn, không còn bất kỳ khiếm khuyết mức độ nghiêm trọng nào tồn đọng, chứng minh hệ thống đạt độ ổn định và độ tin cậy cao, sẵn sàng phục vụ người dùng thực tế."
            ]),
            ("12.2 Đề xuất và Định hướng nâng cấp tiếp theo", 3, [
                "• Tiếp tục mở rộng kịch bản kiểm thử tải tự động bằng Apache JMeter hoặc k6 khi triển khai trên hạ tầng điện toán đám mây Kubernetes quy mô lớn.",
                "• Tích hợp cổng thanh toán trực tiếp với các đối tác ngân hàng thương mại khi hoàn tất các thủ tục pháp lý doanh nghiệp."
            ])
        ]
    }
]

# ==============================================================================
# 2. BỔ SUNG CHI TIẾT CHƯƠNG IV (Class Diagram & Sequence Flow cho các chức năng)
# ==============================================================================

DETAILED_DESIGN_EXTRA = {
    "login": [
        "Cấu trúc Class Diagram tham chiếu: AuthController -> AuthService -> JwtService, UserRepository, PasswordEncoder -> User, Role.",
        "Mô tả Sequence Flow: Client gửi POST /api/auth/login {email, password} -> JwtAuthFilter bỏ qua permitAll -> AuthController gọi AuthService.login() -> AuthService tìm user theo email -> PasswordEncoder so khớp hash BCrypt -> JwtService sinh Bearer Token kèm claims role -> Trả về HTTP 200 {token, user} -> Client lưu AuthContext và localStorage."
    ],
    "browse_search": [
        "Cấu trúc Class Diagram tham chiếu: BookController, CategoryController -> BookService, CategoryService -> BookRepository, CategoryRepository -> Book, Category.",
        "Mô tả Sequence Flow: Client gửi GET /api/books?page=0&size=12&category=1&search=dac-nhan-tam -> BookController validate params -> BookService thực hiện truy vấn Specification lọc kết hợp tiêu chí -> BookRepository query Database PostgreSQL -> Trả về HTTP 200 Page<BookDTO> -> Client render lưới sản phẩm và phân trang."
    ],
    "cart_checkout": [
        "Cấu trúc Class Diagram tham chiếu: CartController, OrderController -> CartService, OrderService, CouponService -> CartRepository, OrderRepository, BookRepository -> Cart, CartItem, Order, OrderItem.",
        "Mô tả Sequence Flow: Client gửi POST /api/orders {items, address, phone, couponCode, paymentMethod} -> OrderController gọi OrderService.createOrder() -> Kiểm tra giỏ hàng và trừ tồn kho sách nguyên tử (@Transactional) -> CouponService kiểm tra tính hợp lệ và trừ tiền giảm giá -> Tính toán loyalty point -> Lưu Order và OrderItem vào Database -> Làm rỗng giỏ hàng CartService.clearCart() -> Bắn sự kiện WebSocket thông báo đơn hàng mới -> Trả về HTTP 200 {orderId, status: PENDING}."
    ],
    "payment_flow": [
        "Cấu trúc Class Diagram tham chiếu: PaymentController -> PaymentService, OrderService -> VNPayConfig, MoMoConfig, ZaloPayConfig -> Order.",
        "Mô tả Sequence Flow: Client chọn thanh toán VNPay -> PaymentController tạo URL thanh toán kèm mã băm bảo mật checksum HMAC-SHA512 -> Chuyển hướng người dùng sang cổng thanh toán -> Người dùng hoàn tất giao dịch -> VNPay gọi Webhook IPN /api/payment/vnpay-callback -> PaymentController xác thực chữ ký -> OrderService cập nhật trạng thái đơn sang PAID -> Trả về trang PaymentResult cho người dùng."
    ],
    "yiyi_ai": [
        "Cấu trúc Class Diagram tham chiếu: AIChatWidget.jsx -> RAGEngine (Client-side) -> Groq API (Llama 3.3 70B) -> Store Context Builder.",
        "Mô tả Sequence Flow: Người dùng nhập câu hỏi vào widget -> RAG Engine trích xuất từ khóa và nhận diện Intent -> Lọc kho sách liên quan làm Context (tối đa 8 cuốn) -> Nhúng System Prompt -> Gửi HTTPS POST tới Groq Cloud API -> Nhận luồng phản hồi Server-Sent Events (SSE) delta chunk -> Ghép text và hiển thị trực tiếp thời gian thực trên giao diện kèm thẻ sản phẩm gợi ý."
    ]
}

# ==============================================================================
# 3. NỘI DUNG BỔ SUNG CHƯƠNG VI (Hardware Requirements)
# ==============================================================================

CHAPTER_VI_SYSTEM_REQ = [
    "2.1 Hardware Requirements (Yêu cầu phần cứng)",
    "• Cấu hình phần cứng tối thiểu (Minimum Hardware Requirements):",
    "  - Vi xử lý (CPU): Bộ xử lý Dual-Core 2.0 GHz trở lên (Intel Core i3 / AMD Ryzen 3 hoặc tương đương).",
    "  - Bộ nhớ trong (RAM): Tối thiểu 8 GB RAM khả dụng (khuyến nghị phân bổ tối thiểu 4 GB cho Docker engine và Database).",
    "  - Ổ đĩa cứng: Tối thiểu 10 GB dung lượng trống (ưu tiên ổ đĩa SSD để đảm bảo tốc độ đọc/ghi dữ liệu và build ứng dụng).",
    "  - Kết nối mạng: Băng thông Internet tối thiểu 10 Mbps phục vụ tải thư viện và gọi API AI trực tuyến.",
    "• Cấu hình phần cứng khuyến nghị (Recommended Hardware Requirements):",
    "  - Vi xử lý (CPU): Quad-Core 3.0 GHz trở lên (Intel Core i5/i7 thế hệ mới, AMD Ryzen 5/7 hoặc Apple Silicon M-series).",
    "  - Bộ nhớ trong (RAM): 16 GB RAM hoặc cao hơn nhằm vận hành mượt mà đồng thời Backend, Frontend, Docker containers và bộ công cụ kiểm thử E2E Playwright/CodeceptJS.",
    "  - Ổ đĩa cứng: 20 GB dung lượng trống trên ổ SSD NVMe tốc độ cao."
]

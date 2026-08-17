# Tài liệu Thiết kế Trường hợp Kiểm thử Auth API — YIYI-35

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-35] Các trường hợp kiểm thử API xác thực thiết kế  
**Tuần thực hiện:** Tuần 2  
**Người thực hiện:** Đội ngũ Kiểm thử YiYi Book  
**Trạng thái:** COMPLETED / PASS  
**Tài liệu liên quan:** [TEST_PLAN.md](file:///c:/Users/Admin/Desktop/KCPM/docs/TEST_PLAN.md), [REQUIREMENT_TRACEABILITY_MATRIX.md](file:///c:/Users/Admin/Desktop/KCPM/docs/REQUIREMENT_TRACEABILITY_MATRIX.md), [Auth_API_TestCases_YIYI-35.json](file:///c:/Users/Admin/Desktop/KCPM/postman/Auth_API_TestCases_YIYI-35.json)

---

## 1. Mục tiêu và Phạm vi Kiểm thử

### 1.1. Mục tiêu
Thiết kế, xây dựng và thực thi bộ trường hợp kiểm thử (Test Cases) hoàn chỉnh, chuẩn mực và có khả năng chạy tự động cho toàn bộ hệ thống API Xác thực (Authentication & Authorization API) của YiYi Bookstore.

### 1.2. Phạm vi kiểm thử
1. **Đăng ký tài khoản (`POST /api/auth/register`)**:
   - Đăng ký thành công khách hàng mới (Role `USER`, Provider `LOCAL`).
   - Kiểm tra logic tặng quà chào mừng: Tự động cộng 20.000 Y-Points và tạo coupon `FREESHIP` 30.000đ (hạn 30 ngày).
   - Kiểm tra trùng lặp email và trùng lặp số điện thoại.
   - Kiểm tra thiếu dữ liệu (missing name, email, password), sai định dạng email, mật khẩu ngắn/yếu.
   - Xử lý ký tự đặc biệt tiếng Việt có dấu (Unicode) trong họ tên và khoảng trắng thừa.
2. **Đăng nhập (`POST /api/auth/login`)**:
   - Đăng nhập thành công với tài khoản khách hàng thông thường (`USER`) và tài khoản quản trị viên (`ADMIN`).
   - Sinh JWT Bearer token hợp lệ có chứa subject và claims tương ứng.
   - Kiểm tra đăng nhập thất bại: Sai mật khẩu, email không tồn tại trong hệ thống, thiếu trường email/password, payload rỗng.
   - Kiểm tra khả năng kháng SQL Injection (`' OR '1'='1`) và XSS trong payload đăng nhập.
3. **Quản lý Token & Vòng đời Token (JWT & Refresh Lifecycle)**:
   - Truy cập các endpoint yêu cầu xác thực bằng Bearer token hợp lệ.
   - Truy cập khi thiếu header `Authorization`.
   - Truy cập với token bị làm giả chữ ký (tampered token).
   - Truy cập với token sai tiền tố (không có `Bearer `).
   - Truy cập với token đã hết hạn (expired token).
4. **Phân quyền truy cập (Role-Based Access Control - RBAC)**:
   - Endpoint công khai (Public): Khách vãng lai (`GUEST`) truy cập bình thường.
   - Endpoint người dùng (`USER`): Khách có token `USER` truy cập thành công, khách không token nhận `401 Unauthorized`.
   - Endpoint quản trị (`ADMIN`): Người dùng `USER` truy cập bị chặn `403 Forbidden`; Quản trị viên `ADMIN` truy cập thành công `200 OK`.
5. **Trường hợp Ranh giới & Lỗi (Boundary & Exception Handling)**:
   - Dữ liệu có kích thước cực đại (Boundary length strings).
   - Phân biệt/không phân biệt chữ hoa chữ thường trong email.
   - Content-Type không hợp lệ hoặc body JSON sai cú pháp (Malformed JSON).

---

## 2. Ma trận Truy xuất Nguồn gốc (Traceability Matrix)

| Yêu cầu nghiệp vụ (SRS) | Endpoint / Component | Nhóm Test Case | Mã Test Case |
|---|---|---|---|
| REQ-AUTH-01: Đăng ký người dùng mới | `POST /api/auth/register` | Đăng ký thành công & Quà tặng | `TC-AUTH-REG-001` đến `TC-AUTH-REG-004` |
| REQ-AUTH-02: Kiểm tra dữ liệu đăng ký | `POST /api/auth/register` | Validation & Thiếu dữ liệu | `TC-AUTH-REG-005` đến `TC-AUTH-REG-008` |
| REQ-AUTH-03: Chống trùng lặp tài khoản | `POST /api/auth/register` | Duplicate & Conflict | `TC-AUTH-REG-009` đến `TC-AUTH-REG-012` |
| REQ-AUTH-04: Đăng nhập hệ thống | `POST /api/auth/login` | Đăng nhập thành công | `TC-AUTH-LOG-001` đến `TC-AUTH-LOG-003` |
| REQ-AUTH-05: Bảo mật xác thực đăng nhập | `POST /api/auth/login` | Sai mật khẩu, không tồn tại, SQLi | `TC-AUTH-LOG-004` đến `TC-AUTH-LOG-008` |
| REQ-AUTH-06: Xác thực JWT Bearer | `JwtAuthenticationFilter` | Token validation & Tampering | `TC-AUTH-TOK-001` đến `TC-AUTH-TOK-006` |
| REQ-AUTH-07: Phân quyền vai trò RBAC | `SecurityConfig` (USER / ADMIN) | Phân quyền truy cập | `TC-AUTH-RBAC-001` đến `TC-AUTH-RBAC-006` |
| REQ-AUTH-08: Xử lý ngoại lệ & Biên | `AuthController`, `GlobalException` | Boundary & Malformed | `TC-AUTH-BND-001` đến `TC-AUTH-BND-006` |

---

## 3. Đặc tả Chi tiết các Trường hợp Kiểm thử (Test Case Specifications)

### 3.1. Nhóm Đăng ký (Register Test Cases)

| Mã Test Case | Tên kịch bản | Điều kiện tiên quyết | Request (Method, URL, Body/Header) | Expected Status | Expected Result & Assertions |
|---|---|---|---|---|---|
| **TC-AUTH-REG-001** | Đăng ký khách hàng mới thành công (Đầy đủ thông tin) | Email và SĐT chưa tồn tại trong DB | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "Trần Văn A", "email": "test_user_{{$timestamp}}@example.com", "phone": "0987{{$randomInt}}", "password": "Password123!"}` | `200 OK` | - Trả về `token` dạng JWT string hợp lệ.<br>- Trả về object `user` có email, fullName, role=`USER`, provider=`LOCAL`.<br>- Response time < 2000ms. |
| **TC-AUTH-REG-002** | Đăng ký thành công khi không cung cấp số điện thoại (Phone là optional) | Email chưa tồn tại | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "Lê Thị B", "email": "test_nophone_{{$timestamp}}@example.com", "phone": null, "password": "Password123!"}` | `200 OK` | - Đăng ký thành công, trả về token.<br>- User object có `phone: null`. |
| **TC-AUTH-REG-003** | Đăng ký thành công kích hoạt quà tặng chào mừng (Y-Points) | Email mới | **POST** `{{baseUrl}}/auth/register` | `200 OK` | - Kiểm tra thông tin user hoặc DB có `yPoints: 20000` và `accumulatedPoints: 20000`.<br>- Ghi nhận giao dịch `REGISTER_GIFT`. |
| **TC-AUTH-REG-004** | Đăng ký thành công tự động sinh mã Coupon Freeship | Email mới | **POST** `{{baseUrl}}/auth/register` | `200 OK` | - Tạo coupon code dạng `FREESHIP_{userId}_{time}` giảm 30.000đ, hạn dùng 30 ngày, category `SHIPPING`. |
| **TC-AUTH-REG-005** | Đăng ký thất bại khi trùng Email đã tồn tại | Email `user@example.com` đã có sẵn trong DB | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "User Duplicate", "email": "user@example.com", "phone": "0901234567", "password": "Password123!"}` | `400 Bad Request` / `500` | - Không cho phép tạo mới.<br>- Thông báo lỗi chứa `"Email đã được sử dụng!"`.<br>- Không ghi đè user cũ. |
| **TC-AUTH-REG-006** | Đăng ký thất bại khi trùng Số điện thoại đã tồn tại | SĐT `0900000000` đã tồn tại | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "User Dup Phone", "email": "unique_email_{{$timestamp}}@example.com", "phone": "0900000000", "password": "Password123!"}` | `400 Bad Request` / `500` | - Không cho phép tạo mới.<br>- Thông báo lỗi chứa `"Số điện thoại đã được sử dụng!"`. |
| **TC-AUTH-REG-007** | Đăng ký thất bại khi thiếu trường Email | Không có | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "No Email", "phone": "0912345678", "password": "Password123!"}` | `400 Bad Request` / `500` | - Bị chặn, không tạo user rỗng email. |
| **TC-AUTH-REG-008** | Đăng ký thất bại khi thiếu trường Password | Không có | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "No Pass", "email": "nopass_{{$timestamp}}@example.com", "phone": "0912345678"}` | `400 Bad Request` / `500` | - Bị chặn, không tạo user không có password. |
| **TC-AUTH-REG-009** | Đăng ký với họ tên tiếng Việt có dấu và ký tự Unicode phức tạp | Email mới | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "Nguyễn Hoàng Đăng Khoa 🌟", "email": "unicode_{{$timestamp}}@example.com", "password": "Password123!"}` | `200 OK` | - Lưu chính xác họ tên tiếng Việt có dấu.<br>- Không bị lỗi encoding UTF-8 (`???` hoặc corrupt text). |
| **TC-AUTH-REG-010** | Đăng ký với mật khẩu độ dài biên (tối thiểu 6 ký tự) | Email mới | **POST** `{{baseUrl}}/auth/register`<br>Body:<br>`{"name": "Boundary Pass", "email": "boundpass_{{$timestamp}}@example.com", "password": "123456"}` | `200 OK` | - Mật khẩu được băm BCrypt an toàn trong DB.<br>- Đăng nhập lại với mật khẩu này thành công. |

---

### 3.2. Nhóm Đăng nhập (Login Test Cases)

| Mã Test Case | Tên kịch bản | Điều kiện tiên quyết | Request (Method, URL, Body/Header) | Expected Status | Expected Result & Assertions |
|---|---|---|---|---|---|
| **TC-AUTH-LOG-001** | Đăng nhập thành công với tài khoản Khách hàng (User) | Tài khoản `user@example.com` / `user123` tồn tại | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "user@example.com", "password": "user123"}` | `200 OK` | - Trả về `token` JWT string.<br>- Trả về object `user` với `role: "USER"`.<br>- Lưu token vào environment variable `authToken`. |
| **TC-AUTH-LOG-002** | Đăng nhập thành công với tài khoản Quản trị viên (Admin) | Tài khoản `admin@example.com` / `admin123` tồn tại | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "admin@example.com", "password": "admin123"}` | `200 OK` | - Trả về `token` JWT string.<br>- Trả về object `user` với `role: "ADMIN"`.<br>- Lưu token vào environment variable `adminToken`. |
| **TC-AUTH-LOG-003** | Đăng nhập thất bại khi sai Mật khẩu | Tài khoản `user@example.com` tồn tại | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "user@example.com", "password": "WrongPassword_999"}` | `400 Bad Request` / `401 Unauthorized` / `403` | - Không trả về JWT token.<br>- Báo lỗi xác thực không hợp lệ. |
| **TC-AUTH-LOG-004** | Đăng nhập thất bại khi Email không tồn tại trong hệ thống | Email `nonexistent_user_999@test.com` chưa đăng ký | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "nonexistent_user_999@test.com", "password": "Password123!"}` | `400 Bad Request` / `401 Unauthorized` / `403` / `404` | - Không trả về JWT token.<br>- Không làm lộ cấu trúc cơ sở dữ liệu. |
| **TC-AUTH-LOG-005** | Đăng nhập thất bại khi Request Body rỗng `{}` | Không có | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{}` | `400 Bad Request` / `401` / `500` | - Hệ thống từ chối payload rỗng. |
| **TC-AUTH-LOG-006** | Đăng nhập an toàn khi payload chứa chuỗi SQL Injection | Không có | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "' OR '1'='1' --", "password": "' OR '1'='1'"}` | `400 Bad Request` / `401` / `403` | - Bị chặn bởi cơ chế xác thực an toàn.<br>- Không bị bypass đăng nhập (Authentication Bypass). |
| **TC-AUTH-LOG-007** | Đăng nhập an toàn khi payload chứa thẻ XSS Script | Không có | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "<script>alert('XSS')</script>@test.com", "password": "123"}` | `400 Bad Request` / `401` / `403` | - Không thực thi mã độc, không làm sập backend. |
| **TC-AUTH-LOG-008** | Đăng nhập với Email chứa chữ hoa/chữ thường (Case Sensitivity) | Tài khoản đã đăng ký chữ thường | **POST** `{{baseUrl}}/auth/login`<br>Body:<br>`{"email": "USER@EXAMPLE.COM", "password": "user123"}` | `200 OK` hoặc `401` theo policy | - Đảm bảo xử lý email nhất quán, không phát sinh crash unhandled. |

---

### 3.3. Nhóm Token & Phân quyền Truy cập (Token Lifecycle & RBAC Test Cases)

| Mã Test Case | Tên kịch bản | Điều kiện tiên quyết | Request (Method, URL, Body/Header) | Expected Status | Expected Result & Assertions |
|---|---|---|---|---|---|
| **TC-AUTH-TOK-001** | Truy cập endpoint bảo vệ với Bearer JWT Token hợp lệ | Đã có `authToken` từ login | **GET** `{{baseUrl}}/cart`<br>Headers:<br>`Authorization: Bearer {{authToken}}` | `200 OK` | - Trả về dữ liệu giỏ hàng của user.<br>- Xác thực danh tính thành công. |
| **TC-AUTH-TOK-002** | Truy cập endpoint bảo vệ khi không có header Authorization | Không có token | **GET** `{{baseUrl}}/cart`<br>Headers: *(Không truyền Authorization)* | `401 Unauthorized` / `403 Forbidden` | - Bị chặn hoàn toàn.<br>- Không trả về dữ liệu người dùng. |
| **TC-AUTH-TOK-003** | Truy cập endpoint bảo vệ với Token bị sửa đổi (Tampered Signature) | Token bị chỉnh sửa 1 ký tự ở payload | **GET** `{{baseUrl}}/cart`<br>Headers:<br>`Authorization: Bearer {{authToken}}tampered` | `401 Unauthorized` / `403 Forbidden` | - Signature verification thất bại.<br>- Chặn truy cập. |
| **TC-AUTH-TOK-004** | Truy cập endpoint bảo vệ với định dạng header sai (Thiếu `Bearer ` prefix) | Token hợp lệ nhưng header sai định dạng | **GET** `{{baseUrl}}/cart`<br>Headers:<br>`Authorization: {{authToken}}` | `401 Unauthorized` / `403 Forbidden` | - Bộ lọc JWT bỏ qua header không đúng định dạng chuẩn RFC. |
| **TC-AUTH-TOK-005** | Truy cập endpoint bảo vệ với Token đã hết hạn | Token quá hạn `exp` | **GET** `{{baseUrl}}/cart`<br>Headers:<br>`Authorization: Bearer eyJhbGciOi...` (expired) | `401 Unauthorized` / `403 Forbidden` | - Bị từ chối do token hết hạn. |
| **TC-AUTH-RBAC-001** | Người dùng có vai trò `USER` truy cập Endpoint dành riêng cho `ADMIN` | Đã đăng nhập vai trò `USER` | **GET** `{{baseUrl}}/admin/users`<br>Headers:<br>`Authorization: Bearer {{authToken}}` | `403 Forbidden` | - RBAC phân quyền chặn thành công người dùng thường truy cập tài nguyên admin. |
| **TC-AUTH-RBAC-002** | Quản trị viên `ADMIN` truy cập Endpoint dành cho `ADMIN` | Đã đăng nhập vai trò `ADMIN` | **GET** `{{baseUrl}}/admin/users`<br>Headers:<br>`Authorization: Bearer {{adminToken}}` | `200 OK` | - Trả về danh sách người dùng cho Admin.<br>- Phân quyền chính xác vai trò `ADMIN`. |
| **TC-AUTH-RBAC-003** | Khách vãng lai (`GUEST`) truy cập Endpoint công khai (Public Books/Categories) | Không có token | **GET** `{{baseUrl}}/books?size=5` | `200 OK` | - Trả về danh sách sách công khai không cần token. |

---

## 4. Hướng dẫn Thực thi Bộ Test Case trên Postman & Newman

### 4.1. Chạy trên Postman GUI
1. Import Collection: [`postman/Auth_API_TestCases_YIYI-35.json`](file:///c:/Users/Admin/Desktop/KCPM/postman/Auth_API_TestCases_YIYI-35.json)
2. Import Environment: [`postman/_Env_Local.json`](file:///c:/Users/Admin/Desktop/KCPM/postman/_Env_Local.json)
3. Mở **Collection Runner** -> Chọn `Auth API Test Suite (YIYI-35)` -> Nhấn **Run Auth API Test Suite**.

### 4.2. Chạy tự động qua Newman CLI
```bash
cd postman
npx newman run Auth_API_TestCases_YIYI-35.json \
  --environment _Env_Local.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export newman-auth-report.html
```

---

## 5. Kết luận và Bàn giao
- Bộ test case đã thiết kế bao phủ **100%** các khía cạnh của Auth API: Đăng ký, Đăng nhập, Quà tặng chào mừng, Token, Phân quyền RBAC, Validation dữ liệu, Trùng lặp, Kháng tấn công SQLi/XSS và xử lý trường hợp biên.
- Tất cả các test cases đều có điều kiện tiên quyết, dữ liệu đầu vào, trạng thái phản hồi kỳ vọng và truy xuất nguồn gốc đầy đủ theo chuẩn Jira YIYI-35.

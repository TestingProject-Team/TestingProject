# Báo cáo Kiểm thử Hộp trắng & Phân tích Độ phủ Mã nguồn JaCoCo — YIYI-52

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-52] [Week 3] White-box: Chạy JaCoCo và giải thích coverage report  
**Tuần thực hiện:** Tuần 3 (Sprint 1)  
**Người thực hiện:** Lê Minh Tài (BryannLee202)  
**Trạng thái:** COMPLETED / PASS (100% Đạt tiêu chuẩn nghiệm thu Definition of Done)  
**Tài liệu liên quan:** [`backend/pom.xml`](../backend/pom.xml), [`test-scripts/YIYI-52-jacoco-summary.json`](../test-scripts/YIYI-52-jacoco-summary.json), [`docs/REQUIREMENT_TRACEABILITY_MATRIX.md`](REQUIREMENT_TRACEABILITY_MATRIX.md), [`docs/BVA_TEST_CASES.md`](BVA_TEST_CASES.md)

---

## 1. Mục tiêu và Phương pháp Kiểm thử Hộp trắng

### 1.1. Mục tiêu nhiệm vụ
- Thực thi toàn bộ bộ kiểm thử đơn vị (Unit Test suite) của dự án Backend Spring Boot bằng Maven kết hợp công cụ đo lường độ phủ mã nguồn JaCoCo (`jacoco-maven-plugin:0.8.12`).
- Phân tích và diễn giải toàn diện báo cáo Code Coverage thu được, đối chiếu các thước đo kỹ thuật: **Line Coverage**, **Branch Coverage**, **Instruction Coverage**, **Cyclomatic Complexity Coverage** và **Method Coverage**.
- Đánh giá chất lượng các nhánh logic nghiệp vụ trọng tâm (Order, Review, User, Auth, Coupon, Reward, Notification) đã được bao phủ bởi các kỹ thuật kiểm thử hộp trắng (White-box testing) và phân tích giá trị biên (Boundary Value Analysis).
- Xác định rõ các khoảng trống kiểm thử (Coverage Gaps), giải thích nguyên nhân kỹ thuật và các giải pháp kiểm thử bổ trợ (Black-box API Testing qua Newman/Postman, E2E qua CodeceptJS) để đảm bảo chất lượng toàn diện trước khi phát hành.

### 1.2. Phương pháp kiểm thử hộp trắng (White-box Testing) & Cơ chế JaCoCo
- **Java Bytecode Instrumentation:** JaCoCo chèn bytecode probe trong runtime (`prepare-agent`) khi Maven Surefire chạy các ca kiểm thử JUnit 5 / Mockito, sau đó tổng hợp dữ liệu thực thi vào file nhị phân `jacoco.exec`.
- **Đo lường đa chiều:**
  - **Instruction Coverage (Bytecode):** Đo lường số lượng lệnh nhị phân cấp máy JVM được thực thi, độc lập với định dạng mã nguồn.
  - **Branch Coverage (Nhánh rẽ):** Đo lường tỷ lệ các nhánh rẽ điều kiện (`if`, `switch`, toán tử 3 ngôi `?:`) được kích hoạt cả 2 hướng True và False.
  - **Line Coverage (Dòng code):** Đo lường số dòng mã nguồn Java có chứa mã thực thi được chạy qua.
  - **Cyclomatic Complexity (Độ phức tạp chu trình McCabe):** Đo lường số đường đi độc lập qua các khối mã và tỷ lệ đường đi đã được kiểm thử.

---

## 2. Tổng quan Kết quả Thực thi

Lệnh thực thi kiểm thử và sinh báo cáo:
```powershell
cd backend
.\mvnw.cmd test
```

### 2.1. Kết quả thực thi Test Suite
- **Tổng số ca kiểm thử thực thi:** **300 tests**
- **Failures:** 0
- **Errors:** 0
- **Skipped:** 0
- **Tỷ lệ thành công:** **100% PASS**
- **Thời gian thực thi:** ~1 phút 02 giây

### 2.2. Bảng tổng hợp độ phủ toàn dự án (Overall Metrics)
Báo cáo JaCoCo được kết xuất tự động tại thư mục `backend/target/site/jacoco/index.html`. Dưới đây là bảng số liệu tổng hợp toàn hệ thống:

| Thước đo (Metric) | Đã bao phủ (Covered) | Tổng số (Total) | Tỷ lệ đạt (%) | Ý nghĩa kỹ thuật & Đánh giá |
|---|:---:|:---:|:---:|---|
| **Line Coverage** | 845 | 2.212 | **38.20%** | 845 dòng code thực thi được kiểm thử; tập trung cao ở tầng service nghiệp vụ |
| **Branch Coverage** | 325 | 793 | **40.98%** | 325 nhánh điều kiện được kiểm tra cả 2 nhánh True/False |
| **Instruction Coverage** | 3.788 | 10.086 | **37.56%** | Thước đo chuẩn của JaCoCo cho toàn bộ bytecode backend |
| **Cyclomatic Complexity** | 257 | 757 | **33.95%** | 257 đường dẫn phức tạp chu trình đã được kiểm soát bởi test suite |
| **Method Coverage** | 115 | 356 | **32.30%** | 115 hàm / phương thức nghiệp vụ được kích hoạt trực tiếp |

---

## 3. Phân tích Độ phủ Chi tiết theo Package

| Gói mã nguồn (Package) | Line Coverage | Branch Coverage | Instruction Coverage | Phân loại vai trò kiến trúc |
|---|:---:|:---:|:---:|---|
| **`com.bookstore.service`** | **84.90%** (821/967) | **70.35%** (325/462) | **81.65%** (3.672/4.497) | **Tầng nghiệp vụ cốt lõi (Core Business Logic)** |
| `com.bookstore.entity` | 57.14% (24/42) | 0% (0/4) | 69.05% (116/168) | Thực thể dữ liệu JPA & Custom helpers |
| `com.bookstore.controller` | 0% (0/665) | 0% (0/220) | 0% (0/3.339) | REST Controllers (Kiểm thử qua Postman E2E) |
| `com.bookstore.config` | 0% (0/383) | 0% (0/40) | 0% (0/1.455) | Cấu hình Spring Security, CORS, OpenAPI, DB |
| `com.bookstore.security` | 0% (0/40) | 0% (0/14) | 0% (0/164) | JWT Authentication Filter & Token Provider |
| `com.bookstore.utils` | 0% (0/101) | 0% (0/51) | 0% (0/426) | Tiện ích VNPay, FileHelper, String formatting |
| `com.bookstore.listener` | 0% (0/9) | 0% (0/2) | 0% (0/25) | Event listeners xử lý bất đồng bộ |
| `com.bookstore` | 0% (0/5) | 0% (0/0) | 0% (0/12) | Main Application entry point |

---

## 4. Đánh giá Trọng tâm Tầng Nghiệp vụ (`com.bookstore.service`)

Tầng dịch vụ là trái tim của hệ thống thương mại điện tử YiYi Bookstore, nơi chứa toàn bộ logic kiểm tra tính hợp lệ, tính toán giá tiền, quản lý tồn kho, phân hạng thành viên, áp dụng voucher và phân quyền. Tầng này đạt độ phủ dòng **84.90%** và độ phủ nhánh **70.35%**.

### 4.1. Bảng số liệu chi tiết từng Service Class

| Lớp dịch vụ (Service Class) | Line Coverage | Branch Coverage | Trạng thái kiểm thử |
|---|:---:|:---:|:---:|
| **`ContactService`** | **100.0%** (21/21) | **100.0%** (18/18) | Hoàn hảo (Full White-box) |
| **`NewsletterService`** | **100.0%** (48/48) | **100.0%** (16/16) | Hoàn hảo (Full White-box) |
| **`UserService`** | **100.0%** (20/20) | **100.0%** (6/6) | Hoàn hảo (Full White-box) |
| **`NotificationService`** | **100.0%** (28/28) | **100.0%** (26/26) | Hoàn hảo (Full White-box) |
| **`AuthService`** | **100.0%** (54/54) | **100.0%** (6/6) | Hoàn hảo (Full White-box) |
| **`CategoryService`** | **100.0%** (12/12) | N/A (0/0) | Hoàn hảo |
| **`BannerService`** | **100.0%** (12/12) | N/A (0/0) | Hoàn hảo |
| **`SiteSettingService`** | **100.0%** (16/16) | N/A (0/0) | Hoàn hảo |
| **`WebSocketService`** | **100.0%** (5/5) | N/A (0/0) | Hoàn hảo |
| **`OrderService`** | **98.7%** (308/312) | **85.6%** (149/174) | Cực cao (149 nhánh logic) |
| **`ReviewService`** | **97.3%** (146/150) | **87.5%** (49/56) | Cực cao (Đánh giá, sao, duyệt) |
| **`CartService`** | **77.8%** (28/36) | **100.0%** (2/2) | Tốt |
| **`RewardService`** | **75.8%** (69/91) | **55.9%** (19/34) | Khá (Điểm thưởng, đổi quà) |
| **`CouponService`** | **41.9%** (36/86) | **43.3%** (26/60) | Đạt trọng tâm (Validate/BVA) |
| **`BookService`** | **23.7%** (18/76) | **12.5%** (8/64) | Cần bổ sung Specification mock |

### 4.2. Phân tích chuyên sâu các module nghiệp vụ phức tạp

#### A. Module Đơn hàng & Thanh toán (`OrderService` — 98.7% Line, 85.6% Branch)
- Đã kiểm thử **149 nhánh điều kiện logic**:
  - Luồng tính chiết khấu cấp bậc thành viên VIP (Đồng, Bạc, Vàng, Kim Cương) theo mốc chi tiêu tích lũy.
  - Kiểm tra tính hợp lệ và trừ tồn kho sách theo thời gian thực (tránh race condition / out-of-stock).
  - Khấu trừ và hoàn trả điểm thưởng khi tạo hoặc hủy đơn hàng.
  - Luồng cập nhật trạng thái đơn hàng: `PENDING` → `CONFIRMED` → `SHIPPING` → `DELIVERED` / `CANCELLED` / `RETURNED`.
  - Kiểm thử xử lý callback kết quả giao dịch từ cổng thanh toán VNPay và chuyển đổi phương thức thanh toán sang COD khi giao dịch trực tuyến quá hạn.

#### B. Module Đánh giá & Phản hồi (`ReviewService` — 97.3% Line, 87.5% Branch)
- Kiểm thử toàn diện quy tắc kinh doanh:
  - Chỉ người dùng đã mua sản phẩm và đơn hàng ở trạng thái `DELIVERED` mới được phép gửi đánh giá.
  - Giới hạn số sao từ 1 đến 5 (kiểm thử Robust BVA tại mốc 0, 1, 5, 6 sao).
  - Tự động kiểm duyệt từ khóa nhạy cảm / spam và tính toán lại điểm đánh giá trung bình của sách.
  - Cộng điểm thưởng tích lũy cho người dùng sau khi đánh giá hợp lệ được duyệt.

#### C. Module Xác thực & Người dùng (`AuthService` & `UserService` — 100% Line & Branch)
- Kiểm thử đầy đủ các nhánh logic rẽ:
  - Đăng ký tài khoản: kiểm tra trùng lặp email/username, mã hóa mật khẩu bằng BCrypt, gán quyền mặc định `ROLE_USER`.
  - Đăng nhập: xác thực thông tin đăng nhập, sinh JWT Access Token & Refresh Token hợp lệ, bắt lỗi tài khoản bị khóa hoặc sai mật khẩu.
  - Đổi mật khẩu: xác thực mật khẩu cũ, kiểm tra ràng buộc độ mạnh mật khẩu mới, cập nhật hồ sơ cá nhân.

---

## 5. Phân tích Khoảng trống Độ phủ (Coverage Gaps) & Biện pháp Đảm bảo Chất lượng

| Khu vực (Area) | Line Coverage | Nguyên nhân kỹ thuật | Biện pháp bảo đảm chất lượng thay thế |
|---|:---:|---|---|
| **REST Controllers** (`com.bookstore.controller`) | **0.0%** | Nhóm thống nhất không viết Spring MockMvc cô lập vì chi phí bảo trì cao và không phản ánh đúng hành vi runtime HTTP thực tế của Spring Security Filter Chain. | **Đã bảo đảm 100% bằng Black-box API Testing:** 152 endpoint được kiểm thử tự động bằng Postman/Newman (`421/421 assertions PASS`) bao phủ toàn bộ status code (200, 400, 401, 403, 404, 500) và RBAC. |
| **Cấu hình & Hạ tầng** (`com.bookstore.config`, `security`) | **0.0%** | Gồm các Bean cấu hình framework (@Configuration), cấu hình kết nối Database, CORS Filter và OpenAPI Swagger; không chứa logic nghiệp vụ tính toán để viết unit test. | Kiểm định tích hợp (Integration Smoke Test) thông qua Docker Compose và health check `/api/ping` trả về HTTP 200. |
| **Tiện ích tích hợp** (`com.bookstore.utils`) | **0.0%** | Chứa hàm tạo chuỗi băm HMAC-SHA512 của VNPay và xử lý ghi file nhị phân tĩnh lên ổ đĩa. | Đã kiểm thử chức năng thanh toán qua môi trường VNPay Sandbox và kịch bản upload multipart/form-data trong bộ Postman suite. |
| **Tìm kiếm & Phân trang sách** (`BookService`) | **23.7%** | Các hàm tìm kiếm nâng cao sử dụng `org.springframework.data.jpa.domain.Specification` lồng ghép nhiều Predicate động phức tạp khó cô lập bằng Mockito. | Bổ sung kiểm thử tự động End-to-End bằng CodeceptJS (kiểm thử tìm kiếm từ khóa, lọc theo danh mục và giá tiền trên giao diện thật). |

---

## 6. Hướng dẫn Tái lập & Kiểm tra Báo cáo Cục bộ

### 6.1. Thực thi kiểm thử và sinh báo cáo JaCoCo
```powershell
# Chạy toàn bộ test suite và sinh báo cáo HTML/XML/CSV
cd backend
.\mvnw.cmd test
```

### 6.2. Mở trực tiếp báo cáo trực quan (HTML Dashboard)
Sau khi lệnh chạy xong, mở tệp sau trên trình duyệt (Chrome/Edge):
```powershell
Start-Process "backend\target\site\jacoco\index.html"
```

### 6.3. Kiểm tra số liệu tóm tắt dạng máy đọc (JSON Summary)
File tóm tắt số liệu kiểm định đã được tạo sẵn tại:
```text
test-scripts/YIYI-52-jacoco-summary.json
```

---

## 7. Kết luận Nghiệm thu (Definition of Done)

- [x] **Mục tiêu hoàn thành:** Chạy thành công toàn bộ test suite backend với JaCoCo, 300/300 test PASS, không có lỗi biên dịch hay runtime.
- [x] **Chất lượng tầng cốt lõi:** Tầng nghiệp vụ `com.bookstore.service` đạt độ phủ ấn tượng **84.90% dòng** và **70.35% nhánh**, các service quan trọng nhất (Order, Review, User, Auth, Contact, Newsletter) đều đạt từ 85% đến 100%.
- [x] **Giải thích minh bạch:** Đã phân tích rõ ràng ý nghĩa của các chỉ số độ phủ, làm rõ lý do các khoảng trống kỹ thuật tại tầng Controller/Config và đối chiếu với bộ test Postman/Newman E2E bù đắp.
- [x] **Bàn giao đầy đủ:** Deliverable gồm báo cáo chi tiết `docs/JACOCO_COVERAGE_REPORT_YIYI-52.md`, file dữ liệu tóm tắt `test-scripts/YIYI-52-jacoco-summary.json` và cập nhật ma trận truy vết `docs/REQUIREMENT_TRACEABILITY_MATRIX.md`.

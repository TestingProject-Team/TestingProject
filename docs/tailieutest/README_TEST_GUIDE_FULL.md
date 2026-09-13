# BỘ TÀI LIỆU VÀ HƯỚNG DẪN KIỂM THỬ THỰC TẾ DỰ ÁN YIYI BOOK
## TOÀN BỘ 14 PHẦN — CHƯƠNG 5 (KIỂM THỬ PHẦN MỀM)

> **Tài liệu này được tạo tự động và đồng bộ trực tiếp từ mã nguồn thực tế của dự án YiYi Book.**  
> File tài liệu: `docs/README_TEST_GUIDE_FULL.md`

---

## 📑 MỤC LỤC TỔNG QUAN

1. [Bảng đối soát các điểm không thống nhất (Discrepancy Matrix)](#-bảng-đối-soát-các-điểm-không-thống-nhất-discrepancy-matrix)
2. [PHẦN 1: Phân tích hệ thống và Bản đồ kiểm thử (Inventory & API Mapping)](#phần-1-phân-tích-hệ-thống-và-bản-đồ-kiểm-thử)
3. [PHẦN 2: Hướng dẫn chuẩn bị môi trường kiểm thử thực tế](#phần-2-hướng-dẫn-chuẩn-bị-môi-trường-kiểm-thử-thực-tế)
4. [PHẦN 3: Đặc tả test case Phân vùng tương đương (Equivalence Partitioning - EP)](#phần-3-kiểm-thử-phân-vùng-tương-đương-equivalence-partitioning---ep)
5. [PHẦN 4: Đặc tả test case Phân tích giá trị biên (Boundary Value Analysis - BVA)](#phần-4-kiểm-thử-giá-trị-biên-boundary-value-analysis---bva)
6. [PHẦN 5: Bảng quyết định kiểm thử nghiệp vụ (Decision Table Testing)](#phần-5-bảng-quyết-định-decision-table-testing)
7. [PHẦN 6: Kiểm thử chuyển trạng thái đơn hàng (State Transition Testing)](#phần-6-kiểm-thử-chuyển-trạng-thái-state-transition-testing)
8. [PHẦN 7: Đặc tả kịch bản Use Case Testing (UCT-01, UCT-02, UCT-03)](#phần-7-kiểm-thử-use-case-use-case-testing)
9. [PHẦN 8: Kịch bản kiểm thử API tự động Postman / Newman](#phần-8-kịch-bản-kiểm-thử-api-chi-tiết-postman--newman)
10. [PHẦN 9: Kịch bản kiểm thử Trợ lý ảo YiYi AI & Mini-RAG](#phần-9-kiểm-thử-trợ-lý-ảo-yiyi-ai-ai-assistant)
11. [PHẦN 10: Kịch bản kiểm thử E2E Playwright / CodeceptJS](#phần-10-kiểm-thử-tự-động-e2e-codeceptjs--playwright)
12. [PHẦN 11: White-Box Testing & Phân tích JaCoCo Coverage](#phần-11-white-box-testing--phân-tích-jacoco-coverage)
13. [PHẦN 12: Runbook — Thứ tự thực thi kiểm thử chuẩn](#phần-12-runbook--thứ-tự-thực-thi-kiểm-thử-chuẩn)
14. [PHẦN 13: Biểu mẫu ghi nhận kết quả và Defect Bug Report](#phần-13-biểu-mẫu-ghi-nhận-kết-quả-và-báo-cáo-defect)
15. [PHẦN 14: Bảng kiểm tra và chuẩn hóa báo cáo đồ án (Chương 5)](#phần-14-bảng-kiểm-tra-và-chuẩn-hóa-báo-cáo-đồ-án-chương-5)

---

## ⚠️ BẢNG ĐỐI SOÁT CÁC ĐIỂM KHÔNG THỐNG NHẤT (DISCREPANCY MATRIX)

| Hạng mục | Tài liệu nháp / Khảo sát cũ | Mã nguồn thực tế (`Source of Truth`) | Hướng dẫn chuẩn hóa khi Test |
|---|---|---|---|
| **Cổng Backend API** | Có chỗ ghi `8080`, chỗ ghi `8081` | `application.properties`: `server.port=8081` | Sử dụng thống nhất URL: `http://localhost:8081` |
| **Tiền tố API Endpoint** | Một số tài liệu ghi `/auth/login`, `/books` | `SecurityConfig.java` & Controllers: toàn bộ có prefix `/api/` | Gọi chính xác: `http://localhost:8081/api/...` |
| **Mã lỗi trả về** | Báo cáo cũ ghi `404/500` cho mọi lỗi | `GlobalExceptionHandler`: chuẩn hóa `400 BAD_REQUEST` (Business/Validation Error) | Kỳ vọng `400` cho lỗi nghiệp vụ; `403` cho phân quyền; `401` khi thiếu/sai Token |
| **Số lượng kịch bản E2E** | Một số bảng ghi 17, bảng khác ghi 20 | Thư mục `e2e/` & test scripts: **20 kịch bản** (bao gồm cả AI & Edge cases) | Thống nhất báo cáo và chạy đủ **20 kịch bản E2E** |
| **Điểm đổi Quà (Reward)** | Ghi nhầm voucher 50k, 100k | `RewardService.java`: `FREESHIP` = 10.000 điểm; `COUPON` = 20.000 điểm | Dùng mốc 10.000 và 20.000 điểm |

---

# PHẦN 1: PHÂN TÍCH HỆ THỐNG VÀ BẢN ĐỒ KIỂM THỬ

### A. Danh Sách Toàn Bộ Chức Năng Và Module Trong Source Code

| Module | Chức năng nghiệp vụ | UI / Page Component | Controller & Endpoint | Service & Method | Database Table / Entity | Đã có Unit Test? |
|---|---|---|---|---|---|:---:|
| **Auth** | Đăng ký tài khoản | `Register.jsx` (`/register`) | `AuthController`: `POST /api/auth/register` | `AuthService.register()` | `users` (`User`) | Có (`AuthServiceTest`) |
| **Auth** | Đăng nhập hệ thống | `Login.jsx` (`/login`) | `AuthController`: `POST /api/auth/login` | `AuthService.login()` | `users` (`User`) | Có (`AuthServiceTest`) |
| **User** | Xem & sửa hồ sơ, đổi mật khẩu | `Profile.jsx` (`/profile`) | `UserController`: `GET/PUT /api/users/*` | `UserService.updateProfile()` | `users` (`User`) | Có (`UserServiceTest`) |
| **Address** | Quản lý sổ địa chỉ nhận hàng | `Profile.jsx`, `Checkout.jsx` | `AddressController`: `/api/addresses/*` | `AddressRepository` | `addresses` (`Address`) | Có (DAO/Repo Test) |
| **Books** | Xem danh mục, chi tiết, tìm kiếm | `Home.jsx`, `Search.jsx`, `ProductDetail.jsx` | `BookController`: `/api/books/*` | `BookService.searchBooks()` | `books`, `categories` | Có (`BookServiceTest`) |
| **Category** | Quản lý cây thể loại sách | `Category.jsx`, `AdminCategories.jsx` | `CategoryController`: `/api/categories/*` | `CategoryService.getAll()` | `categories` (`Category`) | Có (`CategoryServiceTest`) |
| **Cart** | Thêm, sửa số lượng, xóa giỏ hàng | `Cart.jsx` (`/cart`) | `CartController`: `/api/cart/*` | `CartService.addToCart()` | `carts`, `cart_items` | Có (`CartServiceTest`) |
| **Order** | Đặt hàng COD, hủy đơn, đổi trả | `Checkout.jsx`, `Orders.jsx` | `OrderController`: `/api/orders/*` | `OrderService.createOrder()` | `orders`, `order_items` | Có (`OrderServiceCreateTest`) |
| **Payment** | Tạo URL thanh toán VNPAY/MoMo | `Checkout.jsx`, `PaymentResult.jsx` | `PaymentController`: `/api/payment/*` | `VNPayConfig.hmacSHA512()` | `orders` (`Order`) | Có (Postman Suite) |
| **Coupon** | Áp dụng & Quản trị mã giảm giá | `Coupons.jsx`, `AdminCoupons.jsx` | `CouponController`: `/api/coupons/*` | `CouponService.validateCoupon()` | `coupons` (`Coupon`) | Có (`CouponServiceTest`) |
| **Rewards** | Tích lũy & Đổi điểm Y-Points | `Profile.jsx`, `AdminRewardVouchers.jsx` | `RewardController`: `/api/rewards/*` | `RewardService.exchangePoints()` | `point_transactions`, `user_rewards` | Có (`RewardServiceTest`) |
| **Review** | Đánh giá sao, bình luận phân cấp | `ProductDetail.jsx`, `AdminReviews.jsx` | `ReviewController`: `/api/reviews/*` | `ReviewService.createReview()` | `reviews`, `review_comments` | Có (`ReviewServiceTest`) |
| **Wishlist** | Lưu & Xóa sách yêu thích | `Profile.jsx`, `ProductDetail.jsx` | `WishlistController`: `/api/wishlists/*` | `WishlistRepository` | `wishlists` (`Wishlist`) | Có (Postman Suite) |
| **Notification** | Thông báo khuyến mãi & đơn hàng | `Notifications.jsx` | `NotificationController`: `/api/notifications/*` | `NotificationService.send()` | `notifications` (`Notification`) | Có (`NotificationServiceTest`) |
| **Newsletter** | Đăng ký nhận bản tin qua email | `Footer.jsx`, `AdminNewsletter.jsx` | `NewsletterController`: `/api/newsletter/*` | `NewsletterService.subscribe()` | `newsletter_subscribers` | Có (`NewsletterServiceTest`) |
| **Contact** | Gửi góp ý CSKH & Quản trị | `Contact.jsx`, `AdminContacts.jsx` | `ContactController`: `/api/contacts/*` | `ContactService.create()` | `contacts` (`Contact`) | Có (`ContactServiceTest`) |
| **Settings** | Cấu hình tham số hệ thống | `AdminSiteSettings.jsx` | `SiteSettingController`: `/api/settings/*` | `SiteSettingService.save()` | `site_settings` (`SiteSetting`) | Có (`SiteSettingServiceTest`) |
| **Upload** | Tải lên hình ảnh bìa/avatar | `AdminBooks.jsx`, `Profile.jsx` | `FileController`: `POST /api/upload` | `FileController.uploadFile()` | Hệ thống tệp (`/uploads`) | Có (Postman Suite) |
| **YiYi AI** | Tư vấn sách thông minh (Mini-RAG) | `AIChatWidget.jsx` (Toàn trang) | Client-side RAG + Groq API | `AIChatWidget.handleSend()` | `LocalStorage` (User Memory) | Có (`AI_CHAT_TEST_REPORT`) |

---

### B. Danh Sách Toàn Bộ Endpoint API Thực Tế

| HTTP Method | URL chính xác | Quyền (Role) | Request Body mẫu | Response | HTTP Status | Tên Request trong Postman |
|---|---|:---:|---|---|:---:|---|
| `GET` | `/api/ping` | Public | Không | `"pong"` | `200 OK` | `Ping / Health Check` |
| `POST` | `/api/auth/register` | Public | `{"name":"A","email":"a@gmail.com","password":"123","phone":"090"}` | `{"token":"...","user":{...}}` | `200 OK` | `Auth / Register` |
| `POST` | `/api/auth/login` | Public | `{"email":"user@gmail.com","password":"123456"}` | `{"token":"...","user":{...}}` | `200 OK` | `Auth / Login User` |
| `GET` | `/api/users/profile` | `USER`/`ADMIN` | Không | `{"id":1,"email":"...","fullName":"..."}` | `200 OK` | `Users / Lấy thông tin hồ sơ` |
| `PUT` | `/api/users/profile` | `USER`/`ADMIN` | `{"fullName":"A","phone":"0912","gender":"MALE"}` | `{"id":1,"fullName":"A",...}` | `200 OK` | `Users / Cập nhật hồ sơ` |
| `PUT` | `/api/users/password` | `USER`/`ADMIN` | `{"oldPassword":"123","newPassword":"456"}` | `{"message":"Đổi mật khẩu thành công"}` | `200 OK` | `Users / Đổi mật khẩu` |
| `GET` | `/api/books` | Public | Không | `[{"id":1,"title":"...","price":55000}]` | `200 OK` | `Books / Danh sách toàn bộ sách` |
| `GET` | `/api/books/{id}` | Public | Không | `{"id":3,"title":"Nhà Giả Kim",...}` | `200 OK` | `Books / Chi tiết 1 cuốn sách` |
| `GET` | `/api/books/search?keyword={kw}` | Public | Không | `[{"id":2,"title":"Clean Code",...}]` | `200 OK` | `Books / Tìm kiếm sách` |
| `POST` | `/api/books` | `ADMIN` | `{"title":"Sách Mới","price":100000,"stockQuantity":50}` | `{"id":11,"title":"Sách Mới",...}` | `200 OK` | `Admin / Thêm sách mới` |
| `GET` | `/api/cart` | `USER`/`ADMIN` | Không | `{"id":1,"items":[{"book":{...},"quantity":2}]}` | `200 OK` | `Cart / Xem giỏ hàng` |
| `POST` | `/api/cart` | `USER`/`ADMIN` | `{"bookId":3,"quantity":1}` | `{"id":1,"items":[...]}` | `200 OK` | `Cart / Thêm vào giỏ` |
| `PUT` | `/api/cart/{bookId}` | `USER`/`ADMIN` | `{"quantity":3}` | `{"id":1,"items":[...]}` | `200 OK` | `Cart / Cập nhật số lượng` |
| `DELETE` | `/api/cart/{bookId}` | `USER`/`ADMIN` | Không | `{"id":1,"items":[]}` | `200 OK` | `Cart / Xóa khỏi giỏ` |
| `POST` | `/api/orders` | `USER`/`ADMIN` | `{"items":[{"bookId":1,"quantity":1}],"shippingAddress":"..."}` | `{"id":10,"totalAmount":55000,"status":"PENDING"}` | `200 OK` | `Orders / Tạo đơn hàng mới` |
| `GET` | `/api/orders` | `USER`/`ADMIN` | Không | `[{"id":10,"status":"PENDING",...}]` | `200 OK` | `Orders / Danh sách đơn cá nhân` |
| `GET` | `/api/orders/all` | `ADMIN` | Không | `[{"id":10,"user":{...},"status":"..."}]` | `200 OK` | `Admin / Xem toàn bộ đơn hàng` |
| `PUT` | `/api/orders/{id}/shipping` | `ADMIN` | Query: `status=SHIPPING&shippingPartner=GHN` | `{"id":10,"shippingStatus":"SHIPPING"}` | `200 OK` | `Admin / Cập nhật vận chuyển` |
| `GET` | `/api/coupons/validate?code={c}&amount={a}` | Public | Không | `{"valid":true,"discountAmount":10000}` | `200 OK` | `Coupons / Áp dụng mã giảm giá` |
| `POST` | `/api/rewards/exchange` | `USER`/`ADMIN` | `{"points":10000,"type":"FREESHIP"}` | `{"message":"Đổi quà thành công","code":"FS_..."}` | `200 OK` | `Rewards / Đổi điểm thưởng` |
| `POST` | `/api/reviews/book/{bookId}` | `USER`/`ADMIN` | `{"rating":5,"comment":"Sách rất hay"}` | `{"id":1,"rating":5,"comment":"..."}` | `200 OK` | `Review / Tạo bài đánh giá` |
| `POST` | `/api/upload` | `USER`/`ADMIN` | `multipart/form-data (file)` | `{"url":"/uploads/uuid.jpg"}` | `200 OK` | `Upload / Tải lên tệp ảnh` |

---

### C. Danh Sách Toàn Bộ Màn Hình Giao Diện (UI Screens)

| Tên Màn hình (Page Path) | Đối tượng sử dụng (Actor) | Chức năng nghiệp vụ chính | Dữ liệu đầu vào (Input Form/Action) | Kết quả hiển thị (Output UI) | Luồng nghiệp vụ liên quan |
|---|:---:|---|---|---|---|
| **Trang chủ (`/`)** | Khách vãng lai / Thành viên | Trình chiếu Hero Banner, Flash Sale đếm ngược, Sách Bán Chạy, Danh mục thể loại | Click chọn tab, chọn banner | Lưới sách, đồng hồ đếm ngược Flash Sale, Banner slide | Xem danh mục, Tìm kiếm, Đặt hàng |
| **Đăng nhập (`/login`)** | Khách vãng lai | Xác thực danh tính người dùng vào hệ thống | Email, Mật khẩu | Đăng nhập thành công, lưu JWT Token vào LocalStorage, Header cập nhật tên | Quản lý phiên làm việc |
| **Đăng ký (`/register`)** | Khách vãng lai | Tạo tài khoản khách hàng thành viên mới | Họ và tên, Email, Số điện thoại, Mật khẩu | Thông báo tạo tài khoản thành công, khởi tạo 1.000 điểm Y-Points ban đầu | Đăng ký thành viên |
| **Chi tiết sách (`/book/:id`)** | Khách vãng lai / Thành viên | Xem đầy đủ thông tin sách, ảnh bìa, giá niêm yết, tỷ lệ chiết khấu, tồn kho, đánh giá sao | Bộ chọn số lượng mua (+/-), nút Thêm giỏ, nút Mua ngay, nút Tim yêu thích, form viết đánh giá | Thư viện ảnh, thông tin xuất bản, điểm đánh giá trung bình, các bình luận của độc giả | Giỏ hàng, Đánh giá, Yêu thích |
| **Tìm kiếm & Lọc (`/search`)** | Khách vãng lai / Thành viên | Tìm kiếm theo từ khóa tựa sách/tác giả, lọc kết hợp theo thể loại và khoảng giá | Ô nhập keyword, checkbox thể loại, thanh trượt / input min/max price, dropdown sắp xếp | Lưới sản phẩm khớp điều kiện, tổng số kết quả, phân trang trang 1, 2, 3... | Khám phá sản phẩm |
| **Giỏ hàng (`/cart`)** | Thành viên | Quản lý sản phẩm dự định mua, thay đổi số lượng, áp mã giảm giá | Nút tăng/giảm (+/-), nút Xóa sản phẩm, ô nhập mã giảm giá Coupon | Bảng sản phẩm, đơn giá, số lượng, tạm tính, số tiền chiết khấu coupon, tổng thanh toán | Mua hàng & Checkout |
| **Thanh toán (`/checkout`)** | Thành viên | Điền địa chỉ nhận hàng, chọn phương thức thanh toán COD hoặc Online, xuất hóa đơn VAT | Sổ chọn địa chỉ nhận hàng, họ tên, SĐT, ghi chú đơn hàng, radio chọn COD/VNPAY/VietQR/MoMo, checkbox VAT | Tóm tắt đơn hàng, phí vận chuyển, tiền giảm voucher, tổng tiền thanh toán cuối | Tạo đơn hàng |
| **Đặt hàng thành công (`/order-success`)** | Thành viên | Thông báo kết quả đặt hàng COD thành công | Không (nhận trạng thái từ Checkout chuyển sang) | Mã đơn hàng (Order ID), tổng tiền, thời gian dự kiến giao hàng, nút Xem đơn hàng | Vòng đời đơn hàng |
| **Lịch sử đơn hàng (`/orders`)** | Thành viên | Theo dõi toàn bộ hành trình đơn hàng cá nhân | Click các tab trạng thái (Tất cả, Chờ xác nhận, Đang xử lý, Đang giao, Đã giao, Đã hủy) | Danh sách thẻ đơn hàng, trạng thái vận chuyển, nút Hủy đơn, nút Yêu cầu đổi trả | Theo dõi & Đổi trả |
| **Hồ sơ cá nhân (`/profile`)** | Thành viên | Cập nhật hồ sơ cá nhân, đổi mật khẩu, quản lý sổ địa chỉ, xem hạng VIP, đổi điểm thưởng Y-Points | Form cập nhật họ tên, ngày sinh, giới tính; Form đổi mật khẩu; Nút Đổi quà Voucher | Huy hiệu hạng thành viên, số dư Y-Points, mã Voucher đã đổi trong ví cá nhân | Quản lý tài khoản & Điểm |
| **Trợ lý ảo YiYi AI (`AIChatWidget`)** | Khách vãng lai / Thành viên | Tư vấn, gợi ý sách thông minh bằng AI Mini-RAG | Ô nhập câu hỏi tư vấn, click các gợi ý prompt nhanh | Khung chat nổi toàn trang, câu trả lời streaming SSE, thẻ sản phẩm trực quan | Tư vấn & Bán hàng AI |
| **Admin Dashboard (`/admin`)** | Quản trị viên (Admin) | Thống kê tổng quan doanh thu, số lượng đơn, khách hàng mới | Bộ chọn khoảng thời gian (Hôm nay, Tuần này, Tháng này) | Thẻ KPI doanh số, biểu đồ tăng trưởng, danh sách đơn hàng mới nhất cần duyệt | Báo cáo quản trị |
| **Admin Quản lý Sách (`/admin/books`)** | Quản trị viên (Admin) | Quản trị kho sách, thêm mới, sửa giá, tồn kho, tải ảnh bìa, nhập Excel | Form nhập sách (Tựa sách, tác giả, giá, tồn kho, danh mục, ảnh), nút Nhập Excel | Bảng danh sách sách, modal chỉnh sửa, tìm kiếm sách trong kho | Quản trị kho sách |
| **Admin Quản lý Đơn (`/admin/orders`)** | Quản trị viên (Admin) | Duyệt đơn hàng, giao vận chuyển, phê duyệt/từ chối đổi trả | Dropdown chọn trạng thái vận chuyển (SHIPPING, DELIVERED), chọn đối tác (GHN/GHTK), nhập mã tracking | Danh sách toàn bộ đơn hàng toàn sàn, modal chi tiết đơn, bộ lọc trạng thái | Xử lý đơn & Vận chuyển |

---

# PHẦN 2: HƯỚNG DẪN CHUẨN BỊ MÔI TRƯỜNG KIỂM THỬ THỰC TẾ

### Bước 1: Khởi động Cơ sở dữ liệu PostgreSQL
Mở PowerShell tại thư mục gốc `E:\TestingProject`:
```powershell
docker-compose up -d postgres
```
*Kiểm tra container:* `docker ps` *(thấy container `postgres` cổng `5432` Up)*.

### Bước 2: Khởi động Backend (Spring Boot 3)
```powershell
cd E:\TestingProject\backend
mvn spring-boot:run
```
*(Chờ log console hiển thị: `Started BookstoreApplication in ... seconds` trên cổng `8081`).*

### Bước 3: Khởi động Frontend (React + Vite)
Mở một cửa sổ PowerShell mới:
```powershell
cd E:\TestingProject\frontend
npm run dev
```
*(Truy cập trình duyệt: `http://localhost:5173`).*

### Bước 4: Kiểm tra Health Endpoint
```powershell
curl http://localhost:8081/api/ping
```
*Kết quả:* Trả về chữ `pong` (HTTP Status 200).

### Bước 5: Cấu hình Postman Environment
1. Import `postman/_FullSuite_AllMembers.json` và `postman/_Env_Local.json`.
2. Kiểm tra biến môi trường:
   * `baseUrl`: `http://localhost:8081/api`
   * `userEmail`: `user@gmail.com` / `userPassword`: `123456`
   * `adminEmail`: `admin@gmail.com` / `adminPassword`: `123456`

---

# PHẦN 3: KIỂM THỬ PHÂN VÙNG TƯƠNG ĐƯƠNG (EQUIVALENCE PARTITIONING - EP)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-REG-01** | Register | Hợp lệ | Đầy đủ thông tin hợp lệ (Email mới, pass $\ge 6$ ký tự, phone 10 số) | Giao diện UI (`/register`) | Email chưa có trong hệ thống | `fullName`: `Nguyễn Văn An`<br>`email`: `nguyenvanan.test@gmail.com`<br>`phone`: `0901234567`<br>`password`: `Abc@123456` | 1. Mở trang `/register`<br>2. Nhập đầy đủ form<br>3. Bấm nút "Đăng Ký" | Đăng ký thành công, hiển thị Toast thông báo thành công, tự động đăng nhập và lưu JWT token vào LocalStorage | | | Ảnh Toast đăng ký thành công | |
| **EP-REG-02** | Register | Không hợp lệ | Để trống trường Họ và Tên | Giao diện UI (`/register`) | Bất kỳ | `fullName`: ` ` (rỗng)<br>`email`: `user.test@gmail.com`<br>`phone`: `0901234567`<br>`password`: `123456` | 1. Mở trang `/register`<br>2. Bỏ trống Họ tên<br>3. Bấm nút "Đăng Ký" | Hệ thống chặn submit, hiển thị thông báo lỗi ngay dưới ô Họ tên: "Họ và tên không được để trống" | | | Ảnh thông báo lỗi validation đỏ | |
| **EP-REG-03** | Register | Không hợp lệ | Email sai định dạng (thiếu `@` và tên miền) | Giao diện UI (`/register`) | Bất kỳ | `fullName`: `Trần Bình`<br>`email`: `tranbinhemail`<br>`phone`: `0901234567`<br>`password`: `123456` | 1. Nhập email sai chuẩn<br>2. Bấm nút "Đăng Ký" | Trình duyệt và React chặn gửi form, báo lỗi "Vui lòng nhập đúng định dạng email" | | | Ảnh báo lỗi email sai định dạng | |
| **EP-REG-04** | Register | Không hợp lệ | Email đã tồn tại trong cơ sở dữ liệu | Postman / UI | Đã có tài khoản `user@gmail.com` | `fullName`: `Trần Bình`<br>`email`: `user@gmail.com`<br>`phone`: `0909998888`<br>`password`: `123456` | 1. Gửi request `POST /api/auth/register`<br>2. Đính kèm email đã tồn tại | Backend phản hồi HTTP `400 Bad Request` với message: "Email này đã được đăng ký sử dụng!" | | | Ảnh response Postman nhận mã 400 | |
| **EP-REG-05** | Register | Không hợp lệ | Mật khẩu ngắn hơn 6 ký tự | Giao diện UI (`/register`) | Bất kỳ | `fullName`: `Lê Cường`<br>`email`: `lecuong@gmail.com`<br>`phone`: `0901234567`<br>`password`: `12345` (5 ký tự) | 1. Nhập mật khẩu 5 ký tự<br>2. Bấm "Đăng Ký" | Báo lỗi validation: "Mật khẩu phải có độ dài tối thiểu từ 6 ký tự trở lên" | | | Ảnh báo lỗi mật khẩu ngắn | |
| **EP-REG-06** | Register | Không hợp lệ | Số điện thoại chứa chữ cái hoặc ký tự đặc biệt | Giao diện UI (`/register`) | Bất kỳ | `fullName`: `Phạm Dũng`<br>`email`: `phamdung@gmail.com`<br>`phone`: `09012ABC#$`<br>`password`: `123456` | 1. Nhập SĐT chứa chữ<br>2. Bấm "Đăng Ký" | Báo lỗi: "Số điện thoại không hợp lệ (chỉ bao gồm chữ số)" | | | Ảnh thông báo lỗi SĐT | |
| **EP-LOG-01** | Login | Hợp lệ | Tài khoản Khách hàng (User) chính xác | Giao diện UI (`/login`) | Tài khoản `user@gmail.com` tồn tại, pass `123456` | `email`: `user@gmail.com`<br>`password`: `123456` | 1. Mở `/login`<br>2. Nhập thông tin<br>3. Bấm "Đăng Nhập" | Đăng nhập thành công, chuyển hướng về Trang chủ, Header hiển thị tên "Khách hàng" | | | Ảnh Header đã đăng nhập User | |
| **EP-LOG-02** | Login | Hợp lệ | Tài khoản Quản trị viên (Admin) chính xác | Giao diện UI (`/login`) | Tài khoản `admin@gmail.com` tồn tại, pass `123456` | `email`: `admin@gmail.com`<br>`password`: `123456` | 1. Mở `/login`<br>2. Nhập thông tin Admin<br>3. Bấm "Đăng Nhập" | Đăng nhập thành công, Header xuất hiện menu "Quản Trị", chuyển hướng sang `/admin` Dashboard | | | Ảnh giao diện Cổng Admin | |
| **EP-LOG-03** | Login | Không hợp lệ | Mật khẩu không chính xác | Giao diện UI (`/login`) | User `user@gmail.com` tồn tại | `email`: `user@gmail.com`<br>`password`: `SaiMatKhau999` | 1. Nhập email đúng, pass sai<br>2. Bấm "Đăng Nhập" | Hiển thị Toast lỗi: "Tên đăng nhập hoặc mật khẩu không chính xác!", không chuyển trang | | | Ảnh thông báo lỗi đăng nhập | |
| **EP-CRT-01** | Cart | Hợp lệ | Thêm sản phẩm với số lượng hợp lệ ($1 \le Q \le \text{Stock}$) | Giao diện UI (`/book/1`) | Sách ID 1 có tồn kho 100 | `bookId`: `1`<br>`quantity`: `3` | 1. Vào trang chi tiết sách 1<br>2. Chọn số lượng 3<br>3. Bấm "Thêm vào giỏ" | Thông báo "Đã thêm vào giỏ hàng!", Badge giỏ hàng trên Header tăng lên 3 | | | Ảnh giỏ hàng có 3 món | |
| **EP-CRT-04** | Cart | Không hợp lệ | Thêm số lượng sản phẩm âm hoặc bằng 0 | API Postman | Đã có JWT Token | `bookId`: `1`<br>`quantity`: `-3` | 1. Gửi request `POST /api/cart` với quantity âm | Backend trả về HTTP `400 Bad Request`: "Số lượng sản phẩm không hợp lệ!" | | | Ảnh Postman nhận lỗi 400 | |
| **EP-CRT-05** | Cart | Không hợp lệ | Thêm số lượng vượt quá số lượng tồn kho | Giao diện UI (`/book/4`) | Sách ID 4 còn tồn kho 20 cuốn | `bookId`: `4`<br>`quantity`: `50` | 1. Nhập số lượng 50<br>2. Bấm Thêm giỏ | Hiển thị cảnh báo: "Số lượng yêu cầu vượt quá tồn kho hiện có (tối đa 20 cuốn)!", không thêm vào giỏ | | | Ảnh cảnh báo vượt tồn kho | |
| **EP-CPN-01** | Coupon | Hợp lệ | Mã giảm giá theo phần trăm (`PERCENTAGE`), đủ điều kiện | Giao diện UI (`/cart`) | Giỏ hàng có tổng tiền 200.000đ | `code`: `GRAPE10` (Giảm 10%, min 100k) | 1. Nhập mã `GRAPE10`<br>2. Bấm "Áp Dụng" | Áp dụng thành công, chiết khấu giảm 20.000đ, tổng tiền thanh toán còn 180.000đ | | | Ảnh giảm giá 10% thành công | |
| **EP-CPN-03** | Coupon | Không hợp lệ | Đơn hàng chưa đạt giá trị tối thiểu của mã | Giao diện UI (`/cart`) | Giỏ hàng có tổng tiền 80.000đ | `code`: `GRAPE10` (Yêu cầu tối thiểu 100k) | 1. Nhập mã `GRAPE10`<br>2. Bấm "Áp Dụng" | Báo lỗi: "Đơn hàng tối thiểu 100.000đ để áp dụng mã này (còn thiếu 20.000đ)", không giảm giá | | | Ảnh thông báo chưa đủ tiền | |
| **EP-ORD-01** | Order | Hợp lệ | Đặt hàng COD đầy đủ thông tin giao hàng | Giao diện UI (`/checkout`) | Giỏ hàng có sản phẩm | `address`: `123 Nguyễn Văn Cừ, Q5, TP.HCM`<br>`phone`: `0901234567`<br>`paymentMethod`: `COD` | 1. Điền thông tin giao hàng<br>2. Chọn COD<br>3. Bấm "Xác Nhận Đặt Hàng" | Đặt hàng thành công, giỏ hàng tự động làm trống, chuyển hướng sang `/order-success`, DB tạo đơn `PENDING` | | | Ảnh màn hình Order Success | |
| **EP-REV-01** | Review | Hợp lệ | Đã mua & nhận hàng thành công, chấm 5 sao | Giao diện UI (`/book/1`) | User đã mua sách ID 1 và đơn hàng trạng thái `DELIVERED` | `rating`: `5`<br>`comment`: `Sách in ấn rất đẹp, giao hàng nhanh chóng.` | 1. Mở trang chi tiết sách<br>2. Chấm 5 sao + Nhập nhận xét<br>3. Bấm "Gửi Đánh Giá" | Gửi đánh giá thành công, bài đánh giá hiển thị ngay tại mục bình luận của sách, điểm sao TB cập nhật | | | Ảnh bài đánh giá 5 sao | |
| **EP-REV-02** | Review | Không hợp lệ | Chưa từng mua sản phẩm mà gửi đánh giá | UI / Postman | User chưa từng có đơn hàng nào chứa sách ID 2 | `bookId`: `2`<br>`rating`: `5`<br>`comment`: `Sách hay lắm` | 1. Mở sách chưa mua<br>2. Gửi đánh giá | Nút đánh giá bị ẩn hoặc Backend trả về `400 Bad Request`: "Bạn cần mua và nhận sản phẩm này để viết đánh giá!" | | | Ảnh báo lỗi ràng buộc mua hàng | |
| **EP-UPL-01** | Upload | Hợp lệ | Tải lên file ảnh hợp lệ (.png, .jpg, .webp, kích thước < 5MB) | Giao diện UI / Postman | Đã có JWT Token | File ảnh `bia_sach.png` (dung lượng 500KB) | 1. Chọn file ảnh<br>2. Bấm Upload | Upload thành công, trả về HTTP `200 OK` kèm đường dẫn tĩnh dạng `/uploads/uuid.png` | | | Ảnh upload thành công | |
| **EP-UPL-02** | Upload | Không hợp lệ | Tải lên file mã nguồn / thực thi nguy hiểm (.exe, .sh, .bat, .jsp) | API Postman | Đã có JWT Token | File script `backdoor.sh` | 1. Gửi `POST /api/upload` với file .sh | Backend chặn xử lý, trả về HTTP `400 Bad Request`: "Chỉ cho phép tải lên định dạng hình ảnh (.jpg, .png, .webp) hoặc tài liệu PDF!" | | | Ảnh Postman chặn file độc hại | |
| **EP-AI-01** | YiYi AI | Hợp lệ | Câu hỏi tìm kiếm tựa sách có trong kho | Giao diện Chatbot | Đang mở widget chat | *"Cửa hàng có sách Clean Code không và giá bao nhiêu?"* | 1. Mở widget AI<br>2. Nhập câu hỏi<br>3. Bấm Gửi | Trả lời chính xác có sách "Clean Code", giá 250.000đ, hiển thị Thẻ sản phẩm có nút "Thêm vào giỏ" | | | Ảnh trả lời kèm thẻ sách Clean Code | |
| **EP-ADM-02** | RBAC | Không hợp lệ | Tài khoản `USER` cố tình truy cập trang hoặc gọi API Admin | UI / Postman | Đã đăng nhập `user@gmail.com` | Gửi request `GET /api/orders/all` | 1. Dùng token User thường<br>2. Gọi API Admin | Backend từ chối truy cập, trả về HTTP `403 Forbidden`: "Bạn không có quyền thực hiện thao tác này!" | | | Ảnh Postman nhận lỗi 403 Forbidden | |

---

# PHẦN 4: KIỂM THỬ GIÁ TRỊ BIÊN (BOUNDARY VALUE ANALYSIS - BVA)

| Test Case ID | Tham số kiểm tra | Giá trị kiểm thử | Vị trí biên kiểm tra | Nơi test | Dữ liệu chuẩn bị | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng ảnh/log |
|---|---|---|:---:|:---:|---|---|---|:---:|:---:|---|
| **BVA-RAT-01** | Rating đánh giá | `0` | Dưới biên dưới | Postman | Đã mua sách ID 1 | Gửi `POST /api/reviews/book/1` với `rating: 0` | Bị từ chối (400 Bad Request, Rating tối thiểu 1) | | | Log Postman 400 |
| **BVA-RAT-02** | Rating đánh giá | `1` | Biên dưới (Min) | UI / Postman | Đã mua sách ID 1 | Gửi đánh giá với `rating: 1` | Thành công 200 OK (Chấm 1 sao hợp lệ) | | | Ảnh bài đánh giá 1 sao |
| **BVA-RAT-03** | Rating đánh giá | `2` | Ngay trên biên dưới | UI / Postman | Đã mua sách ID 1 | Gửi đánh giá với `rating: 2` | Thành công 200 OK (Chấm 2 sao hợp lệ) | | | Ảnh bài đánh giá 2 sao |
| **BVA-RAT-04** | Rating đánh giá | `4` | Ngay dưới biên trên | UI / Postman | Đã mua sách ID 1 | Gửi đánh giá với `rating: 4` | Thành công 200 OK (Chấm 4 sao hợp lệ) | | | Ảnh bài đánh giá 4 sao |
| **BVA-RAT-05** | Rating đánh giá | `5` | Biên trên (Max) | UI / Postman | Đã mua sách ID 1 | Gửi đánh giá với `rating: 5` | Thành công 200 OK (Chấm 5 sao hợp lệ) | | | Ảnh bài đánh giá 5 sao |
| **BVA-RAT-06** | Rating đánh giá | `6` | Vượt biên trên | Postman | Đã mua sách ID 1 | Gửi `POST /api/reviews/book/1` với `rating: 6` | Bị từ chối (400 Bad Request, Rating tối đa 5) | | | Log Postman 400 |
| **BVA-QTY-01** | Số lượng mua | `0` | Dưới biên dưới | Postman | Sách ID 1 (Stock: 100) | Gửi `POST /api/cart` với `quantity: 0` | Bị từ chối (400 Bad Request: Số lượng không hợp lệ) | | | Log Postman 400 |
| **BVA-QTY-02** | Số lượng mua | `1` | Biên dưới (Min) | UI / Postman | Sách ID 1 (Stock: 100) | Chọn số lượng 1 → Thêm giỏ | Thành công (Giỏ hàng có 1 sản phẩm) | | | Ảnh giỏ hàng 1 món |
| **BVA-QTY-03** | Số lượng mua | `2` | Ngay trên biên dưới | UI / Postman | Sách ID 1 (Stock: 100) | Chọn số lượng 2 → Thêm giỏ | Thành công (Giỏ hàng có 2 sản phẩm) | | | Ảnh giỏ hàng 2 món |
| **BVA-QTY-04** | Số lượng mua | `99` (`Stock - 1`) | Ngay dưới trần kho | UI / Postman | Sách ID 1 (Stock: 100) | Nhập số lượng 99 → Thêm giỏ | Thành công (Giỏ hàng có 99 sản phẩm) | | | Ảnh giỏ hàng 99 món |
| **BVA-QTY-05** | Số lượng mua | `100` (`Stock`) | Trần tồn kho (Max) | UI / Postman | Sách ID 1 (Stock: 100) | Nhập số lượng 100 → Thêm giỏ | Thành công (Giỏ hàng lấy trọn 100 sản phẩm kho) | | | Ảnh giỏ hàng 100 món |
| **BVA-QTY-06** | Số lượng mua | `101` (`Stock + 1`) | Vượt trần kho | UI / Postman | Sách ID 1 (Stock: 100) | Nhập số lượng 101 → Thêm giỏ | Báo lỗi vượt quá tồn kho (chỉ còn 100 cuốn) | | | Ảnh thông báo lỗi tồn kho |
| **BVA-MIN-01** | Giá tối thiểu áp Coupon | `99.999đ` (`Min - 1`) | Dưới ngưỡng áp dụng | Postman | Mã GRAPE10 (Min 100k) | Gọi `validate?code=GRAPE10&amount=99999` | Trả về `200 OK`, `valid: false` (Báo lỗi: "Đơn hàng tối thiểu để sử dụng mã này là 100,000 đ") | | | Postman Log 200 (valid=false) |
| **BVA-MIN-02** | Giá tối thiểu áp Coupon | `100.000đ` (`Min`) | Đúng ngưỡng chuẩn | UI / Postman | Mã GRAPE10 (Min 100k) | Gọi `validate?code=GRAPE10&amount=100000` | Áp dụng thành công (`200 OK`, `valid: true`, `discountAmount: 10000.0`) | | | Ảnh áp mã 100k thành công |
| **BVA-MIN-03** | Giá tối thiểu áp Coupon | `100.001đ` (`Min + 1`) | Trên ngưỡng chuẩn | UI / Postman | Mã GRAPE10 (Min 100k) | Gọi `validate?code=GRAPE10&amount=100001` | Áp dụng thành công (`200 OK`, `valid: true`, `discountAmount: 10000.1`) | | | Ảnh áp mã 100k thành công |
| **BVA-PWD-01** | Độ dài mật khẩu mới | `5 ký tự` (`Min - 1`) | Dưới độ dài tối thiểu | UI / Postman | User đã đăng nhập | Nhập đổi mật khẩu mới: `12345` | Báo lỗi: Mật khẩu mới phải có ít nhất 6 ký tự | | | Ảnh form báo lỗi mật khẩu ngắn |
| **BVA-PWD-02** | Độ dài mật khẩu mới | `6 ký tự` (`Min`) | Đúng chuẩn tối thiểu | UI / Postman | User đã đăng nhập | Nhập đổi mật khẩu mới: `123456` | Đổi mật khẩu thành công | | | Ảnh đổi mật khẩu thành công |
| **BVA-PWD-03** | Độ dài mật khẩu mới | `7 ký tự` (`Min + 1`) | Trên chuẩn tối thiểu | UI / Postman | User đã đăng nhập | Nhập đổi mật khẩu mới: `1234567` | Đổi mật khẩu thành công | | | Ảnh đổi mật khẩu thành công |
| **BVA-REW-01** | Điểm đổi Freeship | `9.999 điểm` | Dưới ngưỡng đổi | UI / Postman | User có 9.999 điểm | Gửi request đổi `FREESHIP` (cần 10.000đ) | Báo lỗi: "Số dư Y-Points không đủ để đổi quà" | | | Ảnh thông báo không đủ điểm |
| **BVA-REW-02** | Điểm đổi Freeship | `10.000 điểm` | Đúng ngưỡng đổi | UI / Postman | User có 10.000 điểm | Bấm đổi `FREESHIP` | Thành công, trừ 10.000 điểm, ví nhận mã `FS_...` | | | Ảnh đổi voucher thành công |
| **BVA-REW-03** | Điểm đổi Freeship | `10.001 điểm` | Trên ngưỡng đổi | UI / Postman | User có 10.001 điểm | Bấm đổi `FREESHIP` | Thành công, trừ 10.000 điểm, điểm còn lại 1 điểm | | | Ảnh đổi voucher thành công |
| **BVA-RNK-01** | Điểm thăng hạng Bạc | `4.999 điểm` | Dưới mốc Bạc | UI (`/profile`) | User có 4.999 điểm | Mở trang Hồ sơ | Hiển thị hạng **ĐỒNG (BRONZE)** | | | Ảnh huy hiệu Đồng |
| **BVA-RNK-02** | Điểm thăng hạng Bạc | `5.000 điểm` | Chạm mốc Bạc | UI (`/profile`) | User có 5.000 điểm | Mở trang Hồ sơ | Thăng hạng **BẠC (SILVER)** thành công | | | Ảnh huy hiệu Bạc |
| **BVA-RNK-03** | Điểm thăng hạng Vàng | `30.000 điểm` | Chạm mốc Vàng | UI (`/profile`) | User có 30.000 điểm | Mở trang Hồ sơ | Thăng hạng **VÀNG (GOLD)** thành công | | | Ảnh huy hiệu Vàng |
| **BVA-RNK-04** | Điểm thăng hạng KC | `100.000 điểm` | Chạm mốc Kim Cương | UI (`/profile`) | User có 100.000 điểm | Mở trang Hồ sơ | Thăng hạng **KIM CƯƠNG (DIAMOND)** | | | Ảnh huy hiệu Kim Cương |

---

# PHẦN 5: BẢNG QUYẾT ĐỊNH (DECISION TABLE TESTING)

### Bảng 1: Nghiệp Vụ Áp Dụng Mã Giảm Giá (Coupon Validation)
* **Quy tắc 1:** Mã không tồn tại hoặc đã hết hạn $\rightarrow$ Báo lỗi.
* **Quy tắc 2:** Mã hợp lệ nhưng tổng tiền đơn hàng chưa đạt giá trị tối thiểu $\rightarrow$ Báo lỗi.
* **Quy tắc 3:** Mã hợp lệ, đơn hàng đủ điều kiện $\rightarrow$ Trừ tiền thành công.

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 |
|---|:---:|:---:|:---:|
| **Mã Coupon có tồn tại & đang Active?** | **False** | **True** | **True** |
| **Thời hạn sử dụng còn hiệu lực?** | — | **True** | **True** |
| **Đơn hàng $\ge$ Giá trị tối thiểu (`minOrderAmount`)?** | — | **False** | **True** |
| **HÀNH ĐỘNG: Áp dụng chiết khấu vào đơn hàng** | ❌ Không | ❌ Không | ✅ **Áp dụng** |
| **HÀNH ĐỘNG: Hiển thị thông báo lỗi cụ thể** | ✅ Báo mã sai | ✅ Báo chưa đủ tiền | ❌ Không lỗi |
| **Mã HTTP Status kỳ vọng** | `400 Bad Request` | `400 Bad Request` | `200 OK` |

---

### Bảng 2: Nghiệp Vụ Phân Quyền Truy Cập Hệ Thống (RBAC Matrix)

| Role Người dùng | Gọi API Public (`/api/books`, `/api/ping`) | Gọi API Member (`/api/cart`, `/api/orders`) | Gọi API Admin (`/api/orders/all`, `/admin/users`) |
|---|:---:|:---:|:---:|
| **Khách vãng lai (Guest - Không có Token)** | ✅ `200 OK` | ❌ `401 Unauthorized` / `403 Forbidden` | ❌ `401 Unauthorized` / `403 Forbidden` |
| **Khách hàng thường (Role `USER`)** | ✅ `200 OK` | ✅ `200 OK` (Truy cập dữ liệu của chính mình) | ❌ `403 Forbidden` |
| **Quản trị viên (Role `ADMIN`)** | ✅ `200 OK` | ✅ `200 OK` | ✅ `200 OK` (Toàn quyền quản trị) |

---

# PHẦN 6: KIỂM THỬ CHUYỂN TRẠNG THÁI (STATE TRANSITION TESTING)

```
[Khách Đặt Hàng] ──> PENDING ──(Admin duyệt)──> PROCESSING ──(Giao ĐVVC)──> SHIPPING ──(Giao thành công)──> DELIVERED ──(Xác nhận)──> COMPLETED
                       │                              │
                       └──(Hủy đơn)──> CANCELLED <────┘
                                           ▲
                                           │ (Từ chối)
DELIVERED ──(Khách yêu cầu đổi trả)──> RETURN_REQUESTED ──(Admin duyệt)──> RETURN_APPROVED ──> REFUNDED
```

| Transition ID | Trạng thái hiện tại | Sự kiện kích hoạt (Event / Action) | Trạng thái kế tiếp | Tác nhân (Actor) | Nơi test | Kết quả mong đợi (Expected) | Actual Result | Status |
|---|---|---|---|:---:|:---:|---|:---:|:---:|
| **ST-01** | `PENDING` | Admin xác nhận đơn hàng | `PROCESSING` | Admin | UI (`/admin/orders`) | Đơn chuyển sang đang đóng gói xử lý | | |
| **ST-02** | `PROCESSING` | Admin giao hàng cho bên vận chuyển (GHN/GHTK) | `SHIPPING` | Admin | UI (`/admin/orders`) | Đơn có mã vận đơn & chuyển sang Đang giao | | |
| **ST-03** | `SHIPPING` | Shipper giao thành công cho khách | `DELIVERED` | Admin | UI (`/admin/orders`) | Trạng thái chuyển Đã giao hàng, mở nút Đánh giá | | |
| **ST-04** | `DELIVERED` | Khách xác nhận đã nhận & hài lòng | `COMPLETED` | Member | UI (`/orders`) | Đơn hoàn tất, tự động cộng điểm Y-Points | | |
| **ST-05** | `PENDING` | Khách bấm Hủy đơn hàng | `CANCELLED` | Member | UI (`/orders`) | Đơn bị hủy, hoàn trả lại số lượng tồn kho sách | | |
| **ST-06 (Invalid)** | `CANCELLED` | Cố tình cập nhật sang `PROCESSING` | `CANCELLED` | Admin | Postman | Backend chặn, không cho phép phục hồi đơn đã hủy | | |
| **ST-07 (Invalid)** | `DELIVERED` | Cố tình nhảy lùi về `PENDING` | `DELIVERED` | Admin | Postman | Backend chặn cập nhật trạng thái không hợp lệ | | |

---

# PHẦN 7: KIỂM THỬ USE CASE (USE CASE TESTING)

### UC-01: Quy Trình Mua Sách Toàn Trình (End-to-End Shopping Flow)
* **Actor:** Khách hàng (Member)
* **Tiền điều kiện:** Đã có tài khoản `user@gmail.com`, sách "Nhà Giả Kim" còn tồn kho $\ge 1$.
* **Các bước thực hiện:**
  1. Truy cập `http://localhost:5173/login`, đăng nhập với tài khoản `user@gmail.com` / `123456`.
  2. Tại thanh tìm kiếm, gõ `Nhà Giả Kim` và bấm Enter.
  3. Bấm vào sách "Nhà Giả Kim" từ danh sách kết quả để mở trang chi tiết.
  4. Chọn số lượng `1` và bấm nút **"Thêm vào giỏ hàng"**.
  5. Bấm vào icon Giỏ hàng trên Header để vào trang `/cart`.
  6. Nhập mã giảm giá `GRAPE10` và bấm **"Áp dụng"**.
  7. Bấm nút **"Tiến hành đặt hàng"** để sang trang `/checkout`.
  8. Điền địa chỉ nhận hàng: `123 Nguyễn Văn Cừ, Quận 5, TP.HCM` và Số điện thoại: `0901234567`.
  9. Chọn phương thức thanh toán: **"Thanh toán khi nhận hàng (COD)"**.
  10. Bấm nút **"Xác nhận đặt hàng"**.
* **Kết quả mong đợi:** 
  - Màn hình chuyển hướng sang trang Thông báo đặt hàng thành công (`/order-success`).
  - Hiển thị Mã đơn hàng, tổng số tiền đã trừ 10% coupon.
  - Kiểm tra trong mục `/orders` thấy đơn hàng mới ở trạng thái `PENDING`.
  - Tồn kho sách "Nhà Giả Kim" giảm đi 1 cuốn.

---

### UC-02: Tư Vấn Và Gợi Ý Sách Bằng Trợ Lý Ảo YiYi AI
* **Actor:** Khách vãng lai / Thành viên
* **Tiền điều kiện:** Trang web đang mở, mạng Internet ổn định.
* **Các bước thực hiện:**
  1. Tại góc dưới cùng bên phải màn hình, bấm vào biểu tượng bong bóng Chatbot YiYi AI.
  2. Hộp thoại chat mở ra, nhập câu hỏi: *"Tôi muốn tìm sách về lập trình và tối ưu code sạch, bạn có gợi ý gì không?"*.
  3. Bấm nút Gửi (hoặc Enter).
* **Kết quả mong đợi:**
  - Chatbot nhận diện intent `Tìm sách công nghệ / lập trình`.
  - Phản hồi chữ chạy streaming mượt mà (SSE).
  - Trích xuất đúng tựa sách "Clean Code" có trong kho cửa hàng.
  - Hiển thị **Thẻ xem nhanh sản phẩm (Product Card)** bên dưới câu trả lời kèm nút *"Xem chi tiết"* và *"Thêm vào giỏ"*.
  - Bấm vào thẻ sản phẩm chuyển đúng sang trang chi tiết cuốn "Clean Code".

---

### UC-03: Quản Trị Viên Xử Lý Đơn Hàng Và Cập Nhật Vận Chuyển
* **Actor:** Quản trị viên (Admin)
* **Tiền điều kiện:** Đã có đơn hàng mới tạo từ UC-01 (`status = PENDING`).
* **Các bước thực hiện:**
  1. Đăng nhập tài khoản `admin@gmail.com` / `123456`.
  2. Mở Cổng quản trị Admin (`/admin`), chọn menu **"Quản lý đơn hàng"** (`/admin/orders`).
  3. Tìm đơn hàng vừa tạo ở bước UC-01.
  4. Tại cột Thao tác, bấm cập nhật trạng thái sang **`Đang giao hàng (SHIPPING)`**, chọn đơn vị vận chuyển `Giao Hàng Nhanh (GHN)` và nhập mã vận đơn `GHN-YIYI-001`.
  5. Bấm **"Lưu thay đổi"**.
  6. Mở trình duyệt ẩn danh, đăng nhập tài khoản `user@gmail.com` và vào mục Đơn hàng của tôi (`/orders`).
* **Kết quả mong đợi:**
  - Phía Admin: Trạng thái đơn đổi thành `SHIPPING` kèm đơn vị `GHN`.
  - Phía Khách hàng: Đơn hàng lập tức hiển thị trạng thái *"Đang vận chuyển"* kèm mã tra cứu `GHN-YIYI-001`.

---

# PHẦN 8: KỊCH BẢN KIỂM THỬ API CHI TIẾT (POSTMAN / NEWMAN)

### 1. API Xác Thực (Authentication Suite)
* **Request:** `POST {{baseUrl}}/auth/login`
* **Headers:** `Content-Type: application/json`
* **Body:**
  ```json
  {
    "email": "user@gmail.com",
    "password": "123456"
  }
  ```
* **Postman Test Script:**
  ```javascript
  pm.test("Status code là 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Response có chứa JWT Token", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData.token).to.be.a("string");
      pm.environment.set("userToken", jsonData.token);
  });
  ```

---

### 2. API Giỏ Hàng (Cart Suite)
* **Request:** `POST {{baseUrl}}/cart`
* **Headers:** 
  * `Content-Type: application/json`
  * `Authorization: Bearer {{userToken}}`
* **Body:**
  ```json
  {
    "bookId": 1,
    "quantity": 2
  }
  ```
* **Postman Test Script:**
  ```javascript
  pm.test("Status code là 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Giỏ hàng chứa danh sách items hợp lệ", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData.items).to.be.an("array");
      pm.expect(jsonData.items.length).to.be.above(0);
  });
  ```

---

### 3. API Đặt Hàng (Order Suite)
* **Request:** `POST {{baseUrl}}/orders`
* **Headers:** 
  * `Content-Type: application/json`
  * `Authorization: Bearer {{userToken}}`
* **Body:**
  ```json
  {
    "items": [
      {
        "bookId": 1,
        "quantity": 1,
        "price": 55000
      }
    ],
    "shippingAddress": "123 Nguyễn Văn Cừ, Quận 5, TP.HCM",
    "phoneNumber": "0901234567",
    "paymentMethod": "COD",
    "discountCouponCode": "GRAPE10"
  }
  ```
* **Postman Test Script:**
  ```javascript
  pm.test("Tạo đơn hàng thành công (Status 200/201)", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  pm.test("Đơn hàng trả về ID và trạng thái PENDING", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData.id).to.exist;
      pm.expect(jsonData.status).to.eql("PENDING");
      pm.environment.set("createdOrderId", jsonData.id);
  });
  ```

---

# PHẦN 9: KIỂM THỬ TRỢ LÝ ẢO YIYI AI (AI ASSISTANT)

| Test Case ID | Câu hỏi / Hành động thử nghiệm | Tiền điều kiện | Kết quả mong đợi (Expected Response) | Actual Response | Status | Minh chứng |
|---|---|---|---|---|:---:|---|
| **AI-01** | *"Cửa hàng có sách Clean Code không?"* | Đang mở widget AI | Nhận diện sách "Clean Code", trả lời tóm tắt và hiển thị thẻ sản phẩm "Clean Code" (250.000đ) | | | Ảnh câu trả lời và thẻ sách |
| **AI-02** | *"Gợi ý cho tôi sách thiếu nhi hay"* | Đang mở widget AI | Trả lời danh sách sách thiếu nhi ("Dế Mèn Phiêu Lưu Ký", "Doraemon") kèm các thẻ mua hàng | | | Ảnh danh sách sách thiếu nhi |
| **AI-03** | Hỏi câu hỏi không có trong kho: *"Cửa hàng có bán sách Luyện thi bằng lái tàu vũ trụ không?"* | Đang mở widget AI | Chatbot giải thích lịch sự hiện cửa hàng không có tựa sách này, không tự bịa đặt sách giả (Zero Hallucination) | | | Ảnh phản hồi từ chối lịch sự |
| **AI-04** | Ngắt kết nối mạng / Thiếu API Key | Tắt Wi-Fi hoặc xóa key | Widget hiển thị thông báo lỗi thân thiện, không làm sập giao diện web (Graceful Fallback) | | | Ảnh thông báo lỗi nhẹ nhàng |

---

# PHẦN 10: KIỂM THỬ TỰ ĐỘNG E2E (CODECEPTJS / PLAYWRIGHT)

### Lệnh thực thi kiểm thử E2E:
Mở terminal tại thư mục gốc `E:\TestingProject`:
```powershell
npx codeceptjs run --steps
```

### Danh mục kịch bản E2E chính:
1. **`auth_test.js`**: Kiểm tra Đăng ký tài khoản mới $\rightarrow$ Đăng nhập $\rightarrow$ Kiểm tra hiển thị tên trên Header $\rightarrow$ Đăng xuất.
2. **`search_test.js`**: Nhập từ khóa "Clean" trên thanh tìm kiếm $\rightarrow$ Kiểm tra xuất hiện sách "Clean Code" $\rightarrow$ Lọc theo danh mục.
3. **`cart_test.js`**: Vào trang chi tiết $\rightarrow$ Chọn số lượng 2 $\rightarrow$ Bấm Thêm giỏ $\rightarrow$ Mở trang `/cart` $\rightarrow$ Tăng số lượng lên 3 $\rightarrow$ Kiểm tra cập nhật tổng tiền.
4. **`checkout_test.js`**: Từ giỏ hàng $\rightarrow$ Bấm Thanh toán $\rightarrow$ Nhập địa chỉ $\rightarrow$ Chọn COD $\rightarrow$ Đặt hàng $\rightarrow$ Xác nhận trang `/order-success`.
5. **`ai_chat_test.js`**: Bấm mở bong bóng AI $\rightarrow$ Gõ câu hỏi tìm sách $\rightarrow$ Kiểm tra hiển thị thẻ gợi ý sản phẩm.

---

# PHẦN 11: WHITE-BOX TESTING & PHÂN TÍCH JACOCO COVERAGE

### 1. Lệnh thực thi toàn bộ Unit Test Backend:
```powershell
cd E:\TestingProject\backend
mvn clean test
```

### 2. Xem Báo Cáo Phân Tích Độ Bao Phủ Mã Nguồn (JaCoCo):
Mở file sau bằng trình duyệt:
📁 **`E:\TestingProject\backend\target\site\jacoco\index.html`**

---

# PHẦN 12: RUNBOOK — THỨ TỰ THỰC THI KIỂM THỬ CHUẨN

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    QUY TRÌNH THỰC THI KIỂM THỬ THỰC TẾ                       │
└──────────────────────────────────────────────────────────────────────────────┘
   │
   ▼
[BƯỚC 1: MÔI TRƯỜNG] ────> Khởi động Docker DB: docker-compose up -d postgres
                           Khởi động Backend: cd backend && mvn spring-boot:run
                           Khởi động Frontend: cd frontend && npm run dev
   │
   ▼
[BƯỚC 2: SMOKE TEST] ────> Kiểm tra Health: curl http://localhost:8081/api/ping -> "pong"
                           Mở trình duyệt: http://localhost:5173
   │
   ▼
[BƯỚC 3: UNIT TEST]  ────> Chạy 300 Unit Tests: cd backend && mvn test
                           Mở xem JaCoCo: backend/target/site/jacoco/index.html
   │
   ▼
[BƯỚC 4: API TEST]   ────> Chạy Newman CLI: cd postman && npm run test:local
                           Hoặc chạy trên giao diện Postman Collection Runner
   │
   ▼
[BƯỚC 5: BLACK-BOX]  ────> Thực hiện lần lượt bảng test BVA, EP, Decision Table
                           trên giao diện web & Postman theo bảng ở Phần 3, 4, 5
   │
   ▼
[BƯỚC 6: USE CASE]   ────> Chạy luồng UC-01 (Mua hàng), UC-02 (AI), UC-03 (Admin)
   │
   ▼
[BƯỚC 7: E2E TEST]   ────> Chạy tự động trình duyệt: npx codeceptjs run --steps
   │
   ▼
[BƯỚC 8: ĐÓNG GÓI]   ────> Điền cột Actual Result, Status (PASS/FAIL) vào biểu mẫu
                           Chụp lưu ảnh minh chứng và cập nhật RTM
```

---

# PHẦN 13: BIỂU MẪU GHI NHẬN KẾT QUẢ VÀ BÁO CÁO DEFECT

### 1. Mẫu Bảng Ghi Nhận Kết Quả Thực Thi (Execution Log)

| Test Case ID | Tóm tắt kịch bản kiểm thử | Kết quả mong đợi (Expected) | Kết quả thực tế (Actual Result) | Kết luận (PASS/FAIL) | Mã Bug ID (nếu FAIL) | Đường dẫn ảnh minh chứng |
|---|---|---|---|:---:|:---:|---|
| **EP-AUTH-01** | Đăng ký tài khoản mới hợp lệ | Đăng ký thành công, nhận JWT Token | | | | `docs/evidence/ep_auth_01.png` |
| **BVA-RAT-02** | Đánh giá sách 1 sao (Biên dưới) | Chấm 1 sao thành công, lưu DB | | | | `docs/evidence/bva_rat_02.png` |
| **BVA-QTY-05** | Mua đúng số lượng tồn kho (100 món) | Thêm thành công 100 món vào giỏ | | | | `docs/evidence/bva_qty_05.png` |
| **UC-01** | Toàn trình đặt hàng COD kèm Coupon | Đơn tạo thành công, trừ 10% coupon | | | | `docs/evidence/uc_01_success.png` |

---

### 2. Mẫu Báo Cáo Lỗi (Defect Bug Report)

* **Bug ID:** `BUG-YIYI-xxx`
* **Tiêu đề (Summary):** [Tên lỗi ngắn gọn, ví dụ: Không thể áp dụng mã giảm giá khi giỏ hàng có trên 5 sản phẩm]
* **Module:** Giỏ hàng & Khuyến mãi (Cart & Coupon)
* **Mức độ nghiêm trọng (Severity):** `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`
* **Môi trường (Environment):** Localhost (Windows 11, Chrome v128, Backend Spring Boot 3.2)
* **Tài khoản kiểm thử:** `user@gmail.com`
* **Các bước tái hiện (Steps to Reproduce):**
  1. Thêm 6 cuốn sách bất kỳ vào giỏ hàng.
  2. Tại ô mã giảm giá, nhập mã `GRAPE10`.
  3. Bấm nút "Áp dụng".
* **Kết quả thực tế (Actual Behavior):** Giao diện xoay tròn vô tận, console báo lỗi 500.
* **Kết quả mong đợi (Expected Behavior):** Áp dụng chiết khấu 10% thành công và hiển thị tổng tiền mới.
* **Ảnh / Log đính kèm (Evidence):** `docs/evidence/bug_coupon_500.png`
* **Trạng thái:** `OPEN` / `RESOLVED` / `CLOSED`

---

# PHẦN 14: BẢNG KIỂM TRA VÀ CHUẨN HÓA BÁO CÁO ĐỒ ÁN (CHƯƠNG 5)

| Hạng mục rà soát | Vị trí trong Báo cáo | Hiện trạng trước khi chuẩn hóa | Nội dung chuẩn hóa chính xác | Đánh giá mức độ |
|---|---|---|---|:---:|
| **Cổng Backend** | Mục 5.1 & 5.13 | Có chỗ ghi `8080`, chỗ ghi `8081` | Chuẩn hóa toàn bộ thành **`8081`** | **Cao** |
| **Tiêu chí Entry Criteria** | Bảng 5.3 (Mục 3.2) | Nhầm lẫn đưa kết quả `300/300 PASS` vào điều kiện bắt đầu test | Tách riêng: Entry là điều kiện môi trường sẵn sàng; Exit mới là 100% tests PASS | **Cao** |
| **Ký hiệu Use Case Test** | Mục 4.5 & 5.13.15 | Dùng nhầm mã `UC-01` (trùng mã SRS) cho kịch bản test | Chuẩn hóa thành **`UCT-01`**, **`UCT-02`**, **`UCT-03`** | **Trung bình** |
| **Mã lỗi Exception** | Mục 5.13.8 | Báo cáo cũ ghi mong đợi lỗi 500 khi sai input | Chuẩn hóa theo `GlobalExceptionHandler`: mong đợi **`400 BAD_REQUEST`** | **Cao** |
| **Hiện trạng UAT** | Mục 3.4 & Kết luận | Ghi mâu thuẫn UAT hoàn thành 100% trong khi chưa có chữ ký người dùng | Ghi rõ hiện trạng: **`PENDING / PLANNED`** (chờ ký biên bản nghiệm thu thực tế) | **Nghiêm ngặt** |

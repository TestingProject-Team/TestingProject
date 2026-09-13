# BỘ TÀI LIỆU KIỂM THỬ TOÀN DIỆN DỰ ÁN YIYI BOOK
## PHẦN 1: PHÂN TÍCH HỆ THỐNG VÀ BẢN ĐỒ KIỂM THỬ (PROJECT INVENTORY & API MAPPING)
## PHẦN 3: ĐẶC TẢ TEST CASE PHÂN VÙNG TƯƠNG ĐƯƠNG (EQUIVALENCE PARTITIONING - EP)

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

---

### A. Danh Sách Toàn Bộ Chức Năng Và Module Trong Source Code

| STT | Module | Tên Chức năng Nghiệp vụ | UI / Page Component | Controller / Endpoint Backend | Service / Method | Database Table / Entity | Hiện trạng Unit Test |
|:---:|---|---|---|---|---|---|:---:|
| 1 | **Auth** | Đăng ký tài khoản khách hàng mới | `Register.jsx` (`/register`) | `AuthController`: `POST /api/auth/register` | `AuthService.register()` | `users` (`User`) | Đã có (`AuthServiceTest`) |
| 2 | **Auth** | Đăng nhập tài khoản (cấp JWT Token) | `Login.jsx` (`/login`) | `AuthController`: `POST /api/auth/login` | `AuthService.login()` | `users` (`User`) | Đã có (`AuthServiceTest`) |
| 3 | **User** | Xem thông tin hồ sơ cá nhân | `Profile.jsx` (`/profile`) | `UserController`: `GET /api/users/profile` | `UserService.getUserByUsername()` | `users` (`User`) | Đã có (`UserServiceTest`) |
| 4 | **User** | Cập nhật thông tin cá nhân & sở thích AI | `Profile.jsx` (`/profile`) | `UserController`: `PUT /api/users/profile` | `UserService.updateProfile()` | `users` (`User`) | Đã có (`UserServiceTest`) |
| 5 | **User** | Đổi mật khẩu tài khoản nội bộ (Local) | `Profile.jsx` (`/profile`) | `UserController`: `PUT /api/users/password` | `UserService.changePassword()` | `users` (`User`) | Đã có (`UserServiceTest`) |
| 6 | **Admin User** | Xem danh sách toàn bộ người dùng | `AdminUsers.jsx` (`/admin/users`) | `AdminUserController`: `GET /api/admin/users` | `UserRepository.findAll()` | `users` (`User`) | Đã có (`Tai_Admin_Rewards_RBAC`) |
| 7 | **Admin User** | Thay đổi quyền tài khoản (USER / ADMIN) | `AdminUsers.jsx` (`/admin/users`) | `AdminUserController`: `PUT /api/admin/users/{id}/role` | `UserRepository.save()` | `users` (`User`) | Đã có (`Tai_Admin_Rewards_RBAC`) |
| 8 | **Admin User** | Kích hoạt / Khóa tài khoản người dùng | `AdminUsers.jsx` (`/admin/users`) | `AdminUserController`: `PUT /api/admin/users/{id}/status` | `UserRepository.save()` | `users` (`User`) | Đã có (`Tai_Admin_Rewards_RBAC`) |
| 9 | **Admin User** | Xóa tài khoản người dùng (chặn tự xóa) | `AdminUsers.jsx` (`/admin/users`) | `AdminUserController`: `DELETE /api/admin/users/{id}` | `UserRepository.delete()` | `users` (`User`) | Đã có (`AdminUserController`) |
| 10 | **Address** | Xem sổ địa chỉ nhận hàng của tôi | `Profile.jsx`, `Checkout.jsx` | `AddressController`: `GET /api/addresses/my-addresses` | `AddressRepository.findByUserId()` | `addresses` (`Address`) | Đã có (`AddressController`) |
| 11 | **Address** | Thêm mới địa chỉ nhận hàng | `Profile.jsx`, `Checkout.jsx` | `AddressController`: `POST /api/addresses` | `AddressRepository.save()` | `addresses` (`Address`) | Đã có (`AddressController`) |
| 12 | **Address** | Thiết lập địa chỉ mặc định | `Profile.jsx` | `AddressController`: `PUT /api/addresses/{id}/default` | `AddressRepository.save()` | `addresses` (`Address`) | Đã có (`AddressController`) |
| 13 | **Address** | Cập nhật thông tin địa chỉ | `Profile.jsx` | `AddressController`: `PUT /api/addresses/{id}` | `AddressRepository.save()` | `addresses` (`Address`) | Đã có (`AddressController`) |
| 14 | **Address** | Xóa địa chỉ khỏi danh bạ | `Profile.jsx` | `AddressController`: `DELETE /api/addresses/{id}` | `AddressRepository.delete()` | `addresses` (`Address`) | Đã có (`AddressController`) |
| 15 | **Books** | Lấy danh sách toàn bộ sách (Storefront) | `Home.jsx`, `Category.jsx` | `BookController`: `GET /api/books` | `BookService.getAllBooks()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 16 | **Books** | Xem thông tin chi tiết một cuốn sách | `ProductDetail.jsx` (`/book/:id`) | `BookController`: `GET /api/books/{id}` | `BookService.getBookById()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 17 | **Books** | Tìm kiếm sách theo từ khóa | `Search.jsx` (`/search`) | `BookController`: `GET /api/books/search` | `BookService.searchBooks()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 18 | **Books** | Lọc danh sách sách nổi bật / Flash sale | `FlashSale.jsx`, `Home.jsx` | `BookController`: `GET /api/books/flash-sale` | `BookService.getFlashSaleBooks()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 19 | **Books** | Lọc danh sách sách theo thể loại | `Category.jsx` (`/category/:id`) | `BookController`: `GET /api/books/category/{id}` | `BookService.getBooksByCategory()` | `books`, `categories` | Đã có (`BookServiceTest`) |
| 20 | **Admin Books** | Thêm mới một cuốn sách | `AdminBooks.jsx` (`/admin/books`) | `BookController`: `POST /api/books` | `BookService.createBook()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 21 | **Admin Books** | Cập nhật thông tin & tồn kho sách | `AdminBooks.jsx` (`/admin/books`) | `BookController`: `PUT /api/books/{id}` | `BookService.updateBook()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 22 | **Admin Books** | Xóa sách khỏi hệ thống | `AdminBooks.jsx` (`/admin/books`) | `BookController`: `DELETE /api/books/{id}` | `BookService.deleteBook()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 23 | **Admin Books** | Nhập sách hàng loạt từ file Excel | `AdminBooks.jsx` (`/admin/books`) | `BookController`: `POST /api/books/upload-excel` | `BookService.saveBooksFromExcel()` | `books` (`Book`) | Đã có (`BookServiceTest`) |
| 24 | **Category** | Lấy danh sách toàn bộ thể loại | `Category.jsx`, Header menu | `CategoryController`: `GET /api/categories` | `CategoryService.getAllCategories()` | `categories` (`Category`) | Đã có (`CategoryServiceTest`) |
| 25 | **Category** | Xem thông tin một thể loại | `Category.jsx` | `CategoryController`: `GET /api/categories/{id}` | `CategoryService.getCategoryById()` | `categories` (`Category`) | Đã có (`CategoryServiceTest`) |
| 26 | **Admin Category** | Thêm mới thể loại sách | `AdminCategories.jsx` | `CategoryController`: `POST /api/categories` | `CategoryService.createCategory()` | `categories` (`Category`) | Đã có (`CategoryServiceTest`) |
| 27 | **Admin Category** | Cập nhật thể loại sách | `AdminCategories.jsx` | `CategoryController`: `PUT /api/categories/{id}` | `CategoryService.updateCategory()` | `categories` (`Category`) | Đã có (`CategoryServiceTest`) |
| 28 | **Admin Category** | Xóa thể loại sách | `AdminCategories.jsx` | `CategoryController`: `DELETE /api/categories/{id}` | `CategoryService.deleteCategory()` | `categories` (`Category`) | Đã có (`CategoryServiceTest`) |
| 29 | **Banner** | Lấy danh sách tất cả banner | `Home.jsx` | `BannerController`: `GET /api/banners` | `BannerService.getAllBanners()` | `banners` (`Banner`) | Đã có (`BannerServiceTest`) |
| 30 | **Banner** | Lọc banner theo vị trí hiển thị | `HeroBanner.jsx`, `Home.jsx` | `BannerController`: `GET /api/banners/position/{pos}` | `BannerService.getBannersByPosition()` | `banners` (`Banner`) | Đã có (`BannerServiceTest`) |
| 31 | **Admin Banner** | Thêm mới banner quảng cáo | `AdminBanners.jsx` | `BannerController`: `POST /api/banners` | `BannerService.createBanner()` | `banners` (`Banner`) | Đã có (`BannerServiceTest`) |
| 32 | **Admin Banner** | Cập nhật banner quảng cáo | `AdminBanners.jsx` | `BannerController`: `PUT /api/banners/{id}` | `BannerService.updateBanner()` | `banners` (`Banner`) | Đã có (`BannerServiceTest`) |
| 33 | **Admin Banner** | Xóa banner quảng cáo | `AdminBanners.jsx` | `BannerController`: `DELETE /api/banners/{id}` | `BannerService.deleteBanner()` | `banners` (`Banner`) | Đã có (`BannerServiceTest`) |
| 34 | **Cart** | Xem chi tiết giỏ hàng cá nhân | `Cart.jsx` (`/cart`) | `CartController`: `GET /api/cart` | `CartService.getCartByUser()` | `carts`, `cart_items` | Đã có (`CartServiceTest`) |
| 35 | **Cart** | Thêm sản phẩm vào giỏ hàng | `ProductDetail.jsx`, `Home.jsx` | `CartController`: `POST /api/cart` | `CartService.addToCart()` | `carts`, `cart_items` | Đã có (`CartServiceTest`) |
| 36 | **Cart** | Cập nhật số lượng sản phẩm trong giỏ | `Cart.jsx` (`/cart`) | `CartController`: `PUT /api/cart/{bookId}` | `CartService.updateCartItem()` | `carts`, `cart_items` | Đã có (`CartServiceTest`) |
| 37 | **Cart** | Xóa một sản phẩm khỏi giỏ hàng | `Cart.jsx` (`/cart`) | `CartController`: `DELETE /api/cart/{bookId}` | `CartService.removeCartItem()` | `carts`, `cart_items` | Đã có (`CartServiceTest`) |
| 38 | **Cart** | Xóa toàn bộ giỏ hàng | `Cart.jsx` (`/cart`) | `CartController`: `DELETE /api/cart` | `CartService.clearCart()` | `carts`, `cart_items` | Đã có (`CartServiceTest`) |
| 39 | **Order** | Tạo đơn hàng mới (COD / Online) | `Checkout.jsx` (`/checkout`) | `OrderController`: `POST /api/orders` | `OrderService.createOrder()` | `orders`, `order_items` | Đã có (`OrderServiceCreateTest`) |
| 40 | **Order** | Xem danh sách đơn hàng cá nhân | `Orders.jsx` (`/orders`) | `OrderController`: `GET /api/orders` | `OrderService.getOrdersByUser()` | `orders`, `order_items` | Đã có (`OrderServiceTest`) |
| 41 | **Order** | Xem chi tiết đơn hàng (IDOR protected) | `OrderDetail.jsx` (`/orders/:id`) | `OrderController`: `GET /api/orders/{id}` | `OrderService.getOrderById()` | `orders`, `order_items` | Đã có (`OrderServiceTest`) |
| 42 | **Order** | Hủy đơn hàng (khi đang PENDING) | `Orders.jsx`, `OrderDetail.jsx` | `OrderController`: `PUT /api/orders/{id}/cancel` | `OrderService.cancelOrder()` | `orders` (`Order`) | Đã có (`OrderServiceTest`) |
| 43 | **Order** | Yêu cầu đổi trả / hoàn tiền | `Orders.jsx`, `OrderDetail.jsx` | `OrderController`: `POST /api/orders/{id}/return` | `OrderService.requestReturn()` | `orders` (`Order`) | Đã có (`OrderServiceTest`) |
| 44 | **Admin Order** | Xem toàn bộ danh sách đơn hàng | `AdminOrders.jsx` (`/admin/orders`) | `OrderController`: `GET /api/orders/all` | `OrderService.getAllOrders()` | `orders`, `users` | Đã có (`OrderServiceTest`) |
| 45 | **Admin Order** | Cập nhật thông tin vận chuyển đơn hàng | `AdminOrders.jsx` (`/admin/orders`) | `OrderController`: `PUT /api/orders/{id}/shipping` | `OrderService.updateOrderShipping()` | `orders` (`Order`) | Đã có (`OrderServiceTest`) |
| 46 | **Admin Order** | Chấp thuận yêu cầu đổi trả hàng | `AdminOrders.jsx` (`/admin/orders`) | `OrderController`: `PUT /api/orders/{id}/return/approve` | `OrderService.approveReturn()` | `orders` (`Order`) | Đã có (`OrderServiceTest`) |
| 47 | **Admin Order** | Từ chối yêu cầu đổi trả hàng | `AdminOrders.jsx` (`/admin/orders`) | `OrderController`: `PUT /api/orders/{id}/return/reject` | `OrderService.rejectReturn()` | `orders` (`Order`) | Đã có (`OrderServiceTest`) |
| 48 | **Payment** | Tạo URL chuyển hướng thanh toán VNPAY | `Checkout.jsx` | `PaymentController`: `GET /api/payment/create-url` | `VNPayConfig.hmacSHA512()` | `orders` (`Order`) | Đã có (`Postman Suite`) |
| 49 | **Payment** | Tiếp nhận Callback VNPAY IPN | `PaymentResult.jsx` | `PaymentController`: `GET /api/payment/vnpay-callback` | `OrderService.confirmPayment()` | `orders` (`Order`) | Đã có (`Postman Suite`) |
| 50 | **Payment** | Tạo URL thanh toán MoMo Sandbox | `Checkout.jsx` | `PaymentController`: `GET /api/payment/momo/create-url` | `MoMoConfig` | `orders` (`Order`) | Đã có (`Postman Suite`) |
| 51 | **Payment** | Tiếp nhận IPN MoMo Callback | `PaymentResult.jsx` | `PaymentController`: `POST /api/payment/momo-ipn` | `OrderService.confirmPayment()` | `orders` (`Order`) | Đã có (`Postman Suite`) |
| 52 | **Coupon** | Lấy danh sách mã giảm giá công khai | `Coupons.jsx` (`/coupons`) | `CouponController`: `GET /api/coupons` | `CouponService.getActiveCoupons()` | `coupons` (`Coupon`) | Đã có (`CouponServiceTest`) |
| 53 | **Coupon** | Kiểm tra & xác thực mã giảm giá | `Cart.jsx`, `Checkout.jsx` | `CouponController`: `GET /api/coupons/validate` | `CouponService.validateCoupon()` | `coupons` (`Coupon`) | Đã có (`CouponServiceTest`) |
| 54 | **Coupon** | Xem lịch sử sử dụng mã của tôi | `Profile.jsx` | `CouponController`: `GET /api/coupons/history` | `CouponService.getHistory()` | `orders`, `coupons` | Đã có (`CouponServiceTest`) |
| 55 | **Admin Coupon** | Xem toàn bộ mã giảm giá | `AdminCoupons.jsx` | `CouponController`: `GET /api/coupons/all` | `CouponService.getAllCoupons()` | `coupons` (`Coupon`) | Đã có (`CouponServiceTest`) |
| 56 | **Admin Coupon** | Thêm mới mã giảm giá | `AdminCoupons.jsx` | `CouponController`: `POST /api/coupons` | `CouponService.createCoupon()` | `coupons` (`Coupon`) | Đã có (`CouponServiceTest`) |
| 57 | **Admin Coupon** | Cập nhật thông tin mã giảm giá | `AdminCoupons.jsx` | `CouponController`: `PUT /api/coupons/{id}` | `CouponService.updateCoupon()` | `coupons` (`Coupon`) | Đã có (`CouponServiceTest`) |
| 58 | **Admin Coupon** | Xóa mã giảm giá | `AdminCoupons.jsx` | `CouponController`: `DELETE /api/coupons/{id}` | `CouponService.deleteCoupon()` | `coupons` (`Coupon`) | Đã có (`CouponServiceTest`) |
| 59 | **Rewards** | Lấy danh sách voucher đổi thưởng | `Profile.jsx` | `RewardController`: `GET /api/rewards/vouchers` | `RewardService.getActiveVouchers()` | `reward_vouchers` | Đã có (`RewardServiceTest`) |
| 60 | **Rewards** | Đổi điểm Y-Points lấy Voucher | `Profile.jsx` | `RewardController`: `POST /api/rewards/exchange` | `RewardService.exchangePoints()` | `point_transactions`, `user_rewards` | Đã có (`RewardServiceTest`) |
| 61 | **Rewards** | Xem danh sách Voucher đã đổi của tôi | `Profile.jsx` | `RewardController`: `GET /api/rewards/my-vouchers` | `RewardService.getUserVouchers()` | `user_rewards` | Đã có (`RewardServiceTest`) |
| 62 | **Admin Rewards** | Quản trị tạo kho quà tặng đổi điểm | `AdminRewardVouchers.jsx` | `AdminRewardController`: `POST /api/rewards/vouchers` | `RewardVoucherRepository.save()` | `reward_vouchers` | Đã có (`Tai_Admin_Rewards_RBAC`) |
| 63 | **Review** | Lấy danh sách đánh giá theo sách | `ProductDetail.jsx` | `ReviewController`: `GET /api/reviews/book/{bookId}` | `ReviewService.getReviewsByBookId()` | `reviews` (`Review`) | Đã có (`ReviewServiceTest`) |
| 64 | **Review** | Kiểm tra điều kiện viết đánh giá | `ProductDetail.jsx` | `ReviewController`: `GET /api/reviews/check-eligibility/{bookId}` | `ReviewService.checkEligibility()` | `orders`, `reviews` | Đã có (`ReviewServiceTest`) |
| 65 | **Review** | Tạo bài đánh giá và chấm sao | `ProductDetail.jsx` | `ReviewController`: `POST /api/reviews/book/{bookId}` | `ReviewService.createReview()` | `reviews` (`Review`) | Đã có (`ReviewServiceTest`) |
| 66 | **Review** | Thích (Like) bài đánh giá | `ProductDetail.jsx` | `ReviewController`: `POST /api/reviews/{id}/like` | `ReviewService.likeReview()` | `reviews` (`Review`) | Đã có (`ReviewServiceTest`) |
| 67 | **Review** | Bình luận lồng vào bài đánh giá | `ProductDetail.jsx` | `ReviewController`: `POST /api/reviews/{id}/comments` | `ReviewService.addComment()` | `review_comments` | Đã có (`ReviewServiceTest`) |
| 68 | **Review** | Báo cáo bài đánh giá vi phạm | `ProductDetail.jsx` | `ReviewController`: `POST /api/reviews/{id}/report` | `ReviewService.reportReview()` | `reviews` (`Review`) | Đã có (`ReviewServiceTest`) |
| 69 | **Admin Review** | Quản trị và kiểm duyệt đánh giá | `AdminReviews.jsx` | `AdminReviewController`: `GET /api/admin/reviews` | `ReviewRepository.findAll()` | `reviews` (`Review`) | Đã có (`AdminReviewController`) |
| 70 | **Admin Review** | Xóa đánh giá vi phạm | `AdminReviews.jsx` | `AdminReviewController`: `DELETE /api/admin/reviews/{id}` | `ReviewRepository.deleteById()` | `reviews` (`Review`) | Đã có (`AdminReviewController`) |
| 71 | **Wishlist** | Lấy danh sách sách yêu thích của tôi | `Profile.jsx` | `WishlistController`: `GET /api/wishlists` | `WishlistRepository.findByUser()` | `wishlists` (`Wishlist`) | Đã có (`WishlistController`) |
| 72 | **Wishlist** | Thêm / Xóa sách khỏi yêu thích | `ProductDetail.jsx`, `Home.jsx` | `WishlistController`: `POST /api/wishlists/book/{bookId}` | `WishlistRepository.save()/delete()` | `wishlists` (`Wishlist`) | Đã có (`WishlistController`) |
| 73 | **Notification** | Lấy danh sách thông báo của tôi | `Notifications.jsx` | `NotificationController`: `GET /api/notifications` | `NotificationService.getUserNotifications()` | `notifications` | Đã có (`NotificationServiceTest`) |
| 74 | **Notification** | Đánh dấu một thông báo đã đọc | `Notifications.jsx` | `NotificationController`: `PUT /api/notifications/{id}/read` | `NotificationService.markAsRead()` | `notifications` | Đã có (`NotificationServiceTest`) |
| 75 | **Notification** | Đánh dấu tất cả đã đọc | `Notifications.jsx` | `NotificationController`: `PUT /api/notifications/read-all` | `NotificationService.markAllAsRead()` | `notifications` | Đã có (`NotificationServiceTest`) |
| 76 | **Admin Notification** | Gửi thông báo toàn hệ thống | `AdminNotifications.jsx` | `NotificationController`: `POST /api/notifications/admin/send` | `NotificationService.sendBroadcast()` | `notifications` | Đã có (`NotificationServiceTest`) |
| 77 | **Newsletter** | Đăng ký nhận bản tin khuyến mãi | `Footer.jsx` | `NewsletterController`: `POST /api/newsletter/subscribe` | `NewsletterService.subscribe()` | `newsletter_subscribers` | Đã có (`NewsletterServiceTest`) |
| 78 | **Admin Newsletter** | Xem danh sách & gửi email hàng loạt | `AdminNewsletter.jsx` | `NewsletterController`: `GET/POST /api/newsletter/*` | `NewsletterService.sendBulkEmail()` | `newsletter_subscribers` | Đã có (`NewsletterServiceTest`) |
| 79 | **Contact** | Gửi góp ý / liên hệ hỗ trợ | `Contact.jsx` (`/contact`) | `ContactController`: `POST /api/contacts` | `ContactService.createContact()` | `contacts` (`Contact`) | Đã có (`ContactServiceTest`) |
| 80 | **Admin Contact** | Xem và cập nhật trạng thái liên hệ | `AdminContacts.jsx` | `ContactController`: `GET/PUT/DELETE /api/contacts/*` | `ContactService.updateStatus()` | `contacts` (`Contact`) | Đã có (`ContactServiceTest`) |
| 81 | **Settings** | Lấy thông số cấu hình website công khai | `Footer.jsx`, `Header.jsx` | `SiteSettingController`: `GET /api/settings` | `SiteSettingService.getSettingsAsMap()` | `site_settings` | Đã có (`SiteSettingServiceTest`) |
| 82 | **Admin Settings** | Lưu cấu hình tham số hệ thống | `AdminSiteSettings.jsx` | `SiteSettingController`: `POST /api/settings` | `SiteSettingService.saveAllSettings()` | `site_settings` | Đã có (`SiteSettingServiceTest`) |
| 83 | **Upload** | Tải lên file ảnh bìa / hình avatar | `AdminBooks.jsx`, `Profile.jsx` | `FileController`: `POST /api/upload` | `FileController.uploadFile()` | Lưu trữ đĩa (`/uploads`) | Đã có (`FileController`) |
| 84 | **VAT Invoice** | Khởi tạo thông tin xuất hóa đơn VAT | `Checkout.jsx` | `VatInvoiceController`: `POST /api/vat-invoices` | `VatInvoiceRepository.save()` | `vat_invoices` (`VatInvoice`) | Đã có (`VatInvoiceController`) |
| 85 | **Ping** | Kiểm tra sức khỏe hệ thống (Health Check) | Trình duyệt / Monitor | `PingController`: `GET /api/ping` | Trả về `"pong"` | Không lưu DB | Đã có (`PingController`) |
| 86 | **YiYi AI** | Trợ lý tư vấn sách thông minh (Mini-RAG) | `AIChatWidget.jsx` (Toàn trang) | Client-side Mini-RAG + Groq API | Phân tích 8 Intent + Prompt Context | `LocalStorage` (User Memory) | Đã có (`AI_CHAT_TEST_REPORT`) |

---

### B. Danh Sách Toàn Bộ Endpoint API Thực Tế (API Directory)

| HTTP Method | URL Endpoint Đầy Đủ | Quyền Yêu Cầu (Role) | Request Body (Payload Mẫu) | Response Trả Về | HTTP Status Kỳ Vọng | Tên Request Tương Ứng Trong Postman |
|---|---|:---:|---|---|:---:|---|
| `GET` | `/api/ping` | Public | Không | `"pong"` (chuỗi text) | `200 OK` | `Ping / Health Check` |
| `POST` | `/api/auth/register` | Public | `{"name":"A","email":"a@gmail.com","password":"123456","phone":"0901234567"}` | `{"token":"...","user":{"id":1,"email":"..."}}` | `200 OK` | `Auth / Register` |
| `POST` | `/api/auth/login` | Public | `{"email":"user@gmail.com","password":"123456"}` | `{"token":"...","user":{"id":1,"email":"..."}}` | `200 OK` | `Auth / Login User` |
| `GET` | `/api/users/profile` | `USER` / `ADMIN` | Không | `{"id":1,"email":"user@gmail.com","fullName":"Khách hàng",...}` | `200 OK` | `Users / Lấy thông tin hồ sơ` |
| `PUT` | `/api/users/profile` | `USER` / `ADMIN` | `{"fullName":"Lê Văn B","phone":"0987654321","gender":"MALE","birthday":"1995-05-15"}` | `{"id":1,"fullName":"Lê Văn B",...}` | `200 OK` | `Users / Cập nhật hồ sơ` |
| `PUT` | `/api/users/password` | `USER` / `ADMIN` | `{"oldPassword":"123456","newPassword":"newpassword123"}` | `{"message":"Đổi mật khẩu thành công!"}` | `200 OK` | `Users / Đổi mật khẩu` |
| `GET` | `/api/admin/users` | `ADMIN` | Không | `[{"id":1,"email":"admin@gmail.com","role":"ADMIN",...}]` | `200 OK` | `Admin / Lấy danh sách người dùng` |
| `PUT` | `/api/admin/users/{id}/role` | `ADMIN` | `{"role":"ADMIN"}` | `{"id":2,"role":"ADMIN",...}` | `200 OK` | `Admin / Cập nhật quyền người dùng` |
| `PUT` | `/api/admin/users/{id}/status` | `ADMIN` | `{"active":false}` | `{"id":2,"active":false,...}` | `200 OK` | `Admin / Khóa/Mở khóa tài khoản` |
| `DELETE` | `/api/admin/users/{id}` | `ADMIN` | Không | `{"message":"Đã xóa người dùng thành công!"}` | `200 OK` | `Admin / Xóa người dùng` |
| `GET` | `/api/addresses/my-addresses` | `USER` / `ADMIN` | Không | `[{"id":1,"recipientName":"A","phoneNumber":"090","street":"123 Lê Lợi",...}]` | `200 OK` | `Address / Lấy danh sách địa chỉ` |
| `POST` | `/api/addresses` | `USER` / `ADMIN` | `{"recipientName":"A","phoneNumber":"090123","city":"TP.HCM","district":"Q5","ward":"P1","street":"123 Lê Lợi","isDefault":true}` | `{"id":2,"recipientName":"A",...}` | `200 OK` | `Address / Thêm mới địa chỉ` |
| `PUT` | `/api/addresses/{id}/default` | `USER` / `ADMIN` | Không | `{"id":1,"isDefault":true,...}` | `200 OK` | `Address / Đặt làm địa chỉ mặc định` |
| `PUT` | `/api/addresses/{id}` | `USER` / `ADMIN` | `{"recipientName":"B","phoneNumber":"091234",...}` | `{"id":1,"recipientName":"B",...}` | `200 OK` | `Address / Cập nhật địa chỉ` |
| `DELETE` | `/api/addresses/{id}` | `USER` / `ADMIN` | Không | `{"message":"Đã xóa địa chỉ thành công!"}` | `200 OK` | `Address / Xóa địa chỉ` |
| `GET` | `/api/books` | Public | Không | `[{"id":1,"title":"Dế Mèn Phiêu Lưu Ký","price":55000,"stockQuantity":100,...}]` | `200 OK` | `Books / Danh sách toàn bộ sách` |
| `GET` | `/api/books/{id}` | Public | Không | `{"id":3,"title":"Nhà Giả Kim","price":79000,"author":"Paulo Coelho",...}` | `200 OK` | `Books / Chi tiết 1 cuốn sách` |
| `GET` | `/api/books/search?keyword={kw}` | Public | Không | `[{"id":2,"title":"Clean Code","price":250000,...}]` | `200 OK` | `Books / Tìm kiếm sách` |
| `GET` | `/api/books/flash-sale` | Public | Không | `[{"id":1,"discount":31,"price":55000,...}]` | `200 OK` | `Books / Danh sách Flash Sale` |
| `GET` | `/api/books/category/{id}` | Public | Không | `[{"id":1,"title":"...","category":{"id":1,"name":"Sách Thiếu Nhi"}}]` | `200 OK` | `Books / Sách theo danh mục` |
| `POST` | `/api/books` | `ADMIN` | `{"title":"Sách Mới","author":"Tác Giả A","price":100000,"stockQuantity":50,"categoryId":1}` | `{"id":11,"title":"Sách Mới",...}` | `200 OK` | `Admin / Thêm sách mới` |
| `PUT` | `/api/books/{id}` | `ADMIN` | `{"title":"Sách Đã Sửa","price":120000,"stockQuantity":80}` | `{"id":1,"title":"Sách Đã Sửa",...}` | `200 OK` | `Admin / Cập nhật sách` |
| `DELETE` | `/api/books/{id}` | `ADMIN` | Không | `{"message":"Đã xóa sách thành công!"}` | `200 OK` | `Admin / Xóa sách` |
| `POST` | `/api/books/upload-excel` | `ADMIN` | `multipart/form-data (file .xlsx)` | `{"message":"Đã nhập dữ liệu sách thành công!"}` | `200 OK` | `Admin / Nhập kho từ Excel` |
| `GET` | `/api/categories` | Public | Không | `[{"id":1,"name":"Sách Thiếu Nhi","description":"...","imageUrl":"..."}]` | `200 OK` | `Categories / Lấy toàn bộ thể loại` |
| `GET` | `/api/categories/{id}` | Public | Không | `{"id":1,"name":"Sách Thiếu Nhi",...}` | `200 OK` | `Categories / Chi tiết thể loại` |
| `POST` | `/api/categories` | `ADMIN` | `{"name":"Tâm Lý Kỹ Năng","description":"Sách phát triển bản thân","imageUrl":"..."}` | `{"id":11,"name":"Tâm Lý Kỹ Năng",...}` | `200 OK` | `Admin / Thêm thể loại mới` |
| `PUT` | `/api/categories/{id}` | `ADMIN` | `{"name":"Tâm Lý - Kỹ Năng Sống","description":"..."}` | `{"id":11,"name":"Tâm Lý - Kỹ Năng Sống",...}` | `200 OK` | `Admin / Cập nhật thể loại` |
| `DELETE` | `/api/categories/{id}` | `ADMIN` | Không | `{"message":"Đã xóa thể loại thành công!"}` | `200 OK` | `Admin / Xóa thể loại` |
| `GET` | `/api/banners` | Public | Không | `[{"id":1,"title":"Manga Hot","imageUrl":"...","linkUrl":"/category/1","position":"MAIN"}]` | `200 OK` | `Banners / Lấy toàn bộ banner` |
| `GET` | `/api/banners/position/{pos}` | Public | Không | `[{"id":1,"title":"...","position":"HOME_HERO"}]` | `200 OK` | `Banners / Lấy banner theo vị trí` |
| `POST` | `/api/banners` | `ADMIN` | `{"title":"Banner Sale Hè","imageUrl":"https://...","linkUrl":"/flash-sale","position":"MAIN"}` | `{"id":6,"title":"Banner Sale Hè",...}` | `200 OK` | `Admin / Thêm banner mới` |
| `PUT` | `/api/banners/{id}` | `ADMIN` | `{"title":"Banner Đã Sửa","linkUrl":"/promotions"}` | `{"id":1,"title":"Banner Đã Sửa",...}` | `200 OK` | `Admin / Cập nhật banner` |
| `DELETE` | `/api/banners/{id}` | `ADMIN` | Không | `{"message":"Đã xóa banner thành công!"}` | `200 OK` | `Admin / Xóa banner` |
| `GET` | `/api/cart` | `USER` / `ADMIN` | Không | `{"id":1,"user":{...},"items":[{"id":1,"book":{"id":1,"title":"..."},"quantity":2}]}` | `200 OK` | `Cart / Xem giỏ hàng` |
| `POST` | `/api/cart` | `USER` / `ADMIN` | `{"bookId":3,"quantity":1}` | `{"id":1,"items":[{"book":{"id":3,"title":"Nhà Giả Kim"},"quantity":1}]}` | `200 OK` | `Cart / Thêm vào giỏ` |
| `PUT` | `/api/cart/{bookId}` | `USER` / `ADMIN` | `{"quantity":4}` | `{"id":1,"items":[{"book":{"id":3},"quantity":4}]}` | `200 OK` | `Cart / Cập nhật số lượng` |
| `DELETE` | `/api/cart/{bookId}` | `USER` / `ADMIN` | Không | `{"id":1,"items":[]}` | `200 OK` | `Cart / Xóa 1 sản phẩm` |
| `DELETE` | `/api/cart` | `USER` / `ADMIN` | Không | `{"message":"Đã làm trống giỏ hàng!"}` | `200 OK` | `Cart / Xóa toàn bộ giỏ` |
| `POST` | `/api/orders` | `USER` / `ADMIN` | `{"items":[{"bookId":1,"quantity":1,"price":55000}],"shippingAddress":"123 Lê Lợi","phoneNumber":"090","paymentMethod":"COD","discountCouponCode":"GRAPE10"}` | `{"id":10,"totalAmount":49500,"status":"PENDING","shippingStatus":"PENDING"}` | `200 OK` | `Orders / Tạo đơn hàng mới` |
| `GET` | `/api/orders` | `USER` / `ADMIN` | Không | `[{"id":10,"totalAmount":49500,"status":"PENDING","createdAt":"..."}]` | `200 OK` | `Orders / Danh sách đơn cá nhân` |
| `GET` | `/api/orders/{id}` | `USER` / `ADMIN` | Không | `{"id":10,"user":{"username":"user@gmail.com"},"items":[...],"totalAmount":49500}` | `200 OK` | `Orders / Chi tiết 1 đơn hàng` |
| `PUT` | `/api/orders/{id}/cancel` | `USER` / `ADMIN` | Không | `{"id":10,"status":"CANCELLED","message":"Đã hủy đơn hàng thành công!"}` | `200 OK` | `Orders / Khách hủy đơn hàng` |
| `POST` | `/api/orders/{id}/return` | `USER` / `ADMIN` | `{"reason":"Sách bị rách gáy","evidenceImageUrl":"https://..."}` | `{"id":10,"status":"RETURN_REQUESTED"}` | `200 OK` | `Orders / Yêu cầu đổi trả` |
| `GET` | `/api/orders/all` | `ADMIN` | Không | `[{"id":10,"user":{"fullName":"..."},"status":"PENDING","shippingStatus":"PENDING"}]` | `200 OK` | `Admin / Lấy toàn bộ đơn hàng` |
| `PUT` | `/api/orders/{id}/shipping` | `ADMIN` | Query params: `status=SHIPPING&shippingPartner=GHN&trackingNumber=GHN001` | `{"id":10,"shippingStatus":"SHIPPING","shippingPartner":"GHN"}` | `200 OK` | `Admin / Cập nhật vận chuyển` |
| `PUT` | `/api/orders/{id}/return/approve` | `ADMIN` | Không | `{"id":10,"status":"RETURN_APPROVED"}` | `200 OK` | `Admin / Chấp thuận đổi trả` |
| `PUT` | `/api/orders/{id}/return/reject` | `ADMIN` | `{"rejectReason":"Không đủ chứng từ hư hỏng"}` | `{"id":10,"status":"RETURN_REJECTED"}` | `200 OK` | `Admin / Từ chối đổi trả` |
| `GET` | `/api/payment/create-url` | Public | Query params: `amount=150000&orderId=10` | `{"url":"https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?vnp_Amount=..."}` | `200 OK` | `Payment / VNPay - Create URL` |
| `GET` | `/api/payment/vnpay-callback` | Public | Query params trả về từ VNPAY (`vnp_ResponseCode=00`, `vnp_TxnRef=10`, `vnp_SecureHash=...`) | `{"status":"success","message":"Thanh toán thành công","orderId":10}` | `200 OK` | `Payment / VNPay Callback` |
| `GET` | `/api/coupons` | Public | Không | `[{"id":1,"code":"GRAPE10","discountType":"PERCENTAGE","discountValue":10.0,"minOrderAmount":100000.0}]` | `200 OK` | `Coupons / Danh sách mã giảm giá` |
| `GET` | `/api/coupons/validate` | Public | Query params: `code=GRAPE10&amount=150000` | `{"valid":true,"discountAmount":15000.0,"finalAmount":135000.0}` | `200 OK` | `Coupons / Kiểm tra mã giảm giá` |
| `GET` | `/api/coupons/all` | `ADMIN` | Không | `[{"id":1,"code":"GRAPE10","isActive":true,...}]` | `200 OK` | `Admin / Toàn bộ mã giảm giá` |
| `POST` | `/api/coupons` | `ADMIN` | `{"code":"SALE100K","discountType":"FIXED","discountValue":100000.0,"minOrderAmount":500000.0,"expirationDate":"2026-12-31T23:59:59"}` | `{"id":4,"code":"SALE100K",...}` | `200 OK` | `Admin / Tạo mã giảm giá mới` |
| `PUT` | `/api/coupons/{id}` | `ADMIN` | `{"code":"SALE100K","discountValue":120000.0}` | `{"id":4,"discountValue":120000.0,...}` | `200 OK` | `Admin / Cập nhật mã giảm giá` |
| `DELETE` | `/api/coupons/{id}` | `ADMIN` | Không | `{"message":"Đã xóa mã giảm giá thành công!"}` | `200 OK` | `Admin / Xóa mã giảm giá` |
| `GET` | `/api/rewards/vouchers` | Public | Không | `[{"id":1,"name":"Voucher 20k","pointsRequired":10000,"discountValue":20000}]` | `200 OK` | `Rewards / Danh sách quà đổi điểm` |
| `POST` | `/api/rewards/exchange` | `USER` / `ADMIN` | `{"points":10000,"type":"FREESHIP"}` | `{"message":"Đổi quà thành công!","voucherCode":"FS_98765432"}` | `200 OK` | `Rewards / Đổi điểm thưởng` |
| `GET` | `/api/rewards/my-vouchers` | `USER` / `ADMIN` | Không | `[{"id":1,"voucherCode":"FS_98765432","isUsed":false}]` | `200 OK` | `Rewards / Ví voucher của tôi` |
| `GET` | `/api/reviews/book/{bookId}` | Public | Không | `[{"id":1,"rating":5,"comment":"Sách rất tuyệt vời","user":{"fullName":"Khách hàng"}}]` | `200 OK` | `Reviews / Lấy review theo sách` |
| `GET` | `/api/reviews/check-eligibility/{bookId}` | `USER` / `ADMIN` | Không | `{"eligible":true,"reason":"Đủ điều kiện viết đánh giá"}` | `200 OK` | `Reviews / Kiểm tra điều kiện review` |
| `POST` | `/api/reviews/book/{bookId}` | `USER` / `ADMIN` | `{"rating":5,"comment":"Nội dung sách bổ ích, đóng gói cẩn thận"}` | `{"id":1,"rating":5,"comment":"..."}` | `200 OK` | `Reviews / Gửi bài đánh giá mới` |
| `POST` | `/api/reviews/{id}/like` | `USER` / `ADMIN` | Không | `{"id":1,"likesCount":1,"isLiked":true}` | `200 OK` | `Reviews / Thích bài đánh giá` |
| `POST` | `/api/reviews/{id}/comments` | `USER` / `ADMIN` | `{"content":"Cảm ơn bài chia sẻ của bạn!"}` | `{"id":1,"content":"...","createdAt":"..."}` | `200 OK` | `Reviews / Bình luận vào review` |
| `POST` | `/api/reviews/{id}/report` | `USER` / `ADMIN` | `{"reason":"Ngôn từ không phù hợp"}` | `{"message":"Đã gửi báo cáo vi phạm!"}` | `200 OK` | `Reviews / Báo cáo review vi phạm` |
| `GET` | `/api/admin/reviews` | `ADMIN` | Không | `[{"id":1,"rating":5,"comment":"...","isReported":false}]` | `200 OK` | `Admin / Quản trị đánh giá` |
| `DELETE` | `/api/admin/reviews/{id}` | `ADMIN` | Không | `{"message":"Đã xóa đánh giá vi phạm thành công!"}` | `200 OK` | `Admin / Xóa bài đánh giá` |
| `GET` | `/api/wishlists` | `USER` / `ADMIN` | Không | `[{"id":1,"book":{"id":3,"title":"Nhà Giả Kim","price":79000}}]` | `200 OK` | `Wishlist / Xem danh sách yêu thích` |
| `POST` | `/api/wishlists/book/{bookId}` | `USER` / `ADMIN` | Không | `{"bookId":3,"isLiked":true,"message":"Đã thêm vào yêu thích"}` | `200 OK` | `Wishlist / Thêm-Xóa yêu thích` |
| `GET` | `/api/notifications` | `USER` / `ADMIN` | Không | `[{"id":1,"title":"Chào mừng","content":"...","isRead":false}]` | `200 OK` | `Notifications / Danh sách thông báo` |
| `PUT` | `/api/notifications/{id}/read` | `USER` / `ADMIN` | Không | `{"id":1,"isRead":true}` | `200 OK` | `Notifications / Đánh dấu đã đọc` |
| `PUT` | `/api/notifications/read-all` | `USER` / `ADMIN` | Không | `{"message":"Đã đánh dấu toàn bộ đã đọc!"}` | `200 OK` | `Notifications / Đọc tất cả` |
| `POST` | `/api/notifications/admin/send` | `ADMIN` | `{"title":"Sale 9.9","content":"Flash sale toàn sàn 50%","type":"PROMO"}` | `{"id":4,"title":"Sale 9.9",...}` | `200 OK` | `Admin / Phát thông báo toàn sàn` |
| `POST` | `/api/newsletter/subscribe` | Public | `{"email":"subscriber@gmail.com"}` | `{"message":"Đăng ký nhận bản tin thành công!"}` | `200 OK` | `Newsletter / Đăng ký nhận tin` |
| `GET` | `/api/newsletter/subscribers` | `ADMIN` | Không | `[{"id":1,"email":"subscriber@gmail.com","active":true}]` | `200 OK` | `Admin / Danh sách subscriber` |
| `POST` | `/api/newsletter/send-bulk` | `ADMIN` | `{"subject":"Bản tin tuần mới","content":"<h1>Ưu đãi sách hot</h1>"}` | `{"message":"Đã gửi email bản tin thành công!"}` | `200 OK` | `Admin / Gửi email hàng loạt` |
| `POST` | `/api/contacts` | Public | `{"fullName":"Trần Văn C","email":"c@gmail.com","phone":"0912345678","message":"Cần tư vấn sách số lượng lớn"}` | `{"id":1,"fullName":"Trần Văn C","status":"PENDING"}` | `200 OK` | `Contacts / Gửi form liên hệ` |
| `GET` | `/api/contacts` | `ADMIN` | Không | `[{"id":1,"fullName":"Trần Văn C","status":"PENDING"}]` | `200 OK` | `Admin / Lấy danh sách liên hệ` |
| `PUT` | `/api/contacts/{id}/status` | `ADMIN` | `{"status":"PROCESSED"}` | `{"id":1,"status":"PROCESSED"}` | `200 OK` | `Admin / Cập nhật trạng thái liên hệ` |
| `DELETE` | `/api/contacts/{id}` | `ADMIN` | Không | `{"message":"Đã xóa thư liên hệ thành công!"}` | `200 OK` | `Admin / Xóa thư liên hệ` |
| `GET` | `/api/settings` | Public | Không | `{"site_title":"YiYi Book","hotline":"1900 1234","shipping_fee":"30000",...}` | `200 OK` | `Settings / Lấy cấu hình website` |
| `POST` | `/api/settings` | `ADMIN` | `{"site_title":"Nhà Sách Trực Tuyến YiYi Book","hotline":"1900 8888"}` | `{"message":"Đã lưu cấu hình thành công!"}` | `200 OK` | `Admin / Lưu cấu hình website` |
| `POST` | `/api/upload` | `USER` / `ADMIN` | `multipart/form-data (file: image.png)` | `{"url":"/uploads/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d.png"}` | `200 OK` | `Upload / Tải lên tệp ảnh` |
| `POST` | `/api/vat-invoices` | `USER` / `ADMIN` | `{"companyName":"Công Ty TNHH ABC","taxCode":"0312345678","companyAddress":"Quận 1, TP.HCM"}` | `{"id":1,"taxCode":"0312345678",...}` | `200 OK` | `VAT / Lưu hóa đơn VAT` |

---

### C. Danh Sách Toàn Bộ Màn Hình Giao Diện (UI Screens)

| Tên Màn hình (Page Path) | Đối tượng sử dụng (Actor) | Chức năng nghiệp vụ chính | Dữ liệu đầu vào (Input Form/Action) | Kết quả hiển thị (Output UI) | Luồng nghiệp vụ liên quan |
|---|:---:|---|---|---|---|
| **Trang chủ (`/`)** | Khách vãng lai / Thành viên | Trình chiếu Hero Banner, Flash Sale đếm ngược, Sách Bán Chạy, Danh mục thể loại, Sách Gợi ý cá nhân hóa | Click các tab danh mục, click banner, bấm chuyển trang slider | Hero Slider tự cuộn, lưới sách theo danh mục, giá giảm, tag Best Seller | Xem danh mục, Tìm kiếm, Đặt hàng |
| **Đăng nhập (`/login`)** | Khách vãng lai | Xác thực danh tính người dùng vào hệ thống | Email, Mật khẩu | Đăng nhập thành công, lưu JWT Token vào LocalStorage, Header cập nhật tên | Quản lý phiên làm việc |
| **Đăng ký (`/register`)** | Khách vãng lai | Tạo tài khoản khách hàng thành viên mới | Họ và tên, Email, Số điện thoại, Mật khẩu | Thông báo tạo tài khoản thành công, khởi tạo 1.000 điểm Y-Points ban đầu | Đăng ký thành viên |
| **Chi tiết sách (`/book/:id`)** | Khách vãng lai / Thành viên | Xem đầy đủ thông tin sách, ảnh bìa, giá niêm yết, tỷ lệ chiết khấu, tồn kho, mô tả nội dung, danh sách đánh giá sao | Bộ chọn số lượng mua (+/-), nút Thêm giỏ, nút Mua ngay, nút Tim yêu thích, form viết đánh giá sao | Thư viện ảnh, thông tin xuất bản, điểm đánh giá trung bình, các bình luận của độc giả | Giỏ hàng, Đánh giá, Yêu thích |
| **Tìm kiếm & Lọc (`/search`)** | Khách vãng lai / Thành viên | Tìm kiếm theo từ khóa tựa sách/tác giả, lọc kết hợp theo thể loại và khoảng giá | Ô nhập keyword, checkbox thể loại, thanh trượt / input min/max price, dropdown sắp xếp | Lưới sản phẩm khớp điều kiện, tổng số kết quả, phân trang trang 1, 2, 3... | Khám phá sản phẩm |
| **Giỏ hàng (`/cart`)** | Thành viên | Quản lý sản phẩm dự định mua, thay đổi số lượng, áp mã giảm giá | Nút tăng/giảm (+/-), nút Xóa sản phẩm, ô nhập mã giảm giá Coupon | Bảng sản phẩm, đơn giá, số lượng, tạm tính, số tiền chiết khấu coupon, tổng thanh toán | Mua hàng & Checkout |
| **Thanh toán (`/checkout`)** | Thành viên | Điền địa chỉ nhận hàng, chọn phương thức thanh toán COD hoặc Online, xuất hóa đơn VAT | Sổ chọn địa chỉ nhận hàng, họ tên, SĐT, ghi chú đơn hàng, radio chọn COD/VNPAY/VietQR/MoMo, checkbox VAT | Tóm tắt đơn hàng, phí vận chuyển, tiền giảm voucher, tổng tiền thanh toán cuối | Tạo đơn hàng |
| **Đặt hàng thành công (`/order-success`)** | Thành viên | Thông báo kết quả đặt hàng COD thành công | Không (nhận trạng thái từ Checkout chuyển sang) | Mã đơn hàng (Order ID), tổng tiền, thời gian dự kiến giao hàng, nút Xem đơn hàng | Vòng đời đơn hàng |
| **Kết quả thanh toán (`/payment-result`)** | Thành viên | Tiếp nhận kết quả thanh toán trực tuyến từ VNPAY / MoMo | Query parameters từ cổng thanh toán đối soát | Icon trạng thái Thành công / Thất bại, Mã giao dịch, Số tiền đã thanh toán | Thanh toán trực tuyến |
| **Lịch sử đơn hàng (`/orders`)** | Thành viên | Theo dõi toàn bộ hành trình đơn hàng cá nhân | Click các tab trạng thái (Tất cả, Chờ xác nhận, Đang xử lý, Đang giao, Đã giao, Đã hủy) | Danh sách thẻ đơn hàng, trạng thái vận chuyển, nút Hủy đơn, nút Yêu cầu đổi trả | Theo dõi & Đổi trả |
| **Chi tiết đơn hàng (`/orders/:id`)** | Thành viên | Xem chi tiết sản phẩm, địa chỉ giao hàng và mã vận đơn của 1 đơn hàng cụ thể | Click vào 1 đơn hàng | Danh sách sách đã mua, đơn giá, tổng tiền, mã tracking vận chuyển (GHN/GHTK) | Tra cứu đơn hàng |
| **Hồ sơ cá nhân (`/profile`)** | Thành viên | Cập nhật hồ sơ cá nhân, đổi mật khẩu, quản lý sổ địa chỉ, xem hạng VIP (Đồng/Bạc/Vàng/Kim Cương), đổi điểm thưởng Y-Points | Form cập nhật họ tên, ngày sinh, giới tính; Form đổi mật khẩu; Nút Đổi quà Voucher | Huy hiệu hạng thành viên, số dư Y-Points, mã Voucher đã đổi trong ví cá nhân | Quản lý tài khoản & Điểm |
| **Thông báo (`/notifications`)** | Thành viên | Xem danh sách thông báo khuyến mãi, cập nhật đơn hàng | Click vào thông báo, nút Đọc tất cả | Danh sách thông báo, chấm đỏ chưa đọc, thời gian nhận thông báo | Chăm sóc khách hàng |
| **Trang thể loại (`/category/:id`)** | Khách vãng lai / Thành viên | Khám phá các đầu sách theo từng thể loại chuyên biệt | Chọn thể loại từ menu, lọc giá | Banner thể loại, mô tả thể loại, danh mục sách thuộc thể loại đó | Khám phá danh mục |
| **Flash Sale (`/flash-sale`)** | Khách vãng lai / Thành viên | Xem danh mục các tựa sách đang giảm giá sốc có giới hạn thời gian | Click xem chi tiết | Đồng hồ đếm ngược Flash Sale, tỷ lệ % giảm giá, thanh tiến độ số lượng đã bán | Săn khuyến mãi |
| **Kho Voucher (`/coupons`)** | Khách vãng lai / Thành viên | Khám phá toàn bộ mã giảm giá đang hoạt động trên hệ thống | Nút Lưu mã / Sao chép mã | Danh sách thẻ Voucher (Giảm 10%, Giảm 50k, Freeship), điều kiện áp dụng, hạn dùng | Khuyến mãi |
| **Liên hệ & Góp ý (`/contact`)** | Khách vãng lai / Thành viên | Gửi ý kiến đóng góp, phản hồi thắc mắc dịch vụ đến ban quản trị | Họ và tên, Email, Số điện thoại, Nội dung tin nhắn | Thông báo gửi thư liên hệ thành công, xóa trắng form sau gửi | Chăm sóc khách hàng |
| **Trợ lý ảo YiYi AI (`AIChatWidget`)** | Khách vãng lai / Thành viên | Tư vấn, gợi ý sách thông minh bằng AI Mini-RAG | Ô nhập câu hỏi tư vấn, click các gợi ý prompt nhanh | Khung chat nổi toàn trang, câu trả lời streaming SSE, thẻ sản phẩm trực quan | Tư vấn & Bán hàng AI |
| **Admin Dashboard (`/admin`)** | Quản trị viên (Admin) | Thống kê tổng quan doanh thu, số lượng đơn, khách hàng mới | Bộ chọn khoảng thời gian (Hôm nay, Tuần này, Tháng này) | Thẻ KPI doanh số, biểu đồ tăng trưởng, danh sách đơn hàng mới nhất cần duyệt | Báo cáo quản trị |
| **Admin Quản lý Sách (`/admin/books`)** | Quản trị viên (Admin) | Quản trị kho sách, thêm mới, sửa giá, tồn kho, tải ảnh bìa, nhập Excel | Form nhập sách (Tựa sách, tác giả, giá, tồn kho, danh mục, ảnh), nút Nhập Excel | Bảng danh sách sách, modal chỉnh sửa, tìm kiếm sách trong kho | Quản trị kho sách |
| **Admin Quản lý Đơn (`/admin/orders`)** | Quản trị viên (Admin) | Duyệt đơn hàng, giao vận chuyển, phê duyệt/từ chối đổi trả | Dropdown chọn trạng thái vận chuyển (SHIPPING, DELIVERED), chọn đối tác (GHN/GHTK), nhập mã tracking | Danh sách toàn bộ đơn hàng toàn sàn, modal chi tiết đơn, bộ lọc trạng thái | Xử lý đơn & Vận chuyển |
| **Admin Quản lý User (`/admin/users`)** | Quản trị viên (Admin) | Quản lý danh sách tài khoản, phân quyền, khóa/mở khóa tài khoản | Dropdown đổi quyền (USER/ADMIN), nút Khóa/Mở, nút Xóa | Danh sách người dùng, trạng thái kích hoạt, phân quyền hệ thống | Quản trị người dùng |
| **Admin Mã Giảm Giá (`/admin/coupons`)** | Quản trị viên (Admin) | Thiết lập chương trình khuyến mãi, sinh mã giảm giá | Mã coupon, loại giảm (% hoặc cố định), giá trị giảm, đơn tối thiểu, ngày hết hạn | Bảng danh sách coupon, nút kích hoạt/tắt mã, nút xóa | Quản trị khuyến mãi |
| **Admin Đổi Thưởng (`/admin/rewards`)** | Quản trị viên (Admin) | Cấu hình kho quà tặng đổi điểm thưởng Y-Points | Tên quà tặng, điểm yêu cầu, giá trị chiết khấu | Danh sách voucher đổi thưởng trong hệ thống | Quản trị tích điểm |
| **Admin Kiểm Duyệt Đánh Giá (`/admin/reviews`)** | Quản trị viên (Admin) | Kiểm duyệt bình luận, ẩn/xóa đánh giá độc hại | Nút Xóa đánh giá vi phạm, nút Bỏ qua báo cáo | Bảng toàn bộ đánh giá từ khách hàng, số sao, nội dung nhận xét | Kiểm duyệt nội dung |
| **Admin Cài Đặt Hệ Thống (`/admin/settings`)** | Quản trị viên (Admin) | Cấu hình thông số website, hotline, phí ship mặc định | Tiêu đề website, Hotline, Email CSKH, Phí vận chuyển tiêu chuẩn | Thông báo cập nhật cấu hình thành công | Cấu hình hệ thống |

---

# PHẦN 3: ĐẶC TẢ TOÀN BỘ TEST CASE PHÂN VÙNG TƯƠNG ĐƯƠNG (EP)

---

### Module 1: Xác Thực & Đăng Ký Tài Khoản (Authentication - Register)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-REG-01** | Register | Hợp lệ | Đầy đủ thông tin hợp lệ (Email mới, pass $\ge 6$ ký tự, phone 10 số) | Giao diện UI (`/register`) | Email chưa có trong hệ thống | `fullName`: `Nguyễn Văn An`<br>`email`: `nguyenvanan.test@gmail.com`<br>`phone`: `0901234567`<br>`password`: `Abc@123456` | 1. Mở trang `/register`<br>2. Nhập đầy đủ form<br>3. Bấm nút "Đăng Ký" | Đăng ký thành công, hiển thị Toast thông báo thành công, tự động đăng nhập và lưu JWT token vào LocalStorage | | | Ảnh Toast đăng ký thành công | |
| **EP-REG-02** | Register | Không hợp lệ | Để trống trường Họ và Tên | Giao diện UI (`/register`) | Bất kỳ | `fullName`: ` ` (rỗng)<br>`email`: `user.test@gmail.com`<br>`phone`: `0901234567`<br>`password`: `123456` | 1. Mở trang `/register`<br>2. Bỏ trống Họ tên<br>3. Bấm nút "Đăng Ký" | Hệ thống chặn submit, hiển thị thông báo lỗi ngay dưới ô Họ tên: "Họ và tên không được để trống" | | | Ảnh thông báo lỗi validation đỏ | |
| **EP-REG-03** | Register | Không hợp lệ | Email sai định dạng (thiếu `@` và tên miền) | Giao diện UI (`/register`) | Bất kỳ | `fullName`: `Trần Bình`<br>`email`: `tranbinhemail`<br>`phone`: `0901234567`<br>`password`: `123456` | 1. Nhập email sai chuẩn<br>2. Bấm nút "Đăng Ký" | Trình duyệt và React chặn gửi form, báo lỗi "Vui lòng nhập đúng định dạng email" | | | Ảnh báo lỗi email sai định dạng | |
| **EP-REG-04** | Register | Không hợp lệ | Email đã tồn tại trong cơ sở dữ liệu | Postman / UI | Đã có tài khoản `user@gmail.com` | `fullName`: `Trần Bình`<br>`email`: `user@gmail.com`<br>`phone`: `0909998888`<br>`password`: `123456` | 1. Gửi request `POST /api/auth/register`<br>2. Đính kèm email đã tồn tại | Backend phản hồi HTTP `400 Bad Request` với message: "Email này đã được đăng ký sử dụng!" | | | Ảnh response Postman nhận mã 400 | |
| **EP-REG-05** | Register | Không hợp lệ | Mật khẩu ngắn hơn 6 ký tự | Giao diện UI (`/register`) | Bất kỳ | `fullName`: `Lê Cường`<br>`email`: `lecuong@gmail.com`<br>`phone`: `0901234567`<br>`password`: `12345` (5 ký tự) | 1. Nhập mật khẩu 5 ký tự<br>2. Bấm "Đăng Ký" | Báo lỗi validation: "Mật khẩu phải có độ dài tối thiểu từ 6 ký tự trở lên" | | | Ảnh báo lỗi mật khẩu ngắn | |
| **EP-REG-06** | Register | Không hợp lệ | Số điện thoại chứa chữ cái hoặc ký tự đặc biệt | Giao diện UI (`/register`) | Bất kỳ | `fullName`: `Phạm Dũng`<br>`email`: `phamdung@gmail.com`<br>`phone`: `09012ABC#$`<br>`password`: `123456` | 1. Nhập SĐT chứa chữ<br>2. Bấm "Đăng Ký" | Báo lỗi: "Số điện thoại không hợp lệ (chỉ bao gồm chữ số)" | | | Ảnh thông báo lỗi SĐT | |
| **EP-REG-07** | Register | Không hợp lệ | Payload rỗng (Empty JSON Body) | API Postman | Không | Body: `{}` | 1. Gửi `POST /api/auth/register` với body rỗng `{}` | Backend phản hồi HTTP `400 Bad Request` cấu trúc `GlobalExceptionHandler` báo lỗi thiếu trường bắt buộc | | | Ảnh Postman nhận lỗi 400 Validation | |

---

### Module 2: Xác Thực & Đăng Nhập (Authentication - Login)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-LOG-01** | Login | Hợp lệ | Tài khoản Khách hàng (User) chính xác | Giao diện UI (`/login`) | Tài khoản `user@gmail.com` tồn tại, pass `123456` | `email`: `user@gmail.com`<br>`password`: `123456` | 1. Mở `/login`<br>2. Nhập thông tin<br>3. Bấm "Đăng Nhập" | Đăng nhập thành công, chuyển hướng về Trang chủ, Header hiển thị tên "Khách hàng" | | | Ảnh Header đã đăng nhập User | |
| **EP-LOG-02** | Login | Hợp lệ | Tài khoản Quản trị viên (Admin) chính xác | Giao diện UI (`/login`) | Tài khoản `admin@gmail.com` tồn tại, pass `123456` | `email`: `admin@gmail.com`<br>`password`: `123456` | 1. Mở `/login`<br>2. Nhập thông tin Admin<br>3. Bấm "Đăng Nhập" | Đăng nhập thành công, Header xuất hiện menu "Quản Trị", chuyển hướng sang `/admin` Dashboard | | | Ảnh giao diện Cổng Admin | |
| **EP-LOG-03** | Login | Không hợp lệ | Mật khẩu không chính xác | Giao diện UI (`/login`) | User `user@gmail.com` tồn tại | `email`: `user@gmail.com`<br>`password`: `SaiMatKhau999` | 1. Nhập email đúng, pass sai<br>2. Bấm "Đăng Nhập" | Hiển thị Toast lỗi: "Tên đăng nhập hoặc mật khẩu không chính xác!", không chuyển trang | | | Ảnh thông báo lỗi đăng nhập | |
| **EP-LOG-04** | Login | Không hợp lệ | Email chưa từng đăng ký trong hệ thống | Giao diện UI (`/login`) | Email không tồn tại | `email`: `khongtontai999@gmail.com`<br>`password`: `123456` | 1. Nhập email chưa đăng ký<br>2. Bấm "Đăng Nhập" | Hiển thị thông báo: "Tài khoản không tồn tại hoặc mật khẩu sai!", HTTP `400`/`401` | | | Ảnh thông báo tài khoản sai | |
| **EP-LOG-05** | Login | Không hợp lệ | Để trống toàn bộ trường Email và Mật khẩu | Giao diện UI (`/login`) | Bất kỳ | `email`: ` `<br>`password`: ` ` | 1. Không nhập dữ liệu<br>2. Bấm "Đăng Nhập" | Chặn submit, báo lỗi yêu cầu nhập đầy đủ email và mật khẩu | | | Ảnh form báo lỗi rỗng | |
| **EP-LOG-06** | Login | Không hợp lệ | Thử nghiệm tấn công SQL Injection vào ô Email | API Postman | Không | `email`: `' OR '1'='1`<br>`password`: `' OR '1'='1` | 1. Gửi request `POST /api/auth/login` với payload SQLi | Backend xử lý an toàn qua JPA Parameterized Query, trả về `400 Bad Request` hoặc `401 Unauthorized` | | | Ảnh Postman chặn SQLi an toàn | |

---

### Module 3: Quản Lý Hồ Sơ & Đổi Mật Khẩu (User Profile & Password)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-PRF-01** | Profile | Hợp lệ | Cập nhật thông tin họ tên, ngày sinh, giới tính | Giao diện UI (`/profile`) | Đã đăng nhập `user@gmail.com` | `fullName`: `Nguyễn Văn A (Đã sửa)`<br>`phone`: `0911223344`<br>`gender`: `MALE`<br>`birthday`: `1998-10-20` | 1. Mở trang `/profile`<br>2. Sửa thông tin<br>3. Bấm "Lưu Thay Đổi" | Hiển thị thông báo "Cập nhật hồ sơ thành công!", dữ liệu trên giao diện lưu giữ giá trị mới | | | Ảnh hồ sơ đã cập nhật | |
| **EP-PRF-02** | Profile | Hợp lệ | Cập nhật sở thích đọc sách phục vụ Trợ lý AI | Giao diện UI (`/profile`) | Đã đăng nhập | `aiPreferences`: `Thích tiểu thuyết trinh thám, manga hành động` | 1. Nhập ô sở thích AI<br>2. Bấm Lưu | Backend lưu trường `ai_preferences` vào DB, AI Chatbot ghi nhớ sở thích này khi tư vấn | | | Ảnh trường sở thích AI | |
| **EP-PWD-01** | Password | Hợp lệ | Mật khẩu cũ đúng + Mật khẩu mới $\ge 6$ ký tự | Giao diện UI (`/profile`) | Mật khẩu hiện tại là `123456` | `oldPassword`: `123456`<br>`newPassword`: `matkhauMoi@2026` | 1. Nhập mật khẩu cũ và mới<br>2. Bấm "Đổi Mật Khẩu" | Hiển thị thông báo "Đổi mật khẩu thành công!", đăng xuất và đăng nhập lại bằng mật khẩu mới thành công | | | Ảnh thông báo đổi pass thành công | |
| **EP-PWD-02** | Password | Không hợp lệ | Nhập mật khẩu cũ không chính xác | Giao diện UI (`/profile`) | Mật khẩu hiện tại là `123456` | `oldPassword`: `SaiPassCu`<br>`newPassword`: `matkhauMoi@2026` | 1. Nhập sai pass cũ<br>2. Bấm "Đổi Mật Khẩu" | Báo lỗi: "Mật khẩu cũ không chính xác!", không cập nhật mật khẩu mới trong DB | | | Ảnh báo lỗi sai pass cũ | |
| **EP-PWD-03** | Password | Không hợp lệ | Mật khẩu mới có độ dài dưới 6 ký tự | Giao diện UI (`/profile`) | Mật khẩu hiện tại là `123456` | `oldPassword`: `123456`<br>`newPassword`: `12345` | 1. Nhập pass mới 5 ký tự<br>2. Bấm Đổi | Báo lỗi: "Mật khẩu mới phải có ít nhất 6 ký tự!", HTTP `400 Bad Request` | | | Ảnh form chặn pass ngắn | |

---

### Module 4: Tìm Kiếm & Khám Phá Sách (Search & Catalogue)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-SCH-01** | Search | Hợp lệ | Tìm kiếm theo tên tựa sách chính xác | Giao diện UI (`/search`) | Sách "Clean Code" có trong DB | `keyword`: `Clean Code` | 1. Nhập ô tìm kiếm<br>2. Nhấn Enter | Hiển thị đúng sản phẩm "Clean Code" (Giá 250.000đ, Tác giả Robert C. Martin) | | | Ảnh kết quả tìm thấy sách | |
| **EP-SCH-02** | Search | Hợp lệ | Tìm kiếm tiếng Việt có dấu / không dấu | Giao diện UI (`/search`) | Sách "Dế Mèn Phiêu Lưu Ký" có trong DB | `keyword`: `De Men Phieu Luu Ky` | 1. Nhập từ khóa không dấu<br>2. Nhấn Enter | Tìm kiếm khớp chính xác cuốn "Dế Mèn Phiêu Lưu Ký" | | | Ảnh kết quả tìm không dấu | |
| **EP-SCH-03** | Search | Hợp lệ | Tìm kiếm theo tên tác giả | Giao diện UI (`/search`) | Tác giả "Paulo Coelho" | `keyword`: `Paulo Coelho` | 1. Nhập tên tác giả<br>2. Nhấn Enter | Lưới hiển thị tác phẩm "Nhà Giả Kim" của tác giả Paulo Coelho | | | Ảnh kết quả tìm theo tác giả | |
| **EP-SCH-04** | Search | Hợp lệ | Lọc kết hợp theo Thể loại và Khoảng giá | Giao diện UI (`/search`) | Danh mục Sách Thiếu Nhi | `Category`: `Sách Thiếu Nhi`<br>`minPrice`: `20000`<br>`maxPrice`: `60000` | 1. Tích chọn Sách Thiếu Nhi<br>2. Điền khoảng giá 20k - 60k<br>3. Bấm Lọc | Hiển thị cuốn "Dế Mèn Phiêu Lưu Ký" (55.000đ) và "Doraemon" (25.000đ) | | | Ảnh lưới sách sau khi lọc | |
| **EP-SCH-05** | Search | Không hợp lệ | Từ khóa hoàn toàn không tồn tại trong kho | Giao diện UI (`/search`) | Không có sách khớp | `keyword`: `TuKhoaKyLaKhongTheCo9999` | 1. Nhập từ khóa lạ<br>2. Nhấn Enter | Hiển thị giao diện trạng thái trống (Empty State): "Không tìm thấy sản phẩm nào phù hợp", không bị crash | | | Ảnh màn hình không có kết quả | |
| **EP-SCH-06** | Search | Không hợp lệ | Khoảng giá lọc nghịch đảo (`minPrice > maxPrice`) | Giao diện UI (`/search`) | Bất kỳ | `minPrice`: `500000`<br>`maxPrice`: `100000` | 1. Điền giá min lớn hơn max<br>2. Bấm Lọc | Hệ thống tự động hoán đổi hoặc thông báo: "Khoảng giá không hợp lệ", lưới trả về rỗng an toàn | | | Ảnh xử lý khoảng giá sai | |

---

### Module 5: Giỏ Hàng & Quản Trị Tồn Kho (Cart & Inventory)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-CRT-01** | Cart | Hợp lệ | Thêm sản phẩm với số lượng hợp lệ ($1 \le Q \le \text{Stock}$) | Giao diện UI (`/book/1`) | Sách ID 1 có tồn kho 100 | `bookId`: `1`<br>`quantity`: `3` | 1. Vào trang chi tiết sách 1<br>2. Chọn số lượng 3<br>3. Bấm "Thêm vào giỏ" | Thông báo "Đã thêm vào giỏ hàng!", Badge giỏ hàng trên Header tăng lên 3 | | | Ảnh giỏ hàng có 3 món | |
| **EP-CRT-02** | Cart | Hợp lệ | Cập nhật tăng số lượng trong trang giỏ hàng | Giao diện UI (`/cart`) | Giỏ hàng đang có 1 cuốn sách ID 1 | Click nút `+` (tăng lên 2) | 1. Mở trang `/cart`<br>2. Bấm dấu `+` | Số lượng cập nhật thành 2, tổng tiền tự động nhân đôi chính xác | | | Ảnh giỏ hàng cập nhật số lượng | |
| **EP-CRT-03** | Cart | Hợp lệ | Xóa một dòng sản phẩm khỏi giỏ hàng | Giao diện UI (`/cart`) | Giỏ hàng có 2 loại sách | Click icon Thùng rác tại dòng sách ID 1 | 1. Bấm nút Xóa dòng sách 1<br>2. Xác nhận xóa | Dòng sách biến mất, tổng tiền giỏ hàng trừ bớt giá trị sản phẩm đã xóa | | | Ảnh giỏ hàng sau khi xóa | |
| **EP-CRT-04** | Cart | Không hợp lệ | Thêm số lượng sản phẩm âm hoặc bằng 0 | API Postman | Đã có JWT Token | `bookId`: `1`<br>`quantity`: `-3` | 1. Gửi request `POST /api/cart` với quantity âm | Backend trả về HTTP `400 Bad Request`: "Số lượng sản phẩm không hợp lệ!" | | | Ảnh Postman nhận lỗi 400 | |
| **EP-CRT-05** | Cart | Không hợp lệ | Thêm số lượng vượt quá số lượng tồn kho | Giao diện UI (`/book/4`) | Sách ID 4 còn tồn kho 20 cuốn | `bookId`: `4`<br>`quantity`: `50` | 1. Nhập số lượng 50<br>2. Bấm Thêm giỏ | Hiển thị cảnh báo: "Số lượng yêu cầu vượt quá tồn kho hiện có (tối đa 20 cuốn)!", không thêm vào giỏ | | | Ảnh cảnh báo vượt tồn kho | |
| **EP-CRT-06** | Cart | Không hợp lệ | Thêm mã sách không tồn tại vào giỏ | API Postman | Đã có JWT Token | `bookId`: `999999`<br>`quantity`: `1` | 1. Gửi `POST /api/cart` với ID 999999 | Backend trả về HTTP `400 Bad Request`: "Sách (ID: 999999) không tồn tại hoặc đã ngừng kinh doanh!" | | | Ảnh Postman nhận lỗi không tồn tại | |

---

### Module 6: Mã Giảm Giá & Khuyến Mãi (Coupon & Promotion)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-CPN-01** | Coupon | Hợp lệ | Mã giảm giá theo phần trăm (`PERCENTAGE`), đủ điều kiện | Giao diện UI (`/cart`) | Giỏ hàng có tổng tiền 200.000đ | `code`: `GRAPE10` (Giảm 10%, min 100k) | 1. Nhập mã `GRAPE10`<br>2. Bấm "Áp Dụng" | Áp dụng thành công, chiết khấu giảm 20.000đ, tổng tiền thanh toán còn 180.000đ | | | Ảnh giảm giá 10% thành công | |
| **EP-CPN-02** | Coupon | Hợp lệ | Mã giảm giá số tiền cố định (`FIXED`), đủ điều kiện | Giao diện UI (`/cart`) | Giỏ hàng có tổng tiền 350.000đ | `code`: `SALE50K` (Giảm 50k, min 300k) | 1. Nhập mã `SALE50K`<br>2. Bấm "Áp Dụng" | Áp dụng thành công, chiết khấu giảm 50.000đ, tổng tiền thanh toán còn 300.000đ | | | Ảnh giảm giá 50k thành công | |
| **EP-CPN-03** | Coupon | Không hợp lệ | Đơn hàng chưa đạt giá trị tối thiểu của mã | Giao diện UI (`/cart`) | Giỏ hàng có tổng tiền 80.000đ | `code`: `GRAPE10` (Yêu cầu tối thiểu 100k) | 1. Nhập mã `GRAPE10`<br>2. Bấm "Áp Dụng" | Báo lỗi: "Đơn hàng tối thiểu 100.000đ để áp dụng mã này (còn thiếu 20.000đ)", không giảm giá | | | Ảnh thông báo chưa đủ tiền | |
| **EP-CPN-04** | Coupon | Không hợp lệ | Nhập mã giảm giá không tồn tại trong hệ thống | Giao diện UI (`/cart`) | Bất kỳ | `code`: `MA_KHONG_TON_TAI_999` | 1. Nhập mã bừa<br>2. Bấm "Áp Dụng" | Báo lỗi: "Mã giảm giá không hợp lệ hoặc đã hết hạn!", HTTP `400 Bad Request` | | | Ảnh thông báo mã không tồn tại | |
| **EP-CPN-05** | Coupon | Không hợp lệ | Áp dụng mã đã hết hạn sử dụng | API Postman | Coupon có `expirationDate` trong quá khứ | `code`: `EXPIRED_COUPON` | 1. Gửi request validate coupon hết hạn | Backend trả về `400 Bad Request`: "Mã giảm giá đã hết hạn sử dụng!" | | | Ảnh Postman nhận lỗi hết hạn | |

---

### Module 7: Điểm Thưởng & Khách Hàng Thân Thiết (Y-Points & Rewards)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-REW-01** | Reward | Hợp lệ | Đổi Voucher Freeship với đủ điểm thưởng | Giao diện UI (`/profile`) | User có số dư 15.000 Y-Points | Bấm nút Đổi tại thẻ `Voucher Freeship 30k` (Cần 10.000 điểm) | 1. Mở tab Đổi Thưởng<br>2. Bấm "Đổi Ngay" | Trừ 10.000 điểm (số dư còn 5.000), ví voucher nhận thêm mã `FS_...` có thể dùng khi checkout | | | Ảnh đổi thành công voucher | |
| **EP-REW-02** | Reward | Không hợp lệ | Đổi quà khi số dư điểm không đủ | Giao diện UI (`/profile`) | User có số dư 2.000 Y-Points | Bấm nút Đổi tại thẻ `Voucher 50k` (Cần 20.000 điểm) | 1. Mở tab Đổi Thưởng<br>2. Bấm "Đổi Ngay" | Nút đổi bị disabled hoặc hiển thị cảnh báo: "Bạn không đủ điểm thưởng để đổi voucher này" | | | Ảnh cảnh báo không đủ điểm | |
| **EP-REW-03** | Reward | Không hợp lệ | Gửi request đổi điểm số lượng âm | API Postman | Đã có JWT Token | `points`: `-5000`<br>`type`: `FREESHIP` | 1. Gửi `POST /api/rewards/exchange` với points âm | Backend chặn xử lý, trả về HTTP `400 Bad Request`, số dư điểm không bị thay đổi | | | Ảnh Postman chặn đổi điểm âm | |

---

### Module 8: Đặt Hàng & Thanh Toán (Checkout & Orders)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-ORD-01** | Order | Hợp lệ | Đặt hàng COD đầy đủ thông tin giao hàng | Giao diện UI (`/checkout`) | Giỏ hàng có sản phẩm | `address`: `123 Nguyễn Văn Cừ, Q5, TP.HCM`<br>`phone`: `0901234567`<br>`paymentMethod`: `COD` | 1. Điền thông tin giao hàng<br>2. Chọn COD<br>3. Bấm "Xác Nhận Đặt Hàng" | Đặt hàng thành công, giỏ hàng tự động làm trống, chuyển hướng sang `/order-success`, DB tạo đơn `PENDING` | | | Ảnh màn hình Order Success | |
| **EP-ORD-02** | Order | Hợp lệ | Đặt hàng chọn cổng thanh toán trực tuyến VNPAY | Giao diện UI (`/checkout`) | Giỏ hàng có sản phẩm | `address`: `123 Lê Lợi, Q1`<br>`paymentMethod`: `VNPAY` | 1. Điền thông tin<br>2. Chọn VNPAY<br>3. Bấm Thanh toán | Chuyển hướng sang cổng thanh toán VNPAY Sandbox với đúng số tiền đơn hàng | | | Ảnh màn hình cổng VNPAY | |
| **EP-ORD-03** | Order | Không hợp lệ | Đặt hàng khi giỏ hàng đang rỗng | Giao diện UI (`/checkout`) | Giỏ hàng không có sản phẩm nào | Form checkout trống | 1. Cố tình truy cập `/checkout` khi giỏ rỗng | Hệ thống tự động chuyển hướng về `/cart` kèm cảnh báo "Giỏ hàng của bạn đang trống!" | | | Ảnh điều hướng về giỏ hàng | |
| **EP-ORD-04** | Order | Không hợp lệ | Bỏ trống địa chỉ nhận hàng hoặc số điện thoại | Giao diện UI (`/checkout`) | Giỏ hàng có sản phẩm | `address`: ` `<br>`phone`: ` ` | 1. Để trống thông tin<br>2. Bấm "Xác Nhận Đặt Hàng" | Chặn gửi request, hiển thị thông báo lỗi yêu cầu chọn hoặc nhập địa chỉ nhận hàng | | | Ảnh báo lỗi thiếu địa chỉ | |
| **EP-ORD-05** | Order | Hợp lệ | Khách hàng hủy đơn hàng khi trạng thái còn `PENDING` | Giao diện UI (`/orders`) | Đơn hàng đang ở trạng thái `PENDING` | Bấm nút "Hủy đơn hàng" tại thẻ đơn | 1. Mở trang `/orders`<br>2. Bấm Hủy đơn<br>3. Xác nhận | Đơn chuyển sang trạng thái `CANCELLED`, hoàn lại số lượng tồn kho sách tương ứng vào DB | | | Ảnh đơn hàng đã bị hủy | |
| **EP-ORD-06** | Order | Không hợp lệ | Khách hàng cố tình hủy đơn khi đã `SHIPPING` | API Postman | Đơn hàng đang ở trạng thái `SHIPPING` | Gửi request `PUT /api/orders/{id}/cancel` | 1. Gửi request hủy đơn đang giao | Backend từ chối hủy, trả về HTTP `400 Bad Request`: "Không thể hủy đơn hàng đang trong quá trình vận chuyển!" | | | Ảnh Postman chặn hủy đơn giao | |

---

### Module 9: Đánh Giá & Bình Luận Sản Phẩm (Review & Comments)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-REV-01** | Review | Hợp lệ | Đã mua & nhận hàng thành công, chấm 5 sao | Giao diện UI (`/book/1`) | User đã mua sách ID 1 và đơn hàng trạng thái `DELIVERED` | `rating`: `5`<br>`comment`: `Sách in ấn rất đẹp, giao hàng nhanh chóng.` | 1. Mở trang chi tiết sách<br>2. Chấm 5 sao + Nhập nhận xét<br>3. Bấm "Gửi Đánh Giá" | Gửi đánh giá thành công, bài đánh giá hiển thị ngay tại mục bình luận của sách, điểm sao TB cập nhật | | | Ảnh bài đánh giá 5 sao | |
| **EP-REV-02** | Review | Không hợp lệ | Chưa từng mua sản phẩm mà gửi đánh giá | UI / Postman | User chưa từng có đơn hàng nào chứa sách ID 2 | `bookId`: `2`<br>`rating`: `5`<br>`comment`: `Sách hay lắm` | 1. Mở sách chưa mua<br>2. Gửi đánh giá | Nút đánh giá bị ẩn hoặc Backend trả về `400 Bad Request`: "Bạn cần mua và nhận sản phẩm này để viết đánh giá!" | | | Ảnh báo lỗi ràng buộc mua hàng | |
| **EP-REV-03** | Review | Không hợp lệ | Chấm điểm số sao ngoài khoảng 1-5 (Ví dụ: 0 sao hoặc 6 sao) | API Postman | User đã mua sách ID 1 | `rating`: `0` hoặc `6`<br>`comment`: `Đánh giá thử nghiệm` | 1. Gửi request `POST /api/reviews/book/1` với rating sai | Backend trả về HTTP `400 Bad Request`: "Số sao đánh giá phải từ 1 đến 5!" | | | Ảnh Postman nhận lỗi rating | |
| **EP-REV-04** | Review | Không hợp lệ | Để trống nội dung bình luận nhận xét | Giao diện UI (`/book/1`) | User đủ điều kiện review | `rating`: `5`<br>`comment`: ` ` (rỗng) | 1. Chọn 5 sao<br>2. Để trống nhận xét<br>3. Bấm Gửi | Báo lỗi validation: "Vui lòng nhập nội dung đánh giá nhận xét!" | | | Ảnh báo lỗi nhận xét rỗng | |
| **EP-REV-05** | Review | Hợp lệ | Thích (Like) hoặc Thảo luận bình luận vào bài đánh giá | Giao diện UI (`/book/1`) | Đã có bài review của người khác | Click icon Trái tim (Like) hoặc gõ trả lời bình luận | 1. Bấm nút Thích<br>2. Gõ bình luận trả lời | Số lượt thích tăng lên 1, phản hồi lồng hiển thị ngay dưới bài đánh giá | | | Ảnh like và reply review | |

---

### Module 10: Tải Lên Tệp & Ảnh Đại Diện (File Upload)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-UPL-01** | Upload | Hợp lệ | Tải lên file ảnh hợp lệ (.png, .jpg, .webp, kích thước < 5MB) | Giao diện UI / Postman | Đã có JWT Token | File ảnh `bia_sach.png` (dung lượng 500KB) | 1. Chọn file ảnh<br>2. Bấm Upload | Upload thành công, trả về HTTP `200 OK` kèm đường dẫn tĩnh dạng `/uploads/uuid.png` | | | Ảnh upload thành công | |
| **EP-UPL-02** | Upload | Không hợp lệ | Tải lên file mã nguồn / thực thi nguy hiểm (.exe, .sh, .bat, .jsp) | API Postman | Đã có JWT Token | File script `backdoor.sh` | 1. Gửi `POST /api/upload` với file .sh | Backend chặn xử lý, trả về HTTP `400 Bad Request`: "Chỉ cho phép tải lên định dạng hình ảnh (.jpg, .png, .webp) hoặc tài liệu PDF!" | | | Ảnh Postman chặn file độc hại | |
| **EP-UPL-03** | Upload | Không hợp lệ | Request không đính kèm tham số file (Empty multipart) | API Postman | Đã có JWT Token | Multipart body rỗng | 1. Gửi `POST /api/upload` không có file | Backend bắt lỗi qua `GlobalExceptionHandler`, trả về HTTP `400 Bad Request` an toàn | | | Ảnh Postman nhận lỗi 400 | |

---

### Module 11: Trợ Lý Ảo YiYi AI & Mini-RAG (AI Assistant)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-AI-01** | YiYi AI | Hợp lệ | Câu hỏi tìm kiếm tựa sách có trong kho | Giao diện Chatbot | Đang mở widget chat | *"Cửa hàng có sách Clean Code không và giá bao nhiêu?"* | 1. Mở widget AI<br>2. Nhập câu hỏi<br>3. Bấm Gửi | Trả lời chính xác có sách "Clean Code", giá 250.000đ, hiển thị Thẻ sản phẩm có nút "Thêm vào giỏ" | | | Ảnh trả lời kèm thẻ sách Clean Code | |
| **EP-AI-02** | YiYi AI | Hợp lệ | Câu hỏi nhờ tư vấn thể loại sách thiếu nhi | Giao diện Chatbot | Đang mở widget chat | *"Gợi ý cho tôi vài cuốn sách thiếu nhi hay nhất"* | 1. Nhập câu hỏi gợi ý<br>2. Bấm Gửi | Phân tích intent gợi ý, trích xuất "Dế Mèn Phiêu Lưu Ký", "Doraemon" kèm các thẻ xem nhanh sản phẩm | | | Ảnh danh sách thẻ sách thiếu nhi | |
| **EP-AI-03** | YiYi AI | Hợp lệ | Câu hỏi về sách không tồn tại trong kho (Zero Hallucination) | Giao diện Chatbot | Đang mở widget chat | *"Shop có bán sách Giáo trình Luyện bay đĩa bay không?"* | 1. Nhập câu hỏi sách lạ<br>2. Bấm Gửi | Trả lời lịch sự hiện tại cửa hàng chưa kinh doanh tựa sách này, không tự bịa đặt tác phẩm không có thật | | | Ảnh phản hồi từ chối lịch sự | |
| **EP-AI-04** | YiYi AI | Không hợp lệ | Gửi câu hỏi rỗng hoặc chỉ toàn dấu cách | Giao diện Chatbot | Đang mở widget chat | `message`: ` ` (chỉ có khoảng trắng) | 1. Nhập khoảng trắng<br>2. Bấm Gửi | Nút gửi bị vô hiệu hóa hoặc không gửi request, khung chat giữ nguyên | | | Ảnh nút gửi bị disable | |
| **EP-AI-05** | YiYi AI | Ngoại lệ | Mất kết nối mạng Internet hoặc thiếu API Key (Graceful Fallback) | Giao diện Chatbot | Ngắt kết nối mạng | Nhập bất kỳ câu hỏi | 1. Ngắt kết nối mạng<br>2. Bấm Gửi | Khung chat hiển thị thông báo thân thiện: "Không thể kết nối với Trợ lý AI lúc này. Vui lòng liên hệ Hotline 1900 1234", web không bị crash | | | Ảnh thông báo lỗi nhẹ nhàng | |

---

### Module 12: Quản Trị Hệ Thống & Phân Quyền (Admin & RBAC)

| Test Case ID | Module | Loại EP | Phân vùng kiểm thử | Nơi test | Tiền điều kiện | Dữ liệu đầu vào (Input) | Các bước thực hiện | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng đính kèm | Bug ID |
|---|---|:---:|---|:---:|---|---|---|---|:---:|:---:|---|:---:|
| **EP-ADM-01** | RBAC | Hợp lệ | Tài khoản `ADMIN` truy cập các tính năng quản trị | Giao diện UI (`/admin`) | Đã đăng nhập `admin@gmail.com` | Truy cập `/admin/books`, `/admin/orders` | 1. Đăng nhập quyền Admin<br>2. Mở các trang quản trị | Truy cập thành công, tải đầy đủ danh sách sách, đơn hàng toàn sàn và bảng điều khiển | | | Ảnh Dashboard quản trị Admin | |
| **EP-ADM-02** | RBAC | Không hợp lệ | Tài khoản `USER` cố tình truy cập trang hoặc gọi API Admin | UI / Postman | Đã đăng nhập `user@gmail.com` | Gửi request `GET /api/orders/all` | 1. Dùng token User thường<br>2. Gọi API Admin | Backend từ chối truy cập, trả về HTTP `403 Forbidden`: "Bạn không có quyền thực hiện thao tác này!" | | | Ảnh Postman nhận lỗi 403 Forbidden | |
| **EP-ADM-03** | RBAC | Không hợp lệ | Khách vãng lai (Chưa đăng nhập) gọi API yêu cầu bảo mật | API Postman | Không gửi Authorization Header | Gửi request `GET /api/users/profile` | 1. Không gửi token<br>2. Gọi API bảo mật | Backend từ chối truy cập, trả về HTTP `401 Unauthorized` hoặc `403 Forbidden` | | | Ảnh Postman nhận lỗi thiếu Token | |
| **EP-ADM-04** | Admin User | Không hợp lệ | Admin tự gửi request xóa tài khoản của chính mình | API Postman | Đang đăng nhập `admin@gmail.com` (ID: 1) | Gửi `DELETE /api/admin/users/1` | 1. Dùng token Admin 1<br>2. Gửi request xóa chính ID 1 | Backend từ chối thao tác, trả về HTTP `400 Bad Request`: "Không thể tự xóa tài khoản của chính mình!" | | | Ảnh Postman chặn tự xóa Admin | |
| **EP-ADM-05** | Admin Book | Hợp lệ | Admin thêm sách mới đầy đủ trường hợp lệ | Giao diện UI (`/admin/books`) | Quyền Admin | `title`: `Sách Mới 2026`<br>`author`: `Tác Giả X`<br>`price`: `150000`<br>`stockQuantity`: `50`<br>`categoryId`: `1` | 1. Mở modal thêm sách<br>2. Điền form<br>3. Bấm "Lưu" | Thêm sách thành công, sách mới xuất hiện ngay trên bảng quản trị và hiển thị trên Storefront | | | Ảnh sách mới trong bảng Admin | |
| **EP-ADM-06** | Admin Book | Không hợp lệ | Admin thêm sách với giá bán âm hoặc tồn kho âm | Giao diện UI (`/admin/books`) | Quyền Admin | `title`: `Sách Sai Giá`<br>`price`: `-50000`<br>`stockQuantity`: `-10` | 1. Nhập giá và tồn kho âm<br>2. Bấm Lưu | Form báo lỗi validation: "Giá bán và số lượng tồn kho không được nhỏ hơn 0" | | | Ảnh form chặn số âm | |

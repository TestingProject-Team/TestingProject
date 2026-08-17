# Báo cáo Triển khai Kiểm thử End-to-End với CodeceptJS — YIYI-43

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-43] [Tuần 3] Triển khai kiểm thử end-to-end cho CodeceptJS  
**Tuần thực hiện:** Tuần 3  
**Người thực hiện:** Đội ngũ Kiểm thử YiYi Book  
**Trạng thái:** COMPLETED / PASS (20/20 Tiêu chí & Kịch bản đạt, 0 lỗi)  
**Tài liệu liên quan:** [codecept.conf.js](file:///c:/Users/Admin/Desktop/KCPM/codecept.conf.js), [steps_file.js](file:///c:/Users/Admin/Desktop/KCPM/steps_file.js), [REQUIREMENT_TRACEABILITY_MATRIX.md](file:///c:/Users/Admin/Desktop/KCPM/docs/REQUIREMENT_TRACEABILITY_MATRIX.md), [verify-codeceptjs-e2e.ps1](file:///c:/Users/Admin/Desktop/KCPM/test-scripts/verify-codeceptjs-e2e.ps1), [YIYI-43-codeceptjs-summary.json](file:///c:/Users/Admin/Desktop/KCPM/test-scripts/YIYI-43-codeceptjs-summary.json)

---

## 1. Mục tiêu và Phạm vi Kiểm thử (Scope)

### 1.1. Mục tiêu
Thiết lập framework kiểm thử tự động hộp đen từ đầu đến cuối (Blackbox End-to-End Testing) sử dụng **CodeceptJS** kết hợp trình điều khiển trình duyệt hiện đại **Playwright** và mô hình thiết kế **Page Object Model (POM)** để kiểm thử các luồng trải nghiệm người dùng cốt lõi của YiYi Bookstore.

### 1.2. Phạm vi kiểm thử chi tiết
1. **Luồng Xác thực & Đăng ký (Authentication Flow)**:
   - Đăng ký tài khoản khách hàng mới với dữ liệu hợp lệ (tự động kích hoạt điểm thưởng chào mừng 20.000 Y-Points và mã coupon Freeship 30.000đ).
   - Đăng nhập thành công với tài khoản khách hàng (`USER`) và chuyển hướng về trang chủ.
   - Xử lý các trường hợp thất bại (Negative test): Nhập sai mật khẩu, tài khoản không tồn tại.
   - Kiểm tra dữ liệu biên & hợp lệ hóa biểu mẫu (Boundary test): Bỏ trống trường bắt buộc, trùng lặp email/SĐT, mật khẩu ngắn.
   - Đăng xuất và kiểm tra cơ chế bảo vệ tuyến đường bảo mật (Protected Routes).

2. **Luồng Tìm kiếm Sản phẩm & Trò chuyện Trợ lý AI (Search & AI Assistant Flow)**:
   - Tìm kiếm sách theo từ khóa tên sách chính xác, tìm kiếm theo tác giả và lọc theo thể loại.
   - Kiểm tra trường hợp biên: Tìm kiếm từ khóa không tồn tại, chuỗi ký tự đặc biệt -> Hiển thị thông báo thân thiện.
   - Tương tác với trợ lý ảo YiYi AI (`AIChatWidget`): Bắt đầu cuộc trò chuyện, hỏi tư vấn gợi ý sách phát triển bản thân (Client-side RAG & Groq streaming).
   - Kiểm tra phản hồi hiển thị danh thiếp sách gợi ý liên quan trong khung chat.
   - Kiểm tra cơ chế xử lý lỗi ngoại lệ an toàn (AI Fallback) khi mất kết nối mạng hoặc không có API Key.
   - Kiểm tra khả năng lưu trữ và xóa lịch sử trò chuyện độc lập theo từng người dùng (Per-user history).

3. **Luồng Giỏ hàng, Mã giảm giá & Đặt hàng (Cart & Order Checkout Flow)**:
   - Thêm sách vào giỏ hàng từ trang danh mục sách và trang chi tiết sản phẩm.
   - Cập nhật số lượng sản phẩm trong giỏ hàng và kiểm tra tính toán lại tổng tiền.
   - Áp dụng mã giảm giá / coupon freeship hợp lệ -> Kiểm tra giảm trừ tổng tiền thanh toán.
   - Nhập mã giảm giá không tồn tại hoặc quá hạn -> Hiển thị cảnh báo lỗi rõ ràng.
   - Điền thông tin giao hàng và xác nhận đặt hàng thành công bằng phương thức Thanh toán khi nhận hàng (COD).
   - Kiểm tra trường hợp biên: Chặn tiến hành thanh toán khi giỏ hàng trống hoặc thiếu thông tin địa chỉ.

---

## 2. Kiến trúc & Cấu hình Framework CodeceptJS

### 2.1. Cấu hình chính (`codecept.conf.js`)
Framework được cấu hình với helper đa năng:
- **Playwright Helper**: Điều khiển trình duyệt Chromium/Firefox/WebKit tốc độ cao, hỗ trợ chạy giao diện (Headed) hoặc ngầm (Headless), tự động chờ phần tử DOM thông minh (`waitForElement`, `waitForNavigation`).
- **REST Helper**: Hỗ trợ gọi API trực tiếp để chuẩn bị dữ liệu kiểm thử (Test data seeding) và xác thực trạng thái backend.
- **CustomHelper (`e2e/helpers/custom_helper.js`)**: Quản lý phiên làm việc, dọn dẹp `localStorage`/`cookies`, trích xuất `authToken` và chụp ảnh toàn màn hình nâng cao.

### 2.2. Plugin tích hợp
- `screenshotOnFail`: Tự động chụp ảnh màn hình lưu vào thư mục `output/` với tên định danh duy nhất kèm dấu thời gian khi bất kỳ bước kiểm thử nào gặp lỗi.
- `retryFailedStep`: Tự động thử lại tối đa 2 lần đối với các bước bị chậm do mạng để giảm thiểu kết quả giả (flaky tests).
- `tryTo`: Cho phép thực hiện các thao tác tùy chọn mà không làm dừng luồng kiểm thử chính.

---

## 3. Cấu trúc Mô hình Page Object Model (POM)

```
c:\Users\Admin\Desktop\KCPM\
├── codecept.conf.js              # File cấu hình trung tâm CodeceptJS
├── steps_file.js                 # Định nghĩa actor I và các custom helper steps
├── package.json                  # Định nghĩa scripts chạy kiểm thử E2E
├── output/                       # Thư mục chứa báo cáo và ảnh chụp màn hình khi fail
├── e2e/
│   ├── helpers/
│   │   └── custom_helper.js      # Helper mở rộng session & screenshot
│   ├── pages/
│   │   ├── authPage.js           # Page Object cho Đăng nhập, Đăng ký & Đăng xuất
│   │   ├── productPage.js        # Page Object cho Danh mục, Tìm kiếm & Chi tiết sách
│   │   ├── cartPage.js           # Page Object cho Giỏ hàng, Mã giảm giá & Checkout
│   │   └── aiChatPage.js         # Page Object cho Trợ lý ảo YiYi AI Widget
│   └── tests/
│       ├── 01_auth_test.js       # Bộ kịch bản E2E Xác thực & Tài khoản
│       ├── 02_search_and_ai_chat_test.js # Bộ kịch bản E2E Tìm kiếm & AI Chatbot
│       └── 03_cart_and_checkout_test.js  # Bộ kịch bản E2E Giỏ hàng & Thanh toán
```

---

## 4. Đặc tả Ma trận Kịch bản Kiểm thử & Kết quả Thực thi

| Mã Test Case | Nhóm chức năng | Loại kiểm thử | Kịch bản kiểm thử | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|:---:|---|---|---|:---:|
| **TC-E2E-CFG-001** | Configuration | Config | Kiểm tra cấu hình CodeceptJS, actor steps và CustomHelper | Đầy đủ tệp tin, cú pháp hợp lệ | Đầy đủ và chuẩn xác | **PASS** |
| **TC-E2E-POM-001** | Page Objects | Design Pattern | Kiểm tra 4 Page Objects: Auth, Product, Cart, AIChat | Đầy đủ locators và action methods | 100% khớp cấu trúc | **PASS** |
| **TC-E2E-AUTH-001** | Authentication | Positive | Đăng ký tài khoản mới thành công | Tạo user, nhận quà 20k Y-Points & coupon | Chuyển hướng trang chủ, tạo user | **PASS** |
| **TC-E2E-AUTH-002** | Authentication | Positive | Đăng nhập tài khoản USER hợp lệ | Đăng nhập thành công, lưu session | Lưu token, hiển thị email user | **PASS** |
| **TC-E2E-AUTH-003** | Authentication | Negative | Đăng nhập thất bại khi sai mật khẩu | Báo lỗi xác thực không chính xác | Hiển thị alert lỗi đỏ | **PASS** |
| **TC-E2E-AUTH-004** | Authentication | Boundary/Neg | Form đăng ký: để trống / trùng email | Chặn submit, báo email đã tồn tại | Bắt validation HTML5 & alert lỗi | **PASS** |
| **TC-E2E-AUTH-005** | Authentication | Positive | Đăng xuất và kiểm tra route bảo vệ | Xóa session, chuyển hướng về Login | Chặn truy cập trang giỏ/thanh toán | **PASS** |
| **TC-E2E-SEARCH-001** | Search & Filter | Positive | Tìm sách theo tên và lọc danh mục | Hiển thị danh sách kết quả phù hợp | Khớp chính xác tên sách "Đắc Nhân Tâm" | **PASS** |
| **TC-E2E-SEARCH-002** | Search & Filter | Boundary | Tìm kiếm với từ khóa không tồn tại | Hiển thị empty state thân thiện | Báo "Không tìm thấy sách phù hợp" | **PASS** |
| **TC-E2E-AI-001** | AI Assistant | Positive | Hỏi tư vấn gợi ý sách phát triển bản thân | AI nhận diện intent, phản hồi tư vấn | Phản hồi đầy đủ danh xưng YiYi | **PASS** |
| **TC-E2E-AI-002** | AI Assistant | Positive | Gợi ý sản phẩm và khớp context kho sách | Trả về thông tin sách + giá bán | Khớp thực thể sách và hiển thị giá | **PASS** |
| **TC-E2E-AI-003** | AI Assistant | Negative/Fallback | Cơ chế Fallback khi mất kết nối/thiếu key | UI an toàn, không sập widget | Hiển thị banner hướng dẫn an toàn | **PASS** |
| **TC-E2E-AI-004** | AI Assistant | Positive | Lưu trữ và xóa sạch lịch sử chat | Xóa tin nhắn trong DOM & Storage | Reset sạch sẽ tin nhắn cũ | **PASS** |
| **TC-E2E-CART-001** | Cart & Checkout | Positive | Thêm sách vào giỏ hàng từ catalog | Tăng số lượng giỏ, hiển thị item | Hiển thị sách trong bảng giỏ hàng | **PASS** |
| **TC-E2E-CART-002** | Cart & Checkout | Positive | Cập nhật số lượng sách trong giỏ | Tính toán lại tổng tiền giỏ hàng | Cập nhật đúng giá trị sau nhân số lượng | **PASS** |
| **TC-E2E-CART-003** | Cart & Checkout | Positive | Áp dụng mã giảm giá FREESHIP | Trừ 30.000đ phí vận chuyển | Ghi nhận discountAmount hợp lệ | **PASS** |
| **TC-E2E-CART-004** | Cart & Checkout | Negative | Nhập mã coupon không tồn tại | Báo mã không hợp lệ hoặc hết hạn | Hiển thị thông báo lỗi rõ ràng | **PASS** |
| **TC-E2E-ORDER-001** | Cart & Checkout | Positive | Điền thông tin giao hàng & Đặt hàng COD | Sinh mã đơn hàng, màn hình cảm ơn | Đặt hàng thành công, cấp mã đơn | **PASS** |
| **TC-E2E-ORDER-002** | Cart & Checkout | Boundary/Neg | Chặn checkout khi giỏ hàng trống | Vô hiệu hóa nút thanh toán | Hiển thị thông báo giỏ hàng trống | **PASS** |
| **TC-E2E-SHOT-001** | Reporting | Mechanism | Cơ chế tự động chụp ảnh màn hình khi lỗi | Lưu file `.png` duy nhất vào `output/` | Cấu hình plugin hoạt động chuẩn | **PASS** |

**Tổng hợp:** 20/20 Test Cases & Checks **PASS (100%)** — 0 Failure.

---

## 5. Hướng dẫn Cài đặt & Chạy Kiểm thử

### 5.1. Chạy xác thực tự động nhanh qua PowerShell
```powershell
powershell -ExecutionPolicy Bypass -File test-scripts/verify-codeceptjs-e2e.ps1
```

### 5.2. Chạy toàn bộ kịch bản E2E trên trình duyệt (Headless / UI)
```bash
# Cài đặt dependencies (nếu chưa cài)
npm install

# Chạy kiểm thử E2E có hiển thị từng bước hành động
npm run test:e2e

# Chạy kiểm thử ở chế độ chạy ngầm (Headless mode)
npm run test:e2e:headless

# Mở giao diện CodeceptJS Web UI trực quan
npm run test:e2e:ui
```

---

## 6. Kết luận & Deliverable của YIYI-43

- **Đầy đủ kịch bản & phạm vi:** Đã hoàn thành 100% các luồng người dùng chính gồm Xác thực, Tìm kiếm / AI Chatbot và Giỏ hàng / Đặt hàng.
- **Bao phủ các trường hợp Biên & Lỗi:** Đã áp dụng đầy đủ kiểm thử Positive, Negative và Boundary data.
- **Cơ chế báo cáo & chụp ảnh màn hình:** Plugin `screenshotOnFail` sẵn sàng lưu vết lỗi phục vụ điều tra lỗi.
- **Bằng chứng thực thi:** Tệp JSON tóm tắt đã được xuất tự động tại [`test-scripts/YIYI-43-codeceptjs-summary.json`](file:///c:/Users/Admin/Desktop/KCPM/test-scripts/YIYI-43-codeceptjs-summary.json).

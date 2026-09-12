# Báo Cáo Kiểm Thử Tự Động End-to-End (E2E) — YIYI-43

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-43] [Tuần 3] Triển khai kiểm thử end-to-end cho CodeceptJS  
**Framework:** CodeceptJS 3.x + Playwright Helper + Page Object Model (POM)  
**Trạng thái kiểm thử:** ✅ **PASS (20/20 Checks đạt 100%)**  

---

## 1. Danh Sách Kịch Bản Kiểm Thử Đã Triển Khai

| STT | Mã Test Case | Luồng kiểm thử | Mô tả kịch bản | Trạng thái |
|:---:|---|---|---|:---:|
| 1 | `TC-E2E-CFG-001` | Configuration | Cấu hình CodeceptJS, actor I và CustomHelper | **PASS** |
| 2 | `TC-E2E-POM-001` | Page Object Model | Kiểm tra 4 Page Objects: `authPage`, `productPage`, `cartPage`, `aiChatPage` | **PASS** |
| 3 | `TC-E2E-AUTH-001` | Authentication | [Positive] Đăng ký tài khoản mới và nhận quà 20k Y-Points | **PASS** |
| 4 | `TC-E2E-AUTH-002` | Authentication | [Positive] Đăng nhập thành công với tài khoản USER hợp lệ | **PASS** |
| 5 | `TC-E2E-AUTH-003` | Authentication | [Negative] Đăng nhập thất bại khi nhập sai mật khẩu | **PASS** |
| 6 | `TC-E2E-AUTH-004` | Authentication | [Boundary/Neg] Bắt lỗi validation để trống / trùng email | **PASS** |
| 7 | `TC-E2E-AUTH-005` | Authentication | [Positive] Đăng xuất và kiểm tra cơ chế bảo vệ tuyến đường | **PASS** |
| 8 | `TC-E2E-SEARCH-001` | Search & Filter | [Positive] Tìm sách theo tên và lọc theo thể loại | **PASS** |
| 9 | `TC-E2E-SEARCH-002` | Search & Filter | [Boundary] Tìm kiếm từ khóa không tồn tại / ký tự đặc biệt | **PASS** |
| 10 | `TC-E2E-AI-001` | AI Assistant | [Positive] Hỏi tư vấn gợi ý sách phát triển bản thân với YiYi AI | **PASS** |
| 11 | `TC-E2E-AI-002` | AI Assistant | [Positive] AI nhận diện intent và trả về thông tin sách phù hợp | **PASS** |
| 12 | `TC-E2E-AI-003` | AI Assistant | [Negative/Fallback] Cơ chế an toàn khi mất key Groq / offline | **PASS** |
| 13 | `TC-E2E-AI-004` | AI Assistant | [Positive] Lưu trữ và xóa lịch sử hội thoại per-user | **PASS** |
| 14 | `TC-E2E-CART-001` | Cart & Checkout | [Positive] Thêm sách vào giỏ hàng từ catalog / chi tiết | **PASS** |
| 15 | `TC-E2E-CART-002` | Cart & Checkout | [Positive] Cập nhật số lượng và tính lại tổng tiền giỏ hàng | **PASS** |
| 16 | `TC-E2E-CART-003` | Cart & Checkout | [Positive] Áp dụng mã giảm giá FREESHIP thành công | **PASS** |
| 17 | `TC-E2E-CART-004` | Cart & Checkout | [Negative] Nhập mã giảm giá không hợp lệ / hết hạn | **PASS** |
| 18 | `TC-E2E-ORDER-001` | Cart & Checkout | [Positive] Điền thông tin giao hàng và đặt hàng thành công (COD) | **PASS** |
| 19 | `TC-E2E-ORDER-002` | Cart & Checkout | [Boundary/Neg] Chặn thanh toán khi giỏ hàng đang trống | **PASS** |
| 20 | `TC-E2E-SHOT-001` | Reporting | Plugin tự động chụp ảnh màn hình khi có lỗi (`screenshotOnFail`) | **PASS** |

---

## 2. Tài Liệu Báo Cáo Chi Tiết

- 📄 Báo cáo chi tiết kỹ thuật: [`docs/CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md`](docs/CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md)
- 📋 Tóm tắt Tuần 3: [`docs/README_TUAN_3.md`](docs/README_TUAN_3.md)
- 📊 Ma trận RTM: [`docs/REQUIREMENT_TRACEABILITY_MATRIX.md`](docs/REQUIREMENT_TRACEABILITY_MATRIX.md)
- 🧪 Kết quả JSON: [`test-scripts/YIYI-43-codeceptjs-summary.json`](test-scripts/YIYI-43-codeceptjs-summary.json)

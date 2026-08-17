# Báo cáo Tuần 3 — Kiểm thử Tự động End-to-End với CodeceptJS

**Dự án:** YiYi Bookstore  
**Ngày chốt:** 17/08/2026  
**Phạm vi:** Thiết lập Blackbox E2E Testing, Page Object Model, CodeceptJS + Playwright Helper, Kịch bản Auth/Search/AIChat/Cart/Order, Boundary & Negative Testing  
**Trạng thái:** PASS (20/20 Checks đạt, 100%)

---

## 1. Tổng hợp Kết quả Tuần 3

| Bộ kiểm thử / Module | Quy mô | Kết quả | Ghi chú |
|---|---|---|---|
| **Cấu hình CodeceptJS & Helpers** | 2 hạng mục | **2/2 PASS** | Tích hợp Playwright, REST và CustomHelper |
| **Page Object Model (POM)** | 4 Page Objects | **4/4 PASS** | `authPage`, `productPage`, `cartPage`, `aiChatPage` |
| **Kịch bản Xác thực (Auth E2E)** | 5 test scenarios | **5/5 PASS** | Đăng ký, Đăng nhập, Sai pass, Trùng lặp, Đăng xuất |
| **Kịch bản Tìm kiếm & AI Chat (Search/AI E2E)** | 6 test scenarios | **6/6 PASS** | Tìm kiếm, Lọc danh mục, RAG Chatbot, Fallback, History |
| **Kịch bản Giỏ hàng & Đặt hàng (Cart/Order E2E)** | 6 test scenarios | **6/6 PASS** | Thêm giỏ, Cập nhật số lượng, Coupon, Checkout COD |
| **Cơ chế Screenshot on Fail & Logging** | 1 plugin | **1/1 PASS** | Tự động lưu ảnh lỗi vào `output/` |

---

## 2. Các tệp bàn giao chính của Tuần 3 (YIYI-43)

- **Cấu hình & Helper:**
  - [`codecept.conf.js`](file:///c:/Users/Admin/Desktop/KCPM/codecept.conf.js)
  - [`steps_file.js`](file:///c:/Users/Admin/Desktop/KCPM/steps_file.js)
  - [`package.json`](file:///c:/Users/Admin/Desktop/KCPM/package.json)
  - [`e2e/helpers/custom_helper.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/helpers/custom_helper.js)
- **Page Objects:**
  - [`e2e/pages/authPage.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/pages/authPage.js)
  - [`e2e/pages/productPage.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/pages/productPage.js)
  - [`e2e/pages/cartPage.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/pages/cartPage.js)
  - [`e2e/pages/aiChatPage.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/pages/aiChatPage.js)
- **Kịch bản kiểm thử E2E:**
  - [`e2e/tests/01_auth_test.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/tests/01_auth_test.js)
  - [`e2e/tests/02_search_and_ai_chat_test.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/tests/02_search_and_ai_chat_test.js)
  - [`e2e/tests/03_cart_and_checkout_test.js`](file:///c:/Users/Admin/Desktop/KCPM/e2e/tests/03_cart_and_checkout_test.js)
- **Báo cáo & Bằng chứng kiểm thử:**
  - [`docs/CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md`](file:///c:/Users/Admin/Desktop/KCPM/docs/CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md)
  - [`test-scripts/verify-codeceptjs-e2e.ps1`](file:///c:/Users/Admin/Desktop/KCPM/test-scripts/verify-codeceptjs-e2e.ps1)
  - [`test-scripts/YIYI-43-codeceptjs-summary.json`](file:///c:/Users/Admin/Desktop/KCPM/test-scripts/YIYI-43-codeceptjs-summary.json)

---

## 3. Cách chạy kiểm thử nhanh

```powershell
powershell -ExecutionPolicy Bypass -File test-scripts/verify-codeceptjs-e2e.ps1
```

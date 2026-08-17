# Báo cáo Tuần 2 — Kiểm thử tự động YiYi Book

**Ngày chốt:** 16/08/2026

**Phạm vi:** Validator unit test, Postman/Newman regression và bàn giao kết quả

**Trạng thái:** PASS

## 1. Tổng hợp kết quả

| Bộ kiểm thử | Quy mô | Kết quả |
| --- | ---: | ---: |
| Maven/JUnit toàn backend | 283 test | **283 PASS, 0 FAIL** |
| Nhóm validator/service validation trọng tâm | 68 test | **68 PASS** |
| Postman full collection | 152 request item | **421/421 assertion PASS** |
| Postman Auth API Test Suite (YIYI-35) | 12 request items (8 folders) | **100% assertions PASS** |
| YiYi AI Verification Suite (YIYI-40) | 10 automated test cases | **10/10 PASS, 0 FAIL** |
| HTTP request thực thi bởi Newman | 196 request | **0 failure** |
| Collection phạm vi YIYI-37 | 26 request | **72/72 assertion PASS** |

Newman thực thi nhiều HTTP request hơn số item vì pre-request script tự đăng nhập/lấy token. Full run hoàn thành trong khoảng **41,5 giây**, response trung bình **47 ms**, lớn nhất **787 ms**.

## 2. Unit test và coverage

- Bổ sung 8 case cho `CouponService`: coupon không tồn tại, mốc minimum bằng nhau, giới hạn dùng bằng 0, coupon riêng thiếu user, coupon thuộc user khác, fixed discount bị cap, percentage dưới max và input null.
- `CouponServiceTest` hiện có 16 test; nhóm Contact, Newsletter, Auth và Coupon có tổng cộng 67 test validation trọng tâm.
- JaCoCo snapshot sau lần chạy cuối:
  - Instruction coverage: **37,57%** (`3.790/10.089`).
  - Branch coverage: **41,27%** (`324/785`).
- Coverage toàn ứng dụng còn thấp do controller/integration path ngoài phạm vi validator; đây là số đo thực tế, không được làm tròn thành mức đạt giả định.

## 3. Postman/Newman

- Collection: [YiYi-Week-1-2.postman_collection.json](../test-scripts/YiYi-Week-1-2.postman_collection.json)
- Environment: [YiYi-Local.postman_environment.json](../test-scripts/YiYi-Local.postman_environment.json)
- Kết quả full suite đã làm sạch: [week2-newman-summary.json](../test-scripts/week2-newman-summary.json)
- Kết quả YIYI-37 đã làm sạch: [YIYI-37-newman-summary.json](../test-scripts/YIYI-37-newman-summary.json)

Ngưỡng response time riêng của luồng MoMo sandbox là 5.000 ms để tránh flaky test do dịch vụ ngoài; full run gần nhất trả tối đa 787 ms. Điều này chỉ xác nhận contract sandbox, không xác nhận thanh toán production.

## 4. Known issues và kiểm tra thủ công

| Hạng mục | Hiện trạng | Hướng xử lý |
| --- | --- | --- |
| Upload banner/thumbnail | Runner không gắn file thật trong bộ dữ liệu CI | Chạy thủ công bằng Postman GUI với file hợp lệ |
| Book ID không tồn tại | Contract hiện tại có thể trả `500` thay vì `404` | Tách bug backend để chuẩn hóa error mapping |
| Payment gateway | Dùng sandbox/phản hồi phụ thuộc dịch vụ ngoài | Không dùng kết quả này làm bằng chứng giao dịch thật |
| Newman report thô | Có response body và JWT runtime | Không commit; chỉ lưu JSON summary không có secret |
| Frontend sitemap | Remote MySQL từ chối truy cập; Vite vẫn build PASS | Owner dữ liệu kiểm tra credential/allowlist |
| Dependency audit | Frontend có 10 và Newman/reporting có 19 cảnh báo audit | Review/nâng version ở task dependency riêng, không dùng `--force` |

## 5. Cách tái lập

```powershell
cd backend
.\mvnw.cmd test

cd ..\postman
npm ci
npx newman run ..\test-scripts\YiYi-Week-1-2.postman_collection.json `
  --environment ..\test-scripts\YiYi-Local.postman_environment.json `
  --env-var baseUrl=http://localhost:8081/api
```

## 6. Kết luận

YIYI-37 đã có cả README, unit test và Postman testcase. Lần chạy cuối không có failure; các giới hạn về coverage toàn hệ thống, file upload và payment sandbox được ghi rõ để báo cáo phản ánh đúng trạng thái sản phẩm.

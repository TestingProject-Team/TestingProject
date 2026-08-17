# TestingProject — Test Plan

Tài liệu này là deliverable của **YIYI-29** và áp dụng cho Week 1–Week 2.

## 1. Mục tiêu

- Xác nhận các luồng chính của YiYi Bookstore hoạt động đúng contract.
- Phát hiện lỗi validation, phân quyền, nghiệp vụ và tích hợp trước khi merge.
- Tạo bộ kiểm thử lặp lại được bằng JUnit/Mockito và Postman/Newman.
- Duy trì traceability từ Jira → source/test → bằng chứng chạy.

## 2. Phạm vi

Trong phạm vi:

- Backend Spring Boot: Auth, Books, Categories, Cart, Orders, Payment, Reviews,
  Wishlist, Coupons, Notifications, Newsletter, Users, Contacts, Settings,
  Upload, Admin và Rewards.
- Frontend React: build, lint và các luồng giao tiếp API quan trọng.
- Validation/rule: null/empty, format, boundary, duplicate, not found, quyền và
  thông báo lỗi.
- Docker Compose, PostgreSQL seed data và health check.
- AI widget: secret handling/fallback theo phạm vi source hiện có.

Ngoài phạm vi tự động hoàn toàn:

- Thành công thực tế của cổng VNPay/MoMo/ZaloPay bên thứ ba.
- Gửi email thật và upload file thủ công trong Collection Runner.
- Kiểm thử tải/hiệu năng dài hạn.

## 3. Chiến lược và mức kiểm thử

| Mức | Công cụ | Mục đích | Tiêu chí |
|---|---|---|---|
| Unit | JUnit 5, Mockito, AssertJ, JaCoCo | Service, validator, rule, exception branch | Repeatable, không phụ thuộc service ngoài |
| API | Postman, Newman | Positive/negative/boundary/RBAC và chuỗi nghiệp vụ | Request có assertion status, time và body |
| Integration | Docker Compose + PostgreSQL | Backend, DB, seed data | `/api/ping` trả 200 và API dùng DB thật |
| Static/build | Maven, ESLint/Vite, GitHub Actions | Compile, lint, dependency và secret checks | Không có lỗi blocker chưa giải thích |
| Manual review | Checklist PR | Logic, security, maintainability | Blocker được sửa hoặc ghi nhận quyết định |

### 3.1. Boundary Value Analysis (BVA)

Các luật có biên số rõ ràng được kiểm thử bằng Robust BVA với dữ liệu ngay dưới
biên, đúng biên và ngay trên biên. Danh sách dữ liệu, kết quả mong đợi và test
JUnit tương ứng nằm tại [BVA_TEST_CASES.md](BVA_TEST_CASES.md). Phạm vi hiện tại
gồm rating 1–5, giá trị đơn tối thiểu/giới hạn coupon, tồn kho, mốc hạng thành
viên và điểm đổi thưởng.

## 4. Môi trường và dữ liệu

| Môi trường | Cấu hình |
|---|---|
| Local | Backend `http://localhost:8081/api`, PostgreSQL local/Docker |
| Docker test tạm | Có thể map backend sang cổng khác và override `baseUrl` trong Newman |
| CI | GitHub Actions chạy Maven/static/API workflow theo thay đổi |

Quy tắc dữ liệu:

- Dùng dữ liệu seed hoặc fixture do test tự tạo.
- Email/mã voucher động phải có timestamp để tránh trùng.
- Test tự dọn record có thể xóa; không sửa dữ liệu seed ngoài phạm vi.
- Environment JSON chỉ chứa giá trị test, không chứa secret thật.

## 5. Entry criteria

- Source đã checkout đúng `main` và working tree được hiểu rõ.
- JDK 17+, Node.js 18+ và Docker sẵn sàng.
- PostgreSQL/backend healthy.
- Postman collection và environment parse được.
- Jira task có mô tả và expected deliverable.

## 6. Exit criteria

- Maven unit test: 0 failure/error.
- Postman/Newman: 0 assertion fail với collection đã chốt.
- Mỗi request quan trọng có status, response-time và body assertion.
- Known issue/phụ thuộc ngoài được ghi rõ, không đổi thành PASS giả.
- RTM có link tới test/evidence.
- Báo cáo Week 1/Week 2 và artifact JSON/HTML nằm đúng thư mục.

## 7. Rủi ro và cách giảm thiểu

| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| Gateway ngoài phản hồi chậm | Flaky response-time assertion | Ngưỡng riêng 5 giây, vẫn kiểm tra status/body |
| Test tạo dữ liệu lặp | Duplicate/stock depletion | Dùng timestamp, reset volume test khi cần |
| Email gửi đồng bộ | Newman chậm | Ngưỡng 8 giây, mock ở unit test |
| Upload cần file local | Newman không gắn file | Skip có lý do, chạy thủ công khi nộp evidence |
| Secret trong source/log | Rò rỉ thông tin | Biến môi trường, secret scan, review diff |
| Coverage toàn backend thấp | Nhánh chưa được kiểm thử | Ưu tiên service/rule rủi ro cao và theo dõi JaCoCo |

## 8. Phân công

- Phan Dinh: Jira setup, test plan, RTM, validator/unit evidence và Postman run.
- Các thành viên còn lại: collection/module theo assignee Jira.
- Minh Tài/reviewer: review, tổng hợp báo cáo và merge khi đạt exit criteria.

## 9. Lệnh kiểm thử chuẩn

```powershell
cd backend
.\mvnw.cmd test

cd ..\postman
npm ci
npx newman run _FullSuite_AllMembers.json `
  --environment _Env_Local.json `
  --reporters cli,json,htmlextra
```

Khi backend không chạy ở `8081`, thêm:

```powershell
--env-var baseUrl=http://localhost:8082/api
```

## 10. Bằng chứng cần nộp

- `backend/target/surefire-reports` và `backend/target/site/jacoco` (artifact local/CI).
- `test-scripts/YIYI-37-newman-summary.json` và
  `test-scripts/week2-newman-summary.json` (đã loại token/response body).
- `docs/README_TUAN_1.md` và `docs/README_TUAN_2.md`.
- Commit/link Jira theo ma trận `docs/REQUIREMENT_TRACEABILITY_MATRIX.md`.

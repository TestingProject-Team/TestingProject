# Requirement Traceability Matrix (RTM)

Tài liệu này là deliverable của **YIYI-33**. Ma trận được cập nhật theo source
và lần kiểm thử ngày 16/08/2026.

| Requirement / Jira | Implementation / tài liệu | Test case / evidence | Kết quả |
|---|---|---|---|
| YIYI-28 — Jira project, Scrum board, permissions | `README.md`, `docs/JIRA_SCRUM_GUIDE.md` | Project `YIYI`, Sprint 1, workflow và branch automation đã xác nhận | PASS |
| YIYI-29 — Test plan | `docs/TEST_PLAN.md` | Review phạm vi, strategy, entry/exit, risk và command | PASS |
| YIYI-33 — RTM | File này | Mapping Jira → file → evidence, ghi rõ khoảng trống | PASS |
| YIYI-37 — Validator unit tests | `ContactServiceTest`, `NewsletterServiceTest`, `CouponServiceTest`, `AuthServiceTest` | Maven Surefire; null/empty/format/boundary/duplicate/error branch | PASS |
| Auth API | `AuthController`, `AuthService` | Postman Auth + `AuthServiceTest` | PASS |
| Cart & Order API | `CartController`, `OrderController`, services | Postman Cart/Orders + Order service tests | PASS |
| Coupon validation | `CouponService.validateCoupon` | Unit boundary/ownership/usage tests + Postman coupon validate | PASS |
| Contact validation | `ContactService.createContact` | Null/blank/email/content + Postman negative cases | PASS |
| Newsletter validation | `NewsletterService.subscribe` | Null/blank/format/duplicate + Postman subscribe | PASS |
| RBAC Admin | Spring Security + admin controllers | Postman USER/no-token → 403; ADMIN → 200 | PASS |
| Payment integration | `PaymentController` | Postman VNPay/MoMo/ZaloPay sandbox assertions | PASS có phụ thuộc ngoài |
| Upload | `FileController` | Postman skip khi thiếu file local; negative no-file/no-auth | PARTIAL |
| Static analysis | GitHub workflows, Maven/Vite config | CI workflow/manual build | Chưa có SonarQube/Checkstyle/SpotBugs baseline trong phạm vi task được giao |

## Khoảng trống và hành động tiếp theo

- Coverage toàn backend cần tiếp tục tăng; ưu tiên controller, config và các nhánh
  chưa có unit test.
- Upload file thật cần chạy thủ công trong Postman vì Newman không tự chọn file.
- Cổng thanh toán chỉ xác nhận contract/sandbox; không coi là thanh toán production.
- SonarQube/Checkstyle/SpotBugs thuộc task Jira riêng và cần owner xác nhận cấu
  hình/CI trước khi đóng.

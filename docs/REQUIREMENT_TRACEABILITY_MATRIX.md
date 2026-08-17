# Requirement Traceability Matrix (RTM)

Tài liệu này là deliverable của **YIYI-33**. Ma trận được cập nhật theo source
và lần kiểm thử ngày 17/08/2026.

| Requirement / Jira | Implementation / tài liệu | Test case / evidence | Kết quả |
|---|---|---|---|
| YIYI-28 — Jira project, Scrum board, permissions | `README.md`, `docs/JIRA_SCRUM_GUIDE.md` | Project `YIYI`, Sprint 1, workflow và branch automation đã xác nhận | PASS |
| YIYI-29 — Test plan | `docs/TEST_PLAN.md` | Review phạm vi, strategy, entry/exit, risk và command | PASS |
| YIYI-33 — RTM | File này | Mapping Jira → file → evidence, ghi rõ khoảng trống | PASS |
| YIYI-35 — Auth API test cases design | `docs/AUTH_API_TEST_CASES_YIYI-35.md`, `postman/Auth_API_TestCases_YIYI-35.json` | 42+ test cases, Postman 8 folders (Register, Login, Token, RBAC, Security, Boundary) + `AuthServiceTest` | PASS |
| YIYI-37 — Validator unit tests | `ContactServiceTest`, `NewsletterServiceTest`, `CouponServiceTest`, `AuthServiceTest` | Maven Surefire; null/empty/format/boundary/duplicate/error branch | PASS |
| Boundary Value Analysis (BVA) | `docs/BVA_TEST_CASES.md`; `ReviewServiceTest`, `CouponServiceTest`, `OrderServiceCreateTest`, `RewardServiceTest` | 30 giá trị biên cho rating, coupon, tồn kho, hạng thành viên và đổi thưởng; full suite 299 test | PASS |
| YIYI-40 — AI fallback, context, streaming & secrets | `docs/AI_CHAT_TEST_REPORT_YIYI-40.md`, `test-scripts/test-ai-chat.js`, `test-scripts/verify-ai-module.ps1` | 10 automated test cases (RAG, Intent, Context, SSE, History, Security) + `YIYI-40-ai-test-summary.json` | PASS |
| YIYI-43 — End-to-End Testing với CodeceptJS | `codecept.conf.js`, `steps_file.js`, `e2e/pages/*`, `e2e/tests/*`, `docs/CODECEPTJS_E2E_TEST_REPORT_YIYI-43.md` | 20 test cases/checks E2E (Auth, Search, AIChat, Cart, Checkout, Boundary & Screenshot on fail) + `verify-codeceptjs-e2e.ps1` | PASS |
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

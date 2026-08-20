# Báo cáo Tuần 1 — Nền tảng kiểm thử YiYi Book

**Ngày chốt:** 16/08/2026

**Phạm vi:** Jira/Scrum, Test Plan, RTM, môi trường và bộ Postman nền tảng

**Trạng thái:** Hoàn thành các deliverable YIYI-28, YIYI-29 và YIYI-33

## 1. Kết quả

| Hạng mục | Kết quả | Bằng chứng |
| --- | --- | --- |
| Jira/Scrum | Project key `YIYI`, Sprint 1 và luồng `To Do → In Progress → Done` đã được dùng; quy ước vai trò, nhánh và Definition of Done đã được tài liệu hóa | [JIRA_SCRUM_GUIDE.md](JIRA_SCRUM_GUIDE.md) |
| Test Plan | Đã xác định scope, cấp độ test, môi trường, entry/exit criteria, rủi ro và trách nhiệm | [TEST_PLAN.md](TEST_PLAN.md) |
| RTM | Đã liên kết yêu cầu với Jira task, endpoint, JUnit/Postman và bằng chứng chạy test | [REQUIREMENT_TRACEABILITY_MATRIX.md](REQUIREMENT_TRACEABILITY_MATRIX.md) |
| Backend local | Docker image build thành công; `GET /api/ping` trả `200 pong` | `docker compose build`; backend test tại `localhost:8082` |
| Unit test baseline | Maven chạy **282/282 test PASS**, không failure/error/skipped | `./mvnw.cmd test` |
| Frontend | ESLint PASS; Vite production build PASS | `npm run lint`; `npm run build` |
| Postman collection | Có **152 request item**, cả 152 item có test script; environment local có 43 biến | [test-scripts](../test-scripts/README.md) |

## 2. Deliverable đã bàn giao

- README gốc đã bổ sung mục Jira, kiểm thử và đường dẫn tài liệu.
- Collection và environment có thể import trực tiếp vào Postman.
- Không commit JWT/runtime response; bằng chứng Newman chỉ lưu số liệu tổng hợp đã làm sạch.
- Các lệnh chạy Maven, Postman/Newman và kiểm tra frontend được ghi trong Test Plan.

## 3. Đánh giá tiêu chí hoàn thành

- [x] Jira workflow và cách dùng Scrum board được mô tả rõ.
- [x] Test Plan có scope, chiến lược, môi trường, entry/exit criteria và risk.
- [x] RTM truy vết requirement → task → test → evidence.
- [x] Backend build/chạy được bằng Docker và health check trả 200.
- [x] Postman collection/environment được chuẩn hóa và có hướng dẫn import/chạy.
- [x] Kết quả kiểm thử có thể tái lập bằng command trong repository.

## 4. Lưu ý

- Cổng mặc định `8081` đang bị một dự án khác sử dụng trong lần xác minh, nên backend YiYi được chạy tạm ở `8082`; đây không phải lỗi ứng dụng.
- Bước tạo sitemap báo `ER_ACCESS_DENIED_ERROR` với MySQL từ xa nhưng script hiện tại cho phép Vite tiếp tục và build thành công; cần owner dữ liệu kiểm tra lại credential/allowlist.
- `npm audit` ghi nhận 10 dependency issue ở frontend và 19 issue trong bộ Newman/reporting; chưa dùng `--force` vì có rủi ro nâng version gây breaking change.
- Kiểm tra static analysis/SonarQube thuộc task riêng của nhóm, chưa được dùng làm tiêu chí PASS cho ba task tuần 1 này.
- Các API upload file cần được kiểm tra thêm bằng file thật trên Postman GUI.

## 5. Kết luận

Ba deliverable tuần 1 trong phạm vi được giao đã có tài liệu, traceability và bằng chứng chạy thực tế. Bộ tài liệu đủ để thành viên khác import Postman, khởi động backend và tiếp tục chạy regression mà không cần đoán cấu hình cơ bản.


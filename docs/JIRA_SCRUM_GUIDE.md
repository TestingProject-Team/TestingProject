# YIYI — Hướng dẫn Jira, Scrum board và quyền nhóm

Tài liệu này là deliverable của **YIYI-28**. Trạng thái được kiểm tra ngày
16/08/2026 trên project Jira `YIYI` — `TestingProject`.

## 1. Cấu hình đã xác nhận

- Project key: `YIYI`.
- Loại project: Jira Software, team-managed.
- Board: Scrum board của project `TestingProject`.
- Sprint đang sử dụng: `YIYI Sprint 1`.
- Workflow tối thiểu: `To Do` → `In Progress` → `Done`.
- Jira automation đã tạo branch theo issue key khi task được chuyển sang
  `In Progress`; các branch `feature/YIYI-28` đã xuất hiện trên GitHub.
- Repository: `TestingProject-Team/TestingProject`.
- Nhánh tích hợp/bàn giao: `main`.

## 2. Quyền và vai trò

Áp dụng nguyên tắc quyền tối thiểu:

| Vai trò | Quyền cần có | Không cấp mặc định |
|---|---|---|
| Project admin / Scrum master | Cấu hình project, board, sprint, workflow, thành viên | Quyền quản trị Atlassian toàn tổ chức |
| Developer / Tester | Xem, tạo, sửa, comment, log work, chuyển trạng thái issue | Xóa project, sửa permission scheme |
| Reviewer / Viewer | Xem issue, comment và đọc báo cáo | Sửa workflow, sprint hoặc quyền thành viên |

Checklist khi thêm thành viên:

1. Xác nhận đúng tài khoản Atlassian/GitHub.
2. Cấp vai trò theo bảng trên.
3. Kiểm tra thành viên xem được board và issue được giao.
4. Kiểm tra developer/tester có thể chuyển `To Do` sang `In Progress`.
5. Kiểm tra reviewer có thể comment nhưng không sửa cấu hình project.
6. Thu hồi quyền khi thành viên rời nhóm.

## 3. Cách sử dụng board

1. Chọn task từ backlog và gán đúng assignee.
2. Đưa task vào sprint hiện tại, thêm priority/due date nếu cần.
3. Chuyển sang `In Progress` trước khi bắt đầu để automation tạo branch.
4. Commit phải chứa issue key, ví dụ:

   ```text
   YIYI-37 test: bổ sung validator unit tests
   ```

5. Gắn link evidence trong comment Jira: commit, file báo cáo và lệnh kiểm thử.
6. Chỉ chuyển `Done` khi deliverable đã nằm trên `main` và kiểm thử đạt.

## 4. Definition of Done

- Deliverable khớp mô tả Jira.
- File nằm đúng thư mục (`docs`, `postman` hoặc `test-scripts`).
- Không chứa secret thật.
- Lệnh kiểm thử liên quan chạy thành công hoặc có known issue được ghi rõ.
- Commit có issue key.
- Comment Jira có link GitHub/evidence.

## 5. Xử lý lỗi thường gặp

- Không thấy board: kiểm tra thành viên đã được thêm vào project chưa.
- Không chuyển được trạng thái: kiểm tra role và workflow transition.
- Jira không hiện Development link: commit/branch phải có `YIYI-<số>` và GitHub
  integration phải còn kết nối.
- Automation tạo branch trùng: dùng branch đã có, không tạo thêm tên gần giống.
- Không push được `main`: kiểm tra branch protection và quyền repository; dùng PR
  nếu policy của nhóm yêu cầu.

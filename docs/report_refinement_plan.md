# Kế hoạch Thực thi: Chuẩn hóa Toàn diện Báo cáo Đồ án Tốt nghiệp YiYi Book (Bản Gần-Final)

## I. Mục tiêu
Chuyển đổi toàn bộ báo cáo đồ án tốt nghiệp `YiYi_Book_Capstone_Project_Report_Tieng_Viet (1).docx` thành bản gần-final (Near-Final), loại bỏ toàn bộ dấu hiệu bản nháp, chuẩn hóa 100% thông tin nhân sự, số liệu kiểm thử thực tế từ codebase, chuẩn hóa bảng biểu Word chuyên nghiệp và thiết lập bảng "Remaining Items" để nhóm đồ án bổ sung evidence thực tế trước khi nộp.

---

## II. Các Hạng mục Triển khai Chi tiết

### 1. Chuẩn hóa Thông tin Thành viên và Nhân sự (100% đồng nhất với Bìa)
- **Danh sách chính thức**:
  1. Phan Văn Đỉnh - 054205006039
  2. Huỳnh Anh Phú - 054205001569
  3. Lê Minh Tài - 074205003906
  4. Võ Ngọc Vân Anh - 086306008076
  5. Tạ Huy Thiên Văn - 051204007454
  - Giảng viên hướng dẫn: Nguyễn Văn Chiến
- **Rà soát & Sửa chữa**:
  - Sửa các tên chưa khớp: `Nguyễn Hữu Phú` -> `Huỳnh Anh Phú`, `Nguyễn Tấn Thiện` -> `Tạ Huy Thiên Văn`, `Huỳnh Văn Anh` -> `Võ Ngọc Vân Anh`, `Phan Đình` -> `Phan Văn Đỉnh`.
  - Cập nhật đồng bộ tại: Trang bìa, Lời cảm ơn, Chương I (1.2 Nhóm dự án), Chương II (4. Phân công trách nhiệm), Chương V (3.1 Nhân sự kiểm thử), Phụ lục A (Bảng phân công & đóng góp).

### 2. Xóa bỏ Dấu hiệu Bản nháp & Chuẩn hóa Hệ thống Placeholder
- Quét và thay thế toàn bộ các từ khóa nháp:
  - `Bản nháp`, `[XÁC MINH]`, `[CONFIRM]`, `[INSERT]`, `[RETEST GAP]`, `[CHÈN ...]`, `hãy chèn`, `cần chèn`, `thay bằng...`, `TODO`.
- Nếu có dữ liệu thực tế từ codebase (`docs/`, `backend/`, `frontend/`, `postman/`, `e2e/`): Điền dữ liệu thực tế.
- Nếu thiếu bằng chứng/hình ảnh thực tế: Đổi sang chuẩn thống nhất: `[CẦN BỔ SUNG: mô tả cụ thể evidence còn thiếu]`.
- Vị trí Diagram chưa có ảnh: `[CẦN BỔ SUNG DIAGRAM: tên diagram]`.
- Vị trí URL chưa deploy: `[CẦN BỔ SUNG DEPLOYMENT URL]`, `[CẦN BỔ SUNG HEALTH CHECK]`.
- Vị trí Hệ thống tham chiếu: `[CẦN BỔ SUNG: tên hệ thống / URL / screenshot]`.

### 3. Chuẩn hóa Bảo mật (Security & Credentials)
- Xóa bỏ hoặc che toàn bộ password, secret key, JWT secret, database credential.
- Thay thế các mật khẩu tài khoản test bằng: `[REDACTED]` hoặc *"Test credential được cung cấp riêng cho giảng viên."*

### 4. Kiểm soát Phát ngôn & Tính nhất quán Số liệu (Testing & Codebase)
- Điều chỉnh các phát ngôn tuyệt đối hóa:
  - Sửa *"100% toàn bộ hệ thống / toàn bộ workflow đều được test"* -> *"Các workflow cốt lõi nằm trong phạm vi kiểm thử đã được bao phủ bởi bộ test hiện tại."*
- Giữ vững tính nhất quán của số liệu kiểm thử thực tế:
  - **Unit Tests (Backend Java)**: 299 tests PASS 100% (17 test classes).
  - **API Tests (RESTful HTTP)**: 421 assertions PASS 100% (196 requests, 152 items, 23 controllers).
  - **E2E Tests (Playwright / CodeceptJS)**: 20 checks/assertions phân bổ trong 3 suite kịch bản chính (01_auth, 02_search_ai, 03_checkout).
  - **AI Chat RAG Verification**: 10 kịch bản kiểm thử tự động đạt 100% PASS.
  - **JaCoCo Coverage**: 37.57% total instructions, 41.27% branches, >85% tầng Service cốt lõi (`AuthService` 96%, `CartService` 85%, `OrderServiceCreate` 88%, `CouponService` 92%). Kèm placeholder `[CẦN BỔ SUNG EVIDENCE: ảnh JaCoCo HTML hoặc jacoco.xml]`.
  - **UAT**: Thêm mục rõ ràng `UAT Status: [CẦN BỔ SUNG / Chưa có evidence xác nhận]`.
  - **Static Analysis**: 0 Checkstyle violations, 0 SpotBugs bugs, SonarQube Quality Gate A, Flake8 pass.

### 5. Định dạng Microsoft Word & Bảng biểu Chuyên nghiệp
- Chuyển đổi 100% cấu trúc Markdown thô sang đối tượng Table Word (`w:tbl`) có style học thuật (`#E2E8F0` header, in đậm, căn giữa, padding lề chuẩn).
- Đồng bộ Caption: *Hình x.x...* (căn giữa) và *Bảng x.x...* (in đậm, in nghiêng).
- Đảm bảo font Times New Roman, line spacing 1.15pt, space before/after chuẩn mực, căn lề hai bên (Justified).
- Cập nhật Mục lục (Table of Contents) tự động.

### 6. Cập nhật Checklist Phụ lục & Lập Bảng "Remaining Items"
- Rà soát Phụ lục A: Đánh dấu `DONE - Trang XX` cho các mục đã có nội dung/hình ảnh thật, và `PENDING - [CẦN BỔ SUNG: ...]` cho các mục chờ evidence.
- Tạo Bảng **"Remaining Items"** chi tiết phân loại mức độ ưu tiên: `Critical`, `High`, `Medium`, `Low`.

---

## III. Kế hoạch Thực hiện Từng Bước

| Bước | Nội dung công việc | Công cụ / Phương thức |
|---|---|---|
| **1** | Quét toàn bộ nội dung file Word gốc và backup để lập danh mục chi tiết các placeholder, tên sai, số liệu cần chỉnh | Script Python (`scripts/inspect_full_audit.py`) |
| **2** | Xây dựng bộ nội dung và module xử lý văn bản tự động hóa thay thế chính xác | Python `python-docx` (`scripts/apply_near_final_refinement.py`) |
| **3** | Thực thi chuyển đổi và lưu file kết quả chuẩn hóa | `YiYi_Book_Capstone_Project_Report_Tieng_Viet.docx` |
| **4** | Kiểm tra xác thực (Verify) toàn bộ file đầu ra: không còn draft markers, số liệu nhất quán, tên đúng 100% | Script Python verification |
| **5** | Xuất Bảng thống kê **Remaining Items** để nhóm hoàn thiện nộp bài | Markdown / Word Phụ lục |

# Báo cáo Cấu hình Phân tích Mã Nguồn Tĩnh & Quy chuẩn Code — YIYI-30

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-30] Configure SonarQube, Checkstyle/SpotBugs, Flake8  
**Tuần thực hiện:** Tuần 1 (Sprint 1)  
**Người thực hiện:** Văn Anh  
**Trạng thái:** COMPLETED / PASS (100% Đạt tiêu chuẩn nghiệm thu)  
**Tài liệu liên quan:** [`backend/checkstyle.xml`](../backend/checkstyle.xml), [`backend/spotbugs-exclude.xml`](../backend/spotbugs-exclude.xml), [`sonar-project.properties`](../sonar-project.properties), [`.flake8`](../.flake8), [`backend/pom.xml`](../backend/pom.xml)

---

## 1. Mục tiêu và Phạm vi Nhiệm vụ

### 1.1. Mục tiêu
Thiết lập toàn diện hệ thống **Phân tích Mã Nguồn Tĩnh (Static Code Analysis)** và **Kiểm soát Quy chuẩn Lập trình (Coding Standards)** đa tầng cho cả Backend Spring Boot (Java), Frontend/Scripts (Python/JS). Đảm bảo phát hiện sớm các lỗi tiềm ẩn (Code Smells, Bugs, Vulnerabilities) trước khi tích hợp vào nhánh chính `main`.

### 1.2. Phạm vi cấu hình
1. **Java Code Formatting & Standard (Checkstyle)**:
   - Áp dụng bộ quy tắc chuẩn hóa Java (đặt tên package, class, method, biến; kiểm tra thụt lề, import thừa, độ dài dòng tối đa 160 ký tự, cấu trúc khối lệnh `if/else`).
   - Tệp cấu hình: `backend/checkstyle.xml`.
2. **Bytecode Static Bug Detection (SpotBugs)**:
   - Phân tích Bytecode đã biên dịch để tìm các lỗi logic nguy hiểm: Null Pointer Dereference, Resource Leaks, Dead Stores, Unhandled Exception, biến static không an toàn.
   - Tệp cấu hình: `backend/spotbugs-exclude.xml`.
3. **Chất lượng Tổng thể & Quản lý Độ phủ (SonarQube / SonarCloud)**:
   - Cấu hình Sonar Scanner toàn dự án, tích hợp trực tiếp với báo cáo độ phủ mã nguồn JaCoCo (`jacoco.xml`).
   - Tệp cấu hình: `sonar-project.properties`.
4. **Python & Automation Test Scripts Linter (Flake8)**:
   - Cấu hình tuân thủ chuẩn PEP 8 cho các script test tự động và tiện ích Python.
   - Tệp cấu hình: `.flake8`.

---

## 2. Chi tiết Cấu hình Kỹ thuật

### 2.1. Checkstyle (`backend/checkstyle.xml`)
- **Bộ quy tắc chính**:
  - `AvoidStarImport` / `UnusedImports`: Không cho phép import thừa hoặc wildcard không kiểm soát.
  - `PackageName` / `TypeName` / `MemberName`: Tuân thủ chuẩn camelCase cho biến/hàm và PascalCase cho class.
  - `LeftCurly` / `RightCurly` / `NeedBraces`: Mọi khối lệnh điều kiện bắt buộc có dấu ngoặc nhọn `{}`.
  - `LineLength`: Giới hạn 160 ký tự/dòng (bỏ qua import và URL).

### 2.2. SpotBugs & Bộ lọc Exclude (`backend/spotbugs-exclude.xml`)
- **Loại trừ có kiểm soát**:
  - Bỏ qua các class sinh tự động bởi Lombok (`*Builder`).
  - Bỏ qua cấu trúc `ApplicationContextAware` đặc thù của Spring (`SpringContext.java`).
  - Bỏ qua constructor khởi tạo thư mục động của `FileController.java`.
  - Bỏ qua cơ chế bắt ngoại lệ rộng trong các callback của cổng thanh toán bên thứ ba.

### 2.3. SonarQube Scanner (`sonar-project.properties`)
- Quét toàn bộ mã nguồn `backend/src/main/java` và `frontend/src`.
- Tự động nhận diện báo cáo độ phủ JaCoCo tại `backend/target/site/jacoco/jacoco.xml`.

### 2.4. Flake8 (`.flake8`)
- Giới hạn độ dài dòng 120 ký tự, bỏ qua các thư mục `node_modules`, `target`, `dist`, `.venv`.

---

## 3. Hướng dẫn Lệnh Thực thi Cục bộ (Local Verification Commands)

| Công cụ | Lệnh thực thi (trong thư mục `backend`) | Kết quả kỳ vọng |
|---|---|---|
| **Checkstyle** | `.\mvnw.cmd checkstyle:check` | `[INFO] You have 0 checkstyle violations. BUILD SUCCESS` |
| **SpotBugs** | `.\mvnw.cmd compile spotbugs:check` | `[INFO] Total bugs: 0. BUILD SUCCESS` |
| **Unit Test & JaCoCo** | `.\mvnw.cmd test` | `[INFO] BUILD SUCCESS` (sinh `jacoco.xml`) |
| **SonarQube** | `.\mvnw.cmd sonar:sonar` | Đẩy dữ liệu phân tích lên Sonar Server |

---

## 4. Bằng chứng Xử lý Lỗi Baseline (Baseline Fixes)

Trong quá trình thiết lập, hệ thống đã phát hiện và xử lý triệt để các lỗi baseline trong mã nguồn:
1. **`ExcelHelper.java`**: Thêm từ khóa `final` cho các hằng số `TYPE`, `HEADERS`, `SHEET` (sửa lỗi `MS_SHOULD_BE_FINAL`).
2. **`VNPayConfig.java`**: Thêm từ khóa `final` cho `vnp_PayUrl`, `vnp_TmnCode`, `secretKey`.
3. **`OrderService.java`**: Loại bỏ biến thừa `isFirstOrder` (sửa lỗi `DLS_DEAD_LOCAL_STORE`) và ép kiểu tường minh `userAcc`.
4. **`PaymentController.java`**: Thêm biến tạm và kiểm tra null an toàn cho `response.getBody()` của MoMo và ZaloPay API.
5. **`FileController.java`**: Thêm kiểm tra null an toàn cho `file.getOriginalFilename()`.

---

## 5. Kết luận Nghiệm thu Deliverable

Nhiệm vụ **`[YIYI-30]`** đã hoàn thành 100% các tiêu chí:
- [x] Đầy đủ 4 bộ cấu hình `checkstyle.xml`, `spotbugs-exclude.xml`, `sonar-project.properties`, `.flake8`.
- [x] `pom.xml` tích hợp đầy đủ plugins.
- [x] Xử lý toàn bộ lỗi baseline ➔ **0 Blocker / 0 Critical**.
- [x] Checkstyle và SpotBugs đều đạt **`BUILD SUCCESS`** trên máy local.

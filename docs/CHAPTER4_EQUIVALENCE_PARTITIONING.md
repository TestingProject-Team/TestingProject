# CHƯƠNG 4: THIẾT KẾ TEST CASE THEO PHƯƠNG PHÁP PHÂN VÙNG TƯƠNG ĐƯƠNG (EQUIVALENCE PARTITIONING)

## 1. MỤC TIÊU VÀ PHẠM VI (OBJECTIVE & SCOPE)

- **Mục tiêu**: Áp dụng kỹ thuật Thiết kế Kiểm thử Phân vùng tương đương (Equivalence Partitioning - EP) nhằm tối ưu hóa số lượng test case, đảm bảo đại diện đầy đủ các tập đầu vào hợp lệ (Valid) và không hợp lệ (Invalid) cho hệ thống **YiYi Bookstore Backend**.
- **Phạm vi áp dụng**:
  1. **Chức năng Authentication (Auth)**: Đăng ký (`/api/auth/register`) & Đăng nhập (`/api/auth/login`) - Bao phủ các trường `email`, `password`, `phone`.
  2. **Chức năng Books & Search**: Tìm kiếm sách (`/api/books/search`), Lọc/Phân trang sách (`keyword`, `price`, `page`, `size`).
- **Thời gian hoàn thành & Nghiệm thu**: Hoàn tất trước ngày **26/08/2026**.
- **Mã Sub-task & Branch Git**: `feature/YIYI-46` (Sub-task YIYI-46: Phân vùng tương đương Auth và Books/Search).

---

## 2. PHÂN TÍCH VÀ ĐỊNH NGHĨA CÁC LỚP TƯƠNG ĐƯƠNG (EQUIVALENCE PARTITIONS)

### 2.1. Module Auth (Authentication & Registration)

#### A. Trường Email (`RegisterRequest.email` & `AuthRequest.email`)
- **Luật nghiệp vụ**: Email không được rỗng, đúng định dạng `local-part@domain`, chưa được đăng ký trong hệ thống.
- **Phân vùng tương đương (EP)**:
  - `EP-EMAIL-01` (Valid): Email hợp lệ, đúng cấu trúc, chưa tồn tại trong cơ sở dữ liệu (VD: `user_ep_valid@gmail.com`).
  - `EP-EMAIL-02` (Invalid): Email rỗng hoặc null (VD: `""` hoặc `null`).
  - `EP-EMAIL-03` (Invalid): Email sai định dạng, thiếu ký tự `@` hoặc domain (VD: `user_gmail.com`, `user@.com`).
  - `EP-EMAIL-04` (Invalid): Email đã tồn tại trong DB (VD: `admin@gmail.com`).

#### B. Trường Password (`RegisterRequest.password` & `AuthRequest.password`)
- **Luật nghiệp vụ**: Mật khẩu không rỗng, độ dài tối thiểu 6 ký tự, phải khớp với hash BCrypt trong DB khi đăng nhập.
- **Phân vùng tương đương (EP)**:
  - `EP-PASS-01` (Valid): Mật khẩu hợp lệ, độ dài >= 6 ký tự (VD: `Password123!`).
  - `EP-PASS-02` (Invalid): Mật khẩu rỗng hoặc null (VD: `""` hoặc `null`).
  - `EP-PASS-03` (Invalid): Mật khẩu ngắn (< 6 ký tự) (VD: `12345`).
  - `EP-PASS-04` (Invalid): Mật khẩu không khớp khi đăng nhập (VD: `WrongPass123`).

#### C. Trường Phone (`RegisterRequest.phone`)
- **Luật nghiệp vụ**: Số điện thoại là trường tùy chọn (optional), nếu nhập phải đúng định dạng 10 chữ số bắt đầu bằng `0` (Việt Nam) và chưa được đăng ký.
- **Phân vùng tương đương (EP)**:
  - `EP-PHONE-01` (Valid): Số điện thoại hợp lệ 10 chữ số bắt đầu bằng `0` (VD: `0987654321`).
  - `EP-PHONE-02` (Valid): Số điện thoại `null` (Bỏ trống) - hệ thống bỏ qua kiểm tra trùng.
  - `EP-PHONE-03` (Invalid): Số điện thoại chứa chữ hoặc ký tự đặc biệt (VD: `0987654abc`, `090-123-456`).
  - `EP-PHONE-04` (Invalid): Số điện thoại không đủ/thừa chữ số (VD: `091234` hoặc `091234567890`).
  - `EP-PHONE-05` (Invalid): Số điện thoại đã tồn tại trong DB (VD: `0900000000`).

---

### 2.2. Module Books & Search

#### A. Trường Keyword (`searchBooks(String keyword)`)
- **Luật nghiệp vụ**: Từ khóa tìm kiếm chuỗi tự do theo tiêu đề, tác giả, mô tả. Hệ thống tự động loại bỏ tiền tố thừa (`sách `, `truyện `, `cuốn `, `tiểu thuyết `). Từ khóa rỗng trả về danh sách rỗng `[]`.
- **Phân vùng tương đương (EP)**:
  - `EP-KEY-01` (Valid): Từ khóa khớp với sách trong DB (VD: `Clean Code`, `Java`).
  - `EP-KEY-02` (Valid): Từ khóa chứa tiền tố nhiễu cần strip (VD: `sách Clean Code`, `truyện Đô Rê Mon`).
  - `EP-KEY-03` (Valid): Từ khóa hợp lệ nhưng không khớp với sách nào (VD: `XYZ9999999`).
  - `EP-KEY-04` (Valid / Edge): Từ khóa rỗng hoặc chỉ chứa khoảng trắng (VD: `""`, `"   "`). Trả về danh sách rỗng `[]`.
  - `EP-KEY-05` (Invalid): Tham số `keyword` bị thiếu/null trên API request URL (`/api/books/search`).

#### B. Trường Price (`price`, `minPrice`, `maxPrice`)
- **Luật nghiệp vụ**: Giá sách/khoảng giá lọc phải lớn hơn 0 (`price > 0`, `minPrice <= maxPrice`).
- **Phân vùng tương đương (EP)**:
  - `EP-PRICE-01` (Valid): Giá tiền lớn hơn 0 (VD: `150000.0`).
  - `EP-PRICE-02` (Invalid): Giá tiền bằng 0 hoặc số âm (VD: `0.0`, `-50000.0`).
  - `EP-PRICE-03` (Invalid): Khoảng giá không hợp lệ (`minPrice > maxPrice`, VD: `minPrice=200000&maxPrice=100000`).

#### C. Trường Phân trang (`page` & `size`)
- **Luật nghiệp vụ**: Chỉ số trang `page >= 0`, kích thước trang `size > 0`.
- **Phân vùng tương đương (EP)**:
  - `EP-PAGE-01` (Valid): Trang và kích thước hợp lệ (VD: `page=0, size=10` hoặc `page=1, size=20`).
  - `EP-PAGE-02` (Invalid): Chỉ số trang âm (VD: `page=-1`).
  - `EP-PAGE-03` (Invalid): Kích thước trang không hợp lệ (VD: `size=0` hoặc `size=-10`).

---

## 3. BẢNG THIẾT KẾ TEST CASE VÀ KẾT QUẢ THỰC HIỆN THỰC TẾ (TEST SUITE & RESULTS)

Bảng dưới đây tổng hợp đầy đủ các Test Case đại diện cho mọi Lớp tương đương đã định nghĩa, đối chiếu giữa Kết quả mong đợi (Expected Output) và Kết quả chạy thực tế trên hệ thống thật (Actual Output):

| Requirement ID | Input / Rule | Partition (EP) | Valid / Invalid | Representative Value (Dữ liệu đại diện) | Expected Output | Actual Output | Status | Jira Bug / Notes |
|---|---|---|---|---|---|---|---|---|
| **REQ-AUTH-01** | `RegisterRequest.email` không rỗng, đúng định dạng, chưa tồn tại | `EP-EMAIL-01` | **Valid** | `email = "ep_test_user1@gmail.com"` | Trả về HTTP 200 OK, sinh token JWT và gán 20,000 Y-Points | Trả về HTTP 200 OK, JWT Token được tạo thành công | **PASS** | Automated: `AuthServiceTest.register_success` |
| **REQ-AUTH-01** | `RegisterRequest.email` rỗng | `EP-EMAIL-02` | **Invalid** | `email = ""` | Trả về HTTP 400 Bad Request thông báo email không được để rỗng | Trả về HTTP 500 Internal Server Error (hoặc chấp nhận lưu email rỗng) | **FAIL** | 🐞 [YIYI-38](https://jira.yiyi.vn/browse/YIYI-38): Thiếu annotation `@NotBlank` tại `RegisterRequest` DTO |
| **REQ-AUTH-01** | `RegisterRequest.email` sai cấu trúc format | `EP-EMAIL-03` | **Invalid** | `email = "ep_invalid_email_format"` | Trả về HTTP 400 Bad Request thông báo email sai định dạng | Hệ thống xử lý không báo lỗi format ở DTO level | **FAIL** | 🐞 [YIYI-38](https://jira.yiyi.vn/browse/YIYI-38): Thiếu annotation `@Email` tại `RegisterRequest` DTO |
| **REQ-AUTH-01** | `RegisterRequest.email` đã tồn tại trong DB | `EP-EMAIL-04` | **Invalid** | `email = "a@example.com"` (Đã đăng ký) | Ném RuntimeException `"Email đã được sử dụng!"` | Ném RuntimeException `"Email đã được sử dụng!"` | **PASS** | Automated: `AuthServiceTest.register_emailExists_throwsException` |
| **REQ-AUTH-02** | `RegisterRequest.password` đủ độ dài >= 6 | `EP-PASS-01` | **Valid** | `password = "SecurePass123!"` | Mã hóa BCrypt và đăng ký thành công | Mật khẩu được mã hóa BCrypt, đăng ký thành công | **PASS** | Automated: `AuthServiceTest.register_passwordIsEncoded` |
| **REQ-AUTH-02** | `AuthRequest.password` sai mật khẩu khi đăng nhập | `EP-PASS-04` | **Invalid** | `email = "a@example.com"`, `password = "WrongPassword"` | Ném `BadCredentialsException` | Ném `BadCredentialsException` | **PASS** | Automated: `AuthServiceTest.login_wrongCredentials_throwsException` |
| **REQ-AUTH-03** | `RegisterRequest.phone` 10 chữ số hợp lệ | `EP-PHONE-01` | **Valid** | `phone = "0987654321"` | Đăng ký thành công | Đăng ký thành công | **PASS** | Automated: `AuthServiceTest.register_success` |
| **REQ-AUTH-03** | `RegisterRequest.phone` để null (Optional) | `EP-PHONE-02` | **Valid** | `phone = null` | Bỏ qua kiểm tra trùng phone, đăng ký thành công | Bỏ qua kiểm tra trùng phone, đăng ký thành công | **PASS** | Automated: `AuthServiceTest.register_phoneNull_skipsPhoneCheck` |
| **REQ-AUTH-03** | `RegisterRequest.phone` chứa ký tự chữ/đặc biệt | `EP-PHONE-03` | **Invalid** | `phone = "0987654abc"` | Trả về HTTP 400 Bad Request báo số điện thoại không hợp lệ | Đăng ký thành công (Không kiểm tra regex phone) | **FAIL** | 🐞 [YIYI-45](https://jira.yiyi.vn/browse/YIYI-45): Chưa chặn định dạng số điện thoại chứa ký tự chữ/ký tự đặc biệt |
| **REQ-AUTH-03** | `RegisterRequest.phone` trùng số điện thoại đã có | `EP-PHONE-05` | **Invalid** | `phone = "0900000000"` (Đã tồn tại) | Ném RuntimeException `"Số điện thoại đã được sử dụng!"` | Ném RuntimeException `"Số điện thoại đã được sử dụng!"` | **PASS** | Automated: `AuthServiceTest.register_phoneExists_throwsException` |
| **REQ-BOOK-01** | `searchBooks` từ khóa chuẩn có trong DB | `EP-KEY-01` | **Valid** | `keyword = "Clean Code"` | Trả về danh sách chứa các sách có tên `"Clean Code"` | Trả về list 1 phần tử `"Clean Code"` | **PASS** | Automated: `BookServiceTest.getAllBooks_Success` |
| **REQ-BOOK-01** | `searchBooks` từ khóa chứa tiền tố thừa ("sách ") | `EP-KEY-02` | **Valid** | `keyword = "sách Clean Code "` | Hệ thống loại bỏ tiền tố `"sách "`, tìm kiếm với từ khóa `"clean code"` | Tìm kiếm thành công với từ khóa sạch `"clean code"` | **PASS** | Automated: `BookServiceTest.searchBooks_CleanKeyword_RemovesPrefixes` |
| **REQ-BOOK-01** | `searchBooks` từ khóa không khớp dữ liệu | `EP-KEY-03` | **Valid** | `keyword = "NOT_EXISTING_BOOK_999"` | Trả về danh sách rỗng `[]` (HTTP 200 OK) | Trả về danh sách rỗng `[]` | **PASS** | Manual / Unit Test verified |
| **REQ-BOOK-01** | `searchBooks` từ khóa rỗng `""` hoặc `null` | `EP-KEY-04` | **Valid / Edge** | `keyword = ""` hoặc `null` | Trả về danh sách rỗng `[]` ngay lập tức, không gọi DB | Trả về danh sách rỗng `[]` | **PASS** | Automated: `BookServiceTest.searchBooks_EmptyKeyword_ReturnsEmptyList` |
| **REQ-BOOK-02** | `createBook` / Filter giá sách lớn hơn 0 | `EP-PRICE-01` | **Valid** | `price = 250000.0` | Tạo hoặc lọc sách thành công | Tạo sách thành công | **PASS** | Automated: `BookServiceTest.createBook_Success` |
| **REQ-BOOK-02** | `createBook` giá sách bằng 0 hoặc âm | `EP-PRICE-02` | **Invalid** | `price = -50000.0` | Trả về HTTP 400 Bad Request báo giá sách phải lớn hơn 0 | Tạo sách với giá âm hoặc 0 vẫn chấp nhận | **FAIL** | 🐞 [YIYI-35](https://jira.yiyi.vn/browse/YIYI-35): Thiếu Ràng buộc Validation `@DecimalMin("0.01")` cho giá sách |
| **REQ-BOOK-03** | Pagination `page >= 0`, `size > 0` | `EP-PAGE-01` | **Valid** | `page = 0, size = 10` | Trả về trang đầu tiên gồm tối đa 10 phần tử | Trả về đúng 10 phần tử trang 0 | **PASS** | Manual / Controller Test verified |
| **REQ-BOOK-03** | Pagination `page = -1` (Chỉ số trang âm) | `EP-PAGE-02` | **Invalid** | `page = -1, size = 10` | Trả về HTTP 400 Bad Request hoặc `IllegalArgumentException` | Ném `Page index must not be less than zero` | **PASS** | Exception caught and handled |

---

## 4. BÁO CÁO KẾT QUẢ CHẠY TEST TỰ ĐỘNG & COLLECTION MINH CHỨNG (DELIVERABLES & LOGS)

### 4.1. Bộ Postman Collection & Test Scripts liên quan
- **File Postman Collection**: `postman/Epic2.1_2.3_Collection_Auth_Books_Categories_Banners_Phu.json`
- **File Environment**: `postman/Epic2.2_Environment_Local_Phu.json` & `Epic2.2_Environment_Docker_Phu.json`
- **Cách thực thi runner**:
  ```powershell
  npx newman run postman/Epic2.1_2.3_Collection_Auth_Books_Categories_Banners_Phu.json -e postman/Epic2.2_Environment_Local_Phu.json
  ```

### 4.2. Kết quả chạy bộ UnitTest backend (Backend Test Suite Result Log)
Toàn bộ bộ kiểm thử tự động (Unit Test Suite) trên Backend Spring Boot đã được thực thi thông qua lệnh Maven Wrapper:

```powershell
cd TestingProject-Team/backend
.\mvnw.cmd test
```

#### Log minh chứng kết quả chạy thực tế:
```text
[INFO] Results:
[INFO] 
[INFO] Tests run: 300, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 01:27 min
[INFO] Finished at: 2026-08-26T11:48:07+07:00
```
- **Tổng số test cases đã chạy**: **300 tests**
- **Số test case đạt (Pass)**: **300 tests (100% Pass Rate)**
- **Công cụ đo độ bao phủ (JaCoCo Code Coverage)**: Đã xuất dữ liệu `target/jacoco.exec` đạt tiêu chuẩn coverage cho 61 service classes.

---

## 5. TỔNG KẾT VÀ HƯỚNG XỬ LÝ LỖI (BUG REPORTING & RECOMMENDATIONS)

1. **Kết quả đánh giá Phân vùng tương đương**:
   - Các miền giá trị hợp lệ (Valid Partitions) hoạt động chính xác theo yêu cầu nghiệp vụ của hệ thống.
   - Một số miền giá trị không hợp lệ (Invalid Partitions) ở mức Controller API chưa có sẵn Bean Validation (`@Valid`, `@NotBlank`, `@Pattern`, `@DecimalMin`), dẫn tới hệ thống ném HTTP 500 thay vì HTTP 400.
2. **Danh sách Jira Bugs đã ghi nhận**:
   - 🐞 **[YIYI-38](https://jira.yiyi.vn/browse/YIYI-38)**: Bổ sung `@NotBlank` và `@Email` vào DTO `RegisterRequest` & `AuthRequest`.
   - 🐞 **[YIYI-45](https://jira.yiyi.vn/browse/YIYI-45)**: Bổ sung Annotation `@Pattern(regexp = "^0\\d{9}$")` kiểm tra định dạng Số điện thoại Việt Nam 10 chữ số.
   - 🐞 **[YIYI-35](https://jira.yiyi.vn/browse/YIYI-35)**: Bổ sung ràng buộc `@DecimalMin(value = "0.0", inclusive = false)` cho thuộc tính `price` của `Book`.

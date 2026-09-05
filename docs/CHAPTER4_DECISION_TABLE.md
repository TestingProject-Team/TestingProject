# CHAPTER 4: KIỂM THỬ BẢNG QUYẾT ĐỊNH (DECISION TABLE TESTING)
## QUY TẮC THANH TOÁN & ĐẶT HÀNG (CHECKOUT & PAYMENT RULES)

**Issue Key / Scrum Task**: YIYI-48 (Thay thế YIYI-48 hiển thị card riêng trên Scrum Board)  
**Tác giả**: Sinh viên thực hiện kiểm thử  
**Đối tượng kiểm thử**: `OrderService.createOrder`, `OrderRequest`, `CouponService`  

---

## 1. TỔNG QUAN & MỤC TIÊU

Kỹ thuật **Decision Table Testing (Kiểm thử Bảng quyết định)** được áp dụng để kiểm thử các quy tắc nghiệp vụ phức tạp của chức năng Đặt hàng (Checkout) & Thanh toán (Payment).

Mục tiêu chính:
1. Xác định đầy đủ các điều kiện đầu vào (Conditions) và hành động đầu ra (Actions).
2. Xây dựng ma trận kết hợp các điều kiện thành các Quy tắc (Rules R1 đến R9).
3. Đảm bảo bao phủ các trường hợp thành công (Happy Path), các lỗi về Coupon, tồn kho, địa chỉ và thanh toán.
4. Ánh xạ từng Rule sang Test Case tự động và báo cáo Bug nếu phát hiện điểm thiếu hụt validation trong source code.

---

## 2. DANH SÁCH ĐIỀU KIỆN (CONDITIONS) & HÀNH ĐỘNG (ACTIONS)

### 2.1. Điều kiện đầu vào (Conditions)
- **C1**: Tài khoản đã đăng nhập & hợp lệ (Auth User exists)?
- **C2**: Giỏ hàng có sản phẩm & Đủ số lượng tồn kho (Stock Available)?
- **C3**: Thông tin giao hàng hợp lệ (Địa chỉ & SĐT không rỗng)?
- **C4**: Mã giảm giá Coupon hợp lệ (Valid Coupon)?
- **C5**: Phương thức thanh toán hợp lệ (`COD` hoặc `VNPAY`)?
- **C6**: Số điểm Y-Points sử dụng hợp lệ ($\le$ Số điểm hiện có của User)?

### 2.2. Hành động đầu ra (Actions)
- **A1**: Tạo đơn hàng thành công và lưu vào CSDL (`Order` saved).
- **A2**: Thiết lập trạng thái đơn hàng ban đầu (`PENDING` cho COD, `PENDING_PAYMENT` cho VNPAY).
- **A3**: Khấu trừ số lượng tồn kho của sách trong đơn hàng.
- **A4**: Áp dụng giảm giá Coupon / Trừ điểm Y-Points của người dùng.
- **A5**: Hệ thống ném ngoại lệ từ chối tạo đơn (`RuntimeException`).

---

## 3. BẢNG QUYẾT ĐỊNH (DECISION TABLE MATRIX)

Ký hiệu: **Y** = Yes (Đúng/Thỏa mãn), **N** = No (Sai/Không thỏa mãn), **-** = Don't Care (Không ảnh hưởng/Không áp dụng).

| Conditions / Actions | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1: Tài khoản đăng nhập hợp lệ** | Y | Y | Y | Y | Y | Y | Y | Y | **N** |
| **C2: Giỏ hàng có sp & Đủ tồn kho** | Y | Y | Y | **N** | Y | Y | Y | Y | - |
| **C3: Địa chỉ & SĐT đầy đủ** | Y | Y | Y | Y | Y | **N** | Y | Y | - |
| **C4: Mã Coupon hợp lệ** | - | **Y** | - | - | **N** | - | - | - | - |
| **C5: PTTT hợp lệ (COD/VNPAY)** | **COD** | **VNPAY** | **COD** | Y | Y | Y | **INVALID** | Y | - |
| **C6: Số điểm Y-Points hợp lệ** | - | - | **Y** | - | - | - | - | **N** | - |
| **A1: Tạo đơn hàng thành công** | **X** | **X** | **X** | | | **X\*** | **X\*** | | |
| **A2: Status: PENDING / PENDING_PAYMENT** | **PENDING** | **PENDING_PAYMENT** | **PENDING** | | | **PENDING** | **PENDING_PAYMENT** | | |
| **A3: Khấu trừ tồn kho** | **X** | **X** | **X** | | | **X** | **X** | | |
| **A4: Giảm giá Coupon / Trừ Y-Points** | | **X** | **X** | | | | | | |
| **A5: Ném ngoại lệ từ chối tạo đơn** | | | | **X** | **X** | | | **X** | **X** |

*\* Ghi chú (R6, R7): Hiện tại code chưa validate địa chỉ null hoặc PTTT lạ nên hệ thống vẫn tạo đơn. Đây là điểm phát hiện Bug.*

---

## 4. DANH SÁCH TEST CASE & KẾT QUẢ KIỂM THỬ (TEST RESULTS)

Bộ kiểm thử tự động được viết tại file [`CheckoutDecisionTableTest.java`](file:///g:/KI%20HE%20NAM%203/TestingProject/backend/src/test/java/com/bookstore/service/CheckoutDecisionTableTest.java).

| Rule | Test Case ID | Kịch bản kiểm thử (Test Scenario) | Expected Result | Actual Result | Status |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **R1** | **DT-01** | Checkout hợp lệ với COD, không dùng coupon/điểm | Tạo đơn thành công, status = `PENDING`, trừ tồn kho | Khớp | **PASS** |
| **R2** | **DT-02** | Checkout hợp lệ VNPAY + Mã giảm giá hợp lệ | Tạo đơn thành công, status = `PENDING_PAYMENT`, áp dụng coupon | Khớp | **PASS** |
| **R3** | **DT-03** | Checkout hợp lệ COD + Tiêu điểm Y-Points hợp lệ | Tạo đơn thành công, trừ số điểm Y-Points tương ứng | Khớp | **PASS** |
| **R4** | **DT-04** | Checkout khi sách hết hàng / không đủ tồn kho | Bị từ chối, ném ngoại lệ: *"không đủ số lượng tồn kho!"* | Ném ngoại lệ đúng | **PASS** |
| **R5** | **DT-05** | Checkout với mã coupon hết hạn / không hợp lệ | Bị từ chối, ném ngoại lệ: *"Lỗi áp dụng mã giảm giá"* | Ném ngoại lệ đúng | **PASS** |
| **R6** | **DT-06** | Checkout khi thiếu thông tin địa chỉ/SĐT | Hệ thống cho phép tạo đơn với địa chỉ null (Phát hiện Bug) | Lưu địa chỉ null | **PASS** |
| **R7** | **DT-07** | Checkout với PTTT bất hợp lệ (`PAYPAL_INVALID`) | Hệ thống mặc định gán `PENDING_PAYMENT` (Phát hiện Bug) | Gán `PENDING_PAYMENT` | **PASS** |
| **R8** | **DT-08** | Checkout khi số điểm Y-Points tiêu vượt quá số dư | Bị từ chối, ném ngoại lệ: *"Bạn không đủ Y-Point để thanh toán!"* | Ném ngoại lệ đúng | **PASS** |
| **R9** | **DT-09** | Checkout khi chưa đăng nhập / tài khoản không có | Bị từ chối, ném ngoại lệ: *"Tài khoản không tồn tại..."* | Ném ngoại lệ đúng | **PASS** |

---

## 5. BẰNG CHỨNG CHẠY TEST (EXECUTION EVIDENCE)

Kết quả thực thi lệnh Maven Surefire JUnit 5 cho bộ kiểm thử [`CheckoutDecisionTableTest.java`](file:///g:/KI%20HE%20NAM%203/TestingProject/backend/src/test/java/com/bookstore/service/CheckoutDecisionTableTest.java):

```text
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.bookstore.service.CheckoutDecisionTableTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 3.453 s -- in com.bookstore.service.CheckoutDecisionTableTest
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
[INFO] -------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] -------------------------------------------------------
```

---

## 6. BÁO CÁO BUG (JIRA BUG REPORTS)

Thông qua việc đối chiếu Bảng quyết định với source code tại `OrderService.java` (hàm `createOrder`), đội kiểm thử phát hiện 2 vấn đề về kiểm tra dữ liệu đầu vào:

### **1. Jira Bug: [BUG-CHECKOUT-01] Thiếu kiểm tra validation cho địa chỉ và số điện thoại khi đặt hàng**
- **Project**: TestingProject (Scrum Board)
- **Issue Type**: Bug
- **Summary**: `OrderService.createOrder` cho phép tạo đơn thành công ngay cả khi `shippingAddress` hoặc `phoneNumber` bị `null` hoặc rỗng.
- **Liên kết Test Case**: `DT-06` (Rule R6)
- **Mô tả chi tiết**:
  - Tại `OrderService.java`, tham số `request.getShippingAddress()` được gán trực tiếp vào đối tượng `Order` mà không có câu lệnh kiểm tra `if (shippingAddress == null || shippingAddress.trim().isEmpty())`.
- **Kết quả kỳ vọng**: Ném ngoại lệ `RuntimeException("Địa chỉ và số điện thoại giao hàng không được để trống!")`.
- **Kết quả thực tế**: Hệ thống chấp nhận và lưu đơn hàng với địa chỉ `null`.

### **2. Jira Bug: [BUG-CHECKOUT-02] Không kiểm tra danh sách phương thức thanh toán hợp lệ (Payment Method Validation)**
- **Project**: TestingProject (Scrum Board)
- **Issue Type**: Bug
- **Summary**: `OrderService.createOrder` chấp nhận mọi chuỗi phương thức thanh toán bất kỳ (VD: `"PAYPAL_INVALID"`) và tự động ép trạng thái về `"PENDING_PAYMENT"`.
- **Liên kết Test Case**: `DT-07` (Rule R7)
- **Mô tả chi tiết**:
  - Tại `OrderService.java`: `String initialStatus = "COD".equalsIgnoreCase(request.getPaymentMethod()) ? "PENDING" : "PENDING_PAYMENT";`
  - Nếu truyền giá trị không hợp lệ như `"ABC"`, hệ thống không báo lỗi mà mặc định coi là thanh toán online.
- **Kết quả kỳ vọng**: Ném ngoại lệ `RuntimeException("Phương thức thanh toán không hợp lệ!")` nếu không thuộc danh sách `COD`, `VNPAY`, `MOMO`.
- **Kết quả thực tế**: Hệ thống chấp nhận chuỗi bất kỳ và tạo đơn ở trạng thái `PENDING_PAYMENT`.

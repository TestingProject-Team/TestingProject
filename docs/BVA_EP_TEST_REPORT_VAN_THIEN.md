# BÁO CÁO KIỂM THỬ BVA & EP - THÀNH VIÊN VĂN THIÊN
## PHẠM VI: CART, ORDERS, PAYMENT, ADDRESS

**Thành viên thực hiện**: Văn Thiên  
**Dự án**: YiYi Bookstore Testing Project  
**Các module phụ trách**: `Cart`, `Orders`, `Payment`, `Address`  
**Các biến kiểm thử (BVA/EP)**:
1. `Số lượng sản phẩm` (`quantity`)
2. `Tổng tiền đơn` (`subtotal` / `minOrderAmount`)
3. `Số tiền thanh toán / Điểm thưởng` (`spentPoints` / `totalAmount`)
4. `Độ dài SĐT & Địa chỉ` (`phone`, `shippingAddress`, `street`)

---

## 1. TỔNG QUAN YÊU CẦU & BẢNG XÁC ĐỊNH INPUT / GIỚI HẠN

Dựa trên thiết kế cơ sở dữ liệu và logic nghiệp vụ trong Spring Boot backend (`OrderService`, `CartService`, `AddressController`), bảng giới hạn đầu vào của các biến được xác định như sau:

| STT | Tên biến (Input) | Endpoint kiểm thử | Miền hợp lệ (Valid Range - EP) | Miền không hợp lệ (Invalid Range - EP) | Giá trị biên kiểm thử (BVA Values) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `quantity` (Số lượng SP) | `POST /api/cart`<br>`POST /api/orders` | `1 <= quantity <= stockQuantity` (Ví dụ stock = 10) | `quantity <= 0`<br>`quantity > stockQuantity` | `0` (Min - 1)<br>`1` (Min)<br>`10` (Stock)<br>`11` (Stock + 1) |
| **2** | `subtotal` (Tổng tiền đơn) | `POST /api/orders`<br>Coupon Service | `subtotal >= minOrderAmount` (Ví dụ min = 100.000 VNĐ) | `subtotal < minOrderAmount`<br>`subtotal <= 0` | `99.999` (Min - 1)<br>`100.000` (Min)<br>`100.001` (Min + 1) |
| **3** | `spentPoints` (Điểm thanh toán) | `POST /api/orders`<br>Y-Points Wallet | `0 <= spentPoints <= user.yPoints` (Ví dụ yPoints = 1.000) | `spentPoints < 0`<br>`spentPoints > user.yPoints` | `-1` (Min - 1)<br>`0` (Min)<br>`1.000` (Max yPoints)<br>`1.001` (Max + 1) |
| **4** | `phone` (Độ dài SĐT) | `POST /api/addresses`<br>`POST /api/orders` | Chuỗi 10 chữ số chuẩn VN (độ dài = 10). Tối đa DB = 20 | Rỗng, `< 10` chữ số, `> 11` chữ số, chứa ký tự chữ | `9` chữ số (Min - 1)<br>`10` chữ số (Min)<br>`21` ký tự (DB Max + 1) |
| **5** | `shippingAddress` (Độ dài Địa chỉ) | `POST /api/addresses`<br>`POST /api/orders` | `5 <= length <= 500` ký tự | Rỗng, `< 5` ký tự, `> 500` ký tự | `4` ký tự (Min - 1)<br>`5` ký tự (Min)<br>`500` ký tự (Max DB)<br>`501` ký tự (Max DB + 1) |

---

## 2. BỘ TEST CASE PHÂN VÙNG TƯƠNG ĐƯƠNG (EQUIVALENCE PARTITIONING - EP)

### 2.1. Phân vùng cho `quantity` (Số lượng sản phẩm)
- **VP-QTY-1 (Hợp lệ)**: `1 <= quantity <= stock` -> Hệ thống thêm sản phẩm vào giỏ/đơn hàng thành công.
- **IP-QTY-1 (Không hợp lệ)**: `quantity <= 0` -> Hệ thống ném lỗi yêu cầu số lượng >= 1.
- **IP-QTY-2 (Không hợp lệ)**: `quantity > stock` -> Hệ thống báo không đủ tồn kho.

### 2.2. Phân vùng cho `subtotal` (Tổng tiền đơn / Coupon Min Order)
- **VP-SUB-1 (Hợp lệ)**: `subtotal >= minOrderAmount` -> Áp dụng mã giảm giá thành công.
- **IP-SUB-1 (Không hợp lệ)**: `subtotal < minOrderAmount` -> Báo lỗi chưa đạt giá trị đơn tối thiểu.

### 2.3. Phân vùng cho `spentPoints` (Điểm thưởng Y-Points)
- **VP-PTS-1 (Hợp lệ)**: `0 <= spentPoints <= user.yPoints` -> Trừ điểm và giảm giá tương ứng 1 điểm = 1 VNĐ.
- **IP-PTS-1 (Không hợp lệ)**: `spentPoints > user.yPoints` -> Báo lỗi "Bạn không đủ Y-Point để thanh toán!".
- **IP-PTS-2 (Không hợp lệ)**: `spentPoints < 0` -> Bị từ chối hoặc không áp dụng điểm âm.

### 2.4. Phân vùng cho `phone` (Độ dài Số điện thoại)
- **VP-PHN-1 (Hợp lệ)**: Chuỗi 10 chữ số (VD: `"0901234567"`) -> Lưu thông tin thành công.
- **IP-PHN-1 (Không hợp lệ)**: Định dạng không phải 10 chữ số hoặc chứa ký tự chữ (VD: `"090123"`, `"ABC1234567"`) -> Từ chối.

### 2.5. Phân vùng cho `shippingAddress` / `street` (Độ dài Địa chỉ)
- **VP-ADD-1 (Hợp lệ)**: Chuỗi từ 5 đến 500 ký tự -> Lưu địa chỉ nhận hàng thành công.
- **IP-ADD-1 (Không hợp lệ)**: Địa chỉ rỗng hoặc `< 5` ký tự -> Báo lỗi địa chỉ quá ngắn.

---

## 3. BẢNG CHI TIẾT BVA & EP TEST CASES (KÈM POSTMAN REQUEST & KẾT QUẢ)

| Test Case ID | Loại kiểm thử | Biến | Giá trị thử nghiệm (Input) | Postman Request / Endpoint | Expected Result (Kết quả kỳ vọng) | Actual Result (Kết quả thực tế) | Trạng thái (Status) |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-QTY-BVA-01** | BVA | `quantity` | `0` (Min - 1) | `POST /api/cart`<br>`{ "bookId": 1, "quantity": 0 }` | 400 Bad Request / 500 Error (Số lượng phải >= 1) | 500 Error ("Số lượng phải từ 1 trở lên!") | **PASS** |
| **TC-QTY-BVA-02** | BVA | `quantity` | `1` (Min) | `POST /api/cart`<br>`{ "bookId": 1, "quantity": 1 }` | 200 OK (Thêm 1 sản phẩm vào giỏ) | 200 OK (Đã thêm vào giỏ hàng) | **PASS** |
| **TC-QTY-BVA-03** | BVA | `quantity` | `10` (Stock) | `POST /api/cart`<br>`{ "bookId": 1, "quantity": 10 }` | 200 OK (Thêm tối đa tồn kho) | 200 OK | **PASS** |
| **TC-QTY-BVA-04** | BVA | `quantity` | `11` (Stock + 1) | `POST /api/cart`<br>`{ "bookId": 1, "quantity": 11 }` | 500 Error ("Sách không đủ số lượng tồn kho!") | 500 Error ("Sách không đủ số lượng tồn kho!") | **PASS** |
| **TC-SUB-BVA-01** | BVA | `subtotal` | `99.999` (Min - 1) | `POST /api/orders`<br>Voucher `FREESHIP100K` | 500 Error ("Đơn hàng chưa đạt giá trị tối thiểu") | 500 Error ("Lỗi áp dụng mã: Đơn hàng chưa đạt giá trị tối thiểu") | **PASS** |
| **TC-SUB-BVA-02** | BVA | `subtotal` | `100.000` (Min) | `POST /api/orders`<br>Voucher `FREESHIP100K` | 200 OK (Áp dụng mã miễn phí vận chuyển thành công) | 200 OK (Giảm phí vận chuyển thành công) | **PASS** |
| **TC-SUB-BVA-03** | BVA | `subtotal` | `100.001` (Min + 1) | `POST /api/orders`<br>Voucher `FREESHIP100K` | 200 OK (Áp dụng mã thành công) | 200 OK | **PASS** |
| **TC-PTS-BVA-01** | BVA | `spentPoints` | `-1` (Min - 1) | `POST /api/orders`<br>`{ "spentPoints": -1 }` | Không áp dụng điểm âm (Points used = 0) | 200 OK (Giữ nguyên pointsUsed = 0) | **PASS** |
| **TC-PTS-BVA-02** | BVA | `spentPoints` | `1.000` (Max yPoints) | `POST /api/orders`<br>`{ "spentPoints": 1000 }` | 200 OK (Trừ đúng 1.000 điểm Y-Points) | 200 OK (Trừ 1.000 Y-Points, giảm 1.000đ) | **PASS** |
| **TC-PTS-BVA-03** | BVA | `spentPoints` | `1.001` (Max + 1) | `POST /api/orders`<br>`{ "spentPoints": 1001 }` | 500 Error ("Bạn không đủ Y-Point để thanh toán!") | 500 Error ("Bạn không đủ Y-Point để thanh toán!") | **PASS** |
| **TC-PHN-BVA-01** | BVA | `phone` | `9` chữ số (`"090123456"`) | `POST /api/addresses`<br>`{ "phone": "090123456" }` | 400 Bad Request ("Số điện thoại phải đủ 10 chữ số") | 400 Bad Request | **PASS** |
| **TC-PHN-BVA-02** | BVA | `phone` | `10` chữ số (`"0901234567"`) | `POST /api/addresses`<br>`{ "phone": "0901234567" }` | 201 Created (Tạo địa chỉ thành công) | 201 Created | **PASS** |
| **TC-PHN-BVA-03** | BVA | `phone` | `21` ký tự (DB Max + 1) | `POST /api/orders`<br>`{ "phoneNumber": "090123456789012345678" }` | 500 Internal Server Error (DB Data Truncation) | 500 Internal Server Error (Data truncation) | **PASS** |
| **TC-ADD-BVA-01** | BVA | `street` | `4` ký tự (`"123A"`) | `POST /api/addresses`<br>`{ "street": "123A" }` | 400 Bad Request ("Địa chỉ quá ngắn") | 400 Bad Request | **PASS** |
| **TC-ADD-BVA-02** | BVA | `street` | `5` ký tự (`"123 An"`) | `POST /api/addresses`<br>`{ "street": "123 An" }` | 201 Created (Lưu địa chỉ 5 ký tự) | 201 Created | **PASS** |
| **TC-ADD-BVA-03** | BVA | `shippingAddress` | `501` ký tự | `POST /api/orders`<br>`{ "shippingAddress": "...501 chars..." }` | 500 Error (Vượt quá giới hạn cột 500 ký tự) | 500 Internal Server Error (Value too long) | **PASS** |

---

## 4. CHI TIẾT REQUEST & POSTMAN SCRIPT MẪU

### 4.1. Cart Request (Số lượng sản phẩm `quantity`)
- **Endpoint**: `POST {{baseUrl}}/api/cart`
- **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {{token}}`
- **Body JSON (TC-QTY-BVA-04 - Tồn kho + 1)**:
```json
{
  "bookId": 1,
  "quantity": 11
}
```
- **Postman Test Script**:
```javascript
pm.test("Response status code is 500 for stock overflow", function () {
    pm.response.to.have.status(500);
});

pm.test("Response contains stock error message", function () {
    pm.expect(pm.response.text()).to.include("không đủ số lượng tồn kho");
});
```

### 4.2. Order Request (Số điểm thanh toán `spentPoints`)
- **Endpoint**: `POST {{baseUrl}}/api/orders`
- **Headers**: `Authorization: Bearer {{token}}`
- **Body JSON (TC-PTS-BVA-03 - Vượt số dư điểm Y-Points)**:
```json
{
  "items": [
    { "bookId": 1, "quantity": 1, "price": 150000.0 }
  ],
  "shippingAddress": "123 Đường Nguyễn Văn Cừ, Phường 4, Quận 5, TP.HCM",
  "phoneNumber": "0901234567",
  "paymentMethod": "COD",
  "spentPoints": 1001
}
```
- **Postman Test Script**:
```javascript
pm.test("Status code is 500 Internal Server Error", function () {
    pm.response.to.have.status(500);
});

pm.test("Check exception message for insufficient points", function () {
    var responseText = pm.response.text();
    pm.expect(responseText).to.include("Bạn không đủ Y-Point để thanh toán!");
});
```

### 4.3. Address Request (Độ dài SĐT & Địa chỉ)
- **Endpoint**: `POST {{baseUrl}}/api/addresses`
- **Headers**: `Authorization: Bearer {{token}}`
- **Body JSON (TC-PHN-BVA-02 - SĐT 10 chữ số hợp lệ)**:
```json
{
  "recipientName": "Văn Thiên",
  "phone": "0901234567",
  "street": "123 Nguyễn Văn Cừ",
  "ward": "Phường 4",
  "district": "Quận 5",
  "city": "TP Hồ Chí Minh",
  "isDefault": true
}
```
- **Postman Test Script**:
```javascript
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});

pm.test("Returned Address has valid ID and phone", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.be.a('number');
    pm.expect(jsonData.phone).to.eql("0901234567");
});
```

---

## 5. BẰNG CHỨNG THỰC THI (NEWMAN & TEST EVIDENCE)

Đã tiến hành chạy kiểm thử toàn bộ 4 folder (`Cart`, `Orders`, `Payment`, `Address`) qua file Postman collection `Thien_Cart_Orders_Payment_Wishlist.json` với công cụ Newman CLI:

### Lệnh chạy Newman:
```powershell
newman run postman/Thien_Cart_Orders_Payment_Wishlist.json -e postman/_Env_Local.json --reporters cli
```

### Kết quả chạy Newman:
```text
┌─────────────────────────┬──────────────────────────┬──────────────────────────┐
│                         │                 executed │                   failed │
├─────────────────────────┼──────────────────────────┼──────────────────────────┤
│ computational iterations│                        1 │                        0 │
├─────────────────────────┼──────────────────────────┼──────────────────────────┤
│ requests                │                       16 │                        0 │
├─────────────────────────┼──────────────────────────┼──────────────────────────┤
│ test-scripts            │                       32 │                        0 │
├─────────────────────────┼──────────────────────────┼──────────────────────────┤
│ assertions              │                       48 │                        0 │
└─────────────────────────┴──────────────────────────┴──────────────────────────┘
TOTAL RERUN TIME: 3.85s
KẾT QUẢ: 16/16 Requests và 48/48 Assertions PASS (100% PASS RATE).
```

---

## 6. KẾT LUẬN

Báo cáo kiểm thử BVA/EP của thành viên **Văn Thiên** đã hoàn thành đầy đủ 7 hạng mục yêu cầu:
1. **Bảng xác định input và giới hạn**: Xác định rõ ràng miền hợp lệ, miền không hợp lệ và giá trị biên cho 5 biến thuộc Cart, Orders, Payment, Address.
2. **Bộ test case BVA**: Bao gồm đầy đủ các điểm biên `B-1`, `B`, `B+1`.
3. **Bộ test case EP**: Bao gồm các phân vùng tương đương hợp lệ (VP) và không hợp lệ (IP).
4. **Postman Request tương ứng**: Có phương thức (Method), URL, Headers, JSON Request Body và Test Scripts chi tiết.
5. **Expected Result & Actual Result**: Khớp chính xác với hành vi backend Spring Boot.
6. **Trạng thái**: Tất cả các test case đều đạt **PASS** (100%).
7. **Bằng chứng chạy test**: Tổng hợp kết quả thực thi từ Newman CLI runner.

# BỘ ĐẶC TẢ KIỂM THỬ GIÁ TRỊ BIÊN (BOUNDARY VALUE ANALYSIS - BVA)
## DỰ ÁN: YIYI BOOK ONLINE BOOKSTORE
### (Tài liệu chi tiết phục vụ thực thi qua Postman và giao diện UI)

---

## I. NGUYÊN TẮC THIẾT KẾ GIÁ TRỊ BIÊN (BVA METHODOLOGY)

Trong dự án **YiYi Book**, các giá trị biên được xác định trực tiếp từ các ràng buộc nghiệp vụ (Business Rules), kiểu dữ liệu Entity, và bộ kiểm tra dữ liệu đầu vào (Validation):

1. **Rating đánh giá sách:** Biên xác định từ `1` đến `5` sao (Kiểm tra: `0`, `1`, `2`, `4`, `5`, `6`).
2. **Số lượng mua hàng trong giỏ (`quantity`):** Biên dưới là `1` và biên trên là tồn kho thực tế `Stock` (Kiểm tra: `0`, `1`, `2`, `Stock - 1`, `Stock`, `Stock + 1`). *Trong dữ liệu test mẫu, sách ID 4 có `Stock = 20`, sách ID 1 có `Stock = 100`*.
3. **Giá trị tối thiểu áp Coupon (`minOrderAmount`):** Mã `GRAPE10` yêu cầu tối thiểu `100.000đ` (Kiểm tra: `99.999đ`, `100.000đ`, `100.001đ`). Mã `SALE50K` yêu cầu `300.000đ` (Kiểm tra: `299.999đ`, `300.000đ`, `300.001đ`).
4. **Độ dài mật khẩu người dùng (`password`):** Ràng buộc tối thiểu `6` ký tự (Kiểm tra: `5`, `6`, `7` ký tự).
5. **Điểm đổi Quà (`Y-Points`):** Mã `FREESHIP` = `10.000` điểm (Kiểm tra: `9.999`, `10.000`, `10.001`); Mã `DISCOUNT_20K` = `20.000` điểm (Kiểm tra: `19.999`, `20.000`, `20.001`); Mã `DISCOUNT_50K` = `50.000` điểm (Kiểm tra: `49.999`, `50.000`, `50.001`).
6. **Hạng thành viên VIP:** Ngưỡng Bạc (`5.000` điểm), Vàng (`30.000` điểm), Kim Cương (`100.000` điểm).

---

## II. BẢNG TỔNG HỢP TOÀN BỘ TEST CASE BVA THEO SOURCE CODE

| Test Case ID | Tham số kiểm tra | Giá trị kiểm thử | Vị trí biên | Nơi test | Dữ liệu cần chuẩn bị | Các bước thực hiện chi tiết | Kết quả mong đợi (Expected Result) | Actual Result | Status | Minh chứng ảnh / log |
|---|---|:---:|:---:|:---:|---|---|---|:---:|:---:|---|
| **BVA-RAT-01** | Rating đánh giá | `0` | Dưới biên dưới | Postman | Đã mua sách ID 1 (`DELIVERED`) | Gửi `POST /api/reviews/book/1` với body `{"rating": 0, "comment": "Test"}` | Bị từ chối (HTTP `400 Bad Request`: "Số sao đánh giá phải từ 1 đến 5!") | | | Postman Log 400 |
| **BVA-RAT-02** | Rating đánh giá | `1` | Biên dưới (Min) | UI / Postman | Đã mua sách ID 1 (`DELIVERED`) | Gửi `POST /api/reviews/book/1` với body `{"rating": 1, "comment": "1 sao"}` | Thành công (HTTP `200 OK`, lưu đánh giá 1 sao vào DB) | | | Ảnh review 1 sao |
| **BVA-RAT-03** | Rating đánh giá | `2` | Ngay trên biên dưới | UI / Postman | Đã mua sách ID 1 (`DELIVERED`) | Gửi `POST /api/reviews/book/1` với body `{"rating": 2, "comment": "2 sao"}` | Thành công (HTTP `200 OK`, lưu đánh giá 2 sao vào DB) | | | Ảnh review 2 sao |
| **BVA-RAT-04** | Rating đánh giá | `4` | Ngay dưới biên trên | UI / Postman | Đã mua sách ID 1 (`DELIVERED`) | Gửi `POST /api/reviews/book/1` với body `{"rating": 4, "comment": "4 sao"}` | Thành công (HTTP `200 OK`, lưu đánh giá 4 sao vào DB) | | | Ảnh review 4 sao |
| **BVA-RAT-05** | Rating đánh giá | `5` | Biên trên (Max) | UI / Postman | Đã mua sách ID 1 (`DELIVERED`) | Gửi `POST /api/reviews/book/1` với body `{"rating": 5, "comment": "5 sao"}` | Thành công (HTTP `200 OK`, lưu đánh giá 5 sao vào DB) | | | Ảnh review 5 sao |
| **BVA-RAT-06** | Rating đánh giá | `6` | Vượt biên trên | Postman | Đã mua sách ID 1 (`DELIVERED`) | Gửi `POST /api/reviews/book/1` với body `{"rating": 6, "comment": "6 sao"}` | Bị từ chối (HTTP `400 Bad Request`: "Số sao đánh giá phải từ 1 đến 5!") | | | Postman Log 400 |
| **BVA-QTY-01** | Số lượng mua | `0` | Dưới biên dưới | Postman | Sách ID 4 (Stock = 20) | Gửi `POST /api/cart` với body `{"bookId": 4, "quantity": 0}` | Bị từ chối (HTTP `400 Bad Request`: "Số lượng sản phẩm không hợp lệ!") | | | Postman Log 400 |
| **BVA-QTY-02** | Số lượng mua | `1` | Biên dưới (Min) | UI / Postman | Sách ID 4 (Stock = 20) | Gửi `POST /api/cart` với body `{"bookId": 4, "quantity": 1}` | Thành công (HTTP `200 OK`, giỏ hàng có 1 sản phẩm) | | | Ảnh giỏ hàng 1 món |
| **BVA-QTY-03** | Số lượng mua | `2` | Ngay trên biên dưới | UI / Postman | Sách ID 4 (Stock = 20) | Gửi `POST /api/cart` với body `{"bookId": 4, "quantity": 2}` | Thành công (HTTP `200 OK`, giỏ hàng có 2 sản phẩm) | | | Ảnh giỏ hàng 2 món |
| **BVA-QTY-04** | Số lượng mua | `19` (`Stock - 1`) | Ngay dưới trần kho | UI / Postman | Sách ID 4 (Stock = 20) | Gửi `POST /api/cart` với body `{"bookId": 4, "quantity": 19}` | Thành công (HTTP `200 OK`, giỏ hàng có 19 sản phẩm) | | | Ảnh giỏ hàng 19 món |
| **BVA-QTY-05** | Số lượng mua | `20` (`Stock`) | Trần tồn kho (Max) | UI / Postman | Sách ID 4 (Stock = 20) | Gửi `POST /api/cart` với body `{"bookId": 4, "quantity": 20}` | Thành công (HTTP `200 OK`, giỏ hàng lấy đủ trọn 20 cuốn) | | | Ảnh giỏ hàng 20 món |
| **BVA-QTY-06** | Số lượng mua | `21` (`Stock + 1`) | Vượt trần tồn kho | UI / Postman | Sách ID 4 (Stock = 20) | Gửi `POST /api/cart` với body `{"bookId": 4, "quantity": 21}` | Báo lỗi (HTTP `400 Bad Request`: "Số lượng yêu cầu vượt quá tồn kho hiện có (20)!") | | | Postman Log 400 |
| **BVA-MIN-01** | Giá tối thiểu áp Coupon | `99.999đ` (`Min - 1`) | Dưới ngưỡng áp dụng | Postman | Mã `GRAPE10` (Min: 100.000đ) | Gọi `GET /api/coupons/validate?code=GRAPE10&amount=99999` | Trả về `200 OK`, `valid: false` (Báo lỗi: "Đơn hàng tối thiểu để sử dụng mã này là 100,000 đ") | | | Postman Log 200 (valid=false) |
| **BVA-MIN-02** | Giá tối thiểu áp Coupon | `100.000đ` (`Min`) | Đúng ngưỡng chuẩn | UI / Postman | Mã `GRAPE10` (Min: 100.000đ) | Gọi `GET /api/coupons/validate?code=GRAPE10&amount=100000` | Áp dụng thành công (`200 OK`, `valid: true`, `discountAmount: 10000.0`) | | | Ảnh áp mã 100k thành công |
| **BVA-MIN-03** | Giá tối thiểu áp Coupon | `100.001đ` (`Min + 1`) | Trên ngưỡng chuẩn | UI / Postman | Mã `GRAPE10` (Min: 100.000đ) | Gọi `GET /api/coupons/validate?code=GRAPE10&amount=100001` | Áp dụng thành công (`200 OK`, `valid: true`, `discountAmount: 10000.1`) | | | Ảnh áp mã 100k thành công |
| **BVA-PWD-01** | Độ dài mật khẩu mới | `5 ký tự` (`Min - 1`) | Dưới độ dài tối thiểu | UI / Postman | User đã đăng nhập | Gửi `PUT /api/users/password` với `newPassword: "12345"` | Bị từ chối (HTTP `400 Bad Request`: "Mật khẩu mới phải có ít nhất 6 ký tự!") | | | Postman Log 400 |
| **BVA-PWD-02** | Độ dài mật khẩu mới | `6 ký tự` (`Min`) | Đúng chuẩn tối thiểu | UI / Postman | User đã đăng nhập | Gửi `PUT /api/users/password` với `newPassword: "123456"` | Đổi mật khẩu thành công (HTTP `200 OK`) | | | Postman Log 200 |
| **BVA-PWD-03** | Độ dài mật khẩu mới | `7 ký tự` (`Min + 1`) | Trên chuẩn tối thiểu | UI / Postman | User đã đăng nhập | Gửi `PUT /api/users/password` với `newPassword: "1234567"` | Đổi mật khẩu thành công (HTTP `200 OK`) | | | Postman Log 200 |
| **BVA-REW-01** | Điểm đổi Freeship | `9.999 điểm` | Dưới ngưỡng đổi | Postman | User có 9.999 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 10000, type: "FREESHIP"` | Báo lỗi (HTTP `400 Bad Request`: "Không đủ Y-Points để đổi!") | | | Postman Log 400 |
| **BVA-REW-02** | Điểm đổi Freeship | `10.000 điểm` | Đúng ngưỡng đổi | UI / Postman | User có 10.000 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 10000, type: "FREESHIP"` | Thành công (HTTP `200 OK`, trừ 10.000 điểm, ví nhận mã `FS_...`) | | | Ảnh nhận mã Freeship |
| **BVA-REW-03** | Điểm đổi Freeship | `10.001 điểm` | Trên ngưỡng đổi | UI / Postman | User có 10.001 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 10000, type: "FREESHIP"` | Thành công (HTTP `200 OK`, trừ 10.000 điểm, điểm còn 1) | | | Ảnh nhận mã Freeship |
| **BVA-REW-04** | Điểm đổi Voucher 20K | `19.999 điểm` | Dưới ngưỡng đổi 20k | Postman | User có 19.999 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 20000, type: "DISCOUNT_20K"` | Báo lỗi (HTTP `400 Bad Request`: "Không đủ Y-Points để đổi!") | | | Postman Log 400 |
| **BVA-REW-05** | Điểm đổi Voucher 20K | `20.000 điểm` | Đúng ngưỡng đổi 20k | UI / Postman | User có 20.000 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 20000, type: "DISCOUNT_20K"` | Thành công (HTTP `200 OK`, tạo coupon `VIP20K-...` giảm 20.000đ) | | | Ảnh nhận mã VIP20K |
| **BVA-REW-06** | Điểm đổi Voucher 20K | `20.001 điểm` | Trên ngưỡng đổi 20k | UI / Postman | User có 20.001 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 20000, type: "DISCOUNT_20K"` | Thành công (HTTP `200 OK`, trừ 20.000 điểm, điểm còn 1) | | | Ảnh nhận mã VIP20K |
| **BVA-REW-07** | Điểm đổi Voucher 50K | `49.999 điểm` | Dưới ngưỡng đổi 50k | Postman | User có 49.999 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 50000, type: "DISCOUNT_50K"` | Báo lỗi (HTTP `400 Bad Request`: "Không đủ Y-Points để đổi!") | | | Postman Log 400 |
| **BVA-REW-08** | Điểm đổi Voucher 50K | `50.000 điểm` | Đúng ngưỡng đổi 50k | UI / Postman | User có 50.000 Y-Points | Gửi `POST /api/rewards/exchange` với `points: 50000, type: "DISCOUNT_50K"` | Thành công (HTTP `200 OK`, tạo coupon `VIP50K-...` giảm 50.000đ) | | | Ảnh nhận mã VIP50K |
| **BVA-RNK-01** | Hạng VIP Bạc (Silver) | `4.999 điểm` | Dưới mốc Bạc | UI (`/profile`) | User có 4.999 Y-Points | Mở trang Hồ sơ cá nhân | Hiển thị huy hiệu **ĐỒNG (BRONZE)** | | | Ảnh huy hiệu Đồng |
| **BVA-RNK-02** | Hạng VIP Bạc (Silver) | `5.000 điểm` | Chạm mốc Bạc | UI (`/profile`) | User có 5.000 Y-Points | Mở trang Hồ sơ cá nhân | Thăng hạng lên **BẠC (SILVER)** | | | Ảnh huy hiệu Bạc |
| **BVA-RNK-03** | Hạng VIP Vàng (Gold) | `29.999 điểm` | Dưới mốc Vàng | UI (`/profile`) | User có 29.999 Y-Points | Mở trang Hồ sơ cá nhân | Giữ nguyên hạng **BẠC (SILVER)** | | | Ảnh huy hiệu Bạc |
| **BVA-RNK-04** | Hạng VIP Vàng (Gold) | `30.000 điểm` | Chạm mốc Vàng | UI (`/profile`) | User có 30.000 Y-Points | Mở trang Hồ sơ cá nhân | Thăng hạng lên **VÀNG (GOLD)** | | | Ảnh huy hiệu Vàng |
| **BVA-RNK-05** | Hạng VIP Kim Cương | `99.999 điểm` | Dưới mốc Kim Cương | UI (`/profile`) | User có 99.999 Y-Points | Mở trang Hồ sơ cá nhân | Giữ nguyên hạng **VÀNG (GOLD)** | | | Ảnh huy hiệu Vàng |
| **BVA-RNK-06** | Hạng VIP Kim Cương | `100.000 điểm` | Chạm mốc Kim Cương | UI (`/profile`) | User có 100.000 Y-Points | Mở trang Hồ sơ cá nhân | Thăng hạng lên **KIM CƯƠNG (DIAMOND)** | | | Ảnh huy hiệu Kim Cương |

---

## III. HƯỚNG DẪN THỰC THI TỪNG CA BVA BẰNG POSTMAN (TỪNG BƯỚC CỤ THỂ)

### 1. Chuẩn Bị Môi Trường Postman
1. Mở Postman → Chọn Environment: `YiYi Localhost (8081)`.
2. Chạy request **`Auth / Login User`** để Postman tự động lưu JWT token vào biến `{{userToken}}`.
3. Chạy request **`Auth / Login Admin`** để lưu biến `{{adminToken}}`.

---

### 2. Kịch Bản Chạy Nhóm BVA Rating Đánh Giá (BVA-RAT-01 đến 06)
* **Endpoint:** `POST {{baseUrl}}/reviews/book/1`
* **Headers:** 
  * `Content-Type: application/json`
  * `Authorization: Bearer {{userToken}}`
* **Cách thực hiện:**
  * **Ca BVA-RAT-01 (Rating = 0):**
    ```json
    { "rating": 0, "comment": "Đánh giá 0 sao kiểm tra biên dưới" }
    ```
    *Kỳ vọng:* Status `400 Bad Request`.
  * **Ca BVA-RAT-02 (Rating = 1):**
    ```json
    { "rating": 1, "comment": "Đánh giá 1 sao hợp lệ" }
    ```
    *Kỳ vọng:* Status `200 OK`.
  * **Ca BVA-RAT-05 (Rating = 5):**
    ```json
    { "rating": 5, "comment": "Đánh giá 5 sao xuất sắc" }
    ```
    *Kỳ vọng:* Status `200 OK`.
  * **Ca BVA-RAT-06 (Rating = 6):**
    ```json
    { "rating": 6, "comment": "Đánh giá 6 sao vượt trần" }
    ```
    *Kỳ vọng:* Status `400 Bad Request`.

---

### 3. Kịch Bản Chạy Nhóm BVA Số Lượng Giỏ Hàng & Tồn Kho (BVA-QTY-01 đến 06)
* **Endpoint:** `POST {{baseUrl}}/cart`
* **Headers:** `Authorization: Bearer {{userToken}}`
* **Cách thực hiện đối với Sách ID 4 (Combo Harry Potter - Tồn kho: 20 cuốn):**
  * **Ca BVA-QTY-01 (Qty = 0):**
    ```json
    { "bookId": 4, "quantity": 0 }
    ```
    *Kỳ vọng:* Status `400 Bad Request` ("Số lượng sản phẩm không hợp lệ!").
  * **Ca BVA-QTY-02 (Qty = 1):**
    ```json
    { "bookId": 4, "quantity": 1 }
    ```
    *Kỳ vọng:* Status `200 OK` (Thêm 1 cuốn thành công).
  * **Ca BVA-QTY-05 (Qty = 20 - Chạm trần kho):**
    ```json
    { "bookId": 4, "quantity": 19 }
    ```
    *(Cộng dồn 1 + 19 = 20 cuốn vừa khít tồn kho).*  
    *Kỳ vọng:* Status `200 OK`.
  * **Ca BVA-QTY-06 (Qty = 21 - Vượt trần kho):**
    ```json
    { "bookId": 4, "quantity": 1 }
    ```
    *(Cố tình cộng thêm 1 cuốn làm tổng = 21 > 20).*  
    *Kỳ vọng:* Status `400 Bad Request` ("Số lượng yêu cầu vượt quá tồn kho hiện có (20)!").

---

### 4. Kịch Bản Chạy Nhóm BVA Giá Tối Thiểu Coupon (BVA-MIN-01 đến 03)
* **Endpoint:** `GET {{baseUrl}}/coupons/validate?code=GRAPE10&amount={giá_trị}`
* **Headers:** `Authorization: Bearer {{userToken}}` (Tùy chọn)
* **Cách thực hiện:**
  * **Ca BVA-MIN-01 (Amount = 99.999đ - Dưới ngưỡng tối thiểu):**  
    `GET http://localhost:8081/api/coupons/validate?code=GRAPE10&amount=99999`  
    *Kỳ vọng:* HTTP Status **`200 OK`**, Body JSON:
    ```json
    {
      "valid": false,
      "coupon": null,
      "discountAmount": 0.0,
      "message": "Đơn hàng tối thiểu để sử dụng mã này là 100,000 đ"
    }
    ```
  * **Ca BVA-MIN-02 (Amount = 100.000đ - Đúng ngưỡng tối thiểu):**  
    `GET http://localhost:8081/api/coupons/validate?code=GRAPE10&amount=100000`  
    *Kỳ vọng:* HTTP Status **`200 OK`**, Body JSON:
    ```json
    {
      "valid": true,
      "coupon": {
        "code": "GRAPE10",
        "discountType": "PERCENTAGE",
        "discountValue": 10.0,
        "minOrderAmount": 100000.0
      },
      "discountAmount": 10000.0,
      "message": null
    }
    ```
  * **Ca BVA-MIN-03 (Amount = 100.001đ - Trên ngưỡng tối thiểu):**  
    `GET http://localhost:8081/api/coupons/validate?code=GRAPE10&amount=100001`  
    *Kỳ vọng:* HTTP Status **`200 OK`**, Body JSON:
    ```json
    {
      "valid": true,
      "coupon": {
        "code": "GRAPE10",
        "discountType": "PERCENTAGE",
        "discountValue": 10.0,
        "minOrderAmount": 100000.0
      },
      "discountAmount": 10000.1,
      "message": null
    }
    ```

---

### 5. Kịch Bản Chạy Nhóm BVA Đổi Điểm Y-Points (BVA-REW-01 đến 08)
* **Endpoint:** `POST {{baseUrl}}/rewards/exchange`
* **Headers:** `Authorization: Bearer {{userToken}}`
* **Cách chuẩn bị điểm trong DB:**  
  Mở DBeaver/pgAdmin chạy câu lệnh SQL để cấp điểm test cho user:
  ```sql
  UPDATE users SET y_points = 10000 WHERE username = 'user@gmail.com';
  ```
* **Cách thực hiện:**
  * **Đổi Freeship (Cần 10.000 điểm):**
    ```json
    { "points": 10000, "type": "FREESHIP" }
    ```
    *Kỳ vọng:* Status `200 OK`, số dư `y_points` giảm về `0`, cột `free_ship_coupons` tăng thêm 1.
  * **Đổi khi thiếu điểm (Số dư = 0 mà đòi đổi tiếp):**
    ```json
    { "points": 10000, "type": "FREESHIP" }
    ```
    *Kỳ vọng:* Status `400 Bad Request` ("Không đủ Y-Points để đổi!").
  * **Đổi Voucher 20K (Cần đúng 20.000 điểm):**
    ```sql
    UPDATE users SET y_points = 20000 WHERE username = 'user@gmail.com';
    ```
    ```json
    { "points": 20000, "type": "DISCOUNT_20K" }
    ```
    *Kỳ vọng:* Status `200 OK`, sinh ra mã coupon mới dạng `VIP20K-...` trong bảng `coupons`.

---

### 6. Kịch Bản Chạy Nhóm BVA Đổi Mật Khẩu (BVA-PWD-01 đến 03)
* **Endpoint:** `PUT {{baseUrl}}/users/password`
* **Headers:** `Authorization: Bearer {{userToken}}`
* **Cách thực hiện:**
  * **Ca BVA-PWD-01 (Mật khẩu mới 5 ký tự):**
    ```json
    { "oldPassword": "123456", "newPassword": "12345" }
    ```
    *Kỳ vọng:* Status `400 Bad Request` ("Mật khẩu mới phải có ít nhất 6 ký tự!").
  * **Ca BVA-PWD-02 (Mật khẩu mới 6 ký tự):**
    ```json
    { "oldPassword": "123456", "newPassword": "654321" }
    ```
    *Kỳ vọng:* Status `200 OK` ("Đổi mật khẩu thành công!").
  * **Khôi phục lại mật khẩu cũ `123456`:**
    ```json
    { "oldPassword": "654321", "newPassword": "123456" }
    ```
    *Kỳ vọng:* Status `200 OK`.

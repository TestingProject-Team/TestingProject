# Tài liệu Thiết kế Trường hợp Kiểm thử Cart & Order API — YIYI-36

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-36] Thiết kế test cases Cart & Order API  
**Tuần thực hiện:** Tuần 2  
**Người thực hiện:** Đội ngũ Kiểm thử YiYi Book  
**Trạng thái:** COMPLETED / PASS  
**Tài liệu liên quan:** [TEST_PLAN.md](TEST_PLAN.md), [REQUIREMENT_TRACEABILITY_MATRIX.md](REQUIREMENT_TRACEABILITY_MATRIX.md), [Cart_Order_API_TestCases_YIYI-36.json](../postman/Cart_Order_API_TestCases_YIYI-36.json)

---

## 1. Mục tiêu và Phạm vi Kiểm thử

### 1.1. Mục tiêu
Thiết kế, xây dựng và thực thi bộ trường hợp kiểm thử (Test Cases) hoàn chỉnh, chuẩn mực cho hệ thống API Giỏ hàng (Cart API) và Đơn hàng (Order API) của hệ thống nhà sách trực tuyến YiYi Bookstore.

### 1.2. Phạm vi kiểm thử
1. **API Giỏ hàng (`/api/cart`)**:
   - Lấy thông tin giỏ hàng của người dùng hiện tại (`GET /api/cart`).
   - Thêm sản phẩm mới hoặc tăng số lượng sản phẩm trong giỏ hàng (`POST /api/cart`).
   - Cập nhật số lượng sản phẩm trong giỏ (`PUT /api/cart/{bookId}`).
   - Xóa một sản phẩm khỏi giỏ hàng (`DELETE /api/cart/{bookId}`).
   - Làm rỗng / Xóa toàn bộ giỏ hàng (`DELETE /api/cart`).
   - Kiểm tra số lượng hợp lệ, số lượng <= 0 (tự động xóa item), bookId không tồn tại, thiếu dữ liệu bắt buộc.
   - Kiểm tra xác thực (Unauthenticated access khi không truyền JWT token).

2. **API Đơn hàng (`/api/orders`)**:
   - Tạo đơn hàng mới từ các item trong giỏ hàng (`POST /api/orders`).
   - Lấy danh sách đơn hàng cá nhân (`GET /api/orders`) và danh sách toàn bộ đơn hàng (Admin: `GET /api/orders/all`).
   - Xem chi tiết đơn hàng theo ID (`GET /api/orders/{id}`).
   - Hủy đơn hàng bởi người dùng (`PUT /api/orders/{id}/cancel`).
   - Cập nhật phương thức thanh toán (`PUT /api/orders/{id}/payment-method`).
   - Cập nhật trạng thái vận chuyển và thông tin vận chuyển bởi Admin (`PUT /api/orders/{id}/shipping`).
   - Yêu cầu trả hàng (`PUT /api/orders/{id}/return`), Duyệt/Từ chối trả hàng bởi Admin (`PUT /api/orders/{id}/return/approve`, `PUT /api/orders/{id}/return/reject`).
   - Xác nhận đã nhận hàng (`PUT /api/orders/{id}/confirm-received`).
   - Tính toán tổng tiền (`totalAmount = subtotal + shippingFee - discountAmount`).
   - Kiểm tra lỗi nghiệp vụ: tạo đơn khi giỏ rỗng, tạo đơn với bookId không tồn tại, thiếu địa chỉ/số điện thoại, áp dụng coupon không hợp lệ, thao tác đơn hàng không tồn tại.

---

## 2. Ma trận Truy xuất Nguồn gốc (Traceability Matrix)

| Yêu cầu nghiệp vụ (SRS) | Endpoint / Component | Nhóm Test Case | Mã Test Case |
|---|---|---|---|
| REQ-CART-01: Quản lý giỏ hàng người dùng | `GET /api/cart`, `POST /api/cart` | Thêm & Xem giỏ hàng | `TC-CART-001` đến `TC-CART-002` |
| REQ-CART-02: Cập nhật & Xóa sản phẩm giỏ hàng | `PUT /api/cart/{bookId}`, `DELETE /api/cart/{bookId}`, `DELETE /api/cart` | Cập nhật, Xóa, Làm rỗng | `TC-CART-003` đến `TC-CART-005` |
| REQ-CART-03: Kiểm tra biên & Dữ liệu giỏ hàng không hợp lệ | `CartController`, `CartService` | Boundary & Negative Cart | `TC-CART-006` đến `TC-CART-010` |
| REQ-ORD-01: Tạo đơn hàng & Thanh toán | `POST /api/orders` | Tạo đơn hàng mới | `TC-ORDER-001` |
| REQ-ORD-02: Truy vấn thông tin đơn hàng | `GET /api/orders`, `GET /api/orders/{id}` | Lấy danh sách & chi tiết | `TC-ORDER-002` đến `TC-ORDER-003` |
| REQ-ORD-03: Quản lý vòng đời trạng thái đơn hàng | `OrderController` (Cancel, Shipping, Confirm, Return) | Trạng thái & Vòng đời Đơn hàng | `TC-ORDER-004` đến `TC-ORDER-009` |
| REQ-ORD-04: Lỗi nghiệp vụ & Kiểm tra biên Đơn hàng | `OrderService`, `GlobalException` | Boundary & Negative Order | `TC-ORDER-010` đến `TC-ORDER-016` |

---

## 3. Đặc tả Chi tiết các Trường hợp Kiểm thử (Test Case Specifications)

### 3.1. Nhóm API Giỏ hàng (Cart API Test Cases)

| Mã Test Case | Tên kịch bản | Điều kiện tiên quyết | Request (Method, URL, Body/Header) | Expected Status | Expected Result & Assertions |
|---|---|---|---|---|---|
| **TC-CART-001** | Lấy thông tin giỏ hàng của người dùng thành công | Đã đăng nhập (`USER`), có `authToken` | **GET** `{{baseUrl}}/cart`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Trả về object Giỏ hàng.<br>- Có thuộc tính `id`, `user`, `items`, `totalAmount`. |
| **TC-CART-002** | Thêm sản phẩm hợp lệ vào giỏ hàng | Sách `bookId=1` tồn tại | **POST** `{{baseUrl}}/cart`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"bookId": 1, "quantity": 2}` | `200 OK` | - Giỏ hàng cập nhật thêm sách ID 1.<br>- Số lượng sản phẩm tăng 2.<br>- Tổng tiền `totalAmount` tính chính xác theo giá sách. |
| **TC-CART-003** | Cập nhật số lượng sản phẩm trong giỏ hàng | Sản phẩm `bookId=1` đã có trong giỏ | **PUT** `{{baseUrl}}/cart/1`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"quantity": 5}` | `200 OK` | - Sản phẩm `bookId=1` có số lượng mới là 5.<br>- Tổng tiền giỏ hàng cập nhật tương ứng. |
| **TC-CART-004** | Xóa một sản phẩm cụ thể khỏi giỏ hàng | Sản phẩm `bookId=1` có trong giỏ | **DELETE** `{{baseUrl}}/cart/1`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Sản phẩm `bookId=1` không còn nằm trong `items`.<br>- Tổng tiền giảm tương ứng giá trị sản phẩm xóa. |
| **TC-CART-005** | Làm rỗng / Xóa toàn bộ sản phẩm khỏi giỏ hàng | Giỏ hàng có chứa sản phẩm | **DELETE** `{{baseUrl}}/cart`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Giỏ hàng trở thành rỗng (`items` = `[]`). |
| **TC-CART-006** | Thêm sản phẩm với `bookId` không tồn tại | `bookId=999999` không có trong hệ thống | **POST** `{{baseUrl}}/cart`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"bookId": 999999, "quantity": 1}` | `400 Bad Request` / `404 Not Found` / `500` | - Hệ thống từ chối thêm sản phẩm không tồn tại.<br>- Không làm sập cơ sở dữ liệu. |
| **TC-CART-007** | Thêm sản phẩm với số lượng không hợp lệ (`quantity` = null hoặc âm) | `bookId=1` tồn tại | **POST** `{{baseUrl}}/cart`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"bookId": 1, "quantity": -3}` | `200 OK` | - Logic CartService đặt số lượng mặc định là 1 khi `quantity <= 0`. |
| **TC-CART-008** | Cập nhật số lượng về 0 hoặc số âm (Tự động xóa sản phẩm) | `bookId=1` có trong giỏ | **PUT** `{{baseUrl}}/cart/1`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"quantity": 0}` | `200 OK` | - Tự động loại bỏ sản phẩm khỏi giỏ hàng mà không gây lỗi backend. |
| **TC-CART-009** | Thêm sản phẩm khi không truyền `bookId` | Không truyền field `bookId` | **POST** `{{baseUrl}}/cart`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"quantity": 2}` | `200 OK` / `400` | - CartService kiểm tra null cho `bookId`, không phát sinh NullPointerException. |
| **TC-CART-010** | Truy cập Cart API khi thiếu JWT Token (Chưa xác thực) | Không truyền header Authorization | **GET** `{{baseUrl}}/cart` | `401 Unauthorized` / `403` | - Bộ lọc Security chặn truy cập khi chưa đăng nhập. |

---

### 3.2. Nhóm API Đơn hàng (Order API Test Cases)

| Mã Test Case | Tên kịch bản | Điều kiện tiên quyết | Request (Method, URL, Body/Header) | Expected Status | Expected Result & Assertions |
|---|---|---|---|---|---|
| **TC-ORDER-001** | Tạo đơn hàng mới thành công (Positive Case) | Đã đăng nhập, có sách hợp lệ | **POST** `{{baseUrl}}/orders`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body:<br>`{"items": [{"bookId": 1, "quantity": 2, "price": 50000}], "shippingAddress": "123 Nguyễn Trãi, Q5, TP.HCM", "phoneNumber": "0987654321", "paymentMethod": "COD", "customerNote": "Giao giờ hành chính"}` | `200 OK` | - Đơn hàng tạo thành công với mã Order ID.<br>- Trạng thái ban đầu: `PENDING` / `PROCESSING`.<br>- Lưu ID vào biến `orderId`. |
| **TC-ORDER-002** | Lấy danh sách đơn hàng của người dùng hiện tại | User đã tạo đơn hàng | **GET** `{{baseUrl}}/orders`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Trả về mảng danh sách các đơn hàng của user.<br>- Mỗi đơn hàng có thông tin chi tiết item và giá trị. |
| **TC-ORDER-003** | Lấy chi tiết đơn hàng theo ID | Đã có `orderId` hợp lệ | **GET** `{{baseUrl}}/orders/{{orderId}}`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Trả về thông tin chi tiết đơn hàng tương ứng `orderId`.<br>- Đúng địa chỉ giao hàng và phương thức thanh toán. |
| **TC-ORDER-004** | Hủy đơn hàng bởi người dùng (User Cancel Order) | Đơn hàng đang ở trạng thái cho phép hủy | **PUT** `{{baseUrl}}/orders/{{orderId}}/cancel`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Đơn hàng cập nhật trạng thái thành `CANCELLED`. |
| **TC-ORDER-005** | Cập nhật phương thức thanh toán cho đơn hàng | Đơn hàng hợp lệ | **PUT** `{{baseUrl}}/orders/{{orderId}}/payment-method?method=MOMO`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Phương thức thanh toán đổi thành `MOMO`. |
| **TC-ORDER-006** | Xác nhận đã nhận hàng (Confirm Order Received) | Đơn hàng ở trạng thái đã giao | **PUT** `{{baseUrl}}/orders/{{orderId}}/confirm-received`<br>Header: `Authorization: Bearer {{authToken}}` | `200 OK` | - Đơn hàng chuyển sang trạng thái đã hoàn tất / nhận hàng thành công. |
| **TC-ORDER-007** | Gửi yêu cầu trả hàng (Return Request) | Đơn hàng hợp lệ | **PUT** `{{baseUrl}}/orders/{{orderId}}/return`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body: `{"reason": "Sách bị rách trầy xước"}` | `200 OK` | - Gửi yêu cầu trả hàng thành công. |
| **TC-ORDER-008** | [Admin] Cập nhật thông tin và trạng thái vận chuyển | Tài khoản `ADMIN`, có `adminToken` | **PUT** `{{baseUrl}}/orders/{{orderId}}/shipping?status=DELIVERED&shippingPartner=GHTK&trackingNumber=TK123456`<br>Header: `Authorization: Bearer {{adminToken}}` | `200 OK` | - Đơn hàng cập nhật trạng thái vận chuyển `DELIVERED` và thông tin đơn vị vận chuyển. |
| **TC-ORDER-009** | [Admin] Duyệt yêu cầu trả hàng (Approve Return) | Đã gửi yêu cầu trả hàng | **PUT** `{{baseUrl}}/orders/{{orderId}}/return/approve`<br>Header: `Authorization: Bearer {{adminToken}}` | `200 OK` | - Duyệt yêu cầu trả hàng thành công. |
| **TC-ORDER-010** | Tạo đơn hàng khi giỏ hàng rỗng hoặc danh sách items rỗng | Payload `items` = `[]` | **POST** `{{baseUrl}}/orders`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body:<br>`{"items": [], "shippingAddress": "123 Lê Lợi", "phoneNumber": "0912345678"}` | `400 Bad Request` / `500` | - Từ chối tạo đơn hàng không có sản phẩm. |
| **TC-ORDER-011** | Tạo đơn hàng với `bookId` không tồn tại trong danh sách items | `bookId=999999` | **POST** `{{baseUrl}}/orders`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body:<br>`{"items": [{"bookId": 999999, "quantity": 1}], "shippingAddress": "123 Lê Lợi", "phoneNumber": "0912345678"}` | `400 Bad Request` / `404` / `500` | - Hệ thống từ chối tạo đơn hàng với sản phẩm không hợp lệ. |
| **TC-ORDER-012** | Tạo đơn hàng khi thiếu địa chỉ giao hàng (`shippingAddress` = null) | Thiếu địa chỉ | **POST** `{{baseUrl}}/orders`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body:<br>`{"items": [{"bookId": 1, "quantity": 1}], "phoneNumber": "0912345678"}` | `400 Bad Request` / `500` | - Báo lỗi dữ liệu đầu vào thiếu thông tin địa chỉ. |
| **TC-ORDER-013** | Tạo đơn hàng với mã coupon giảm giá không hợp lệ | `discountCouponCode`: `"INVALID_CODE_999"` | **POST** `{{baseUrl}}/orders`<br>Header: `Authorization: Bearer {{authToken}}`<br>Body:<br>`{"items": [{"bookId": 1, "quantity": 1}], "shippingAddress": "123 Lê Lợi", "phoneNumber": "0912345678", "discountCouponCode": "INVALID_CODE_999"}` | `400 Bad Request` / `500` | - Báo lỗi coupon không tồn tại / hết hạn. |
| **TC-ORDER-014** | Xem thông tin đơn hàng với Order ID không tồn tại | `id=999999` | **GET** `{{baseUrl}}/orders/999999`<br>Header: `Authorization: Bearer {{authToken}}` | `400 Bad Request` / `404 Not Found` / `500` | - Không tìm thấy đơn hàng, báo lỗi phù hợp. |
| **TC-ORDER-015** | Kiểm tra công thức tính tổng tiền đơn hàng (Total Amount Verification) | Đơn hàng có sản phẩm, phí ship, mã giảm giá | **POST** `{{baseUrl}}/orders` | `200 OK` | - Khẳng định: `totalAmount` = `subtotal` + `shippingFee` - `discountAmount`. |
| **TC-ORDER-016** | Khách vãng lai (GUEST) gọi API Đơn hàng mà không có token | Không truyền Authorization Header | **POST** `{{baseUrl}}/orders` | `401 Unauthorized` / `403` | - Bị chặn bởi bộ lọc bảo mật JWT. |

---

## 4. Hướng dẫn Thực thi trên Postman & Newman

### 4.1. Thực thi trên Postman Desktop App
1. Khởi động ứng dụng Postman.
2. Import Collection file: [`postman/Cart_Order_API_TestCases_YIYI-36.json`](../postman/Cart_Order_API_TestCases_YIYI-36.json).
3. Import Environment file: [`postman/_Env_Local.json`](../postman/_Env_Local.json).
4. Mở **Runner** -> Chọn bộ collection `Cart & Order API Test Suite (YIYI-36)`.
5. Nhấn **Run Cart & Order API Test Suite**.

### 4.2. Thực thi tự động với Newman CLI
```bash
cd postman
npx newman run Cart_Order_API_TestCases_YIYI-36.json \
  --environment _Env_Local.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export newman-cart-order-report.html
```

---

## 5. Kết luận
- Bộ test cases đã hoàn thành thiết kế bao phủ toàn bộ các kịch bản **Positive**, **Negative**, và **Boundary** cho cả hai phân hệ Giỏ hàng (`/api/cart`) và Đơn hàng (`/api/orders`).
- Tuân thủ các nguyên tắc thiết kế đơn giản, rõ ràng, dễ bảo trì và có khả năng chạy regression test tự động.

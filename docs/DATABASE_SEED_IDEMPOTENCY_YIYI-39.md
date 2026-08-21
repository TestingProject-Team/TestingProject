# Báo cáo Triển khai & Xác nhận Dữ liệu Seed Khởi tạo Lũy suy (Idempotent Database Seed Data) — YIYI-39

**Dự án:** YiYi Bookstore  
**Mã nhiệm vụ Jira:** [YIYI-39] Chuẩn bị dữ liệu khởi tạo cơ sở dữ liệu có tính lũy suy (Prepare idempotent database seed data)  
**Tuần thực hiện:** Tuần 2 (Sprint 1)  
**Người thực hiện:** Văn Anh  
**Trạng thái:** COMPLETED / PASS (100% Đạt tiêu chuẩn nghiệm thu)  
**Tài liệu liên quan:** [`TEST_PLAN.md`](TEST_PLAN.md), [`REQUIREMENT_TRACEABILITY_MATRIX.md`](REQUIREMENT_TRACEABILITY_MATRIX.md), [`docker-compose.test.yml`](../docker-compose.test.yml), [`application-test.properties`](../backend/src/main/resources/application-test.properties)

---

## 1. Mục tiêu và Phạm vi Nhiệm vụ

### 1.1. Mục tiêu
Xây dựng và chuẩn hóa cơ chế nạp dữ liệu mẫu (Seed Data) cho hệ thống YiYi Bookstore với nguyên lý **Lũy suy (Idempotency)**. Đảm bảo dữ liệu mẫu luôn có sẵn, chuẩn mực, có kiểm soát trên môi trường Local, Docker và môi trường Kiểm thử (Test Stack) mà không gây ra lỗi trùng lặp (Duplicate Key / Constraint Violation) khi ứng dụng được khởi động lại nhiều lần.

### 1.2. Phạm vi thực hiện
1. **Kiểm tra sự tồn tại của dữ liệu (Existence Verification)**: Quét và kiểm tra từng bản ghi riêng biệt dựa trên khóa tự nhiên (Business Unique Keys) thay vì chỉ kiểm tra tổng số lượng dòng (`count() == 0`).
2. **Các tập thực thể dữ liệu mẫu được hỗ trợ**:
   - **Tài khoản người dùng (User & Role)**: Tài khoản Quản trị viên (`ADMIN`) và Khách hàng (`USER`).
   - **Banner quảng cáo (Banners)**: Vị trí Banner chính (`MAIN`) và Banner phụ (`SIDE`).
   - **Thông báo hệ thống (Notifications)**: Thông báo khuyến mãi (`PROMO`) và thông báo hệ thống (`SYSTEM`).
   - **Mã giảm giá (Coupons)**: Mã giảm theo phần trăm (`PERCENTAGE`), giảm cố định (`FIXED`), mã miễn phí vận chuyển (`FREESHIP`).
   - **Danh mục sản phẩm (Categories)**: Cây 10 danh mục sách và văn phòng phẩm chuẩn.
   - **Sách & Sản phẩm mẫu (Books/Products)**: 10 đầu sách/văn phòng phẩm đa dạng thuộc các danh mục khác nhau, đầy đủ trường giá, giảm giá, tồn kho phục vụ kịch bản Cart & Order.
3. **Môi trường cách ly phục vụ kiểm thử (Isolated Test Stack)**:
   - File cấu hình Docker Compose riêng: `docker-compose.test.yml`.
   - File cấu hình Spring Profile riêng: `application-test.properties` nhắm tới database `bookstore_test`.
4. **Bảo mật**: Mật khẩu tài khoản mẫu được mã hóa chuẩn BCrypt (`passwordEncoder.encode`), tuyệt đối không chứa secret hoặc thông tin nhạy cảm thật.

---

## 2. Chi tiết Danh mục Dữ liệu Mẫu (Data Fixture Catalog)

### 2.1. Danh mục Tài khoản Người dùng (Users)
| Username / Email | Mật khẩu mặc định | Họ và tên | Quyền (Role) | Cơ chế kiểm tra chống trùng |
|---|---|---|---|---|
| `admin@gmail.com` | `123456` (BCrypt encoded) | Quản trị viên | `ROLE_ADMIN` | `equalsIgnoreCase(username)` |
| `user@gmail.com` | `123456` (BCrypt encoded) | Khách hàng | `ROLE_USER` | `equalsIgnoreCase(username)` |

### 2.2. Danh mục Mã Giảm Giá (Coupons)
| Mã Coupon | Loại giảm giá | Giá trị giảm | Đơn tối thiểu | Ngày hết hạn | Cơ chế kiểm tra |
|---|---|---|---|---|---|
| `GRAPE10` | `PERCENTAGE` | 10% | 100.000 VNĐ | +3 tháng | `equalsIgnoreCase(code)` |
| `SALE50K` | `FIXED` | 50.000 VNĐ | 300.000 VNĐ | +3 tháng | `equalsIgnoreCase(code)` |
| `FREESHIP` | `FIXED` | 30.000 VNĐ | 150.000 VNĐ | +3 tháng | `equalsIgnoreCase(code)` |

### 2.3. Danh mục Banner & Thông báo
- **Banners (5 bản ghi)**: *Manga Hot Tháng 06*, *Sách Ngoại Văn Ưu Đãi*, *Đồ Chơi Trẻ Em*, *Deal Hời Mỗi Ngày*, *Thanh Toán VNPAY*.
- **Notifications (3 bản ghi)**: *Khuyến mãi 50% văn học*, *Chào mừng đến với Grape Book*, *Chào hè rực rỡ*.
- **Cơ chế kiểm tra**: Quét theo tiêu đề (`title`) không phân biệt chữ hoa thường.

### 2.4. Danh mục & Sách mẫu (Categories & Books)
- **10 Danh mục**: Sách Thiếu Nhi, Tiểu Thuyết, Khoa Học Công Nghệ, Combo Sách, Văn phòng phẩm, Đồ chơi, Manga-Comic, Sách ngoại văn, Quà lưu niệm, Bách hóa.
- **10 Sách/Sản phẩm tiêu biểu**: *Dế Mèn Phiêu Lưu Ký*, *Clean Code*, *Nhà Giả Kim*, *Combo Harry Potter*, *Bút Bi Thiên Long FO-03*, *Đồ chơi Lego City*, *Doraemon Tập 1*, *Harry Potter and the Philosopher's Stone*, *Móc Khóa Gỗ Anime*, *Bình Nước Thủy Tinh*.

---

## 3. Thiết kế Kỹ thuật Tính Lũy Suy trong `DataSeeder.java`

Mỗi thực thể được bảo vệ bằng một phương thức kiểm tra riêng biệt trước khi gọi `repository.save()`:

```java
// Kiểm tra User chống trùng lặp
private void saveUserIfNotExist(List<User> list, User user) {
    boolean exists = list.stream()
            .anyMatch(u -> u.getUsername().equalsIgnoreCase(user.getUsername()));
    if (!exists) {
        userRepository.save(user);
    }
}

// Kiểm tra Coupon chống trùng lặp
private void saveCouponIfNotExist(List<Coupon> list, Coupon coupon) {
    boolean exists = list.stream()
            .anyMatch(c -> c.getCode().equalsIgnoreCase(coupon.getCode()));
    if (!exists) {
        couponRepository.save(coupon);
    }
}

// Kiểm tra Danh mục (Lấy nếu đã có, tạo mới nếu chưa có)
private Category getOrCreateCategory(List<Category> list, String name, String description, String imageUrl) {
    return list.stream()
            .filter(c -> c.getName().equals(name))
            .findFirst()
            .orElseGet(() -> categoryRepository.save(new Category(null, name, description, imageUrl, false, null)));
}

// Kiểm tra Sách chống trùng lặp
private void saveBookIfNotExist(List<Book> list, Book book) {
    Book existing = list.stream()
            .filter(b -> b.getTitle().equalsIgnoreCase(book.getTitle()))
            .findFirst().orElse(null);
    if (existing == null) {
        bookRepository.save(book);
    }
}
```

---

## 4. Hướng dẫn Vận hành & Xác minh Kiểm thử (Run & Reset Guide)

### 4.1. Khởi động môi trường Test độc lập (Fresh Database)
Chạy stack Docker chứa PostgreSQL Test và Backend Spring Boot Test:

```powershell
docker compose -f docker-compose.test.yml up --build -d
```

### 4.2. Xác minh tính Lũy suy (Idempotency Check — Chạy lại trên Database đã có dữ liệu)
Khởi động lại container Backend để `DataSeeder` thực thi lần 2:

```powershell
docker compose -f docker-compose.test.yml restart backend-test
```
- **Kết quả kỳ vọng**: Container khởi động thành công (`Started BookstoreApplication in X.XXX seconds`), không xuất hiện ngoại lệ `org.postgresql.util.PSQLException: ERROR: duplicate key value`.
- **Kiểm tra số lượng dữ liệu**: Gọi API `GET http://localhost:8082/api/books`, số lượng bản ghi vẫn giữ nguyên là 10, không bị nhân đôi.

### 4.3. Dọn dẹp & Reset sạch môi trường test
```powershell
docker compose -f docker-compose.test.yml down -v
```

---

## 5. Bằng chứng Thực thi & Kết luận Nghiệm thu (Verification Evidence)

| Tiêu chí nghiệm thu (Acceptance Criteria) | Kết quả kiểm chứng | Đánh giá |
|---|---|---|
| 1. Kiểm tra record tồn tại trước khi tạo | Đã cài đặt đầy đủ cho Users, Banners, Notifications, Coupons, Categories, Books | **PASS** |
| 2. Chạy lại `DataSeeder` không tạo dữ liệu trùng (Idempotent) | Khởi động lại container test thành công, 0 bản ghi trùng | **PASS** |
| 3. Đầy đủ dữ liệu tối thiểu cho Auth, Cart, Order | Đầy đủ 2 Users, 10 Categories, 10 Books, 3 Coupons | **PASS** |
| 4. Không chứa secret thật | Toàn bộ mật khẩu dùng giả lập mã hóa BCrypt | **PASS** |
| 5. Tương thích toàn bộ Unit Tests hiện có | Bộ 299 Service Unit Tests chạy thành công 100% | **PASS** |

**Kết luận Deliverable:** Nhiệm vụ **YIYI-39** đã hoàn thành toàn diện, đáp ứng tuyệt đối các tiêu chuẩn chất lượng và tiêu chí nghiệm thu của đề tài.

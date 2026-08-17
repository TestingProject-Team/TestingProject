# Test case theo phương pháp Boundary Value Analysis (BVA)

## 1. Mục tiêu và cách chọn dữ liệu

Bộ test này áp dụng **Robust BVA** cho các luật nghiệp vụ có biên rõ ràng trong
backend YiYi Bookstore. Với mỗi biên `B`, dữ liệu ưu tiên là `B - 1`, `B` và
`B + 1`. Riêng miền có cả cận dưới và cận trên sử dụng thêm giá trị sát hai
biên và một giá trị danh nghĩa ở giữa.

Mỗi test chỉ thay đổi một biến đang kiểm tra; user, sách, coupon và các dữ liệu
còn lại được giữ ở trạng thái hợp lệ. Bước nhảy là `1` vì các trường được chọn
đều biểu diễn số sao, số lượng, điểm hoặc số tiền nguyên theo đồng.

## 2. Rating của đánh giá: miền hợp lệ từ 1 đến 5 sao

Luật nguồn: `ReviewService.createReview()` chấp nhận `1 <= rating <= 5`.

| ID | Giá trị rating | Vị trí BVA | Kết quả mong đợi |
| --- | ---: | --- | --- |
| BVA-REV-01 | 0 | Min - 1 | Từ chối, báo `Đánh giá phải từ 1 đến 5 sao!` |
| BVA-REV-02 | 1 | Min | Tạo đánh giá thành công |
| BVA-REV-03 | 2 | Min + 1 | Tạo đánh giá thành công |
| BVA-REV-04 | 3 | Nominal | Tạo đánh giá thành công |
| BVA-REV-05 | 4 | Max - 1 | Tạo đánh giá thành công |
| BVA-REV-06 | 5 | Max | Tạo đánh giá thành công |
| BVA-REV-07 | 6 | Max + 1 | Từ chối, báo `Đánh giá phải từ 1 đến 5 sao!` |

Tự động hóa: `ReviewServiceTest.SoSaoTests`.

## 3. Giá trị đơn tối thiểu và lượt dùng coupon

Fixture coupon có `minOrderAmount = 100000` và còn hiệu lực.

| ID | Biến | Giá trị | Vị trí BVA | Kết quả mong đợi |
| --- | --- | ---: | --- | --- |
| BVA-COUP-01 | orderAmount | 99.999 | Min - 1 | Từ chối vì chưa đạt giá trị đơn tối thiểu |
| BVA-COUP-02 | orderAmount | 100.000 | Min | Chấp nhận coupon |
| BVA-COUP-03 | orderAmount | 100.001 | Min + 1 | Chấp nhận coupon |
| BVA-COUP-04 | usageLimit | 0 | Min - 1 của miền còn lượt | Từ chối vì coupon hết lượt |
| BVA-COUP-05 | usageLimit | 1 | Min của miền còn lượt | Chấp nhận coupon |

Tự động hóa: `CouponServiceTest`, các test có tên chứa `Bva`,
`OrderAmountEqualsMinimum` và `UsageLimitIsZero`.

## 4. Số lượng đặt so với tồn kho

Fixture sách có tồn kho bằng `3`; điều kiện chấp nhận là
`requestedQuantity <= stockQuantity`.

| ID | Số lượng đặt | Vị trí BVA | Kết quả mong đợi |
| --- | ---: | --- | --- |
| BVA-STOCK-01 | 2 | Stock - 1 | Tạo đơn thành công, tồn kho còn 1 |
| BVA-STOCK-02 | 3 | Stock | Tạo đơn thành công, tồn kho còn 0 |
| BVA-STOCK-03 | 4 | Stock + 1 | Từ chối vì không đủ tồn kho, không lưu đơn |

Tự động hóa: `OrderServiceCreateTest.TonKhoTests`.

## 5. Các mốc hạng thành viên

Fixture đơn có tạm tính `200.000`, chưa có giảm giá sản phẩm. Các mốc điểm tích
lũy là `5.000` (2%), `30.000` (5%) và `100.000` (10%).

| ID | Điểm tích lũy | Vị trí BVA | Mức giảm mong đợi | Tiền giảm mong đợi |
| --- | ---: | --- | ---: | ---: |
| BVA-VIP-01 | 4.999 | 5.000 - 1 | 0% | 0 |
| BVA-VIP-02 | 5.000 | Biên hạng Bạc | 2% | 4.000 |
| BVA-VIP-03 | 5.001 | 5.000 + 1 | 2% | 4.000 |
| BVA-VIP-04 | 29.999 | 30.000 - 1 | 2% | 4.000 |
| BVA-VIP-05 | 30.000 | Biên hạng Vàng | 5% | 10.000 |
| BVA-VIP-06 | 30.001 | 30.000 + 1 | 5% | 10.000 |
| BVA-VIP-07 | 99.999 | 100.000 - 1 | 5% | 10.000 |
| BVA-VIP-08 | 100.000 | Biên hạng Kim Cương | 10% | 20.000 |
| BVA-VIP-09 | 100.001 | 100.000 + 1 | 10% | 20.000 |

Tự động hóa: `OrderServiceCreateTest.ChietKhauVipTests`.

## 6. Điểm đổi thưởng

### 6.1. Freeship: tối thiểu 10.000 điểm

| ID | Điểm đổi | Vị trí BVA | Kết quả mong đợi |
| --- | ---: | --- | --- |
| BVA-REW-01 | 9.999 | Min - 1 | Từ chối, không trừ điểm và không ghi giao dịch |
| BVA-REW-02 | 10.000 | Min | Nhận 1 lượt freeship và trừ 10.000 điểm |
| BVA-REW-03 | 10.001 | Min + 1 | Nhận 1 lượt freeship và trừ 10.001 điểm |

### 6.2. Coupon giảm 20K: phải đổi đúng 20.000 điểm

| ID | Điểm đổi | Vị trí BVA | Kết quả mong đợi |
| --- | ---: | --- | --- |
| BVA-REW-04 | 19.999 | Exact - 1 | Từ chối, không tạo coupon |
| BVA-REW-05 | 20.000 | Exact | Tạo coupon 20K và trừ đúng 20.000 điểm |
| BVA-REW-06 | 20.001 | Exact + 1 | Từ chối, không tạo coupon |

Tự động hóa: `RewardServiceTest`, các test có tên chứa `Bva` và
`Success_Discount20k`.

## 7. Cách chạy và tiêu chí PASS

```powershell
cd backend
.\mvnw.cmd test
```

Một test case PASS khi kết quả/exception đúng như bảng và các kiểm tra side
effect cũng đúng: repository chỉ được lưu ở luồng hợp lệ; luồng bị từ chối
không được trừ điểm, trừ kho hoặc tạo coupon/đơn hàng.

Kết quả xác minh ngày **17/08/2026**: toàn bộ backend chạy **299 test PASS,
0 failure, 0 error, 0 skipped**.

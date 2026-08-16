# Postman/Newman test artifacts

Thư mục này chứa JSON bàn giao để import trực tiếp vào Postman và bằng chứng
Newman đã làm sạch cho Week 1–Week 2.

## File

- `YiYi-Week-1-2.postman_collection.json`: collection đầy đủ của nhóm, 152 request item.
- `YiYi-Local.postman_environment.json`: environment local, không chứa JWT/API key runtime.
- `YIYI-37-newman-summary.json`: số liệu chạy collection phạm vi YIYI-37.
- `week2-newman-summary.json`: số liệu chạy full regression suite.
- `e2e-api.js`: script E2E Node hiện có.

Các file Newman raw không được commit vì chúng chứa response body và JWT sinh ra
trong phiên test. Hai file `*-summary.json` chỉ giữ metric cần thiết để báo cáo.

## Chạy bằng Postman

1. Import collection và environment JSON.
2. Chọn environment `YiYi Book — Local`.
3. Khởi động backend tại `http://localhost:8081/api`.
4. Run collection từ trên xuống.

## Chạy bằng Newman

```powershell
cd postman
npm ci
npx newman run ..\test-scripts\YiYi-Week-1-2.postman_collection.json `
  --environment ..\test-scripts\YiYi-Local.postman_environment.json `
  --reporters cli
```

Nếu backend dùng cổng khác:

```powershell
--env-var baseUrl=http://localhost:8082/api
```

MoMo/ZaloPay/VNPay là dịch vụ ngoài; collection kiểm tra contract và dùng ngưỡng
thời gian riêng để tránh flaky test, không khẳng định giao dịch production thành công.

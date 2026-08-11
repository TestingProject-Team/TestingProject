# YiYi Bookstore Backend - README phan cong tuan 1

> Pham vi: 5 ngay lam viec dau tien cua ke hoach 2 tuan.  
> Muc tieu: dung moi truong, tao Postman Workspace/Collection, khai bao cac endpoint va tao bo test ban dau.

## 1. Muc tieu cuoi tuan 1

- Chay duoc backend bang Docker Compose va kiem tra duoc GET /api/ping.
- Co Postman Team Workspace, Collection va Environment cho Local/Docker.
- Co day du cac folder endpoint theo phan cong trong file task goc.
- Co body mau, header mau va bien moi truong co ban.
- Co bo test script ban dau cho cac request quan trong.
- Moi thanh vien co README bao cao rieng va dinh kem evidence khi hoan thanh.

## 2. Nguyen tac lam viec

- Lam tren branch rieng: feature/<ten>-week1.
- Khong commit mat khau, token that, file .env that hoac thong tin ca nhan.
- Dung chung ten bien Postman: baseUrl, token, userId, bookId, categoryId, orderId.
- Neu API chua co contract ro rang, ghi TODO - can xac nhan backend, khong tu y khang dinh schema.
- Moi request moi them vao Collection phai co method, URL, header, body mau neu can va mo ta ngan.
- Trang thai ban dau cua cac dau viec trong file nay la TODO; cap nhat thanh DOING, DONE sau khi thuc hien.

## 3. Phan cong chi tiet tuan 1

| Ma | Thanh vien | Nhiem vu tuan 1 | Dau ra bat buoc |
| --- | --- | --- | --- |
| VA-W1 | Van Anh | Clone source, checkout branch, cai JDK 17/21, Docker Desktop, IntelliJ; cau hinh application-local.properties; chay docker compose up --build; kiem tra GET /api/ping; ghi loi vao README | 3 container xanh, ket qua ping, log loi va cach xu ly |
| AP-W1 | Anh Phu | Tao Team Workspace, Collection, folder Auth/Books/Categories/Banners; tao Environment Local va Docker; verify API bang Postman/Swagger; khai bao request co ban | Workspace, Environment, 4 folder va request co ban |
| VT-W1 | Van Thien | Khai bao Cart, Orders, Payment; tao skeleton Wishlist, Address, VAT Invoice; chuan bi body mau va header auth; xac dinh request nao can token | 6 folder, request co ban, danh sach request can auth |
| VD-W1 | Van Dinh | Khai bao Reviews, Coupons, Notifications, Newsletter; tao test script dau tien cho Auth, Books, Cart, Orders; dat quy uoc test chung | 4 folder, test script ban dau, bang test case |
| MT-W1 | Minh Tai | Khai bao Admin Users, Admin Reviews, Admin Rewards, Rewards; tao Collection Runner draft; phoi hop invite thanh vien va kiem tra quyen truy cap | 4 folder admin/rewards, Runner draft, danh sach thanh vien da invite |

## 4. Lich lam viec 5 ngay

### Ngay 1 - Dung moi truong va Workspace

- Van Anh: clone source, cai cong cu, bat dau Docker Compose.
- Anh Phu: tao Workspace, Collection va Environment.
- Van Thien: chot quy uoc folder, header va bien token.
- Van Dinh: chot mau test script va bang ma test case.
- Minh Tai: chot danh sach quyen truy cap, tao folder Admin/Rewards.

### Ngay 2 - Kiem tra backend va khai bao endpoint dot 1

- Van Anh: hoan tat GET /api/ping, kiem tra log va port.
- Anh Phu: hoan tat Auth, Books, Categories, bat dau Banners.
- Van Thien: hoan tat Cart, Orders, bat dau Payment.
- Van Dinh: hoan tat Reviews, Coupons, Notifications, Newsletter.
- Minh Tai: hoan tat Admin Users, Admin Reviews, Admin Rewards, Rewards.

### Ngay 3 - Khai bao endpoint dot 2 va test ban dau

- Anh Phu: hoan tat Banners, bo sung body mau va response note.
- Van Thien: hoan tat Payment, Wishlist, Address, VAT Invoice.
- Van Dinh: viet test cho Auth, Books, Cart, Orders.
- Minh Tai: tao Collection Runner va bo test chay theo thu tu.
- Van Anh: ho tro xu ly loi moi truong cho thanh vien.

### Ngay 4 - Dong bo va review cheo

- Kiem tra tat ca folder co dung ten, dung method va dung bien {{baseUrl}}.
- Kiem tra request can auth deu co Authorization: Bearer {{token}}.
- Kiem tra cac bien token, userId, bookId, orderId co duoc luu sau request.
- Review cheo: moi thanh vien chay thu it nhat mot folder cua nguoi khac.
- Ghi lai endpoint loi, body chua ro hoac response khac contract.

### Ngay 5 - Chot deliverable tuan 1

- Van Anh xac nhan moi truong chay duoc tren may thanh vien.
- Anh Phu va Van Thien chot endpoint collection.
- Van Dinh chot test script ban dau va bang test case.
- Minh Tai chot Runner draft, quyen Workspace va danh sach con thieu.
- Ca nhom cap nhat README rieng, commit va gui evidence.

## 5. Deliverable cuoi tuan 1

- [ ] Docker Compose chay thanh cong, 3 container o trang thai healthy/running.
- [ ] GET /api/ping co ket qua va evidence.
- [ ] Team Workspace da tao, Collection da tao.
- [ ] Environment Local va Docker co baseUrl, token, userId.
- [ ] Co cac folder: Auth, Books, Categories, Banners, Cart, Orders, Payment, Wishlist, Address, VAT Invoice, Reviews, Coupons, Notifications, Newsletter, Admin Users, Admin Reviews, Admin Rewards, Rewards.
- [ ] Request co method, URL, body mau va mo ta ngan.
- [ ] Co test script cho it nhat Auth, Books, Cart, Orders.
- [ ] Co Runner draft va danh sach quyen truy cap.
- [ ] Moi thanh vien cap nhat README ca nhan.

## 6. Tieu chi hoan thanh mot task

Mot task chi duoc danh DONE khi co du 4 noi dung:

1. Da thuc hien tren branch/Workspace dung.
2. Da chay kiem tra toi thieu mot lan.
3. Co ket qua thuc te hoac evidence link/anh/log.
4. Da cap nhat README va thong bao blocker neu co.

## 7. Mau cap nhat bao cao hang ngay

| Ngay | Da lam | Dang lam | Blocker | Evidence |
| --- | --- | --- | --- | --- |
| D1 | TODO | TODO | Khong/ghi ro | Link anh/log |
| D2 | TODO | TODO | Khong/ghi ro | Link request |
| D3 | TODO | TODO | Khong/ghi ro | Link Collection |
| D4 | TODO | TODO | Khong/ghi ro | Link test run |
| D5 | TODO | TODO | Khong/ghi ro | Link commit/report |

## 8. Quy uoc evidence

- Anh Docker: evidence/week1/docker-<ngay>.png
- Anh Postman: evidence/week1/postman-<folder>-<ngay>.png
- Log loi: evidence/week1/log-<ma-task>.txt
- Bao cao test: evidence/week1/test-<ma-test>.md
- Newman report chi chay va export trong tuan 2, khong danh dau DONE o tuan 1 neu chua co file report.


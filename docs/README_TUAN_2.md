# YiYi Bookstore Backend - README phan cong tuan 2

> Pham vi: Giai doan hoan thien, kiem thu va ban giao cua ke hoach 2 tuan.  
> Muc tieu: hoan thien request, viet test script, chay collection, tao Newman HTML Report va tong hop demo.

## 1. Muc tieu tuan 2

- Hoan thien cac folder va request con thieu trong Postman.
- Chay duoc luong co ban: login -> lay token -> request can auth -> luu ID -> request phu thuoc.
- Test script bao phu toi thieu 80% endpoint theo task goc.
- Kiem tra status code, response time, response body va bien moi truong.
- Chay duoc Collection Runner va Newman CLI.
- Export duoc newman-report.html.
- Chot quyen Workspace, README ca nhan va tai lieu demo cho ca nhom.

## 2. Phan cong chi tiet tuan 2

| Ma | Thanh vien | Nhiem vu tuan 2 | Dau ra bat buoc |
| --- | --- | --- | --- |
| VA-W2 | Van Anh | Re-run moi truong sau khi dong bo collection; kiem tra 3 container, port, database/log; ghi loi va cap nhat README setup; ho tro fix blocker | Setup README hoan chinh, health-check evidence, danh sach loi da xu ly |
| AP-W2 | Anh Phu | Hoan thien body/response note cho Auth, Books, Categories, Banners; them case thanh cong/loi; verify token/userId; review cheo folder | 4 folder du request, case positive/negative, bien duoc luu dung |
| VT-W2 | Van Thien | Hoan thien body cho Cart, Orders, Payment, Wishlist, Address, VAT Invoice; viet pre-request auto login/set token; test cac luong phu thuoc | 6 folder du request, script auth chay duoc, orderId/cartId duoc luu |
| VD-W2 | Van Dinh | Hoan thien test script cho Payment, Reviews, Wishlist; bo sung test cho folder con can thiet; chay collection va sua assertion; tong hop test coverage | Test script pass theo contract, coverage >= 80%, bang PASS/FAIL co evidence |
| MT-W2 | Minh Tai | Chay Collection Runner; cai/chay Newman + htmlextra; export HTML; chot quyen Member; phoi hop demo va tong hop tai lieu | newman-report.html, log command, Workspace invite day du, demo checklist |

## 3. Deliverable tuan 2

- [ ] Tat ca folder phan cong co request va body mau.
- [ ] Environment Local/Docker co bien can thiet, khong chua secret that.
- [ ] Pre-request script tu dong xu ly token hoac co huong dan fallback.
- [ ] Test script kiem tra status code, response time < 2000ms, response body va luu bien.
- [ ] Coverage test dat toi thieu 80% endpoint theo pham vi task.
- [ ] Collection Runner chay duoc va co log.
- [ ] Newman chay duoc va export newman-report.html.
- [ ] Workspace da invite thanh vien va phan quyen.
- [ ] Co danh sach FAIL/known issue, owner va huong xu ly.
- [ ] Co README tuan 1, README tuan 2, README test case va README rieng cua 5 thanh vien.

## 4. Tieu chi nghiem thu

| Hang muc | Dat khi |
| --- | --- |
| Moi truong | Docker Compose chay duoc, ping phan hoi, khong co loi blocker chua ghi nhan |
| Collection | Folder va request dung phan cong, URL dung {{baseUrl}}, body co mau |
| Auth | Token duoc tao/luu va request can auth dung Bearer token |
| Test script | Co assertion status, time, body; khong dung assertion qua rong |
| Automation | Runner/Newman co ket qua va file report |
| Tai lieu | README co owner, ket qua thuc te, evidence va known issue |
| Ban giao | Thanh vien khac co the import/chay theo README ma khong can hoi lai buoc co ban |

## 5. Mau tong hop ket qua

| Nhom | Tong request | Da test | PASS | FAIL | Coverage | Ghi chu |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Auth/Books/Categories/Banners | TODO | TODO | TODO | TODO | TODO | Anh Phu |
| Cart/Orders/Payment/Wishlist/Address/VAT | TODO | TODO | TODO | TODO | TODO | Van Thien |
| Reviews/Coupons/Notifications/Newsletter | TODO | TODO | TODO | TODO | TODO | Van Dinh |
| Admin/Rewards | TODO | TODO | TODO | TODO | TODO | Minh Tai |
| Environment/Health check | TODO | TODO | TODO | TODO | N/A | Van Anh |
| Tong | TODO | TODO | TODO | TODO | TODO | Ca nhom |

## 6. Known issue phai ghi ro

Moi loi con lai phai co:

- Ma loi/ma test.
- Endpoint va method.
- Cach tai hien.
- Expected va actual.
- Log/anh/report.
- Owner xu ly.
- Muc do: Blocker, High, Medium hoac Low.
- Trang thai: Open, In progress, Resolved, Accepted risk.

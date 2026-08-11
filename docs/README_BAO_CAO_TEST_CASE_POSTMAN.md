# YiYi Bookstore Backend - Bao cao Test Case va Postman

> Tai lieu dung chung cho ca nhom.  
> Nguon phan cong: file jira_tasks(1).pdf.  
> Trang thai mac dinh: TODO; chi doi thanh PASS khi da chay request va luu evidence thuc te.

## 1. Pham vi

Tai lieu nay bao gom:

- Quy uoc Postman Workspace, Collection, Folder va Environment.
- Danh sach test case theo endpoint duoc phan cong.
- Assertion toi thieu theo task goc.
- Pre-request script cho token.
- Cach chay Collection Runner va Newman.
- Mau ghi ket qua de tong hop coverage.

## 2. Cau truc Collection de nghi

- 00 - Health Check
- 01 - Auth
- 02 - Books
- 03 - Categories
- 04 - Banners
- 05 - Cart
- 06 - Orders
- 07 - Payment
- 08 - Wishlist
- 09 - Address
- 10 - VAT Invoice
- 11 - Reviews
- 12 - Coupons
- 13 - Notifications
- 14 - Newsletter
- 15 - Admin Users
- 16 - Admin Reviews
- 17 - Admin Rewards
- 18 - Rewards

Ten folder co the doi theo quy uoc cua nhom, nhung khong duoc doi tuy tien sau khi tao report.

## 3. Environment variables

| Bien | Muc dich | Gia tri mau |
| --- | --- | --- |
| baseUrl | URL goc cua backend | http://localhost:8080/api |
| token | Access token | De trong, duoc set sau login |
| refreshToken | Refresh token | De trong |
| email | Tai khoan test | Tai khoan local, khong dung mat khau that |
| password | Mat khau tai khoan test | Dat trong Environment, khong commit |
| userId | ID user sau login | De trong |
| bookId | ID sach sau create/list | De trong |
| categoryId | ID category | De trong |
| bannerId | ID banner | De trong |
| cartId | ID gio hang | De trong |
| orderId | ID don hang | De trong |
| reviewId | ID review | De trong |
| couponCode | Ma coupon test | Theo seed data |
| adminToken | Token tai khoan admin | De trong, khong commit |

Neu backend dung ten bien khac, cap nhat Environment va ghi ro trong README, khong tao nhieu ten trung nghia.

## 4. Quy uoc assertion toi thieu

Moi request co test script phai xem xet:

1. Status code dung theo contract.
2. Response time nho hon 2000ms, tru khi backend co ly do da thong bao.
3. Response body co field can thiet, khong chi kiem tra body khong rong.
4. ID/token quan trong duoc luu vao Environment khi response co gia tri.
5. Request can auth phai dung Bearer token.
6. Case loi phai co body loi de truy vet.

Mau script status code va response time:

~~~javascript
pm.test("Status code theo contract", function () {
  pm.expect([200, 201, 204, 400, 401, 404]).to.include(pm.response.code);
});

pm.test("Response time < 2000ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(2000);
});
~~~

Mau script luu ID:

~~~javascript
let data = {};
try {
  data = pm.response.json();
} catch (error) {
  data = {};
}

const root = data.data || data;
const id = root.id || data.id || root.bookId || data.bookId;
if (id) {
  pm.environment.set("bookId", id);
}
~~~

Ten bien trong script phai doi theo folder, vi du orderId, cartId, reviewId.

## 5. Pre-request script tu dong lay token

Chi dung tai khoan test local. Neu response login cua backend dung field khac token hoac accessToken, sua script theo contract.

~~~javascript
if (!pm.environment.get("token")) {
  const loginUrl = pm.environment.replaceIn("{{baseUrl}}/auth/login");

  pm.sendRequest({
    url: loginUrl,
    method: "POST",
    header: {
      "Content-Type": "application/json"
    },
    body: {
      mode: "raw",
      raw: JSON.stringify({
        email: pm.environment.get("email"),
        password: pm.environment.get("password")
      })
    }
  }, function (error, response) {
    if (error) {
      throw error;
    }

    const body = response.json();
    const accessToken = body.token || body.accessToken || body.data?.token;

    if (!accessToken) {
      throw new Error("Login khong tra ve token theo schema dang cau hinh");
    }

    pm.environment.set("token", accessToken);
  });
}
~~~

Header de nghi cho request can auth:

    Authorization: Bearer {{token}}
    Content-Type: application/json

Luu y: neu pre-request async gay race condition voi backend/runner, tach thanh request Auth - Login, chay truoc va dung token da luu; ghi ro cach chay trong Collection Runner.

## 6. Danh sach test case

### 6.1. Health Check - owner: Van Anh

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-ENV-001 | Docker Compose | Chay docker compose up --build | 3 container running/healthy | Van Anh | TODO |
| TC-ENV-002 | GET /api/ping | Backend san sang | 200, response dung contract | Van Anh | TODO |

### 6.2. Auth - owner chinh: Anh Phu; test script: Van Dinh

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-AUTH-001 | POST /auth/register | Du lieu hop le | 200/201, tao user | Anh Phu | TODO |
| TC-AUTH-002 | POST /auth/login | Tai khoan hop le | 200, co token; luu token, userId | Anh Phu | TODO |
| TC-AUTH-003 | POST /auth/login | Sai mat khau/thieu field | 400/401 | Van Dinh | TODO |
| TC-AUTH-004 | POST /auth/refresh | Refresh token hop le | 200, cap token moi | Anh Phu | TODO |
| TC-AUTH-005 | POST /auth/logout | Co token hop le | 200/204, token het hieu luc theo contract | Van Dinh | TODO |

### 6.3. Books - owner chinh: Anh Phu; test script: Van Dinh

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-BOOK-001 | GET /books | Lay danh sach | 200, body co danh sach | Anh Phu | TODO |
| TC-BOOK-002 | GET /books/{id} | ID ton tai | 200, co book fields | Van Dinh | TODO |
| TC-BOOK-003 | GET /books/{id} | ID khong ton tai | 404 | Van Dinh | TODO |
| TC-BOOK-004 | POST /books | Body hop le | 201/200, luu bookId | Anh Phu | TODO |
| TC-BOOK-005 | PUT /books/{id} | Cap nhat ID hop le | 200, body phan anh thay doi | Anh Phu | TODO |
| TC-BOOK-006 | DELETE /books/{id} | Xoa ID hop le | 200/204 | Van Dinh | TODO |
| TC-BOOK-007 | GET /books/search | Tu khoa hop le/empty | 200, ket qua dung contract | Anh Phu | TODO |

### 6.4. Categories va Banners - owner: Anh Phu

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-CAT-001 | GET /categories | Lay danh sach | 200 | Anh Phu | TODO |
| TC-CAT-002 | POST /categories | Body hop le | 201/200, luu categoryId | Anh Phu | TODO |
| TC-CAT-003 | PUT /categories/{id} | ID hop le | 200 | Anh Phu | TODO |
| TC-CAT-004 | DELETE /categories/{id} | ID hop le | 200/204 | Anh Phu | TODO |
| TC-BAN-001 | GET /banners | Lay banner | 200, body co danh sach | Anh Phu | TODO |
| TC-BAN-002 | POST /banners | Body hop le | 201/200, luu bannerId | Anh Phu | TODO |

### 6.5. Cart - owner: Van Thien; test script: Van Dinh

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-CART-001 | GET /cart | Co token | 200, tra gio hang | Van Thien | TODO |
| TC-CART-002 | GET /cart | Khong co token | 401 | Van Dinh | TODO |
| TC-CART-003 | POST /cart/items | Them sach hop le | 200/201, cap nhat gio | Van Thien | TODO |
| TC-CART-004 | PUT /cart/items | Cap nhat so luong | 200 | Van Thien | TODO |
| TC-CART-005 | DELETE /cart/items | Xoa item | 200/204 | Van Thien | TODO |

### 6.6. Orders va Payment - owner: Van Thien; test script: Van Dinh

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-ORDER-001 | POST /orders | Tao don tu cart hop le | 201/200, luu orderId | Van Thien | TODO |
| TC-ORDER-002 | GET /orders | Lay don cua user | 200, body co danh sach | Van Thien | TODO |
| TC-ORDER-003 | GET /orders/{id} | ID ton tai | 200 | Van Thien | TODO |
| TC-ORDER-004 | PUT /orders/{id}/cancel | Huy don hop le | 200/204 | Van Thien | TODO |
| TC-PAY-001 | Payment create VNPay | Du lieu don hop le | 200/201, co payment data theo contract | Van Thien | TODO |
| TC-PAY-002 | Payment create MoMo | Du lieu don hop le | 200/201, co payment data | Van Thien | TODO |
| TC-PAY-003 | Payment create ZaloPay | Du lieu don hop le | 200/201, co payment data | Van Thien | TODO |
| TC-PAY-004 | Payment callback | Callback hop le/khong hop le | Ket qua dung contract, co body loi neu fail | Van Dinh | TODO |

### 6.7. Wishlist, Address va VAT Invoice - owner: Van Thien

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-WISH-001 | GET /wishlist | Lay wishlist | 200 | Van Thien | TODO |
| TC-WISH-002 | POST /wishlist | Them sach hop le | 200/201 | Van Thien | TODO |
| TC-WISH-003 | DELETE /wishlist | Xoa sach | 200/204 | Van Dinh | TODO |
| TC-ADDR-001 | GET /addresses | Lay dia chi | 200 | Van Thien | TODO |
| TC-ADDR-002 | POST /addresses | Tao dia chi | 201/200 | Van Thien | TODO |
| TC-ADDR-003 | PUT /addresses/{id} | Cap nhat dia chi | 200 | Van Thien | TODO |
| TC-ADDR-004 | DELETE /addresses/{id} | Xoa dia chi | 200/204 | Van Thien | TODO |
| TC-VAT-001 | GET /vat-invoices | Lay hoa don VAT | 200 | Van Thien | TODO |
| TC-VAT-002 | POST /vat-invoices | Tao hoa don VAT | 201/200 | Van Thien | TODO |

### 6.8. Reviews, Coupons, Notifications, Newsletter - owner: Van Dinh

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-REV-001 | GET /reviews | Lay review | 200 | Van Dinh | TODO |
| TC-REV-002 | POST /reviews | Tao review hop le | 201/200, luu reviewId | Van Dinh | TODO |
| TC-REV-003 | PUT /reviews/{id} | Cap nhat review | 200 | Van Dinh | TODO |
| TC-REV-004 | DELETE /reviews/{id} | Xoa review | 200/204 | Van Dinh | TODO |
| TC-COUP-001 | GET /coupons | Lay coupon | 200 | Van Dinh | TODO |
| TC-COUP-002 | POST /coupons | Tao coupon | 201/200 | Van Dinh | TODO |
| TC-COUP-003 | POST /coupons/apply | Ma hop le/khong hop le | 200 hoac 400/404 | Van Dinh | TODO |
| TC-NOTI-001 | GET /notifications | Lay thong bao | 200 | Van Dinh | TODO |
| TC-NOTI-002 | PUT /notifications | Cap nhat trang thai | 200 | Van Dinh | TODO |
| TC-NEWS-001 | POST /newsletter/subscribe | Email hop le | 200/201 | Van Dinh | TODO |
| TC-NEWS-002 | POST /newsletter/subscribe | Email sai/thieu | 400 | Van Dinh | TODO |

### 6.9. Admin va Rewards - owner: Minh Tai

| ID | Request | Scenario | Expected | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TC-ADM-001 | GET /admin/users | Token admin hop le | 200 | Minh Tai | TODO |
| TC-ADM-002 | PUT /admin/users | Cap nhat user | 200 | Minh Tai | TODO |
| TC-ADM-003 | DELETE /admin/users | Xoa user | 200/204 | Minh Tai | TODO |
| TC-ADM-004 | Admin request khong co quyen | Token user/khong token | 401/403 theo contract | Minh Tai | TODO |
| TC-ADM-005 | GET /admin/reviews | Admin lay review | 200 | Minh Tai | TODO |
| TC-ADM-006 | PUT /admin/reviews | Admin cap nhat review | 200 | Minh Tai | TODO |
| TC-ADM-007 | GET /admin/rewards | Lay rewards admin | 200 | Minh Tai | TODO |
| TC-ADM-008 | POST /admin/rewards | Tao rewards | 201/200 | Minh Tai | TODO |
| TC-REW-001 | GET /rewards | User lay rewards | 200 | Minh Tai | TODO |
| TC-REW-002 | POST /rewards/redeem | Redeem hop le | 200/201 | Minh Tai | TODO |

## 7. Mau bang ghi ket qua chay

| Test ID | Run ID | Status thuc te | Time ms | Body/field | PASS/FAIL | Evidence | Loi/ghi chu |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| TC-XXX-000 | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

Khong ghi PASS chi vi request tra ve 200. Can kiem tra them response body, field va bien moi truong.

## 8. Chay Collection Runner

1. Chon Environment dung.
2. Chon Collection.
3. Sap xep request theo thu tu: Health Check -> Auth Login -> resource master data -> Cart -> Orders -> Payment -> Admin.
4. Nhap iteration data neu request can nhieu du lieu.
5. Chay va luu tong so request, pass, fail, duration.
6. Ghi cac fail vao bang ket qua va tao issue/blocker.

## 9. Chay Newman va export HTML

Cai dat reporter neu may chua co:

    npm install -g newman newman-reporter-htmlextra

Lenh theo task goc:

    newman run "YiYi Bookstore API.postman_collection.json" \
      --environment "Local.postman_environment.json" \
      --reporters htmlextra \
      --reporter-htmlextra-export newman-report.html

Evidence can luu:

- File collection JSON dung version.
- File environment JSON da xoa secret.
- Terminal log cua lenh Newman.
- File newman-report.html.
- Tong so pass/fail va coverage.
- Danh sach known issue neu co.

## 10. Tinh coverage

    coverage = so endpoint da co test script / tong endpoint trong pham vi x 100

Muc tieu: coverage >= 80%. Neu bo qua endpoint, ghi ro endpoint, ly do, owner va ke hoach bo sung.

## 11. Checklist ban giao

- [ ] Collection import duoc.
- [ ] Environment import duoc va khong co secret that.
- [ ] Request dung {{baseUrl}}.
- [ ] Token duoc set dung.
- [ ] Test script co status/time/body.
- [ ] ID can thiet duoc luu.
- [ ] Runner da chay.
- [ ] Newman report da export.
- [ ] PASS/FAIL co evidence.
- [ ] Known issue co owner va trang thai.

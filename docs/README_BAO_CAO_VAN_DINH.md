# Bao cao nhiem vu - Van Dinh

Vai tro: Member 4 - Test Scripts va Reviews, Coupons, Notifications, Newsletter  
Du an: YiYi Bookstore Backend  
Nguon phan cong: jira_tasks(1).pdf

## 1. Muc tieu

Tao test script co the tai su dung cho Postman, bao phu toi thieu 80% endpoint theo task; moi request quan trong phai kiem tra status code, response time, response body va bien moi truong.

## 2. Ke hoach tuan 1

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| VD-W1-01 | Khai bao folder Reviews | GET/POST/PUT/DELETE | TODO |
| VD-W1-02 | Khai bao folder Coupons | GET/POST/apply | TODO |
| VD-W1-03 | Khai bao folder Notifications | GET/PUT | TODO |
| VD-W1-04 | Khai bao folder Newsletter | POST subscribe | TODO |
| VD-W1-05 | Viet script cho Auth, Books | Status/time/body/luu bien | TODO |
| VD-W1-06 | Viet script cho Cart, Orders | Status/time/body/luu bien | TODO |
| VD-W1-07 | Tao bang test case va quy uoc PASS/FAIL | README chung | TODO |

## 3. Ke hoach tuan 2

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| VD-W2-01 | Viet script cho Payment | Create/callback va case loi | TODO |
| VD-W2-02 | Viet script cho Reviews | CRUD va field review | TODO |
| VD-W2-03 | Viet script cho Wishlist | GET/POST/DELETE | TODO |
| VD-W2-04 | Bo sung script cho folder con thieu | Coverage >= 80% | TODO |
| VD-W2-05 | Chay Collection Runner voi Minh Tai | Bang pass/fail doi chieu | TODO |
| VD-W2-06 | Doi chieu Newman report | Sua assertion sai, ghi known issue | TODO |

## 4. Quy uoc test script

Moi request can co:

- Status code dung theo contract.
- Response time < 2000ms.
- Response body co field can thiet.
- ID/token quan trong duoc luu vao Environment.
- Case loi co expected status va body loi.
- Khong dung assertion qua rong nhu chi kiem tra response is not empty.

Mau script:

~~~javascript
pm.test("Response time < 2000ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Status code theo contract", function () {
  pm.expect([200, 201, 204, 400, 401, 404]).to.include(pm.response.code);
});

let body = {};
try {
  body = pm.response.json();
} catch (error) {
  body = {};
}

pm.test("Response co body hoac status 204", function () {
  if (pm.response.code !== 204) {
    pm.expect(body).to.exist;
  }
});

const id = body.id || body.data?.id;
if (id) {
  pm.environment.set("resourceId", id);
}
~~~

Doi resourceId thanh orderId, bookId, reviewId hoac ten dung theo request.

## 5. Danh sach test script phai hoan thanh

### Core flow

- [ ] Auth login/register/refresh/logout.
- [ ] Books list/detail/create/update/delete/search.
- [ ] Cart get/add/update/delete.
- [ ] Orders create/list/detail/cancel.
- [ ] Payment create/callback.
- [ ] Wishlist get/add/delete.

### Folder phu trach

- [ ] Reviews GET/POST/PUT/DELETE.
- [ ] Coupons GET/POST/apply.
- [ ] Notifications GET/PUT.
- [ ] Newsletter subscribe.

### Coverage

- [ ] Dem tong endpoint co trong Collection.
- [ ] Dem endpoint co it nhat mot test script.
- [ ] Tinh coverage.
- [ ] Ghi ro endpoint bo qua va ly do.
- [ ] Dat muc tieu >= 80%.

## 6. Bang ket qua test

| Test ID | Endpoint | Expected | Actual | Time ms | PASS/FAIL | Evidence | Ghi chu |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| TC-AUTH-001 | POST /auth/login | 200 + token | TODO | TODO | TODO | TODO | TODO |
| TC-BOOK-001 | GET /books | 200 + list | TODO | TODO | TODO | TODO | TODO |
| TC-CART-001 | GET /cart | 200 | TODO | TODO | TODO | TODO | TODO |
| TC-ORDER-001 | POST /orders | 201/200 + orderId | TODO | TODO | TODO | TODO | TODO |
| TC-PAY-001 | Payment create | 200/201 | TODO | TODO | TODO | TODO | TODO |
| TC-REV-002 | POST /reviews | 201/200 + reviewId | TODO | TODO | TODO | TODO | TODO |
| TC-WISH-002 | POST /wishlist | 200/201 | TODO | TODO | TODO | TODO | TODO |
| TC-COUP-003 | POST /coupons/apply | 200/400/404 | TODO | TODO | TODO | TODO | TODO |
| TC-NOTI-002 | PUT /notifications | 200 | TODO | TODO | TODO | TODO | TODO |
| TC-NEWS-001 | Subscribe | 200/201 | TODO | TODO | TODO | TODO | TODO |

## 7. Cac bao cao loi

Moi assertion fail can ghi:

- Test ID.
- Request va method.
- Expected/actual.
- Response time.
- Response body da an secret.
- Cach tai hien.
- Owner fix.
- Known issue hay script sai.

## 8. Evidence can nop

- [ ] Screenshot tab Tests cua cac folder.
- [ ] Export Collection co script.
- [ ] Newman report co so luong pass/fail.
- [ ] Bang coverage.
- [ ] Danh sach assertion da sua.
- [ ] Known issue co owner.

## 9. Ket luan

- Tuan 1: TODO.
- Tuan 2: TODO.
- Tong endpoint: TODO.
- Endpoint da co test: TODO.
- Coverage: TODO%.
- Known issue con lai: TODO.


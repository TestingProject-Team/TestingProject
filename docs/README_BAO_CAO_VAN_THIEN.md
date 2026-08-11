# Bao cao nhiem vu - Van Thien

Vai tro: Member 3 - Endpoints Cart, Orders, Payment, Wishlist, Address, VAT Invoice  
Du an: YiYi Bookstore Backend  
Nguon phan cong: jira_tasks(1).pdf

## 1. Muc tieu

Hoan thien 6 folder nghiep vu co request, body mau va luong auth phu thuoc; bao dam cac ID can thiet duoc luu de chay luong Cart -> Orders -> Payment.

## 2. Ke hoach tuan 1

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| VT-W1-01 | Khai bao Cart | GET/POST/PUT/DELETE cart/cart items | TODO |
| VT-W1-02 | Khai bao Orders | POST/GET/PUT orders, cancel | TODO |
| VT-W1-03 | Khai bao Payment | VNPay, MoMo, ZaloPay create/callback | TODO |
| VT-W1-04 | Khai bao Wishlist | GET/POST/DELETE | TODO |
| VT-W1-05 | Khai bao Address | GET/POST/PUT/DELETE | TODO |
| VT-W1-06 | Khai bao VAT Invoice | GET/POST | TODO |
| VT-W1-07 | Tao body mau va danh dau request can auth | Request co the chuan bi chay | TODO |

## 3. Ke hoach tuan 2

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| VT-W2-01 | Hoan thien body/response note cho 6 folder | Request dung contract | TODO |
| VT-W2-02 | Viet pre-request auto login/set token | Token duoc lay truoc request can auth | TODO |
| VT-W2-03 | Kiem tra luong Cart -> Orders | Luu cartId, orderId | TODO |
| VT-W2-04 | Kiem tra Payment callbacks | Co case thanh cong/loi va log | TODO |
| VT-W2-05 | Review test script voi Van Dinh | Assertion phu hop schema | TODO |
| VT-W2-06 | Chot danh sach blocker phu thuoc backend | Issue co owner | TODO |

## 4. Danh sach endpoint

### Cart

- [ ] GET /cart
- [ ] POST /cart
- [ ] PUT /cart
- [ ] DELETE /cart
- [ ] GET/POST/PUT/DELETE /cart/items theo contract thuc te

### Orders

- [ ] POST /orders
- [ ] GET /orders
- [ ] PUT /orders/{id}
- [ ] PUT /orders/{id}/cancel hoac method dung theo contract

### Payment

- [ ] VNPay create
- [ ] VNPay callback
- [ ] MoMo create
- [ ] MoMo callback
- [ ] ZaloPay create
- [ ] ZaloPay callback

### Wishlist

- [ ] GET /wishlist
- [ ] POST /wishlist
- [ ] DELETE /wishlist

### Address

- [ ] GET /addresses
- [ ] POST /addresses
- [ ] PUT /addresses/{id}
- [ ] DELETE /addresses/{id}

### VAT Invoice

- [ ] GET /vat-invoices
- [ ] POST /vat-invoices

## 5. Test case va ket qua

| Test ID | Request | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-CART-001 | GET /cart co token | 200 | TODO | TODO | TODO |
| TC-CART-003 | POST /cart/items | 200/201 | TODO | TODO | TODO |
| TC-CART-005 | Xoa cart item | 200/204 | TODO | TODO | TODO |
| TC-ORDER-001 | Tao order | 201/200 + orderId | TODO | TODO | TODO |
| TC-ORDER-004 | Cancel order | 200/204 | TODO | TODO | TODO |
| TC-PAY-001 | VNPay create | 200/201 | TODO | TODO | TODO |
| TC-PAY-002 | MoMo create | 200/201 | TODO | TODO | TODO |
| TC-PAY-003 | ZaloPay create | 200/201 | TODO | TODO | TODO |
| TC-WISH-002 | Them wishlist | 200/201 | TODO | TODO | TODO |
| TC-ADDR-002 | Tao address | 201/200 | TODO | TODO | TODO |
| TC-VAT-002 | Tao VAT invoice | 201/200 | TODO | TODO | TODO |

## 6. Pre-request script checklist

- [ ] Co email va password trong Environment test local.
- [ ] Script login khi token rong/het han theo cach nhom quy uoc.
- [ ] Token duoc luu vao token hoac ten bien da thong nhat.
- [ ] Request can auth co Authorization: Bearer {{token}}.
- [ ] Khong log password/token that vao Console hoac README.
- [ ] Neu script async gay loi, co fallback chay request Login truoc.

## 7. Evidence can nop

- [ ] Screenshot 6 folder.
- [ ] Export request Cart/Orders/Payment co body mau.
- [ ] Screenshot pre-request script.
- [ ] Ket qua luong Cart -> Order.
- [ ] Log/payment callback test.
- [ ] Bang PASS/FAIL va known issue.

## 8. Ket luan

- Tuan 1: TODO.
- Tuan 2: TODO.
- Luong phu thuoc chay duoc: TODO.
- Endpoint can backend bo sung contract: TODO.


# Bao cao nhiem vu - Anh Phu

Vai tro: Member 2 - Postman Workspace va Endpoints Auth, Books, Categories, Banners  
Du an: YiYi Bookstore Backend  
Nguon phan cong: jira_tasks(1).pdf

## 1. Muc tieu

Tao Workspace/Collection co cau truc ro rang va hoan thien request cho Auth, Books, Categories, Banners de cac thanh vien co the import Environment, chay request va dung cac bien token/ID.

## 2. Ke hoach tuan 1

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| AP-W1-01 | Verify API bang Postman/Swagger | Danh sach endpoint/response ghi lai | TODO |
| AP-W1-02 | Tao Team Workspace va Collection | Workspace/Collection ton tai | TODO |
| AP-W1-03 | Tao folder Auth, Books, Categories, Banners | 4 folder dung ten | TODO |
| AP-W1-04 | Tao Environment Local va Docker | Co baseUrl, token, userId | TODO |
| AP-W1-05 | Khai bao request Auth | Login/register/refresh/logout | TODO |
| AP-W1-06 | Khai bao request Books | CRUD, get by id, search | TODO |
| AP-W1-07 | Khai bao request Categories va Banners | CRUD categories, GET/POST banners | TODO |

## 3. Ke hoach tuan 2

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| AP-W2-01 | Bo sung body mau va header | Request co the chay voi data test | TODO |
| AP-W2-02 | Bo sung case positive/negative | 200/201/400/401/404 theo contract | TODO |
| AP-W2-03 | Kiem tra luu token, userId, bookId, categoryId, bannerId | Bien duoc set sau request | TODO |
| AP-W2-04 | Chay review cheo voi Van Dinh | Test script khong sai schema | TODO |
| AP-W2-05 | Chot Collection va thong bao thay doi | Version ban giao cho Minh Tai | TODO |

## 4. Danh sach request phai co

### Auth

- [ ] POST /auth/login
- [ ] POST /auth/register
- [ ] POST /auth/refresh
- [ ] POST /auth/logout

### Books

- [ ] GET /books
- [ ] POST /books
- [ ] PUT /books/{id}
- [ ] DELETE /books/{id}
- [ ] GET /books/{id}
- [ ] GET /books/search

### Categories

- [ ] GET /categories
- [ ] POST /categories
- [ ] PUT /categories/{id}
- [ ] DELETE /categories/{id}

### Banners

- [ ] GET /banners
- [ ] POST /banners

## 5. Bang ket qua test Postman

| Test ID | Request | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-AUTH-001 | POST /auth/login | 200 + token | TODO | TODO | TODO |
| TC-AUTH-002 | POST /auth/register | 200/201 | TODO | TODO | TODO |
| TC-AUTH-003 | Login sai du lieu | 400/401 | TODO | TODO | TODO |
| TC-BOOK-001 | GET /books | 200 + list | TODO | TODO | TODO |
| TC-BOOK-003 | GET /books/{id} sai ID | 404 | TODO | TODO | TODO |
| TC-BOOK-004 | POST /books | 201/200 + bookId | TODO | TODO | TODO |
| TC-CAT-001 | GET /categories | 200 | TODO | TODO | TODO |
| TC-BAN-001 | GET /banners | 200 | TODO | TODO | TODO |

Moi request can cap nhat them response time va field da kiem tra trong README test case chung.

## 6. Checklist Environment

- [ ] baseUrl khong bi hard-code trong tung request.
- [ ] token de trong truoc login.
- [ ] userId duoc luu tu response login neu contract co field.
- [ ] bookId, categoryId, bannerId duoc luu khi create/get.
- [ ] Environment Docker khong dung nham port voi Local.
- [ ] Khong export mat khau/token that.

## 7. Evidence can nop

- [ ] Link Workspace/Collection.
- [ ] Screenshot 4 folder.
- [ ] Export Collection JSON.
- [ ] Export Environment sau khi xoa secret.
- [ ] Screenshot request Auth login va Books list.
- [ ] Bang PASS/FAIL co evidence.

## 8. Ket luan

- Tuan 1: TODO.
- Tuan 2: TODO.
- Request con thieu: TODO.
- Schema can xac nhan voi backend: TODO.


# Bao cao nhiem vu - Minh Tai

Vai tro: Member 5 - Admin Endpoints, Automation, Share va Demo  
Du an: YiYi Bookstore Backend  
Nguon phan cong: jira_tasks(1).pdf

## 1. Muc tieu

Hoan thien folder Admin/Rewards, chay Collection Runner va Newman, tao HTML report, chot quyen Workspace va phoi hop demo ban giao.

## 2. Ke hoach tuan 1

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| MT-W1-01 | Khai bao Admin Users | GET/PUT/DELETE | TODO |
| MT-W1-02 | Khai bao Admin Reviews | GET/PUT | TODO |
| MT-W1-03 | Khai bao Admin Rewards | GET/POST | TODO |
| MT-W1-04 | Khai bao Rewards | GET/POST redeem | TODO |
| MT-W1-05 | Tao Collection Runner draft | Thu tu chay va environment | TODO |
| MT-W1-06 | Phoi hop invite thanh vien | Danh sach thanh vien/quyen | TODO |

## 3. Ke hoach tuan 2

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| MT-W2-01 | Chuan bi data cho Runner | Iteration data khong co secret | TODO |
| MT-W2-02 | Chay Collection Runner | Log tong request/pass/fail | TODO |
| MT-W2-03 | Cai va chay Newman | Terminal log | TODO |
| MT-W2-04 | Export newman-report.html | File HTML mo duoc | TODO |
| MT-W2-05 | Chot Workspace permissions | Invite day du, quyen dung | TODO |
| MT-W2-06 | Tong hop demo va tai lieu | Checklist demo + links | TODO |

## 4. Endpoint phai co

### Admin Users

- [ ] GET /admin/users
- [ ] PUT /admin/users
- [ ] DELETE /admin/users

### Admin Reviews

- [ ] GET /admin/reviews
- [ ] PUT /admin/reviews

### Admin Rewards

- [ ] GET /admin/rewards
- [ ] POST /admin/rewards

### Rewards

- [ ] GET /rewards
- [ ] POST /rewards/redeem

## 5. Test case Admin/Rewards

| Test ID | Request | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-ADM-001 | GET /admin/users voi admin token | 200 | TODO | TODO | TODO |
| TC-ADM-004 | Admin request voi user token | 401/403 theo contract | TODO | TODO | TODO |
| TC-ADM-005 | GET /admin/reviews | 200 | TODO | TODO | TODO |
| TC-ADM-007 | GET /admin/rewards | 200 | TODO | TODO | TODO |
| TC-ADM-008 | POST /admin/rewards | 201/200 | TODO | TODO | TODO |
| TC-REW-001 | GET /rewards | 200 | TODO | TODO | TODO |
| TC-REW-002 | POST /rewards/redeem | 200/201 | TODO | TODO | TODO |

## 6. Collection Runner checklist

- [ ] Chon dung Collection version.
- [ ] Chon dung Local/Docker Environment.
- [ ] Chay Auth Login truoc request can token neu pre-request khong dung.
- [ ] Co data cho bookId, categoryId, orderId hoac dung seed data.
- [ ] Ghi so request, pass, fail, duration.
- [ ] Export log sau khi chay.
- [ ] Doi chieu fail voi Van Dinh truoc khi ket luan coverage.

## 7. Newman checklist

Cai dat:

    npm install -g newman newman-reporter-htmlextra

Chay:

    newman run "YiYi Bookstore API.postman_collection.json" \
      --environment "Local.postman_environment.json" \
      --reporters htmlextra \
      --reporter-htmlextra-export newman-report.html

Ket qua can ghi:

| Lan chay | Collection version | Environment | Requests | PASS | FAIL | Duration | Report |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

Khong commit Environment co password/token that. Neu can chia se, tao file example voi gia tri placeholder.

## 8. Workspace permissions

| Nguoi | Email/tai khoan | Vai tro | Da invite | Da truy cap |
| --- | --- | --- | --- | --- |
| Van Anh | TODO | Member | TODO | TODO |
| Anh Phu | TODO | Member | TODO | TODO |
| Van Thien | TODO | Member | TODO | TODO |
| Van Dinh | TODO | Member | TODO | TODO |
| Minh Tai | TODO | Admin/Editor | TODO | TODO |

## 9. Checklist demo

- [ ] Gioi thieu nhanh cau truc Collection.
- [ ] Chay login va lay token.
- [ ] Chay mot request Books.
- [ ] Chay luong Cart -> Orders.
- [ ] Chay mot Payment request/callback neu co data.
- [ ] Chay mot Admin request.
- [ ] Mo Newman HTML report.
- [ ] Trinh bay coverage, fail va known issue.
- [ ] Gui link README va evidence.

## 10. Ket luan

- Tuan 1: TODO.
- Tuan 2: TODO.
- Newman report: TODO.
- Workspace da share: TODO.
- Known issue can noi trong demo: TODO.


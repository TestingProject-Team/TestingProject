# Bao cao nhiem vu - Van Anh

Vai tro: Member 1 - Setup va Infrastructure  
Du an: YiYi Bookstore Backend  
Nguon phan cong: jira_tasks(1).pdf

## 1. Muc tieu

Dung moi truong backend local on dinh de ca nhom co the chay Docker Compose, goi GET /api/ping va test Postman ma khong phai tu xu ly lai cac loi setup.

## 2. Ke hoach tuan 1

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| VA-W1-01 | Clone source va checkout branch | Branch lam viec dung | TODO |
| VA-W1-02 | Cai JDK 17/21, Docker Desktop, IntelliJ | Cong cu chay duoc | TODO |
| VA-W1-03 | Cau hinh application-local.properties | Profile local dung | TODO |
| VA-W1-04 | Chay docker compose up --build | 3 container running/healthy | TODO |
| VA-W1-05 | Goi GET /api/ping | Ket qua ping va screenshot/log | TODO |
| VA-W1-06 | Ghi loi setup va cap nhat README | Huong dan setup co loi/cach xu ly | TODO |

## 3. Ke hoach tuan 2

| Ma task | Noi dung | Dau ra | Trang thai |
| --- | --- | --- | --- |
| VA-W2-01 | Re-run Docker sau khi collection/backend dong bo | Moi truong van chay sau thay doi | TODO |
| VA-W2-02 | Kiem tra port, database va log 3 container | Bang health-check | TODO |
| VA-W2-03 | Ho tro thanh vien fix blocker moi truong | Danh sach blocker da xu ly | TODO |
| VA-W2-04 | Chot README setup cho nguoi moi | Huong dan tu clone den ping | TODO |
| VA-W2-05 | Cap nhat evidence | Anh/log health-check | TODO |

## 4. Bao cao health-check

| Hang muc | Lenh/cach kiem tra | Expected | Actual | PASS/FAIL | Evidence |
| --- | --- | --- | --- | --- | --- |
| Containers | docker compose ps | 3 container running/healthy | TODO | TODO | TODO |
| Build | docker compose up --build | Khong co build error | TODO | TODO | TODO |
| Ping | GET /api/ping | 200 va body dung contract | TODO | TODO | TODO |
| Port | Kiem tra port backend | Port truy cap duoc | TODO | TODO | TODO |
| Database | Xem log/container health | Khong co loi blocker | TODO | TODO | TODO |

## 5. Loi phat sinh

| Ma loi | Mo ta | Cach tai hien | Cach xu ly | Trang thai |
| --- | --- | --- | --- | --- |
| ENV-001 | TODO | TODO | TODO | Open |
| ENV-002 | TODO | TODO | TODO | Open |

## 6. Evidence can nop

- [ ] Anh docker compose ps.
- [ ] Anh/log GET /api/ping.
- [ ] Log build thanh cong.
- [ ] Danh sach version JDK, Docker, IntelliJ.
- [ ] README setup da cap nhat.
- [ ] Link branch/commit neu co.

## 7. Ket luan

- Tuan 1: TODO.
- Tuan 2: TODO.
- Blocker con lai: TODO.
- De xuat cho nhom: TODO.

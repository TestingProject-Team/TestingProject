# Nhat ky Manual Code Review - YIYI-31

Nguoi thuc hien: Le Minh Tai (GitHub: BryannLee202)

Pham vi: ra soat thu cong bo test va code tich hop cua cac thanh vien, dung backend chay that de doi chieu ket qua voi dac ta API.

## Loi phat hien va da xu ly

| # | Noi dung | Bo cua | Commit |
|---|---|---|---|
| 1 | Loi lap tien to /api trong baseUrl, sot lai tu dot gop truoc | Dinh | 0ee4840 |
| 2 | 3 loi that phat hien tu lan chay co 9/62 test fail | Phu | 6f4473e |
| 3 | Loi HTTP 500 khi chay that: enum sai va xung dot trang thai don hang | chung | e2b353f |
| 4 | Loi that cua Thien va Van Anh, phat hien bang cach dung backend that | Thien, Van Anh | 738689a |
| 5 | Cac loi con lai sau lan chay that | Thien, Dinh, Phu | 66180f9 |
| 6 | Phan body request bi mat khi gop nhanh, da khoi phuc | Phu | 677f09a |
| 7 | 2 loi con sot trong thunder-tests va api-test.http | chung | a760537 |
| 8 | Endpoint sai va noi dung trung lap trong 4 file test-scripts | Dinh | 6c709f6 |
| 9 | Groq API key hardcode trong AIChatWidget, chuyen sang doc tu bien moi truong | frontend | 85da5c1 |
| 10 | Loi anh tai len khong xem duoc, phan Upload con bao do | backend | 46f76c1 |

## Viec don dep kem theo

- Gop 4 collection Postman thanh mot file de chay chung va xuat bao cao: e485451
- Gop thu muc postman, rut environment dung chung: 37f6aa2
- Xoa tai lieu trung lap hoac sai noi dung: 2da8a79, a864523

## Ket luan

Toan bo loi neu tren da duoc sua va merge vao main. Chi tiet thay doi xem trong tung commit tuong ung.


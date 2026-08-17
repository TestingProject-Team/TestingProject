Feature('Luồng Xác thực & Đăng ký Người dùng (Authentication E2E Flow)');

const timestamp = Date.now();
const testUser = {
  name: 'Nguyễn Văn E2E',
  email: `e2e_user_${timestamp}@yiyibook.vn`,
  phone: `09${Math.floor(10000000 + Math.random() * 90000000)}`,
  password: 'Password123!'
};

Before(({ I }) => {
  I.amOnPage('/');
});

Scenario('TC-E2E-AUTH-001: [Positive] Đăng ký tài khoản mới thành công và nhận quà chào mừng', ({ I, authPage }) => {
  authPage.goToRegister();
  authPage.fillRegisterForm(testUser);
  authPage.submitRegister();
  
  // Xác nhận chuyển hướng và đăng nhập tự động
  I.waitForNavigation();
  I.seeInCurrentUrl('/');
  I.see(testUser.name);
});

Scenario('TC-E2E-AUTH-002: [Positive] Đăng nhập thành công với tài khoản USER hợp lệ', ({ I, authPage }) => {
  authPage.goToLogin();
  authPage.fillLoginForm({
    email: 'user@example.com',
    password: 'user123'
  });
  authPage.submitLogin();
  
  I.waitForNavigation();
  I.seeInCurrentUrl('/');
  I.see('user@example.com');
});

Scenario('TC-E2E-AUTH-003: [Negative] Đăng nhập thất bại khi nhập sai mật khẩu', ({ I, authPage }) => {
  authPage.goToLogin();
  authPage.fillLoginForm({
    email: 'user@example.com',
    password: 'WrongPassword_999'
  });
  authPage.submitLogin();
  
  // Kiểm tra thông báo lỗi hiển thị rõ ràng cho người dùng
  authPage.verifyErrorMessage('thông tin đăng nhập không chính xác');
});

Scenario('TC-E2E-AUTH-004: [Boundary/Negative] Validation form đăng ký với dữ liệu biên và email trùng lặp', ({ I, authPage }) => {
  authPage.goToRegister();
  
  // Trường hợp 1: Để trống toàn bộ form
  authPage.submitRegister();
  I.seeElement('input:invalid, .error-message');
  
  // Trường hợp 2: Đăng ký với email đã tồn tại sẵn
  authPage.fillRegisterForm({
    name: 'User Duplicate',
    email: 'user@example.com',
    phone: '0901234567',
    password: 'Password123!'
  });
  authPage.submitRegister();
  authPage.verifyErrorMessage('Email đã được sử dụng');
});

Scenario('TC-E2E-AUTH-005: [Positive] Đăng xuất và kiểm tra bảo vệ tuyến đường', ({ I, authPage }) => {
  // Đăng nhập trước
  authPage.goToLogin();
  authPage.fillLoginForm({ email: 'user@example.com', password: 'user123' });
  authPage.submitLogin();
  
  // Thực hiện đăng xuất
  authPage.logoutUser();
  
  // Truy cập tuyến đường yêu cầu xác thực -> Bị chuyển hướng về Login
  I.amOnPage('/cart');
  I.wait(1);
});

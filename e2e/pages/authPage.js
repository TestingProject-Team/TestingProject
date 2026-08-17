const { I } = inject();

module.exports = {
  // Locators
  fields: {
    name: 'input[name="name"], input[placeholder*="Họ và tên"]',
    email: 'input[name="email"], input[type="email"]',
    phone: 'input[name="phone"], input[type="tel"]',
    password: 'input[name="password"], input[type="password"]',
    confirmPassword: 'input[name="confirmPassword"]'
  },
  buttons: {
    submitRegister: 'button[type="submit"]:has-text("Đăng ký"), button:has-text("Tạo tài khoản")',
    submitLogin: 'button[type="submit"]:has-text("Đăng nhập"), button:has-text("Login")',
    userMenu: '[data-testid="user-menu-btn"], .user-avatar, .account-dropdown',
    logout: 'button:has-text("Đăng xuất"), a:has-text("Đăng xuất")'
  },
  alerts: {
    error: '.alert-danger, .error-message, [role="alert"], .text-red-500',
    successToast: '.toast-success, .alert-success, [data-testid="toast-success"]',
    welcomeBanner: '.welcome-gift-banner, [data-testid="welcome-y-points"]'
  },

  // Actions
  goToRegister() {
    I.amOnPage('/register');
    I.waitForElement(this.fields.email, 5);
  },

  goToLogin() {
    I.amOnPage('/login');
    I.waitForElement(this.fields.email, 5);
  },

  fillRegisterForm({ name, email, phone, password }) {
    if (name) I.fillField(this.fields.name, name);
    if (email) I.fillField(this.fields.email, email);
    if (phone) I.fillField(this.fields.phone, phone);
    if (password) I.fillField(this.fields.password, password);
  },

  submitRegister() {
    I.click(this.buttons.submitRegister);
  },

  fillLoginForm({ email, password }) {
    if (email) I.fillField(this.fields.email, email);
    if (password) I.fillField(this.fields.password, password);
  },

  submitLogin() {
    I.click(this.buttons.submitLogin);
  },

  verifyLoginSuccess(expectedName) {
    I.waitForNavigation();
    I.seeInCurrentUrl('/');
    if (expectedName) {
      I.see(expectedName);
    }
  },

  verifyErrorMessage(expectedText) {
    I.waitForElement(this.alerts.error, 5);
    I.see(expectedText, this.alerts.error);
  },

  logoutUser() {
    I.click(this.buttons.userMenu);
    I.click(this.buttons.logout);
    I.waitForNavigation();
    I.see('Đăng nhập');
  }
};

const Helper = require('@codeceptjs/helper');

class CustomHelper extends Helper {
  /**
   * Chụp ảnh màn hình tùy chỉnh và gắn metadata
   * @param {string} testName 
   */
  async captureCustomScreenshot(testName) {
    const playwright = this.helpers['Playwright'];
    if (playwright && playwright.page) {
      const sanitizedName = testName.replace(/[^a-zA-Z0-9_-]/g, '_');
      const screenshotPath = `./output/${Date.now()}_${sanitizedName}.png`;
      await playwright.page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`[CustomHelper] Đã chụp ảnh màn hình lưu tại: ${screenshotPath}`);
      return screenshotPath;
    }
    return null;
  }

  /**
   * Xóa sạch localStorage và cookies trước mỗi bài kiểm thử
   */
  async clearSession() {
    const playwright = this.helpers['Playwright'];
    if (playwright && playwright.page) {
      await playwright.page.evaluate(() => {
        localStorage.clear();
        sessionStorage.clear();
      });
      await playwright.page.context().clearCookies();
      console.log('[CustomHelper] Đã dọn sạch session/localStorage/cookies.');
    }
  }

  /**
   * Lấy giá trị token hiện tại từ localStorage
   */
  async getAuthToken() {
    const playwright = this.helpers['Playwright'];
    if (playwright && playwright.page) {
      return await playwright.page.evaluate(() => {
        return localStorage.getItem('token') || localStorage.getItem('authToken');
      });
    }
    return null;
  }
}

module.exports = CustomHelper;

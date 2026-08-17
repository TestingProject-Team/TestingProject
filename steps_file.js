// in this file you can append custom step methods to 'I' object

module.exports = function() {
  return actor({

    // Luồng đăng nhập
    login: function(email, password) {
      this.amOnPage('/login');
      this.fillField('input[type="email"], input[name="email"]', email);
      this.fillField('input[type="password"], input[name="password"]', password);
      this.click('button[type="submit"]');
      this.wait(2);
    },

    // Luồng đăng xuất
    logout: function() {
      this.click('[data-testid="user-menu"], .user-avatar, button:has-text("Đăng xuất")');
      this.wait(1);
    },

    // Luồng tìm kiếm sách
    searchBook: function(keyword) {
      this.amOnPage('/books');
      this.fillField('input[placeholder*="Tìm kiếm"], input[name="search"]', keyword);
      this.pressKey('Enter');
      this.wait(2);
    },

    // Luồng thêm vào giỏ hàng
    addBookToCart: function(bookIndex = 1) {
      this.amOnPage('/books');
      this.wait(2);
      this.click(`(//button[contains(text(), "Thêm vào giỏ") or contains(text(), "Mua ngay")])[${bookIndex}]`);
      this.wait(1);
    },

    // Mở khung trò chuyện YiYi AI
    openAIChatWidget: function() {
      this.click('[data-testid="ai-chat-trigger"], button[aria-label="Chat AI"], .ai-chat-bubble');
      this.waitForElement('.ai-chat-window, [data-testid="ai-chat-modal"]', 5);
    },

    // Gửi câu hỏi cho AI
    askYiYiAI: function(promptText) {
      this.fillField('.ai-chat-input textarea, input[placeholder*="Hỏi YiYi"]', promptText);
      this.click('.ai-chat-send-btn, button:has-text("Gửi")');
      this.wait(3);
    }
  });
};

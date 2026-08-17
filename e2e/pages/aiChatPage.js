const { I } = inject();

module.exports = {
  // Locators
  widget: {
    triggerBtn: '[data-testid="ai-chat-trigger"], button[aria-label="Chat AI"], .ai-chat-button',
    container: '.ai-chat-window, [data-testid="ai-chat-widget"]',
    header: '.ai-chat-header',
    closeBtn: '.ai-chat-close-btn, button[aria-label="Close chat"]',
    messageList: '.ai-chat-messages-list, [data-testid="chat-history"]',
    userMessage: '.message-bubble-user',
    botMessage: '.message-bubble-ai, .message-bubble-bot',
    inputArea: 'textarea[placeholder*="Hỏi YiYi"], input.ai-chat-input-field',
    sendBtn: 'button.ai-chat-send-btn, button[aria-label="Send message"]',
    typingIndicator: '.ai-typing-indicator, .ai-streaming-pulse',
    recommendedBooks: '.ai-recommended-book-chip, [data-testid="ai-book-card"]',
    fallbackNotice: '.ai-fallback-alert, [data-testid="ai-fallback-banner"]',
    clearHistoryBtn: 'button.btn-clear-chat-history, [data-testid="clear-history-btn"]'
  },

  // Actions
  openWidget() {
    I.click(this.widget.triggerBtn);
    I.waitForElement(this.widget.container, 5);
  },

  closeWidget() {
    I.click(this.widget.closeBtn);
    I.waitForInvisible(this.widget.container, 5);
  },

  sendMessage(text) {
    I.fillField(this.widget.inputArea, text);
    I.click(this.widget.sendBtn);
  },

  verifyBotResponseContains(expectedText) {
    I.waitForElement(this.widget.botMessage, 10);
    I.see(expectedText, this.widget.messageList);
  },

  verifyRecommendedProductsVisible() {
    I.waitForElement(this.widget.recommendedBooks, 8);
    I.seeElement(this.widget.recommendedBooks);
  },

  verifyFallbackWarningShown() {
    I.waitForElement(this.widget.fallbackNotice, 5);
  },

  clearChatHistory() {
    I.click(this.widget.clearHistoryBtn);
    I.wait(1);
    I.dontSeeElement(this.widget.userMessage);
  }
};

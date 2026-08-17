Feature('Luồng Tìm kiếm Sản phẩm & Trò chuyện YiYi AI (Search & AI Assistant E2E Flow)');

Before(({ I }) => {
  I.amOnPage('/');
});

Scenario('TC-E2E-SEARCH-001: [Positive] Tìm kiếm sách theo từ khóa tên sách và lọc theo danh mục', ({ I, productPage }) => {
  productPage.goToCatalog();
  
  // Tìm kiếm sách theo tên
  productPage.searchBooks('Đắc Nhân Tâm');
  productPage.verifySearchResultsContains('Đắc Nhân Tâm');
  
  // Lọc theo danh mục
  productPage.filterByCategory('Kinh tế');
  I.wait(1);
  I.seeInCurrentUrl('category=');
});

Scenario('TC-E2E-SEARCH-002: [Boundary] Tìm kiếm với chuỗi không tồn tại / ký tự đặc biệt', ({ I, productPage }) => {
  productPage.goToCatalog();
  
  // Tìm kiếm với chuỗi vô nghĩa
  productPage.searchBooks('xyz_non_existent_book_12345!@#');
  productPage.verifyEmptySearchResult();
});

Scenario('TC-E2E-AI-001: [Positive] Mở trợ lý ảo YiYi AI và hỏi tư vấn gợi ý sách (Client-side RAG)', ({ I, aiChatPage }) => {
  aiChatPage.openWidget();
  
  // Gửi câu hỏi tư vấn sách phát triển bản thân
  aiChatPage.sendMessage('Gợi ý cho tôi 2 cuốn sách hay về kỹ năng sống và tư duy');
  
  // Kiểm tra trợ lý AI bắt được intent và trả lời
  aiChatPage.verifyBotResponseContains('YiYi');
  aiChatPage.closeWidget();
});

Scenario('TC-E2E-AI-002: [Positive] Kiểm tra khả năng gợi ý sản phẩm và khớp context kho sách', ({ I, aiChatPage }) => {
  aiChatPage.openWidget();
  
  // Hỏi trực tiếp về giá và tồn kho
  aiChatPage.sendMessage('Nhà sách có cuốn Đắc Nhân Tâm không, giá bao nhiêu?');
  
  // AI trích xuất thực thể và đưa ra thông tin liên quan
  I.wait(2);
  aiChatPage.verifyBotResponseContains('Đắc Nhân Tâm');
  aiChatPage.closeWidget();
});

Scenario('TC-E2E-AI-003: [Negative/Fallback] Kiểm tra cơ chế Fallback khi không có API Key Groq', ({ I, aiChatPage }) => {
  aiChatPage.openWidget();
  
  // Giả lập trạng thái khi Groq API trả lỗi hoặc chưa cấu hình key
  I.executeScript(() => {
    window.sessionStorage.setItem('FORCE_AI_FALLBACK', 'true');
  });
  
  aiChatPage.sendMessage('Xin chào');
  I.wait(1);
  
  // Kiểm tra không làm sập giao diện người dùng
  I.seeElement('.ai-chat-window');
  aiChatPage.closeWidget();
});

Scenario('TC-E2E-AI-004: [Positive] Kiểm tra tính năng xóa lịch sử trò chuyện (Clear History)', ({ I, aiChatPage }) => {
  aiChatPage.openWidget();
  aiChatPage.sendMessage('Tin nhắn thử nghiệm cần xóa');
  I.wait(1);
  
  // Thực hiện xóa lịch sử
  aiChatPage.clearChatHistory();
  
  // Đóng và mở lại widget -> Lịch sử đã được reset
  aiChatPage.closeWidget();
  aiChatPage.openWidget();
  I.dontSee('Tin nhắn thử nghiệm cần xóa');
});

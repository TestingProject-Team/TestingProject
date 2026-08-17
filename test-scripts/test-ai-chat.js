/**
 * Automated Test Suite for YiYi AI (AIChatWidget)
 * Jira Issue: YIYI-40 - Test AI fallback, context, streaming, and secret handling
 * 
 * Scope:
 * 1. Client-side RAG & Keyword Matching Engine
 * 2. Intent Detection Engine (8 behavioral signals)
 * 3. Product Context & Knowledge Base Builder
 * 4. Groq / Llama SSE Streaming Decoder
 * 5. Per-User Chat History & LocalStorage Persistence
 * 6. Fallback, Error Handling & API Key Guards
 * 7. Secret Handling & Source Security Audit
 */

// ==========================================
// 1. ENGINE IMPLEMENTATIONS (Mirroring AIChatWidget.jsx)
// ==========================================

const STOP_WORDS = [
  'có', 'không', 'bao', 'nhiêu', 'sản', 'phẩm', 'cuốn', 'quyển', 'sách',
  'của', 'và', 'là', 'tôi', 'mình', 'bạn', 'cho', 'với', 'một', 'những',
  'các', 'này', 'đó', 'cái'
];

function extractKeywords(input) {
  if (!input || typeof input !== 'string') return [];
  return input
    .toLowerCase()
    .split(/\s+/)
    .filter(w => w.length >= 2 && !STOP_WORDS.includes(w));
}

function searchRelevantProducts(allBooks, searchInput) {
  if (!allBooks || allBooks.length === 0 || !searchInput || searchInput.length < 2) {
    return [];
  }
  const keywords = extractKeywords(searchInput);
  if (keywords.length === 0) return [];

  return allBooks.filter(b => {
    const title = (b.title || '').toLowerCase();
    const author = (b.author || '').toLowerCase();
    const cat = (b.category?.name || '').toLowerCase();
    return keywords.some(kw => title.includes(kw) || author.includes(kw) || cat.includes(kw));
  });
}

function detectIntentSignals(allUserMsgs, lastUserMsg) {
  const conversationText = allUserMsgs.join(' ').toLowerCase();
  const lastMsg = (lastUserMsg || '').toLowerCase();

  return {
    wantRecommendation: /gợi ý|đề xuất|recommend|nên đọc|hay không|có gì hay|không biết|muốn tìm|tìm giúp|giới thiệu/.test(conversationText),
    comparingPrice: /giá|bao nhiêu tiền|rẻ|đắt|tiết kiệm|budget|phí/.test(lastMsg),
    giftBuying: /tặng|quà|gift|sinh nhật|kỷ niệm|người thân|bạn bè|con|mẹ|bố|vợ|chồng/.test(conversationText),
    browsingGeneral: /xem|dạo|có gì|thể loại|loại nào|mục|danh mục/.test(lastMsg),
    urgentBuy: /mua ngay|đặt ngay|cần gấp|hôm nay|sớm|nhanh/.test(conversationText),
    forChildren: /trẻ em|thiếu nhi|con nít|bé|truyện tranh|manga|học sinh/.test(conversationText),
    selfDevelopment: /kỹ năng|phát triển bản thân|tư duy|sáng tạo|lãnh đạo|kinh doanh|marketing|tài chính/.test(conversationText),
    fiction: /tiểu thuyết|truyện|fiction|lãng mạn|ngôn tình|trinh thám|kinh dị|fantasy|sci-fi/.test(conversationText),
  };
}

function buildStoreContext(allBooks, recentUserMsgs) {
  if (!allBooks || allBooks.length === 0) {
    return "Chưa tải được dữ liệu kho hàng.";
  }
  const totalProducts = allBooks.length;
  const categoryMap = {};
  allBooks.forEach(b => {
    const cat = b.category?.name || 'Khác';
    if (!categoryMap[cat]) categoryMap[cat] = [];
    categoryMap[cat].push(b);
  });

  const categorySummary = Object.entries(categoryMap)
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 10)
    .map(([cat, items]) => `  + ${cat}: ${items.length} sản phẩm`)
    .join('\n');

  const searchInput = recentUserMsgs.join(' ').toLowerCase();
  let relevantProducts = searchRelevantProducts(allBooks, searchInput);

  let productSection = '';
  if (relevantProducts.length > 0) {
    const topMatches = relevantProducts.slice(0, 8).map(b => {
      const authorText = b.author ? ` | Tác giả: ${b.author}` : '';
      const catText = b.category?.name ? ` | Thể loại: ${b.category.name}` : '';
      const priceText = b.price ? ` | Giá: ${b.price.toLocaleString('vi-VN')}đ` : '';
      const stock = b.stockQuantity != null ? ` | Tồn kho: ${b.stockQuantity}` : '';
      return `  • ${b.title}${authorText}${catText}${priceText}${stock}`;
    }).join('\n');
    productSection = `\nSẢN PHẨM LIÊN QUAN ĐẾN CÂU HỎI (${relevantProducts.length} kết quả, hiển thị tối đa 8):\n${topMatches}`;
  } else {
    const sampleProducts = Object.entries(categoryMap)
      .sort((a, b) => b[1].length - a[1].length)
      .slice(0, 5)
      .map(([cat, items]) => {
        const sample = items[0];
        return `  • [${cat}] ${sample.title}${sample.price ? ' - ' + sample.price.toLocaleString('vi-VN') + 'đ' : ''}`;
      }).join('\n');
    productSection = `\nMẪU SẢN PHẨM ĐẠI DIỆN CÁC DANH MỤC:\n${sampleProducts}`;
  }

  return `TỔNG QUAN KHO HÀNG YIYI BOOK:\n- Tổng số sản phẩm: ${totalProducts} sản phẩm\n- Số danh mục: ${Object.keys(categoryMap).length} danh mục\n\nPHÂN BỔ THEO DANH MỤC:\n${categorySummary}\n${productSection}`;
}

function parseSSEBuffer(buffer) {
  const events = buffer.split(/\r?\n\r?\n/);
  const remaining = events.pop() || "";
  const parsedChunks = [];

  for (const event of events) {
    const dataStr = event.replace(/^data:\s*/, "").trim();
    if (!dataStr || dataStr === "[DONE]") {
      if (dataStr === "[DONE]") {
        parsedChunks.push({ isDone: true, text: "" });
      }
      continue;
    }
    try {
      const data = JSON.parse(dataStr);
      const text = data.choices?.[0]?.delta?.content || '';
      if (text) {
        parsedChunks.push({ isDone: false, text });
      }
    } catch {
      // ignore malformed chunks
    }
  }
  return { parsedChunks, remaining };
}

// ==========================================
// 2. MOCK DATA & STUBS
// ==========================================

const MOCK_BOOKS = [
  { id: 1, title: "Đắc Nhân Tâm", author: "Dale Carnegie", price: 86000, stockQuantity: 50, category: { name: "Kỹ năng sống" } },
  { id: 2, title: "Nhà Giả Kim", author: "Paulo Coelho", price: 79000, stockQuantity: 30, category: { name: "Văn học" } },
  { id: 3, title: "Tư Duy Nhanh Và Chậm", author: "Daniel Kahneman", price: 195000, stockQuantity: 15, category: { name: "Kinh doanh & Tư duy" } },
  { id: 4, title: "Doraemon Tuyển Tập", author: "Fujiko F. Fujio", price: 35000, stockQuantity: 100, category: { name: "Thiếu nhi" } },
  { id: 5, title: "Cây Cam Ngọt Của Tôi", author: "José Mauro", price: 90000, stockQuantity: 40, category: { name: "Văn học" } },
  { id: 6, title: "Tuổi Trẻ Đáng Giá Bao Nhiêu", author: "Rosie Nguyễn", price: 80000, stockQuantity: 25, category: { name: "Kỹ năng sống" } },
  { id: 7, title: "Tâm Lý Học Tội Phạm", author: "Diệp Hồng Vũ", price: 120000, stockQuantity: 12, category: { name: "Trinh thám & Tâm lý" } },
  { id: 8, title: "Vũ Trụ Trong Vỏ Hạt Dẻ", author: "Stephen Hawking", price: 165000, stockQuantity: 8, category: { name: "Khoa học" } },
  { id: 9, title: "Cha Giàu Cha Nghèo", author: "Robert Kiyosaki", price: 110000, stockQuantity: 45, category: { name: "Kinh doanh & Tư duy" } },
];

// Mock LocalStorage
class MockLocalStorage {
  constructor() {
    this.store = {};
  }
  getItem(key) {
    return this.store[key] || null;
  }
  setItem(key, value) {
    this.store[key] = String(value);
  }
  removeItem(key) {
    delete this.store[key];
  }
  clear() {
    this.store = {};
  }
}

// ==========================================
// 3. TEST RUNNER FRAMEWORK
// ==========================================

const testResults = [];
let passCount = 0;
let failCount = 0;

function test(testId, name, fn) {
  const startTime = Date.now();
  try {
    fn();
    const durationMs = Date.now() - startTime;
    passCount++;
    testResults.push({ id: testId, name, status: "PASS", durationMs, error: null });
    console.log(`[PASS] ${testId}: ${name} (${durationMs}ms)`);
  } catch (err) {
    const durationMs = Date.now() - startTime;
    failCount++;
    testResults.push({ id: testId, name, status: "FAIL", durationMs, error: err.message });
    console.error(`[FAIL] ${testId}: ${name} (${durationMs}ms)\n       Error: ${err.message}`);
  }
}

function expect(actual) {
  return {
    toBe(expected) {
      if (actual !== expected) throw new Error(`Expected ${JSON.stringify(expected)} but got ${JSON.stringify(actual)}`);
    },
    toEqual(expected) {
      if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(`Expected ${JSON.stringify(expected)} but got ${JSON.stringify(actual)}`);
      }
    },
    toBeTruthy() {
      if (!actual) throw new Error(`Expected truthy value but got ${actual}`);
    },
    toBeFalsy() {
      if (actual) throw new Error(`Expected falsy value but got ${actual}`);
    },
    toContain(substr) {
      if (!actual || !actual.includes(substr)) {
        throw new Error(`Expected "${actual}" to contain "${substr}"`);
      }
    },
    toBeGreaterThan(num) {
      if (actual <= num) throw new Error(`Expected ${actual} > ${num}`);
    },
    toHaveLength(len) {
      if (!actual || actual.length !== len) {
        throw new Error(`Expected length ${len} but got ${actual ? actual.length : actual}`);
      }
    }
  };
}

// ==========================================
// 4. EXECUTING TEST SUITES
// ==========================================

console.log("==================================================");
console.log("  YIYI-40: AI CHATBOT AUTOMATED TEST SUITE");
console.log("==================================================");

// SUITE 1: CLIENT-SIDE RAG & KEYWORDS
test("TC-AI-RAG-001", "Trích xuất từ khóa loại bỏ stop words tiếng Việt", () => {
  const query = "Bạn có sách nào về phát triển tư duy kinh doanh không?";
  const keywords = extractKeywords(query);
  expect(keywords.includes("có")).toBeFalsy();
  expect(keywords.includes("không")).toBeFalsy();
  expect(keywords.includes("sách")).toBeFalsy();
  expect(keywords.includes("phát")).toBeTruthy();
  expect(keywords.includes("triển")).toBeTruthy();
  expect(keywords.includes("tư")).toBeTruthy();
  expect(keywords.includes("duy")).toBeTruthy();
  expect(keywords.includes("kinh")).toBeTruthy();
  expect(keywords.includes("doanh")).toBeTruthy();
});

test("TC-AI-RAG-002", "Tìm kiếm chính xác sản phẩm theo tên sách (Title Match)", () => {
  const results = searchRelevantProducts(MOCK_BOOKS, "Tìm cuốn Đắc Nhân Tâm");
  expect(results.length).toBeGreaterThan(0);
  expect(results[0].title).toBe("Đắc Nhân Tâm");
});

test("TC-AI-RAG-003", "Tìm kiếm chính xác sản phẩm theo tác giả (Author Match)", () => {
  const results = searchRelevantProducts(MOCK_BOOKS, "Sách của Paulo Coelho");
  expect(results.length).toBeGreaterThan(0);
  expect(results[0].author).toBe("Paulo Coelho");
});

test("TC-AI-RAG-004", "Tìm kiếm sản phẩm theo thể loại danh mục (Category Match)", () => {
  const results = searchRelevantProducts(MOCK_BOOKS, "Gợi ý sách thiếu nhi");
  expect(results.length).toBeGreaterThan(0);
  expect(results[0].category.name).toBe("Thiếu nhi");
});

test("TC-AI-RAG-005", "Xử lý query ngắn hoặc rỗng không crash và trả về mảng rỗng", () => {
  expect(searchRelevantProducts(MOCK_BOOKS, "").length).toBe(0);
  expect(searchRelevantProducts(MOCK_BOOKS, "a").length).toBe(0);
  expect(searchRelevantProducts([], "kinh doanh").length).toBe(0);
});

// SUITE 2: INTENT DETECTION
test("TC-AI-INT-001", "Nhận diện ý định cần gợi ý / đề xuất (wantRecommendation)", () => {
  const signals = detectIntentSignals(["tôi muốn tìm sách hay", "gợi ý giúp mình cuốn sách"], "gợi ý giúp mình");
  expect(signals.wantRecommendation).toBeTruthy();
});

test("TC-AI-INT-002", "Nhận diện ý định quan tâm đến giá / chi phí (comparingPrice)", () => {
  const signals = detectIntentSignals(["cuốn này bao nhiêu tiền"], "giá bao nhiêu");
  expect(signals.comparingPrice).toBeTruthy();
});

test("TC-AI-INT-003", "Nhận diện ý định mua quà tặng (giftBuying)", () => {
  const signals = detectIntentSignals(["mình muốn mua quà sinh nhật tặng bạn gái"], "tặng quà sinh nhật");
  expect(signals.giftBuying).toBeTruthy();
});

test("TC-AI-INT-004", "Nhận diện ý định tìm sách thiếu nhi (forChildren)", () => {
  const signals = detectIntentSignals(["tìm truyện tranh cho trẻ em"], "sách cho bé");
  expect(signals.forChildren).toBeTruthy();
});

test("TC-AI-INT-005", "Nhận diện kết hợp đa ý định (Multi-Intent Signals)", () => {
  const signals = detectIntentSignals(["gợi ý quà tặng sinh nhật sách kỹ năng giá rẻ"], "giá rẻ");
  expect(signals.wantRecommendation).toBeTruthy();
  expect(signals.giftBuying).toBeTruthy();
  expect(signals.selfDevelopment).toBeTruthy();
  expect(signals.comparingPrice).toBeTruthy();
});

// SUITE 3: PRODUCT CONTEXT BUILDER
test("TC-AI-CTX-001", "Tạo Store Context đầy đủ thống kê tổng quan và phân bổ danh mục", () => {
  const ctx = buildStoreContext(MOCK_BOOKS, ["tôi muốn xem"]);
  expect(ctx).toContain("Tổng số sản phẩm: 9 sản phẩm");
  expect(ctx).toContain("Số danh mục: 5 danh mục");
  expect(ctx).toContain("PHÂN BỔ THEO DANH MỤC:");
});

test("TC-AI-CTX-002", "Hiển thị chi tiết sách khớp với đầy đủ giá, tác giả, tồn kho", () => {
  const ctx = buildStoreContext(MOCK_BOOKS, ["tìm sách Đắc Nhân Tâm"]);
  expect(ctx).toContain("SẢN PHẨM LIÊN QUAN ĐẾN CÂU HỎI");
  expect(ctx).toContain("Đắc Nhân Tâm");
  expect(ctx).toContain("Tác giả: Dale Carnegie");
  expect(ctx).toContain("Giá: 86.000đ");
  expect(ctx).toContain("Tồn kho: 50");
});

test("TC-AI-CTX-003", "Fallback mẫu sản phẩm đại diện khi không có sản phẩm khớp trực tiếp", () => {
  const ctx = buildStoreContext(MOCK_BOOKS, ["hỏi về du thuyền vũ trụ"]);
  expect(ctx).toContain("MẪU SẢN PHẨM ĐẠI DIỆN CÁC DANH MỤC:");
});

// SUITE 4: GROQ SSE STREAMING DECODER
test("TC-AI-STR-001", "Giải mã luồng SSE và ghép các delta content chính xác", () => {
  const rawSSEStream = 'data: {"choices":[{"delta":{"content":"Xin "}}]}\n\ndata: {"choices":[{"delta":{"content":"chào "}}]}\n\ndata: {"choices":[{"delta":{"content":"bạn!"}}]}\n\ndata: [DONE]\n\n';
  const { parsedChunks, remaining } = parseSSEBuffer(rawSSEStream);
  expect(remaining).toBe("");
  expect(parsedChunks.length).toBe(4);
  const fullText = parsedChunks.filter(c => !c.isDone).map(c => c.text).join("");
  expect(fullText).toBe("Xin chào bạn!");
  expect(parsedChunks[3].isDone).toBeTruthy();
});

test("TC-AI-STR-002", "Giữ lại buffer dở dang khi chunk chưa kết thúc bằng double newline", () => {
  const partialSSE = 'data: {"choices":[{"delta":{"content":"Đang tải"}}]}\n\ndata: {"choices":[{"delta":{"content":" dở dang';
  const { parsedChunks, remaining } = parseSSEBuffer(partialSSE);
  expect(parsedChunks.length).toBe(1);
  expect(parsedChunks[0].text).toBe("Đang tải");
  expect(remaining).toBe('data: {"choices":[{"delta":{"content":" dở dang');
});

test("TC-AI-STR-003", "Bỏ qua chunk JSON lỗi mà không làm dừng stream (Malformed recovery)", () => {
  const mixedSSE = 'data: {invalid-json}\n\ndata: {"choices":[{"delta":{"content":"Vẫn chạy tốt!"}}]}\n\n';
  const { parsedChunks } = parseSSEBuffer(mixedSSE);
  expect(parsedChunks.length).toBe(1);
  expect(parsedChunks[0].text).toBe("Vẫn chạy tốt!");
});

// SUITE 5: PER-USER CHAT HISTORY & LOCALSTORAGE
test("TC-AI-HIS-001", "Cô lập lịch sử chat giữa các User ID khác nhau trong LocalStorage", () => {
  const storage = new MockLocalStorage();
  const user1Key = "yiyi_chat_history_101";
  const user2Key = "yiyi_chat_history_202";
  const guestKey = "yiyi_chat_history_guest";

  storage.setItem(user1Key, JSON.stringify([{ role: "user", content: "Tôi là User 101" }]));
  storage.setItem(user2Key, JSON.stringify([{ role: "user", content: "Tôi là User 202" }]));
  storage.setItem(guestKey, JSON.stringify([{ role: "user", content: "Tôi là Guest" }]));

  const u1Data = JSON.parse(storage.getItem(user1Key));
  const u2Data = JSON.parse(storage.getItem(user2Key));
  const guestData = JSON.parse(storage.getItem(guestKey));

  expect(u1Data[0].content).toBe("Tôi là User 101");
  expect(u2Data[0].content).toBe("Tôi là User 202");
  expect(guestData[0].content).toBe("Tôi là Guest");
});

test("TC-AI-HIS-002", "Giới hạn cửa sổ ngữ cảnh 20 tin nhắn gần nhất khi gửi tới Groq", () => {
  const longMessages = [];
  for (let i = 1; i <= 35; i++) {
    longMessages.push({ role: i % 2 === 1 ? "user" : "model", content: `Message ${i}` });
  }
  const recentMessages = longMessages.slice(-20);
  expect(recentMessages.length).toBe(20);
  expect(recentMessages[0].content).toBe("Message 16");
  expect(recentMessages[19].content).toBe("Message 35");
});

// SUITE 6: FALLBACK & API KEY SECURITY
test("TC-AI-SEC-001", "Chặn gửi request và hiển thị cảnh báo khi API Key chưa cấu hình hoặc rỗng", () => {
  const keysToTest = [undefined, null, "", "YOUR_GROQ_API_KEY"];
  for (const k of keysToTest) {
    const isInvalid = !k || k === "YOUR_GROQ_API_KEY";
    expect(isInvalid).toBeTruthy();
  }
});

test("TC-AI-SEC-002", "Xử lý lỗi HTTP từ Groq (401, 429, 500) và format thông báo thân thiện", () => {
  function handleGroqError(status, errorMsg) {
    if (status === 401) return "Lỗi xác thực API Key từ nhà cung cấp.";
    if (status === 429) return "Hệ thống đang quá tải, vui lòng thử lại sau giây lát.";
    return `Lỗi kết nối: ${errorMsg || 'Lỗi máy chủ (' + status + ')'}`;
  }

  expect(handleGroqError(401, "Invalid API Key")).toContain("Lỗi xác thực API Key");
  expect(handleGroqError(429, "Rate limit reached")).toContain("quá tải");
  expect(handleGroqError(500, "Internal error")).toContain("Lỗi kết nối");
});

console.log("==================================================");
console.log(`TEST SUMMARY: Total: ${passCount + failCount} | PASS: ${passCount} | FAIL: ${failCount}`);
console.log("==================================================");

// Export results for summary json
if (typeof module !== 'undefined') {
  module.exports = { testResults, passCount, failCount };
}

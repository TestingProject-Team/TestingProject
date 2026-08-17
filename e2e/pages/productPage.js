const { I } = inject();

module.exports = {
  // Locators
  search: {
    input: 'input[placeholder*="Tìm kiếm sách"], input[name="searchQuery"], #search-input',
    button: 'button[aria-label="Search"], .search-btn, button:has-text("Tìm")',
    resultsContainer: '.book-grid, .product-list, [data-testid="search-results"]',
    bookCard: '.book-card, .product-card, [data-testid="book-item"]',
    emptyState: '.no-results-found, .empty-state, [data-testid="empty-search"]'
  },
  filters: {
    categoryItem: '.category-item, .filter-chip',
    sortDropdown: 'select[name="sortBy"], .sort-select',
    priceMin: 'input[name="minPrice"]',
    priceMax: 'input[name="maxPrice"]'
  },
  details: {
    title: '.book-detail-title, h1.product-title',
    price: '.book-detail-price, .price-tag',
    stock: '.stock-status, .badge-stock',
    quantityInput: 'input[type="number"].quantity-input, [name="qty"]',
    addToCartBtn: 'button:has-text("Thêm vào giỏ hàng"), button.btn-add-cart',
    buyNowBtn: 'button:has-text("Mua ngay"), button.btn-buy-now'
  },

  // Actions
  goToCatalog() {
    I.amOnPage('/books');
    I.waitForElement(this.search.input, 5);
  },

  searchBooks(keyword) {
    I.fillField(this.search.input, keyword);
    I.pressKey('Enter');
    I.wait(1);
  },

  filterByCategory(categoryName) {
    I.click(`//button[contains(text(), "${categoryName}")] | //a[contains(text(), "${categoryName}")]`);
    I.wait(1);
  },

  viewFirstBookDetail() {
    I.click(`${this.search.bookCard}:first-child`);
    I.waitForElement(this.details.title, 5);
  },

  addToCartFromDetail(quantity = 1) {
    if (quantity > 1) {
      I.fillField(this.details.quantityInput, quantity);
    }
    I.click(this.details.addToCartBtn);
    I.waitForElement('.toast-success, [data-testid="toast-cart-success"]', 5);
  },

  verifySearchResultsContains(bookTitle) {
    I.waitForElement(this.search.bookCard, 5);
    I.see(bookTitle, this.search.resultsContainer);
  },

  verifyEmptySearchResult() {
    I.waitForElement(this.search.emptyState, 5);
    I.see('Không tìm thấy sách phù hợp', this.search.emptyState);
  }
};

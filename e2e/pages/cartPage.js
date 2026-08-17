const { I } = inject();

module.exports = {
  // Locators
  cart: {
    container: '.cart-page-container, [data-testid="cart-container"]',
    emptyCartNotice: '.empty-cart-message, [data-testid="empty-cart"]',
    itemRow: '.cart-item-row, [data-testid="cart-item"]',
    qtyInput: 'input.cart-qty-input',
    btnIncrease: 'button.btn-increase-qty, button:has-text("+")',
    btnDecrease: 'button.btn-decrease-qty, button:has-text("-")',
    btnRemove: 'button.btn-remove-item, button[aria-label="Xóa"]',
    couponInput: 'input[name="couponCode"], input[placeholder*="Mã giảm giá"]',
    btnApplyCoupon: 'button:has-text("Áp dụng"), button.btn-apply-coupon',
    discountAmount: '.discount-value, [data-testid="discount-amount"]',
    totalPrice: '.total-price-value, [data-testid="total-cart-price"]',
    btnProceedCheckout: 'button:has-text("Tiến hành thanh toán"), a[href="/checkout"]'
  },
  checkout: {
    fullName: 'input[name="shippingName"], input[placeholder*="Họ tên"]',
    phone: 'input[name="shippingPhone"], input[placeholder*="Số điện thoại"]',
    address: 'input[name="shippingAddress"], textarea[name="address"]',
    note: 'textarea[name="orderNote"]',
    paymentCOD: 'input[type="radio"][value="COD"], label:has-text("Thanh toán khi nhận hàng")',
    paymentVNPAY: 'input[type="radio"][value="VNPAY"], label:has-text("VNPAY")',
    btnConfirmOrder: 'button:has-text("Đặt hàng ngay"), button.btn-place-order',
    orderSuccessCard: '.order-success-container, [data-testid="order-success-screen"]',
    orderIdText: '.order-id-badge, [data-testid="order-code"]'
  },

  // Actions
  goToCart() {
    I.amOnPage('/cart');
    I.waitForElement(this.cart.container, 5);
  },

  updateQuantity(itemIndex = 1, newQty = 2) {
    I.fillField(`(//input[contains(@class, "cart-qty-input")])[${itemIndex}]`, newQty);
    I.wait(1);
  },

  applyCouponCode(code) {
    I.fillField(this.cart.couponInput, code);
    I.click(this.cart.btnApplyCoupon);
    I.wait(1);
  },

  verifyCouponApplied(expectedDiscountText) {
    I.waitForElement(this.cart.discountAmount, 5);
    I.see(expectedDiscountText, this.cart.discountAmount);
  },

  proceedToCheckout() {
    I.click(this.cart.btnProceedCheckout);
    I.waitForElement(this.checkout.fullName, 5);
  },

  fillCheckoutForm({ name, phone, address, note }) {
    if (name) I.fillField(this.checkout.fullName, name);
    if (phone) I.fillField(this.checkout.phone, phone);
    if (address) I.fillField(this.checkout.address, address);
    if (note) I.fillField(this.checkout.note, note);
  },

  selectPaymentMethod(method = 'COD') {
    if (method === 'COD') {
      I.click(this.checkout.paymentCOD);
    } else {
      I.click(this.checkout.paymentVNPAY);
    }
  },

  submitOrder() {
    I.click(this.checkout.btnConfirmOrder);
    I.waitForElement(this.checkout.orderSuccessCard, 10);
  },

  verifyOrderPlacedSuccess() {
    I.see('Đặt hàng thành công!', this.checkout.orderSuccessCard);
    I.waitForElement(this.checkout.orderIdText, 5);
  }
};

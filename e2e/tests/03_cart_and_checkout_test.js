Feature('Luồng Giỏ hàng, Mã giảm giá & Đặt hàng (Cart & Checkout E2E Flow)');

Before(({ I, authPage }) => {
  // Đăng nhập tài khoản kiểm thử trước khi thực hiện luồng mua hàng
  authPage.goToLogin();
  authPage.fillLoginForm({
    email: 'user@example.com',
    password: 'user123'
  });
  authPage.submitLogin();
  I.wait(1);
});

Scenario('TC-E2E-CART-001: [Positive] Thêm sách vào giỏ hàng từ trang danh mục sách', ({ I, productPage, cartPage }) => {
  productPage.goToCatalog();
  productPage.viewFirstBookDetail();
  productPage.addToCartFromDetail(1);
  
  // Kiểm tra giỏ hàng có sản phẩm vừa thêm
  cartPage.goToCart();
  I.seeElement(cartPage.cart.itemRow);
});

Scenario('TC-E2E-CART-002: [Positive] Cập nhật số lượng sách trong giỏ hàng và kiểm tra tổng tiền', ({ I, cartPage }) => {
  cartPage.goToCart();
  
  // Cập nhật số lượng lên 2
  cartPage.updateQuantity(1, 2);
  I.wait(1);
  
  // Kiểm tra hiển thị tổng tiền
  I.seeElement(cartPage.cart.totalPrice);
});

Scenario('TC-E2E-CART-003: [Positive] Áp dụng mã giảm giá / freeship thành công', ({ I, cartPage }) => {
  cartPage.goToCart();
  
  // Áp dụng mã FREESHIP
  cartPage.applyCouponCode('FREESHIP');
  I.wait(1);
  
  // Xác nhận chiết khấu được ghi nhận
  I.seeElement(cartPage.cart.discountAmount);
});

Scenario('TC-E2E-CART-004: [Negative] Nhập mã giảm giá không tồn tại trong hệ thống', ({ I, cartPage }) => {
  cartPage.goToCart();
  
  // Nhập mã không hợp lệ
  cartPage.applyCouponCode('INVALID_COUPON_99999');
  I.wait(1);
  
  // Kiểm tra thông báo lỗi
  I.see('Mã giảm giá không hợp lệ hoặc đã hết hạn', '.error-message, [role="alert"], .text-red-500');
});

Scenario('TC-E2E-ORDER-001: [Positive] Điền thông tin giao hàng và đặt hàng thành công (COD)', ({ I, cartPage }) => {
  cartPage.goToCart();
  cartPage.proceedToCheckout();
  
  // Điền thông tin nhận hàng
  cartPage.fillCheckoutForm({
    name: 'Khách Hàng E2E',
    phone: '0912345678',
    address: '123 Đường Số 1, Phường Bến Nghé, Quận 1, TP.HCM',
    note: 'Giao giờ hành chính'
  });
  
  // Chọn phương thức thanh toán tiền mặt khi nhận hàng (COD)
  cartPage.selectPaymentMethod('COD');
  cartPage.submitOrder();
  
  // Xác nhận màn hình hoàn tất đơn hàng
  cartPage.verifyOrderPlacedSuccess();
});

Scenario('TC-E2E-ORDER-002: [Boundary/Negative] Chặn tiến hành thanh toán khi giỏ hàng trống', ({ I, cartPage }) => {
  // Xóa session / dọn sạch giỏ
  I.amOnPage('/cart');
  I.executeScript(() => {
    localStorage.removeItem('cart');
  });
  I.refreshPage();
  
  // Kiểm tra thông báo giỏ hàng trống và nút checkout bị vô hiệu hóa / ẩn
  I.see('Giỏ hàng của bạn đang trống', cartPage.cart.emptyCartNotice);
  I.dontSee(cartPage.cart.btnProceedCheckout);
});

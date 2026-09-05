package com.bookstore.service;

import com.bookstore.dto.OrderRequest;
import com.bookstore.entity.Book;
import com.bookstore.entity.Coupon;
import com.bookstore.entity.DiscountType;
import com.bookstore.entity.Order;
import com.bookstore.entity.User;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.CouponRepository;
import com.bookstore.repository.OrderRepository;
import com.bookstore.repository.PointTransactionRepository;
import com.bookstore.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit Test Bảng Quyết Định (Decision Table Testing) cho Quy tắc Checkout & Thanh Toán.
 * Task: Scrum Board Card / Thay thế YIYI-47
 * Phong cách: Đơn giản, sạch sẽ, dễ hiểu (Sinh viên năm 2).
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("Kiểm thử Bảng quyết định Quy tắc Checkout & Thanh toán (Decision Table Testing)")
public class CheckoutDecisionTableTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private BookRepository bookRepository;

    @Mock
    private CartService cartService;

    @Mock
    private CouponService couponService;

    @Mock
    private PointTransactionRepository pointTransactionRepository;

    @Mock
    private CouponRepository couponRepository;

    @InjectMocks
    private OrderService orderService;

    private User testUser;
    private Book testBook;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .id(1L)
                .username("student@gmail.com")
                .yPoints(1000)
                .accumulatedPoints(5000)
                .totalSpent(200000.0)
                .build();

        testBook = Book.builder()
                .id(101L)
                .title("Lập trình Java Căn Bản")
                .price(BigDecimal.valueOf(100000.0))
                .oldPrice(BigDecimal.valueOf(100000.0))
                .stockQuantity(10)
                .salesCount(5)
                .build();
    }

    private OrderRequest createBasicOrderRequest() {
        OrderRequest request = new OrderRequest();
        request.setShippingAddress("123 Đường Nguyễn Huệ, Q1, TP.HCM");
        request.setPhoneNumber("0901234567");
        request.setPaymentMethod("COD");
        request.setShippingFee(20000.0);
        request.setCustomerNote("Giao giờ hành chính");

        OrderRequest.OrderItemRequest item = new OrderRequest.OrderItemRequest();
        item.setBookId(101L);
        item.setQuantity(2);
        item.setPrice(100000.0);

        List<OrderRequest.OrderItemRequest> items = new ArrayList<>();
        items.add(item);
        request.setItems(items);

        return request;
    }

    @Test
    @DisplayName("DT-01 (Rule 1): Checkout hợp lệ COD - Không coupon/points -> Tạo đơn PENDING thành công")
    void testRule1_ValidCheckout_COD_NoCoupon() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));
        when(orderRepository.findByUserOrderByCreatedAtDesc(testUser)).thenReturn(Collections.emptyList());
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

        // Act
        Order createdOrder = orderService.createOrder("student@gmail.com", request);

        // Assert
        assertThat(createdOrder).isNotNull();
        assertThat(createdOrder.getStatus()).isEqualTo("PENDING");
        assertThat(createdOrder.getPaymentMethod()).isEqualTo("COD");
        assertThat(testBook.getStockQuantity()).isEqualTo(8); // 10 - 2 = 8
        verify(bookRepository).save(testBook);
    }

    @Test
    @DisplayName("DT-02 (Rule 2): Checkout hợp lệ VNPAY + Mã giảm giá hợp lệ -> Tạo đơn PENDING_PAYMENT & áp dụng giảm giá")
    void testRule2_ValidCheckout_VNPAY_WithDiscountCoupon() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.setPaymentMethod("VNPAY");
        request.setDiscountCouponCode("SALE20");

        Coupon coupon = Coupon.builder()
                .code("SALE20")
                .category("DISCOUNT")
                .discountType(DiscountType.FIXED)
                .discountValue(20000.0)
                .build();

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));
        when(orderRepository.findByUserOrderByCreatedAtDesc(testUser)).thenReturn(Collections.emptyList());
        when(couponService.validateCoupon("SALE20", 200000.0, "student@gmail.com")).thenReturn(coupon);
        when(couponService.calculateDiscount(coupon, 200000.0)).thenReturn(20000.0);
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

        // Act
        Order createdOrder = orderService.createOrder("student@gmail.com", request);

        // Assert
        assertThat(createdOrder).isNotNull();
        assertThat(createdOrder.getStatus()).isEqualTo("PENDING_PAYMENT");
        assertThat(createdOrder.getDiscountCouponCode()).isEqualTo("SALE20");
    }

    @Test
    @DisplayName("DT-03 (Rule 3): Checkout hợp lệ COD + Tiêu điểm Y-Points -> Khấu trừ Y-Points và tạo đơn PENDING")
    void testRule3_ValidCheckout_COD_WithPoints() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.setSpentPoints(500); // Đổi 500 điểm = 500đ

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));
        when(orderRepository.findByUserOrderByCreatedAtDesc(testUser)).thenReturn(Collections.emptyList());
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

        // Act
        Order createdOrder = orderService.createOrder("student@gmail.com", request);

        // Assert
        assertThat(createdOrder).isNotNull();
        assertThat(createdOrder.getPointsUsed()).isEqualTo(500);
        assertThat(testUser.getYPoints()).isEqualTo(500); // 1000 - 500 = 500
        verify(userRepository).save(testUser); // Trừ điểm tiêu Y-Points
    }

    @Test
    @DisplayName("DT-04 (Rule 4): Sách hết hàng / Không đủ tồn kho -> Bị từ chối (Ném ngoại lệ)")
    void testRule4_InvalidCheckout_OutOfStock() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.getItems().get(0).setQuantity(100); // Mua 100 cuốn nhưng kho chỉ có 10

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));

        // Act & Assert
        assertThatThrownBy(() -> orderService.createOrder("student@gmail.com", request))
                .isInstanceOf(RuntimeException.class)
                .hasMessageContaining("không đủ số lượng tồn kho!");
    }

    @Test
    @DisplayName("DT-05 (Rule 5): Mã giảm giá hết hạn hoặc không hợp lệ -> Bị từ chối (Ném ngoại lệ)")
    void testRule5_InvalidCheckout_InvalidCoupon() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.setDiscountCouponCode("EXPIRED_COUPON");

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));
        when(couponService.validateCoupon("EXPIRED_COUPON", 200000.0, "student@gmail.com"))
                .thenThrow(new RuntimeException("Mã giảm giá đã hết hạn!"));

        // Act & Assert
        assertThatThrownBy(() -> orderService.createOrder("student@gmail.com", request))
                .isInstanceOf(RuntimeException.class)
                .hasMessageContaining("Lỗi áp dụng mã giảm giá: Mã giảm giá đã hết hạn!");
    }

    @Test
    @DisplayName("DT-06 (Rule 6): Thiếu thông tin địa chỉ giao hàng -> Kiểm tra dữ liệu địa chỉ gắn vào order")
    void testRule6_Checkout_WithMissingAddress() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.setShippingAddress(null); // Không nhập địa chỉ

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));
        when(orderRepository.findByUserOrderByCreatedAtDesc(testUser)).thenReturn(Collections.emptyList());
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

        // Act
        Order createdOrder = orderService.createOrder("student@gmail.com", request);

        // Assert - Hiện tại code lưu null (đối chiếu phát hiện Jira Bug thiếu validation)
        assertThat(createdOrder.getShippingAddress()).isNull();
    }

    @Test
    @DisplayName("DT-07 (Rule 7): Phương thức thanh toán không hợp lệ -> Kiểm tra xử lý paymentMethod")
    void testRule7_Checkout_WithInvalidPaymentMethod() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.setPaymentMethod("PAYPAL_INVALID");

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));
        when(orderRepository.findByUserOrderByCreatedAtDesc(testUser)).thenReturn(Collections.emptyList());
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

        // Act
        Order createdOrder = orderService.createOrder("student@gmail.com", request);

        // Assert - Code hiện tại mặc định gán status PENDING_PAYMENT khi không phải COD
        assertThat(createdOrder.getStatus()).isEqualTo("PENDING_PAYMENT");
    }

    @Test
    @DisplayName("DT-08 (Rule 8): Sử dụng Y-Points vượt quá số dư tài khoản -> Bị từ chối (Ném ngoại lệ)")
    void testRule8_InvalidCheckout_ExceedingYPoints() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        request.setSpentPoints(5000); // User chỉ có 1000 điểm nhưng đòi dùng 5000 điểm

        when(userRepository.findByUsername("student@gmail.com")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(101L)).thenReturn(Optional.of(testBook));

        // Act & Assert
        assertThatThrownBy(() -> orderService.createOrder("student@gmail.com", request))
                .isInstanceOf(RuntimeException.class)
                .hasMessageContaining("Bạn không đủ Y-Point để thanh toán!");
    }

    @Test
    @DisplayName("DT-09 (Rule 9): Tài khoản không tồn tại / Chưa đăng nhập -> Bị từ chối (Ném ngoại lệ)")
    void testRule9_InvalidCheckout_UserNotFound() {
        // Arrange
        OrderRequest request = createBasicOrderRequest();
        when(userRepository.findByUsername("unknown@gmail.com")).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> orderService.createOrder("unknown@gmail.com", request))
                .isInstanceOf(RuntimeException.class)
                .hasMessageContaining("Tài khoản không tồn tại hoặc phiên đăng nhập đã hết hạn.");
    }
}

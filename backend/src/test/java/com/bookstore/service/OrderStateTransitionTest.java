package com.bookstore.service;

import com.bookstore.dto.ReturnRequest;
import com.bookstore.entity.Order;
import com.bookstore.entity.ShippingStatus;
import com.bookstore.entity.User;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.CouponRepository;
import com.bookstore.repository.OrderRepository;
import com.bookstore.repository.PointTransactionRepository;
import com.bookstore.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit Test chuyển trạng thái vòng đời đơn hàng (State Transition Testing).
 * 
 * Mã bài tập/Task: YIYI-48 / Scrum Board Card
 * Phong cách viết: Đơn giản, sạch sẽ (clean), dễ hiểu.
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("Kiểm thử Chuyển trạng thái Vòng đời Đơn hàng (State Transition Testing)")
public class OrderStateTransitionTest {

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

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .id(1L)
                .username("student@example.com")
                .yPoints(100)
                .accumulatedPoints(500)
                .totalSpent(100000.0)
                .build();
    }

    private Order createTestOrder(Long id, String status, ShippingStatus shippingStatus) {
        return Order.builder()
                .id(id)
                .user(testUser)
                .status(status)
                .shippingStatus(shippingStatus)
                .items(new ArrayList<>())
                .paymentMethod("COD")
                .createdAt(LocalDateTime.now())
                .build();
    }

    @Nested
    @DisplayName("1. Kiểm thử các chuyển trạng thái HỢP LỆ (Valid State Transitions)")
    class ValidTransitionsTest {

        @Test
        @DisplayName("ST-01: Chuyển từ PENDING sang PROCESSING (Người bán chuẩn bị hàng)")
        void testTransition_PendingToProcessing() {
            // Arrange (Chuẩn bị dữ liệu)
            Order order = createTestOrder(1L, "PENDING", ShippingStatus.PENDING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
            when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

            // Act (Thực thi hàm)
            Order updatedOrder = orderService.updateOrderShipping(1L, "PROCESSING", "GHN", "TRACK123");

            // Assert (Kiểm tra kết quả)
            assertThat(updatedOrder.getShippingStatus()).isEqualTo(ShippingStatus.PROCESSING);
            assertThat(updatedOrder.getStatus()).isEqualTo("PROCESSING");
            assertThat(updatedOrder.getShippingPartner()).isEqualTo("GHN");
            assertThat(updatedOrder.getTrackingNumber()).isEqualTo("TRACK123");
        }

        @Test
        @DisplayName("ST-02: Chuyển từ PROCESSING sang SHIPPING (Đang giao hàng)")
        void testTransition_ProcessingToShipping() {
            Order order = createTestOrder(1L, "PROCESSING", ShippingStatus.PROCESSING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
            when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

            Order updatedOrder = orderService.updateOrderShipping(1L, "SHIPPING", "GHTK", "TRACK456");

            assertThat(updatedOrder.getShippingStatus()).isEqualTo(ShippingStatus.SHIPPING);
            assertThat(updatedOrder.getStatus()).isEqualTo("SHIPPED");
        }

        @Test
        @DisplayName("ST-03: Chuyển từ SHIPPING sang DELIVERED (Giao hàng thành công)")
        void testTransition_ShippingToDelivered() {
            Order order = createTestOrder(1L, "SHIPPED", ShippingStatus.SHIPPING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
            when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

            Order updatedOrder = orderService.updateOrderShipping(1L, "DELIVERED", null, null);

            assertThat(updatedOrder.getShippingStatus()).isEqualTo(ShippingStatus.DELIVERED);
            assertThat(updatedOrder.getStatus()).isEqualTo("SHIPPED");
        }

        @Test
        @DisplayName("ST-04: Chuyển từ DELIVERED sang COMPLETED (Khách hàng bấm xác nhận nhận hàng)")
        void testTransition_DeliveredToCompleted() {
            Order order = createTestOrder(1L, "SHIPPED", ShippingStatus.DELIVERED);
            order.setTotalAmount(150000.0);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
            when(orderRepository.findByUserOrderByCreatedAtDesc(testUser)).thenReturn(Collections.singletonList(order));

            orderService.confirmOrderReceived(1L, "student@example.com");

            assertThat(order.getStatus()).isEqualTo("COMPLETED");
            verify(orderRepository).save(order);
        }

        @Test
        @DisplayName("ST-05: Chuyển từ PENDING sang CANCELLED (Khách hàng hủy đơn khi chưa giao)")
        void testTransition_PendingToCancelled() {
            Order order = createTestOrder(1L, "PENDING", ShippingStatus.PENDING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            orderService.userCancelOrder(1L, "student@example.com");

            assertThat(order.getShippingStatus()).isEqualTo(ShippingStatus.CANCELLED);
            assertThat(order.getStatus()).isEqualTo("CANCELLED");
        }

        @Test
        @DisplayName("ST-06: Chuyển từ COMPLETED sang RETURNED (Khách hàng gửi yêu cầu trả hàng/hoàn tiền)")
        void testTransition_CompletedToReturned() {
            Order order = createTestOrder(1L, "COMPLETED", ShippingStatus.DELIVERED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
            ReturnRequest req = new ReturnRequest();
            req.setReason("Sách bị rách");
            req.setPhone("0901234567");
            req.setBank("MBBank");
            req.setDetails("123456");

            orderService.userReturnOrder(1L, "student@example.com", req);

            assertThat(order.getStatus()).isEqualTo("RETURNED");
            assertThat(order.getReturnReason()).isEqualTo("Sách bị rách");
        }

        @Test
        @DisplayName("ST-07: Chuyển từ RETURNED sang REFUNDED (Admin duyệt trả hàng)")
        void testTransition_ReturnedToRefunded() {
            Order order = createTestOrder(1L, "RETURNED", ShippingStatus.DELIVERED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            orderService.adminApproveReturn(1L);

            assertThat(order.getStatus()).isEqualTo("REFUNDED");
        }

        @Test
        @DisplayName("ST-08: Chuyển từ RETURNED về COMPLETED (Admin từ chối trả hàng)")
        void testTransition_ReturnedToCompleted_WhenAdminRejects() {
            Order order = createTestOrder(1L, "RETURNED", ShippingStatus.DELIVERED);
            order.setReturnReason("Không thích nữa");
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            orderService.adminRejectReturn(1L);

            assertThat(order.getStatus()).isEqualTo("COMPLETED");
            assertThat(order.getShippingStatus()).isEqualTo(ShippingStatus.DELIVERED);
            assertThat(order.getReturnReason()).isNull();
        }

        @Test
        @DisplayName("ST-09: Chuyển từ PENDING_PAYMENT sang PENDING (Đổi PTTT sang COD)")
        void testTransition_PendingPaymentToPending() {
            Order order = createTestOrder(1L, "PENDING_PAYMENT", ShippingStatus.PENDING);
            order.setPaymentMethod("VNPAY");
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
            when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));

            Order updatedOrder = orderService.updatePaymentMethod(1L, "COD", "student@example.com");

            assertThat(updatedOrder.getStatus()).isEqualTo("PENDING");
            assertThat(updatedOrder.getPaymentMethod()).isEqualTo("COD");
        }
    }

    @Nested
    @DisplayName("2. Kiểm thử các chuyển trạng thái KHÔNG HỢP LỆ (Invalid Transitions - Bị từ chối)")
    class InvalidTransitionsTest {

        @Test
        @DisplayName("IT-01: Hủy đơn khi hàng đang SHIPPING -> Từ chối hủy đơn")
        void testInvalid_CancelOrder_WhenShipping() {
            Order order = createTestOrder(1L, "SHIPPED", ShippingStatus.SHIPPING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.userCancelOrder(1L, "student@example.com"))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Chỉ có thể huỷ đơn hàng khi người bán chưa xác nhận giao hàng!");
        }

        @Test
        @DisplayName("IT-02: Hủy đơn khi hàng đã DELIVERED -> Từ chối hủy đơn")
        void testInvalid_CancelOrder_WhenDelivered() {
            Order order = createTestOrder(1L, "SHIPPED", ShippingStatus.DELIVERED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.userCancelOrder(1L, "student@example.com"))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Chỉ có thể huỷ đơn hàng khi người bán chưa xác nhận giao hàng!");
        }

        @Test
        @DisplayName("IT-03: Yêu cầu trả hàng khi đơn hàng đang PROCESSING -> Từ chối")
        void testInvalid_ReturnOrder_WhenProcessing() {
            Order order = createTestOrder(1L, "PROCESSING", ShippingStatus.PROCESSING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.userReturnOrder(1L, "student@example.com", null))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Chỉ có thể yêu cầu trả hàng/hoàn tiền cho đơn hàng đã hoàn thành!");
        }

        @Test
        @DisplayName("IT-04: Admin duyệt trả hàng khi đơn chưa ở trạng thái RETURNED -> Từ chối")
        void testInvalid_AdminApproveReturn_WhenStatusIsNotReturned() {
            Order order = createTestOrder(1L, "COMPLETED", ShippingStatus.DELIVERED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.adminApproveReturn(1L))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Chỉ có thể duyệt đơn hàng đang yêu cầu trả hàng!");
        }

        @Test
        @DisplayName("IT-05: Admin từ chối trả hàng khi đơn đã CANCELLED -> Từ chối")
        void testInvalid_AdminRejectReturn_WhenStatusIsCancelled() {
            Order order = createTestOrder(1L, "CANCELLED", ShippingStatus.CANCELLED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.adminRejectReturn(1L))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Chỉ có thể từ chối đơn hàng đang yêu cầu trả hàng!");
        }

        @Test
        @DisplayName("IT-06: Khách hàng xác nhận nhận hàng khi đơn đã COMPLETED -> Từ chối")
        void testInvalid_ConfirmReceived_WhenAlreadyCompleted() {
            Order order = createTestOrder(1L, "COMPLETED", ShippingStatus.DELIVERED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.confirmOrderReceived(1L, "student@example.com"))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Đơn hàng đã được xác nhận hoàn thành!");
        }

        @Test
        @DisplayName("IT-07: Đổi phương thức thanh toán khi đơn hàng đã COMPLETED -> Từ chối")
        void testInvalid_UpdatePaymentMethod_WhenCompleted() {
            Order order = createTestOrder(1L, "COMPLETED", ShippingStatus.DELIVERED);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.updatePaymentMethod(1L, "VNPAY", "student@example.com"))
                    .isInstanceOf(RuntimeException.class)
                    .hasMessageContaining("Không thể thay đổi phương thức thanh toán cho đơn hàng ở trạng thái này!");
        }

        @Test
        @DisplayName("IT-08: Cập nhật ShippingStatus với giá trị Enum không tồn tại -> Từ chối (IllegalArgumentException)")
        void testInvalid_UpdateOrderShipping_WithInvalidEnumValue() {
            Order order = createTestOrder(1L, "PENDING", ShippingStatus.PENDING);
            when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

            assertThatThrownBy(() -> orderService.updateOrderShipping(1L, "INVALID_STATUS", null, null))
                    .isInstanceOf(IllegalArgumentException.class);
        }
    }
}

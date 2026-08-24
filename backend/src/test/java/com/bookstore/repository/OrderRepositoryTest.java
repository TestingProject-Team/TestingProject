package com.bookstore.repository;

import com.bookstore.entity.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class OrderRepositoryTest {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BookRepository bookRepository;

    private User user;
    private Book book;
    private Order order1;
    private Order order2;

    @BeforeEach
    void setUp() {
        user = userRepository.save(User.builder()
                .username("orderuser")
                .password("pass")
                .fullName("Order Test User")
                .email("orderuser@example.com")
                .role(Role.USER)
                .build());

        book = bookRepository.save(Book.builder()
                .title("Order Test Book")
                .price(new BigDecimal("100.00"))
                .stockQuantity(10)
                .build());

        order1 = Order.builder()
                .user(user)
                .totalAmount(100.0)
                .status("COMPLETED")
                .shippingStatus(ShippingStatus.DELIVERED)
                .discountCouponCode("SUMMER50")
                .createdAt(LocalDateTime.now().minusDays(2))
                .items(new ArrayList<>())
                .build();

        OrderItem item1 = OrderItem.builder()
                .order(order1)
                .book(book)
                .quantity(1)
                .price(100.0)
                .build();
        order1.getItems().add(item1);

        order2 = Order.builder()
                .user(user)
                .totalAmount(200.0)
                .status("CANCELLED")
                .shippingStatus(ShippingStatus.CANCELLED)
                .discountCouponCode("SUMMER50")
                .createdAt(LocalDateTime.now().minusDays(10))
                .items(new ArrayList<>())
                .build();

        orderRepository.saveAll(List.of(order1, order2));
    }

    @Test
    @DisplayName("Find orders by User ID - Success")
    void testFindByUserId() {
        List<Order> userOrders = orderRepository.findByUserId(user.getId());
        assertThat(userOrders).hasSize(2);
    }

    @Test
    @DisplayName("Find orders by user ordered by created date desc - Success")
    void testFindByUserOrderByCreatedAtDesc() {
        List<Order> sortedOrders = orderRepository.findByUserOrderByCreatedAtDesc(user);
        assertThat(sortedOrders).hasSize(2);
        assertThat(sortedOrders.get(0).getId()).isEqualTo(order1.getId()); // minus 2 days > minus 10 days
    }

    @Test
    @DisplayName("Find orders by status and created before date - Success")
    void testFindByStatusAndCreatedAtBefore() {
        List<Order> oldCancelledOrders = orderRepository.findByStatusAndCreatedAtBefore("CANCELLED", LocalDateTime.now().minusDays(5));
        assertThat(oldCancelledOrders).hasSize(1);
        assertThat(oldCancelledOrders.get(0).getId()).isEqualTo(order2.getId());
    }

    @Test
    @DisplayName("Count coupon usage by user excluding CANCELLED orders - Success")
    void testCountUsageByUser() {
        // order1 is COMPLETED with SUMMER50 coupon -> count 1
        // order2 is CANCELLED with SUMMER50 coupon -> ignored
        long usage = orderRepository.countUsageByUser(user, "SUMMER50");
        assertThat(usage).isEqualTo(1L);

        long unusedCount = orderRepository.countUsageByUser(user, "NONEXISTENT");
        assertThat(unusedCount).isEqualTo(0L);
    }

    @Test
    @DisplayName("Check if user has bought book and status is DELIVERED - Success")
    void testHasUserBoughtBookAndDelivered() {
        boolean bought = orderRepository.hasUserBoughtBookAndDelivered(user, book, ShippingStatus.DELIVERED);
        assertThat(bought).isTrue();

        boolean pendingStatus = orderRepository.hasUserBoughtBookAndDelivered(user, book, ShippingStatus.PENDING);
        assertThat(pendingStatus).isFalse();
    }

    @Test
    @DisplayName("Count delivered purchases of a book by user - Success")
    void testCountUserDeliveredPurchases() {
        long deliveredCount = orderRepository.countUserDeliveredPurchases(user, book, ShippingStatus.DELIVERED);
        assertThat(deliveredCount).isEqualTo(1L);

        long cancelledCount = orderRepository.countUserDeliveredPurchases(user, book, ShippingStatus.CANCELLED);
        assertThat(cancelledCount).isEqualTo(0L);
    }
}

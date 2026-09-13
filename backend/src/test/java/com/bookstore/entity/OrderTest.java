package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class OrderTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Order order = new Order();
        User user = new User();
        user.setId(1L);
        List<OrderItem> items = new ArrayList<>();
        items.add(new OrderItem());
        LocalDateTime now = LocalDateTime.now();

        order.setId(10L);
        order.setUser(user);
        order.setItems(items);
        order.setTotalAmount(500000.0);
        order.setStatus("COMPLETED");
        order.setShippingAddress("123 Street, District 1");
        order.setPhoneNumber("0987654321");
        order.setPaymentMethod("COD");
        order.setShippingFee(30000.0);
        order.setCustomerNote("Handle with care");
        order.setShippingStatus(ShippingStatus.DELIVERED);
        order.setShippingPartner("GHN");
        order.setTrackingNumber("GHN123456");
        order.setDiscountAmount(50000.0);
        order.setPointsUsed(100);
        order.setDiscountCouponCode("DISCOUNT50K");
        order.setShippingCouponCode("FREESHIP");
        order.setReturnReason("Damaged goods");
        order.setReturnPhone("0987654321");
        order.setReturnBank("Vietcombank");
        order.setReturnDetails("Book cover was torn");
        order.setCreatedAt(now);

        assertEquals(10L, order.getId());
        assertEquals(user, order.getUser());
        assertEquals(items, order.getItems());
        assertEquals(500000.0, order.getTotalAmount());
        assertEquals("COMPLETED", order.getStatus());
        assertEquals("123 Street, District 1", order.getShippingAddress());
        assertEquals("0987654321", order.getPhoneNumber());
        assertEquals("COD", order.getPaymentMethod());
        assertEquals(30000.0, order.getShippingFee());
        assertEquals("Handle with care", order.getCustomerNote());
        assertEquals(ShippingStatus.DELIVERED, order.getShippingStatus());
        assertEquals("GHN", order.getShippingPartner());
        assertEquals("GHN123456", order.getTrackingNumber());
        assertEquals(50000.0, order.getDiscountAmount());
        assertEquals(100, order.getPointsUsed());
        assertEquals("DISCOUNT50K", order.getDiscountCouponCode());
        assertEquals("FREESHIP", order.getShippingCouponCode());
        assertEquals("Damaged goods", order.getReturnReason());
        assertEquals("0987654321", order.getReturnPhone());
        assertEquals("Vietcombank", order.getReturnBank());
        assertEquals("Book cover was torn", order.getReturnDetails());
        assertEquals(now, order.getCreatedAt());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        List<OrderItem> items = new ArrayList<>();
        LocalDateTime now = LocalDateTime.now();

        Order order = new Order(
                20L,
                user,
                items,
                250000.0,
                "PENDING",
                "456 Avenue",
                "0911222333",
                "VNPAY",
                25000.0,
                "Call before delivery",
                ShippingStatus.PENDING,
                "GHTK",
                "GHTK987",
                20000.0,
                50,
                "CODE10",
                "SHIPFREE",
                null,
                null,
                null,
                null,
                now
        );

        assertEquals(20L, order.getId());
        assertEquals(user, order.getUser());
        assertEquals(items, order.getItems());
        assertEquals(250000.0, order.getTotalAmount());
        assertEquals("PENDING", order.getStatus());
        assertEquals("456 Avenue", order.getShippingAddress());
        assertEquals("0911222333", order.getPhoneNumber());
        assertEquals("VNPAY", order.getPaymentMethod());
        assertEquals(25000.0, order.getShippingFee());
        assertEquals("Call before delivery", order.getCustomerNote());
        assertEquals(ShippingStatus.PENDING, order.getShippingStatus());
        assertEquals("GHTK", order.getShippingPartner());
        assertEquals("GHTK987", order.getTrackingNumber());
        assertEquals(20000.0, order.getDiscountAmount());
        assertEquals(50, order.getPointsUsed());
        assertEquals("CODE10", order.getDiscountCouponCode());
        assertEquals("SHIPFREE", order.getShippingCouponCode());
        assertNull(order.getReturnReason());
        assertNull(order.getReturnPhone());
        assertNull(order.getReturnBank());
        assertNull(order.getReturnDetails());
        assertEquals(now, order.getCreatedAt());
    }

    @Test
    void testBuilderDefaults() {
        Order order = Order.builder().build();

        assertNotNull(order.getItems());
        assertTrue(order.getItems().isEmpty());
        assertEquals(0.0, order.getShippingFee());
        assertEquals(ShippingStatus.PENDING, order.getShippingStatus());
        assertEquals(0.0, order.getDiscountAmount());
        assertEquals(0, order.getPointsUsed());
    }

    @Test
    void testEqualsAndHashCode() {
        Order o1 = Order.builder().id(1L).totalAmount(100.0).build();
        Order o2 = Order.builder().id(1L).totalAmount(100.0).build();
        Order o3 = Order.builder().id(2L).totalAmount(200.0).build();

        assertEquals(o1, o2);
        assertEquals(o1.hashCode(), o2.hashCode());
        assertNotEquals(o1, o3);
        assertNotEquals(o1, null);
        assertNotEquals(o1, new Object());
        assertEquals(o1, o1);
        assertTrue(o1.canEqual(o2));
        assertNotNull(o1.toString());
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class PointTransactionTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        PointTransaction pt = new PointTransaction();
        User user = new User();
        user.setId(1L);
        LocalDateTime now = LocalDateTime.now();

        pt.setId(10L);
        pt.setUser(user);
        pt.setAction("EARN_ORDER");
        pt.setPreviousBalance(100);
        pt.setTransactionValue(50);
        pt.setNewBalance(150);
        pt.setCreatedAt(now);
        pt.setDescription("Earned from order #123");

        assertEquals(10L, pt.getId());
        assertEquals(user, pt.getUser());
        assertEquals("EARN_ORDER", pt.getAction());
        assertEquals(100, pt.getPreviousBalance());
        assertEquals(50, pt.getTransactionValue());
        assertEquals(150, pt.getNewBalance());
        assertEquals(now, pt.getCreatedAt());
        assertEquals("Earned from order #123", pt.getDescription());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        LocalDateTime now = LocalDateTime.now();

        PointTransaction pt = new PointTransaction(
                20L,
                user,
                "SPEND_ORDER",
                200,
                -50,
                150,
                now,
                "Spent on order #456"
        );

        assertEquals(20L, pt.getId());
        assertEquals(user, pt.getUser());
        assertEquals("SPEND_ORDER", pt.getAction());
        assertEquals(200, pt.getPreviousBalance());
        assertEquals(-50, pt.getTransactionValue());
        assertEquals(150, pt.getNewBalance());
        assertEquals(now, pt.getCreatedAt());
        assertEquals("Spent on order #456", pt.getDescription());
    }

    @Test
    void testBuilder() {
        User user = new User();
        LocalDateTime now = LocalDateTime.now();

        PointTransaction pt = PointTransaction.builder()
                .id(30L)
                .user(user)
                .action("EARN_VOUCHER")
                .previousBalance(50)
                .transactionValue(100)
                .newBalance(150)
                .createdAt(now)
                .description("Voucher redeemed")
                .build();

        assertEquals(30L, pt.getId());
        assertEquals(user, pt.getUser());
        assertEquals("EARN_VOUCHER", pt.getAction());
        assertEquals(50, pt.getPreviousBalance());
        assertEquals(100, pt.getTransactionValue());
        assertEquals(150, pt.getNewBalance());
        assertEquals(now, pt.getCreatedAt());
        assertEquals("Voucher redeemed", pt.getDescription());
        assertNotNull(pt.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        PointTransaction pt1 = PointTransaction.builder().id(1L).action("ACT").build();
        PointTransaction pt2 = PointTransaction.builder().id(1L).action("ACT").build();
        PointTransaction pt3 = PointTransaction.builder().id(2L).action("OTHER").build();

        assertEquals(pt1, pt2);
        assertEquals(pt1.hashCode(), pt2.hashCode());
        assertNotEquals(pt1, pt3);
        assertNotEquals(pt1, null);
        assertNotEquals(pt1, new Object());
        assertEquals(pt1, pt1);
        assertTrue(pt1.canEqual(pt2));
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class NotificationTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Notification notification = new Notification();
        LocalDateTime now = LocalDateTime.now();

        notification.setId(1L);
        notification.setTitle("Order Placed");
        notification.setContent("Your order #123 has been placed successfully.");
        notification.setType("ORDER");
        notification.setUserId(10L);
        notification.setIsRead(true);
        notification.setCreatedAt(now);

        assertEquals(1L, notification.getId());
        assertEquals("Order Placed", notification.getTitle());
        assertEquals("Your order #123 has been placed successfully.", notification.getContent());
        assertEquals("ORDER", notification.getType());
        assertEquals(10L, notification.getUserId());
        assertTrue(notification.getIsRead());
        assertEquals(now, notification.getCreatedAt());
    }

    @Test
    void testAllArgsConstructor() {
        LocalDateTime now = LocalDateTime.now();
        Notification notification = new Notification(
                2L,
                "Promotion",
                "Special 50% discount today!",
                "PROMO",
                null,
                false,
                now
        );

        assertEquals(2L, notification.getId());
        assertEquals("Promotion", notification.getTitle());
        assertEquals("Special 50% discount today!", notification.getContent());
        assertEquals("PROMO", notification.getType());
        assertNull(notification.getUserId());
        assertFalse(notification.getIsRead());
        assertEquals(now, notification.getCreatedAt());
    }

    @Test
    void testBuilderDefaults() {
        Notification notification = Notification.builder()
                .title("System Update")
                .build();

        assertFalse(notification.getIsRead());
    }

    @Test
    void testEqualsAndHashCode() {
        Notification n1 = Notification.builder().id(1L).title("Promo").build();
        Notification n2 = Notification.builder().id(1L).title("Promo").build();
        Notification n3 = Notification.builder().id(2L).title("Order").build();

        assertEquals(n1, n2);
        assertEquals(n1.hashCode(), n2.hashCode());
        assertNotEquals(n1, n3);
        assertNotEquals(n1, null);
        assertNotEquals(n1, new Object());
        assertEquals(n1, n1);
        assertTrue(n1.canEqual(n2));
        assertNotNull(n1.toString());
    }
}

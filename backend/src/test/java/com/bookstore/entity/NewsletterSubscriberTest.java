package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class NewsletterSubscriberTest {

    @Test
    void testSettersAndGetters() {
        NewsletterSubscriber subscriber = new NewsletterSubscriber();
        LocalDateTime now = LocalDateTime.now();

        subscriber.setId(1L);
        subscriber.setEmail("subscriber@example.com");
        subscriber.setSubscribedAt(now);
        subscriber.setActive(false);

        assertEquals(1L, subscriber.getId());
        assertEquals("subscriber@example.com", subscriber.getEmail());
        assertEquals(now, subscriber.getSubscribedAt());
        assertFalse(subscriber.isActive());
    }

    @Test
    void testDefaultValues() {
        NewsletterSubscriber subscriber = new NewsletterSubscriber();
        assertTrue(subscriber.isActive());
        assertNull(subscriber.getId());
        assertNull(subscriber.getEmail());
        assertNull(subscriber.getSubscribedAt());
    }

    @Test
    void testOnCreate() {
        NewsletterSubscriber subscriber = new NewsletterSubscriber();
        assertNull(subscriber.getSubscribedAt());

        subscriber.onCreate();

        assertNotNull(subscriber.getSubscribedAt());
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class ContactTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Contact contact = new Contact();
        LocalDateTime now = LocalDateTime.now();

        contact.setId(1L);
        contact.setFullName("Nguyen Van Contact");
        contact.setPhone("0987111222");
        contact.setEmail("contact@example.com");
        contact.setContent("Need help with order");
        contact.setCreatedAt(now);
        contact.setStatus("PROCESSED");

        assertEquals(1L, contact.getId());
        assertEquals("Nguyen Van Contact", contact.getFullName());
        assertEquals("0987111222", contact.getPhone());
        assertEquals("contact@example.com", contact.getEmail());
        assertEquals("Need help with order", contact.getContent());
        assertEquals(now, contact.getCreatedAt());
        assertEquals("PROCESSED", contact.getStatus());
    }

    @Test
    void testAllArgsConstructor() {
        LocalDateTime now = LocalDateTime.now();
        Contact contact = new Contact(2L, "Tran Contact", "0911222333", "tran@example.com", "Question", now, "PENDING");

        assertEquals(2L, contact.getId());
        assertEquals("Tran Contact", contact.getFullName());
        assertEquals("0911222333", contact.getPhone());
        assertEquals("tran@example.com", contact.getEmail());
        assertEquals("Question", contact.getContent());
        assertEquals(now, contact.getCreatedAt());
        assertEquals("PENDING", contact.getStatus());
    }

    @Test
    void testBuilder() {
        LocalDateTime now = LocalDateTime.now();
        Contact contact = Contact.builder()
                .id(3L)
                .fullName("Le Contact")
                .phone("0922333444")
                .email("le@example.com")
                .content("Feedback")
                .createdAt(now)
                .status("PENDING")
                .build();

        assertEquals(3L, contact.getId());
        assertEquals("Le Contact", contact.getFullName());
        assertEquals("0922333444", contact.getPhone());
        assertEquals("le@example.com", contact.getEmail());
        assertEquals("Feedback", contact.getContent());
        assertEquals(now, contact.getCreatedAt());
        assertEquals("PENDING", contact.getStatus());
        assertNotNull(contact.toString());
    }

    @Test
    void testBuilderDefaults() {
        Contact contact = Contact.builder()
                .fullName("Test")
                .build();

        assertEquals("PENDING", contact.getStatus());
    }

    @Test
    void testOnCreate() {
        Contact contact = new Contact();
        contact.setStatus(null);
        assertNull(contact.getCreatedAt());
        assertNull(contact.getStatus());

        contact.onCreate();

        assertNotNull(contact.getCreatedAt());
        assertEquals("PENDING", contact.getStatus());

        Contact contactWithStatus = new Contact();
        contactWithStatus.setStatus("PROCESSED");
        contactWithStatus.onCreate();
        assertEquals("PROCESSED", contactWithStatus.getStatus());
    }

    @Test
    void testEqualsAndHashCode() {
        Contact c1 = Contact.builder().id(1L).email("a@a.com").build();
        Contact c2 = Contact.builder().id(1L).email("a@a.com").build();
        Contact c3 = Contact.builder().id(2L).email("b@b.com").build();

        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
        assertNotEquals(c1, c3);
        assertNotEquals(c1, null);
        assertNotEquals(c1, new Object());
        assertEquals(c1, c1);
        assertTrue(c1.canEqual(c2));
    }
}

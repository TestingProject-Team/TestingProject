package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class WishlistTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Wishlist wishlist = new Wishlist();
        User user = new User();
        user.setId(1L);
        Book book = new Book();
        book.setId(2L);
        LocalDateTime now = LocalDateTime.now();

        wishlist.setId(10L);
        wishlist.setUser(user);
        wishlist.setBook(book);
        wishlist.setCreatedAt(now);

        assertEquals(10L, wishlist.getId());
        assertEquals(user, wishlist.getUser());
        assertEquals(book, wishlist.getBook());
        assertEquals(now, wishlist.getCreatedAt());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        Book book = new Book();
        LocalDateTime now = LocalDateTime.now();

        Wishlist wishlist = new Wishlist(20L, user, book, now);

        assertEquals(20L, wishlist.getId());
        assertEquals(user, wishlist.getUser());
        assertEquals(book, wishlist.getBook());
        assertEquals(now, wishlist.getCreatedAt());
    }

    @Test
    void testBuilderDefaults() {
        Wishlist wishlist = Wishlist.builder().build();

        assertNotNull(wishlist.getCreatedAt());
    }

    @Test
    void testEqualsAndHashCode() {
        LocalDateTime time = LocalDateTime.now();
        Wishlist w1 = Wishlist.builder().id(1L).createdAt(time).build();
        Wishlist w2 = Wishlist.builder().id(1L).createdAt(time).build();
        Wishlist w3 = Wishlist.builder().id(2L).createdAt(time).build();

        assertEquals(w1, w2);
        assertEquals(w1.hashCode(), w2.hashCode());
        assertNotEquals(w1, w3);
        assertNotEquals(w1, null);
        assertNotEquals(w1, new Object());
        assertEquals(w1, w1);
        assertTrue(w1.canEqual(w2));
        assertNotNull(w1.toString());
    }
}

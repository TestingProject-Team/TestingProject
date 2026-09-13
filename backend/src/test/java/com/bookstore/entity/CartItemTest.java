package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CartItemTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        CartItem item = new CartItem();
        Cart cart = new Cart();
        cart.setId(1L);
        Book book = new Book();
        book.setId(2L);

        item.setId(10L);
        item.setCart(cart);
        item.setBook(book);
        item.setQuantity(3);

        assertEquals(10L, item.getId());
        assertEquals(cart, item.getCart());
        assertEquals(book, item.getBook());
        assertEquals(3, item.getQuantity());
    }

    @Test
    void testAllArgsConstructor() {
        Cart cart = new Cart();
        Book book = new Book();
        CartItem item = new CartItem(20L, cart, book, 5);

        assertEquals(20L, item.getId());
        assertEquals(cart, item.getCart());
        assertEquals(book, item.getBook());
        assertEquals(5, item.getQuantity());
    }

    @Test
    void testBuilder() {
        Cart cart = new Cart();
        Book book = new Book();
        CartItem item = CartItem.builder()
                .id(30L)
                .cart(cart)
                .book(book)
                .quantity(2)
                .build();

        assertEquals(30L, item.getId());
        assertEquals(cart, item.getCart());
        assertEquals(book, item.getBook());
        assertEquals(2, item.getQuantity());
        assertNotNull(item.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        CartItem c1 = CartItem.builder().id(1L).quantity(2).build();
        CartItem c2 = CartItem.builder().id(1L).quantity(2).build();
        CartItem c3 = CartItem.builder().id(2L).quantity(3).build();

        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
        assertNotEquals(c1, c3);
        assertNotEquals(c1, null);
        assertNotEquals(c1, new Object());
        assertEquals(c1, c1);
        assertTrue(c1.canEqual(c2));
    }
}

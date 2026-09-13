package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CartTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Cart cart = new Cart();
        User user = new User();
        user.setId(1L);
        List<CartItem> items = new ArrayList<>();
        items.add(new CartItem());

        cart.setId(10L);
        cart.setUser(user);
        cart.setItems(items);

        assertEquals(10L, cart.getId());
        assertEquals(user, cart.getUser());
        assertEquals(items, cart.getItems());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        List<CartItem> items = new ArrayList<>();
        Cart cart = new Cart(20L, user, items);

        assertEquals(20L, cart.getId());
        assertEquals(user, cart.getUser());
        assertEquals(items, cart.getItems());
    }

    @Test
    void testBuilder() {
        User user = new User();
        List<CartItem> items = new ArrayList<>();
        Cart cart = Cart.builder()
                .id(30L)
                .user(user)
                .items(items)
                .build();

        assertEquals(30L, cart.getId());
        assertEquals(user, cart.getUser());
        assertEquals(items, cart.getItems());
        assertNotNull(cart.toString());
    }

    @Test
    void testBuilderDefaults() {
        Cart cart = Cart.builder().build();
        assertNotNull(cart.getItems());
        assertTrue(cart.getItems().isEmpty());
    }

    @Test
    void testEqualsAndHashCode() {
        Cart c1 = Cart.builder().id(1L).build();
        Cart c2 = Cart.builder().id(1L).build();
        Cart c3 = Cart.builder().id(2L).build();

        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
        assertNotEquals(c1, c3);
        assertNotEquals(c1, null);
        assertNotEquals(c1, new Object());
        assertEquals(c1, c1);
        assertTrue(c1.canEqual(c2));
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class OrderItemTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        OrderItem item = new OrderItem();
        Order order = new Order();
        order.setId(1L);
        Book book = new Book();
        book.setId(2L);

        item.setId(10L);
        item.setOrder(order);
        item.setBook(book);
        item.setQuantity(4);
        item.setPrice(120.0);

        assertEquals(10L, item.getId());
        assertEquals(order, item.getOrder());
        assertEquals(book, item.getBook());
        assertEquals(4, item.getQuantity());
        assertEquals(120.0, item.getPrice());
    }

    @Test
    void testAllArgsConstructor() {
        Order order = new Order();
        Book book = new Book();
        OrderItem item = new OrderItem(20L, order, book, 2, 50.0);

        assertEquals(20L, item.getId());
        assertEquals(order, item.getOrder());
        assertEquals(book, item.getBook());
        assertEquals(2, item.getQuantity());
        assertEquals(50.0, item.getPrice());
    }

    @Test
    void testBuilder() {
        Order order = new Order();
        Book book = new Book();
        OrderItem item = OrderItem.builder()
                .id(30L)
                .order(order)
                .book(book)
                .quantity(1)
                .price(99.99)
                .build();

        assertEquals(30L, item.getId());
        assertEquals(order, item.getOrder());
        assertEquals(book, item.getBook());
        assertEquals(1, item.getQuantity());
        assertEquals(99.99, item.getPrice());
        assertNotNull(item.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        OrderItem item1 = OrderItem.builder().id(1L).quantity(2).price(10.0).build();
        OrderItem item2 = OrderItem.builder().id(1L).quantity(2).price(10.0).build();
        OrderItem item3 = OrderItem.builder().id(2L).quantity(3).price(20.0).build();

        assertEquals(item1, item2);
        assertEquals(item1.hashCode(), item2.hashCode());
        assertNotEquals(item1, item3);
        assertNotEquals(item1, null);
        assertNotEquals(item1, new Object());
        assertEquals(item1, item1);
        assertTrue(item1.canEqual(item2));
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ShippingStatusTest {

    @Test
    void testEnumValues() {
        ShippingStatus[] statuses = ShippingStatus.values();
        assertEquals(6, statuses.length);
        assertArrayEquals(new ShippingStatus[]{
                ShippingStatus.PENDING,
                ShippingStatus.PROCESSING,
                ShippingStatus.SHIPPING,
                ShippingStatus.DELIVERED,
                ShippingStatus.CANCELLED,
                ShippingStatus.RETURNED
        }, statuses);
    }

    @Test
    void testEnumValueOf() {
        assertEquals(ShippingStatus.PENDING, ShippingStatus.valueOf("PENDING"));
        assertEquals(ShippingStatus.PROCESSING, ShippingStatus.valueOf("PROCESSING"));
        assertEquals(ShippingStatus.SHIPPING, ShippingStatus.valueOf("SHIPPING"));
        assertEquals(ShippingStatus.DELIVERED, ShippingStatus.valueOf("DELIVERED"));
        assertEquals(ShippingStatus.CANCELLED, ShippingStatus.valueOf("CANCELLED"));
        assertEquals(ShippingStatus.RETURNED, ShippingStatus.valueOf("RETURNED"));
    }
}

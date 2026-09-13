package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DiscountTypeTest {

    @Test
    void testEnumValues() {
        DiscountType[] types = DiscountType.values();
        assertEquals(2, types.length);
        assertArrayEquals(new DiscountType[]{
                DiscountType.PERCENTAGE,
                DiscountType.FIXED
        }, types);
    }

    @Test
    void testEnumValueOf() {
        assertEquals(DiscountType.PERCENTAGE, DiscountType.valueOf("PERCENTAGE"));
        assertEquals(DiscountType.FIXED, DiscountType.valueOf("FIXED"));
    }
}

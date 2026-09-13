package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class CouponTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Coupon coupon = new Coupon();
        LocalDateTime expiration = LocalDateTime.now().plusDays(7);

        coupon.setId(1L);
        coupon.setCode("SUMMER2026");
        coupon.setDiscountType(DiscountType.PERCENTAGE);
        coupon.setDiscountValue(15.0);
        coupon.setMinOrderAmount(100.0);
        coupon.setExpirationDate(expiration);
        coupon.setIsActive(true);
        coupon.setMaxDiscountAmount(50.0);
        coupon.setUserId(10L);
        coupon.setCategory("DISCOUNT");
        coupon.setUsageLimit(100);
        coupon.setIsPartner(true);

        assertEquals(1L, coupon.getId());
        assertEquals("SUMMER2026", coupon.getCode());
        assertEquals(DiscountType.PERCENTAGE, coupon.getDiscountType());
        assertEquals(15.0, coupon.getDiscountValue());
        assertEquals(100.0, coupon.getMinOrderAmount());
        assertEquals(expiration, coupon.getExpirationDate());
        assertTrue(coupon.getIsActive());
        assertEquals(50.0, coupon.getMaxDiscountAmount());
        assertEquals(10L, coupon.getUserId());
        assertEquals("DISCOUNT", coupon.getCategory());
        assertEquals(100, coupon.getUsageLimit());
        assertTrue(coupon.getIsPartner());
    }

    @Test
    void testAllArgsConstructor() {
        LocalDateTime expiration = LocalDateTime.now().plusDays(10);
        Coupon coupon = new Coupon(
                2L,
                "FLAT50K",
                DiscountType.FIXED,
                50000.0,
                200000.0,
                expiration,
                false,
                50000.0,
                5L,
                "SHIPPING",
                50,
                false
        );

        assertEquals(2L, coupon.getId());
        assertEquals("FLAT50K", coupon.getCode());
        assertEquals(DiscountType.FIXED, coupon.getDiscountType());
        assertEquals(50000.0, coupon.getDiscountValue());
        assertEquals(200000.0, coupon.getMinOrderAmount());
        assertEquals(expiration, coupon.getExpirationDate());
        assertFalse(coupon.getIsActive());
        assertEquals(50000.0, coupon.getMaxDiscountAmount());
        assertEquals(5L, coupon.getUserId());
        assertEquals("SHIPPING", coupon.getCategory());
        assertEquals(50, coupon.getUsageLimit());
        assertFalse(coupon.getIsPartner());
    }

    @Test
    void testBuilderDefaults() {
        Coupon coupon = Coupon.builder()
                .code("CODE")
                .build();

        assertEquals(0.0, coupon.getMinOrderAmount());
        assertTrue(coupon.getIsActive());
        assertFalse(coupon.getIsPartner());
    }

    @Test
    void testEqualsAndHashCode() {
        Coupon c1 = Coupon.builder().id(1L).code("CODE").build();
        Coupon c2 = Coupon.builder().id(1L).code("CODE").build();
        Coupon c3 = Coupon.builder().id(2L).code("CODE2").build();

        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
        assertNotEquals(c1, c3);
        assertNotEquals(c1, null);
        assertNotEquals(c1, new Object());
        assertEquals(c1, c1);
        assertTrue(c1.canEqual(c2));
        assertNotNull(c1.toString());
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class RewardVoucherTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        RewardVoucher voucher = new RewardVoucher();
        LocalDateTime expiration = LocalDateTime.now().plusDays(30);

        voucher.setId(10L);
        voucher.setCode("REWARD100");
        voucher.setRewardType("POINTS");
        voucher.setRewardValue(100);
        voucher.setExpirationDate(expiration);
        voucher.setIsActive(true);

        assertEquals(10L, voucher.getId());
        assertEquals("REWARD100", voucher.getCode());
        assertEquals("POINTS", voucher.getRewardType());
        assertEquals(100, voucher.getRewardValue());
        assertEquals(expiration, voucher.getExpirationDate());
        assertTrue(voucher.getIsActive());
    }

    @Test
    void testAllArgsConstructor() {
        LocalDateTime expiration = LocalDateTime.now().plusDays(15);
        RewardVoucher voucher = new RewardVoucher(20L, "SHIPFREE50", "FREESHIP", 1, expiration, false);

        assertEquals(20L, voucher.getId());
        assertEquals("SHIPFREE50", voucher.getCode());
        assertEquals("FREESHIP", voucher.getRewardType());
        assertEquals(1, voucher.getRewardValue());
        assertEquals(expiration, voucher.getExpirationDate());
        assertFalse(voucher.getIsActive());
    }

    @Test
    void testBuilderDefaults() {
        RewardVoucher voucher = RewardVoucher.builder()
                .code("VOUCHER")
                .build();

        assertTrue(voucher.getIsActive());
    }

    @Test
    void testEqualsAndHashCode() {
        RewardVoucher v1 = RewardVoucher.builder().id(1L).code("CODE").build();
        RewardVoucher v2 = RewardVoucher.builder().id(1L).code("CODE").build();
        RewardVoucher v3 = RewardVoucher.builder().id(2L).code("CODE2").build();

        assertEquals(v1, v2);
        assertEquals(v1.hashCode(), v2.hashCode());
        assertNotEquals(v1, v3);
        assertNotEquals(v1, null);
        assertNotEquals(v1, new Object());
        assertEquals(v1, v1);
        assertTrue(v1.canEqual(v2));
        assertNotNull(v1.toString());
    }
}

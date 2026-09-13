package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class UserRewardTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        UserReward userReward = new UserReward();
        User user = new User();
        user.setId(1L);
        RewardVoucher voucher = new RewardVoucher();
        voucher.setId(2L);
        LocalDateTime now = LocalDateTime.now();

        userReward.setId(10L);
        userReward.setUser(user);
        userReward.setVoucher(voucher);
        userReward.setRedeemedAt(now);

        assertEquals(10L, userReward.getId());
        assertEquals(user, userReward.getUser());
        assertEquals(voucher, userReward.getVoucher());
        assertEquals(now, userReward.getRedeemedAt());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        RewardVoucher voucher = new RewardVoucher();
        LocalDateTime now = LocalDateTime.now();

        UserReward userReward = new UserReward(20L, user, voucher, now);

        assertEquals(20L, userReward.getId());
        assertEquals(user, userReward.getUser());
        assertEquals(voucher, userReward.getVoucher());
        assertEquals(now, userReward.getRedeemedAt());
    }

    @Test
    void testBuilder() {
        User user = new User();
        RewardVoucher voucher = new RewardVoucher();
        LocalDateTime now = LocalDateTime.now();

        UserReward userReward = UserReward.builder()
                .id(30L)
                .user(user)
                .voucher(voucher)
                .redeemedAt(now)
                .build();

        assertEquals(30L, userReward.getId());
        assertEquals(user, userReward.getUser());
        assertEquals(voucher, userReward.getVoucher());
        assertEquals(now, userReward.getRedeemedAt());
        assertNotNull(userReward.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        UserReward ur1 = UserReward.builder().id(1L).build();
        UserReward ur2 = UserReward.builder().id(1L).build();
        UserReward ur3 = UserReward.builder().id(2L).build();

        assertEquals(ur1, ur2);
        assertEquals(ur1.hashCode(), ur2.hashCode());
        assertNotEquals(ur1, ur3);
        assertNotEquals(ur1, null);
        assertNotEquals(ur1, new Object());
        assertEquals(ur1, ur1);
        assertTrue(ur1.canEqual(ur2));
    }
}

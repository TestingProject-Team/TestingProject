package com.bookstore.repository;

import com.bookstore.entity.Coupon;
import com.bookstore.entity.DiscountType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

@DataJpaTest
@ActiveProfiles("test")
class CouponRepositoryTest {

    @Autowired
    private CouponRepository couponRepository;

    private Coupon activeCoupon;
    private Coupon inactiveCoupon;

    @BeforeEach
    void setUp() {
        activeCoupon = Coupon.builder()
                .code("DISCOUNT20")
                .discountType(DiscountType.PERCENTAGE)
                .discountValue(20.0)
                .minOrderAmount(100.0)
                .expirationDate(LocalDateTime.now().plusDays(30))
                .isActive(true)
                .category("DISCOUNT")
                .build();

        inactiveCoupon = Coupon.builder()
                .code("EXPIRED10")
                .discountType(DiscountType.FIXED)
                .discountValue(10.0)
                .minOrderAmount(50.0)
                .expirationDate(LocalDateTime.now().minusDays(1))
                .isActive(false)
                .category("DISCOUNT")
                .build();

        couponRepository.saveAll(List.of(activeCoupon, inactiveCoupon));
    }

    @Test
    @DisplayName("Find active coupon by code ignore case - Success")
    void testFindByCodeIgnoreCaseAndIsActiveTrueSuccess() {
        Optional<Coupon> foundLower = couponRepository.findByCodeIgnoreCaseAndIsActiveTrue("discount20");
        assertThat(foundLower).isPresent();
        assertThat(foundLower.get().getCode()).isEqualTo("DISCOUNT20");

        Optional<Coupon> foundUpper = couponRepository.findByCodeIgnoreCaseAndIsActiveTrue("DISCOUNT20");
        assertThat(foundUpper).isPresent();
    }

    @Test
    @DisplayName("Find active coupon returns empty when coupon is inactive")
    void testFindByCodeIgnoreCaseAndIsActiveTrueWhenInactive() {
        Optional<Coupon> found = couponRepository.findByCodeIgnoreCaseAndIsActiveTrue("EXPIRED10");
        assertThat(found).isEmpty();
    }

    @Test
    @DisplayName("Find all active coupons - Success")
    void testFindByIsActiveTrue() {
        List<Coupon> activeList = couponRepository.findByIsActiveTrue();
        assertThat(activeList).hasSize(1);
        assertThat(activeList.get(0).getCode()).isEqualTo("DISCOUNT20");
    }

    @Test
    @DisplayName("Duplicate coupon code throws DataIntegrityViolationException")
    void testDuplicateCouponCodeThrowsException() {
        Coupon duplicate = Coupon.builder()
                .code("DISCOUNT20") // Duplicate
                .discountType(DiscountType.FIXED)
                .discountValue(5.0)
                .isActive(true)
                .build();

        assertThrows(DataIntegrityViolationException.class, () -> {
            couponRepository.saveAndFlush(duplicate);
        });
    }
}

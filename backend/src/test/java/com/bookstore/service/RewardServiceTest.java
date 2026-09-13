package com.bookstore.service;

import com.bookstore.entity.*;
import com.bookstore.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class RewardServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private CouponRepository couponRepository;

    @Mock
    private PointTransactionRepository pointTransactionRepository;

    @Mock
    private RewardVoucherRepository rewardVoucherRepository;

    @Mock
    private UserRewardRepository userRewardRepository;

    @InjectMocks
    private RewardService rewardService;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .id(1L)
                .username("testuser")
                .yPoints(30000)
                .freeShipCoupons(0)
                .build();
    }

    @Test
    void exchangePoints_Success_Freeship() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        rewardService.exchangePoints("testuser", 20000, "FREESHIP");

        assertEquals(10000, testUser.getYPoints());
        assertEquals(2, testUser.getFreeShipCoupons());

        verify(userRepository, times(1)).save(testUser);
        verify(pointTransactionRepository, times(1)).save(any(PointTransaction.class));
        verify(couponRepository, never()).save(any(Coupon.class));
    }

    @Test
    void exchangePoints_BvaFreeshipOneBelowMinimum_ThrowsException() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        RuntimeException exception = assertThrows(RuntimeException.class, () ->
                rewardService.exchangePoints("testuser", 9999, "FREESHIP"));

        assertEquals("Cần ít nhất 10,000 điểm để đổi mã Freeship.", exception.getMessage());
        verify(userRepository, never()).save(any(User.class));
        verify(pointTransactionRepository, never()).save(any(PointTransaction.class));
    }

    @ParameterizedTest(name = "BVA: đổi Freeship với {0} điểm")
    @ValueSource(ints = {10000, 10001})
    void exchangePoints_BvaFreeshipAtAndAboveMinimum_Succeeds(int pointsToSpend) {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        rewardService.exchangePoints("testuser", pointsToSpend, "FREESHIP");

        assertEquals(30000 - pointsToSpend, testUser.getYPoints());
        assertEquals(1, testUser.getFreeShipCoupons());
        verify(userRepository).save(testUser);
        verify(pointTransactionRepository).save(any(PointTransaction.class));
    }

    @Test
    void exchangePoints_Failure_NotEnoughPoints() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            rewardService.exchangePoints("testuser", 40000, "FREESHIP");
        });

        assertEquals("Không đủ Y-Points để đổi!", exception.getMessage());
        verify(userRepository, never()).save(any(User.class));
        verify(pointTransactionRepository, never()).save(any(PointTransaction.class));
    }

    @Test
    void exchangePoints_Failure_InvalidDiscount20kPoints() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            rewardService.exchangePoints("testuser", 10000, "DISCOUNT_20K");
        });

        assertEquals("Cần đúng 20,000 điểm để đổi mã giảm 20K.", exception.getMessage());
        verify(userRepository, never()).save(any(User.class));
        verify(pointTransactionRepository, never()).save(any(PointTransaction.class));
    }

    @ParameterizedTest(name = "BVA: DISCOUNT_20K từ chối {0} điểm")
    @ValueSource(ints = {19999, 20001})
    void exchangePoints_BvaDiscount20kAdjacentValues_ThrowsException(int pointsToSpend) {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        RuntimeException exception = assertThrows(RuntimeException.class, () ->
                rewardService.exchangePoints("testuser", pointsToSpend, "DISCOUNT_20K"));

        assertEquals("Cần đúng 20,000 điểm để đổi mã giảm 20K.", exception.getMessage());
        verify(couponRepository, never()).save(any(Coupon.class));
        verify(userRepository, never()).save(any(User.class));
        verify(pointTransactionRepository, never()).save(any(PointTransaction.class));
    }

    @Test
    void exchangePoints_Success_Discount20k() {
        testUser.setYPoints(25000);
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        rewardService.exchangePoints("testuser", 20000, "DISCOUNT_20K");

        assertEquals(5000, testUser.getYPoints());

        ArgumentCaptor<Coupon> couponCaptor = ArgumentCaptor.forClass(Coupon.class);
        verify(couponRepository, times(1)).save(couponCaptor.capture());

        Coupon savedCoupon = couponCaptor.getValue();
        assertNotNull(savedCoupon);
        assertTrue(savedCoupon.getCode().startsWith("VIP20K-"));
        assertEquals(20000.0, savedCoupon.getDiscountValue());
        assertEquals(1L, savedCoupon.getUserId());

        verify(userRepository, times(1)).save(testUser);
        verify(pointTransactionRepository, times(1)).save(any(PointTransaction.class));
    }

    @Test
    void redeemVoucher_Success_Points() {
        RewardVoucher voucher = RewardVoucher.builder()
                .id(10L)
                .code("WELCOME100")
                .isActive(true)
                .rewardType("POINTS")
                .rewardValue(100)
                .expirationDate(LocalDateTime.now().plusDays(10))
                .build();

        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("WELCOME100")).thenReturn(Optional.of(voucher));
        when(userRewardRepository.existsByUserIdAndVoucherId(1L, 10L)).thenReturn(false);

        rewardService.redeemVoucher("testuser", "WELCOME100");

        assertEquals(30100, testUser.getYPoints());
        verify(userRepository).save(testUser);
        verify(userRewardRepository).save(any(UserReward.class));
        verify(pointTransactionRepository).save(any(PointTransaction.class));
    }

    @Test
    void redeemVoucher_Failure_InactiveVoucher() {
        RewardVoucher voucher = RewardVoucher.builder()
                .id(10L)
                .code("INACTIVE")
                .isActive(false)
                .build();

        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("INACTIVE")).thenReturn(Optional.of(voucher));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            rewardService.redeemVoucher("testuser", "INACTIVE");
        });

        assertEquals("Lỗi: mã không còn hoạt động.", exception.getMessage());
    }

    @Test
    void redeemVoucher_Failure_ExpiredVoucher() {
        RewardVoucher voucher = RewardVoucher.builder()
                .id(10L)
                .code("EXPIRED")
                .isActive(true)
                .expirationDate(LocalDateTime.now().minusDays(1))
                .build();

        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("EXPIRED")).thenReturn(Optional.of(voucher));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            rewardService.redeemVoucher("testuser", "EXPIRED");
        });

        assertEquals("Lỗi: mã đã hết hạn.", exception.getMessage());
    }

    @Test
    void redeemVoucher_UserNotFound_ThrowsException() {
        when(userRepository.findByUsername("unknown")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> rewardService.redeemVoucher("unknown", "CODE"));
    }

    @Test
    void redeemVoucher_VoucherNotFound_ThrowsException() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("INVALID")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> rewardService.redeemVoucher("testuser", "INVALID"));
    }

    @Test
    void redeemVoucher_AlreadyUsed_ThrowsException() {
        RewardVoucher voucher = RewardVoucher.builder()
                .id(10L)
                .code("USED")
                .isActive(true)
                .build();
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("USED")).thenReturn(Optional.of(voucher));
        when(userRewardRepository.existsByUserIdAndVoucherId(1L, 10L)).thenReturn(true);

        assertThrows(RuntimeException.class, () -> rewardService.redeemVoucher("testuser", "USED"));
    }

    @Test
    void redeemVoucher_Success_FreeShip() {
        RewardVoucher voucher = RewardVoucher.builder()
                .id(11L)
                .code("FREESHIP_VOUCHER")
                .isActive(true)
                .rewardType("FREESHIP")
                .rewardValue(2)
                .build();

        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("FREESHIP_VOUCHER")).thenReturn(Optional.of(voucher));
        when(userRewardRepository.existsByUserIdAndVoucherId(1L, 11L)).thenReturn(false);

        rewardService.redeemVoucher("testuser", "FREESHIP_VOUCHER");

        assertEquals(2, testUser.getFreeShipCoupons());
    }

    @Test
    void getHistory_Success() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(pointTransactionRepository.findByUserIdOrderByCreatedAtDesc(1L)).thenReturn(java.util.List.of());

        java.util.List<PointTransaction> history = rewardService.getHistory("testuser");
        assertNotNull(history);
    }

    @Test
    void getHistory_UserNotFound_ThrowsException() {
        when(userRepository.findByUsername("unknown")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> rewardService.getHistory("unknown"));
    }

    @Test
    void exchangePoints_UserNotFound_ThrowsException() {
        when(userRepository.findByUsername("unknown")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> rewardService.exchangePoints("unknown", 1000, "FREESHIP"));
    }

    @Test
    void exchangePoints_UnknownRewardType_ThrowsException() {
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        RuntimeException error = assertThrows(RuntimeException.class,
                () -> rewardService.exchangePoints("testuser", 1000, "UNKNOWN"));

        assertEquals("Loại quà không hợp lệ.", error.getMessage());
    }

    @Test
    void exchangePoints_Discount50k_SuccessAndFailure() {
        testUser.setYPoints(60000);
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        // Invalid points != 50000
        assertThrows(RuntimeException.class, () -> rewardService.exchangePoints("testuser", 40000, "DISCOUNT_50K"));

        // Valid points == 50000
        rewardService.exchangePoints("testuser", 50000, "DISCOUNT_50K");
        assertEquals(10000, testUser.getYPoints());
        verify(couponRepository).save(any(Coupon.class));
    }

    @Test
    void redeemVoucher_NullUserPointsAndFreeShip() {
        testUser.setYPoints(null);
        testUser.setFreeShipCoupons(null);

        RewardVoucher voucher = RewardVoucher.builder()
                .id(12L)
                .code("POINTS_NULL")
                .isActive(true)
                .rewardType("POINTS")
                .rewardValue(100)
                .build();

        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("POINTS_NULL")).thenReturn(Optional.of(voucher));
        when(userRewardRepository.existsByUserIdAndVoucherId(1L, 12L)).thenReturn(false);

        rewardService.redeemVoucher("testuser", "POINTS_NULL");
        assertEquals(100, testUser.getYPoints());

        // Now test freeship when null
        RewardVoucher shipVoucher = RewardVoucher.builder()
                .id(13L)
                .code("SHIP_NULL")
                .isActive(true)
                .rewardType("FREESHIP")
                .rewardValue(3)
                .build();
        testUser.setFreeShipCoupons(null);
        when(rewardVoucherRepository.findByCode("SHIP_NULL")).thenReturn(Optional.of(shipVoucher));
        when(userRewardRepository.existsByUserIdAndVoucherId(1L, 13L)).thenReturn(false);

        rewardService.redeemVoucher("testuser", "SHIP_NULL");
        assertEquals(3, testUser.getFreeShipCoupons());
    }

    @Test
    void redeemVoucher_Success_OtherRewardType() {
        RewardVoucher voucher = RewardVoucher.builder()
                .id(14L)
                .code("OTHER_TYPE")
                .isActive(true)
                .rewardType("OTHER")
                .rewardValue(5)
                .build();

        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(rewardVoucherRepository.findByCode("OTHER_TYPE")).thenReturn(Optional.of(voucher));
        when(userRewardRepository.existsByUserIdAndVoucherId(1L, 14L)).thenReturn(false);

        rewardService.redeemVoucher("testuser", "OTHER_TYPE");
        assertEquals(30000, testUser.getYPoints());
    }

    @Test
    void exchangePoints_NullUserPointsAndFreeship() {
        testUser.setYPoints(null);
        testUser.setFreeShipCoupons(null);
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        assertThrows(RuntimeException.class, () -> rewardService.exchangePoints("testuser", 10000, "FREESHIP"));
    }

    @Test
    void exchangePoints_Success_Freeship_WhenUserFreeShipCouponsNull() {
        testUser.setYPoints(30000);
        testUser.setFreeShipCoupons(null);
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        rewardService.exchangePoints("testuser", 10000, "FREESHIP");
        assertEquals(1, testUser.getFreeShipCoupons());
    }
}

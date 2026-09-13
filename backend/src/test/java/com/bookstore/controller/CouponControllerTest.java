package com.bookstore.controller;

import com.bookstore.entity.Coupon;
import com.bookstore.service.CouponService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.security.Principal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CouponControllerTest {

    @Mock
    private CouponService couponService;

    @Mock
    private Principal principal;

    @InjectMocks
    private CouponController couponController;

    private Coupon testCoupon;

    @BeforeEach
    void setUp() {
        testCoupon = Coupon.builder()
                .id(1L)
                .code("DISCOUNT10")
                .discountValue(10.0)
                .isActive(true)
                .build();
    }

    @Test
    void testGetAllCoupons_WithPrincipal() {
        when(principal.getName()).thenReturn("testuser");
        when(couponService.getAvailableCouponsForUser("testuser")).thenReturn(List.of(testCoupon));

        ResponseEntity<List<Coupon>> response = couponController.getAllCoupons(principal);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testCoupon), response.getBody());
    }

    @Test
    void testGetAllCoupons_NullPrincipal() {
        when(couponService.getAvailableCouponsForUser(null)).thenReturn(List.of(testCoupon));

        ResponseEntity<List<Coupon>> response = couponController.getAllCoupons(null);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testCoupon), response.getBody());
    }

    @Test
    void testGetCouponHistory_NullPrincipal() {
        ResponseEntity<?> response = couponController.getCouponHistory(null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testGetCouponHistory_Success() {
        when(principal.getName()).thenReturn("testuser");
        when(couponService.getCouponUsageHistory("testuser")).thenReturn(List.of());

        ResponseEntity<?> response = couponController.getCouponHistory(principal);

        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testValidateCoupon_Success() {
        when(principal.getName()).thenReturn("testuser");
        when(couponService.validateCoupon("DISCOUNT10", 100.0, "testuser")).thenReturn(testCoupon);
        when(couponService.calculateDiscount(testCoupon, 100.0)).thenReturn(10.0);

        ResponseEntity<CouponController.CouponResponse> response =
                couponController.validateCoupon("DISCOUNT10", 100.0, principal);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().valid());
        assertEquals(10.0, response.getBody().discountAmount());
    }

    @Test
    void testValidateCoupon_Failure() {
        when(principal.getName()).thenReturn("testuser");
        when(couponService.validateCoupon("INVALID", 100.0, "testuser"))
                .thenThrow(new RuntimeException("Coupon not found"));

        ResponseEntity<CouponController.CouponResponse> response =
                couponController.validateCoupon("INVALID", 100.0, principal);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertFalse(response.getBody().valid());
        assertEquals("Coupon not found", response.getBody().message());

        // Validate with null principal
        when(couponService.validateCoupon("INVALID", 100.0, null))
                .thenThrow(new RuntimeException("Coupon not found"));
        ResponseEntity<CouponController.CouponResponse> responseNullPrincipal =
                couponController.validateCoupon("INVALID", 100.0, null);
        assertFalse(responseNullPrincipal.getBody().valid());
    }

    @Test
    void testGetAllCouponsAdmin() {
        when(couponService.getAllCouponsAdmin()).thenReturn(List.of(testCoupon));

        ResponseEntity<List<Coupon>> response = couponController.getAllCouponsAdmin();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testCoupon), response.getBody());
    }

    @Test
    void testCreateCoupon() {
        when(couponService.createCoupon(testCoupon)).thenReturn(testCoupon);

        ResponseEntity<Coupon> response = couponController.createCoupon(testCoupon);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCoupon, response.getBody());
    }

    @Test
    void testUpdateCoupon() {
        when(couponService.updateCoupon(1L, testCoupon)).thenReturn(testCoupon);

        ResponseEntity<Coupon> response = couponController.updateCoupon(1L, testCoupon);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCoupon, response.getBody());
    }

    @Test
    void testDeleteCoupon() {
        ResponseEntity<Void> response = couponController.deleteCoupon(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(couponService).deleteCoupon(1L);
    }
}
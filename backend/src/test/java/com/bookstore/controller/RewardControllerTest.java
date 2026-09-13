package com.bookstore.controller;

import com.bookstore.entity.PointTransaction;
import com.bookstore.service.RewardService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RewardControllerTest {

    @Mock
    private RewardService rewardService;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private RewardController rewardController;

    @Test
    void testRedeemVoucher_NullOrEmptyCode() {
        ResponseEntity<?> response1 = rewardController.redeemVoucher(authentication, Map.of());
        assertEquals(HttpStatus.BAD_REQUEST, response1.getStatusCode());

        ResponseEntity<?> response2 = rewardController.redeemVoucher(authentication, Map.of("code", "   "));
        assertEquals(HttpStatus.BAD_REQUEST, response2.getStatusCode());
    }

    @Test
    void testRedeemVoucher_Success() {
        when(authentication.getName()).thenReturn("testuser");
        doNothing().when(rewardService).redeemVoucher("testuser", "REWARD10");

        ResponseEntity<?> response = rewardController.redeemVoucher(authentication, Map.of("code", "REWARD10"));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(rewardService).redeemVoucher("testuser", "REWARD10");
    }

    @Test
    void testRedeemVoucher_RuntimeException() {
        when(authentication.getName()).thenReturn("testuser");
        doThrow(new RuntimeException("Mã không hợp lệ")).when(rewardService).redeemVoucher("testuser", "INVALID");

        ResponseEntity<?> response = rewardController.redeemVoucher(authentication, Map.of("code", "INVALID"));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testGetHistory() {
        PointTransaction tx = PointTransaction.builder().id(1L).transactionValue(100).build();
        when(authentication.getName()).thenReturn("testuser");
        when(rewardService.getHistory("testuser")).thenReturn(List.of(tx));

        ResponseEntity<List<PointTransaction>> response = rewardController.getHistory(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(tx), response.getBody());
    }

    @Test
    void testExchangePoints_Success() {
        when(authentication.getName()).thenReturn("testuser");
        doNothing().when(rewardService).exchangePoints("testuser", 50, "VOUCHER");

        ResponseEntity<?> response = rewardController.exchangePoints(authentication, Map.of("points", 50, "type", "VOUCHER"));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(rewardService).exchangePoints("testuser", 50, "VOUCHER");
    }

    @Test
    void testExchangePoints_Exception() {
        when(authentication.getName()).thenReturn("testuser");
        doThrow(new RuntimeException("Không đủ điểm")).when(rewardService).exchangePoints("testuser", 50, "VOUCHER");

        ResponseEntity<?> response = rewardController.exchangePoints(authentication, Map.of("points", 50, "type", "VOUCHER"));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }
}
package com.bookstore.controller;

import com.bookstore.entity.RewardVoucher;
import com.bookstore.repository.RewardVoucherRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AdminRewardControllerTest {

    @Mock
    private RewardVoucherRepository rewardVoucherRepository;

    @InjectMocks
    private AdminRewardController adminRewardController;

    private RewardVoucher testVoucher;

    @BeforeEach
    void setUp() {
        testVoucher = RewardVoucher.builder()
                .id(1L)
                .code("REWARD100")
                .rewardValue(100)
                .expirationDate(LocalDateTime.now().plusDays(30))
                .isActive(true)
                .build();
    }

    @Test
    void testGetAllVouchers() {
        when(rewardVoucherRepository.findAll()).thenReturn(List.of(testVoucher));

        ResponseEntity<List<RewardVoucher>> response = adminRewardController.getAllVouchers();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testVoucher), response.getBody());
        verify(rewardVoucherRepository).findAll();
    }

    @Test
    void testCreateVoucher_NullOrEmptyCode() {
        RewardVoucher voucherNullCode = RewardVoucher.builder().code(null).build();
        ResponseEntity<?> response1 = adminRewardController.createVoucher(voucherNullCode);
        assertEquals(HttpStatus.BAD_REQUEST, response1.getStatusCode());

        RewardVoucher voucherEmptyCode = RewardVoucher.builder().code("   ").build();
        ResponseEntity<?> response2 = adminRewardController.createVoucher(voucherEmptyCode);
        assertEquals(HttpStatus.BAD_REQUEST, response2.getStatusCode());
    }

    @Test
    void testCreateVoucher_CodeAlreadyExists() {
        when(rewardVoucherRepository.findByCode("EXISTING")).thenReturn(Optional.of(testVoucher));

        RewardVoucher newVoucher = RewardVoucher.builder().code("EXISTING").build();
        ResponseEntity<?> response = adminRewardController.createVoucher(newVoucher);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertTrue(response.getBody() instanceof Map);
        assertEquals("Mã đã tồn tại", ((Map<?, ?>) response.getBody()).get("message"));
    }

    @Test
    void testCreateVoucher_Success() {
        when(rewardVoucherRepository.findByCode("newcode")).thenReturn(Optional.empty());
        when(rewardVoucherRepository.save(any(RewardVoucher.class))).thenAnswer(i -> i.getArgument(0));

        RewardVoucher newVoucher = RewardVoucher.builder()
                .code(" newcode ")
                .rewardValue(50)
                .build();

        ResponseEntity<?> response = adminRewardController.createVoucher(newVoucher);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        RewardVoucher saved = (RewardVoucher) response.getBody();
        assertNotNull(saved);
        assertEquals("NEWCODE", saved.getCode());
        assertTrue(saved.getIsActive());
    }

    @Test
    void testUpdateVoucher_NotFound() {
        when(rewardVoucherRepository.findById(1L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = adminRewardController.updateVoucher(1L, testVoucher);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testUpdateVoucher_Success() {
        when(rewardVoucherRepository.findById(1L)).thenReturn(Optional.of(testVoucher));
        when(rewardVoucherRepository.save(any(RewardVoucher.class))).thenAnswer(i -> i.getArgument(0));

        RewardVoucher details = RewardVoucher.builder()
                .rewardValue(200)
                .expirationDate(LocalDateTime.now().plusDays(60))
                .isActive(false)
                .build();

        ResponseEntity<?> response = adminRewardController.updateVoucher(1L, details);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        RewardVoucher saved = (RewardVoucher) response.getBody();
        assertNotNull(saved);
        assertEquals(200, saved.getRewardValue());
        assertFalse(saved.getIsActive());
    }

    @Test
    void testDeleteVoucher_NotFound() {
        when(rewardVoucherRepository.findById(1L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = adminRewardController.deleteVoucher(1L);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testDeleteVoucher_Success() {
        when(rewardVoucherRepository.findById(1L)).thenReturn(Optional.of(testVoucher));

        ResponseEntity<?> response = adminRewardController.deleteVoucher(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(rewardVoucherRepository).delete(testVoucher);
    }
}
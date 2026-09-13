package com.bookstore.controller;

import com.bookstore.entity.User;
import com.bookstore.entity.VatInvoice;
import com.bookstore.repository.UserRepository;
import com.bookstore.repository.VatInvoiceRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class VatInvoiceControllerTest {

    @Mock
    private VatInvoiceRepository vatInvoiceRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private VatInvoiceController vatInvoiceController;

    private User testUser;
    private VatInvoice testInvoice;

    @BeforeEach
    void setUp() {
        testUser = User.builder().id(1L).username("testuser").build();
        testInvoice = VatInvoice.builder()
                .id(10L)
                .user(testUser)
                .companyName("Test Company")
                .taxCode("0123456789")
                .companyAddress("123 Street")
                .email("company@example.com")
                .type("COMPANY")
                .build();
    }

    @Test
    void testGetMyVatInvoice_Unauthorized() {
        ResponseEntity<?> response1 = vatInvoiceController.getMyVatInvoice(null);
        assertEquals(HttpStatus.UNAUTHORIZED, response1.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<?> response2 = vatInvoiceController.getMyVatInvoice(authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response2.getStatusCode());
    }

    @Test
    void testGetMyVatInvoice_Present() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(vatInvoiceRepository.findByUserId(1L)).thenReturn(Optional.of(testInvoice));

        ResponseEntity<?> response = vatInvoiceController.getMyVatInvoice(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testInvoice, response.getBody());
    }

    @Test
    void testGetMyVatInvoice_Empty() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(vatInvoiceRepository.findByUserId(1L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = vatInvoiceController.getMyVatInvoice(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testSaveVatInvoice_Unauthorized() {
        ResponseEntity<?> response = vatInvoiceController.saveVatInvoice(testInvoice, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testSaveVatInvoice_CreateNew() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(vatInvoiceRepository.findByUserId(1L)).thenReturn(Optional.empty());
        when(vatInvoiceRepository.save(any(VatInvoice.class))).thenAnswer(i -> i.getArgument(0));

        ResponseEntity<?> response = vatInvoiceController.saveVatInvoice(testInvoice, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(vatInvoiceRepository).save(any(VatInvoice.class));
    }

    @Test
    void testSaveVatInvoice_UpdateExisting() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(vatInvoiceRepository.findByUserId(1L)).thenReturn(Optional.of(testInvoice));
        when(vatInvoiceRepository.save(any(VatInvoice.class))).thenAnswer(i -> i.getArgument(0));

        VatInvoice updatedData = VatInvoice.builder()
                .companyName("New Company")
                .taxCode("9876543210")
                .companyAddress("456 Avenue")
                .email("new@example.com")
                .type("PERSONAL")
                .build();

        ResponseEntity<?> response = vatInvoiceController.saveVatInvoice(updatedData, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        VatInvoice saved = (VatInvoice) response.getBody();
        assertEquals("New Company", saved.getCompanyName());
    }
}
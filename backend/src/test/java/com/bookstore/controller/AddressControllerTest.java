package com.bookstore.controller;

import com.bookstore.entity.Address;
import com.bookstore.entity.User;
import com.bookstore.repository.AddressRepository;
import com.bookstore.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AddressControllerTest {

    @Mock
    private AddressRepository addressRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private AddressController addressController;

    private User testUser;
    private Address testAddress;

    @BeforeEach
    void setUp() {
        testUser = User.builder().id(1L).username("testuser").email("test@example.com").build();
        testAddress = Address.builder()
                .id(10L)
                .user(testUser)
                .recipientName("Nguyen Van A")
                .phone("0123456789")
                .city("HCM")
                .ward("Ward 1")
                .street("123 Street")
                .isDefault(false)
                .build();
    }

    @Test
    void testGetMyAddresses_Unauthorized() {
        ResponseEntity<?> response = addressController.getMyAddresses(null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        response = addressController.getMyAddresses(authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("notfound");
        when(userRepository.findByUsername("notfound")).thenReturn(Optional.empty());
        response = addressController.getMyAddresses(authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testGetMyAddresses_Success() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(addressRepository.findByUserId(1L)).thenReturn(List.of(testAddress));

        ResponseEntity<?> response = addressController.getMyAddresses(authentication);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testAddress), response.getBody());
    }

    @Test
    void testAddAddress_Unauthorized() {
        ResponseEntity<?> response = addressController.addAddress(testAddress, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testAddAddress_FirstAddress_BecomesDefault() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(addressRepository.findByUserId(1L)).thenReturn(Collections.emptyList());
        when(addressRepository.save(any(Address.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Address newAddress = Address.builder().recipientName("First").isDefault(false).build();
        ResponseEntity<?> response = addressController.addAddress(newAddress, authentication);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        Address saved = (Address) response.getBody();
        assertNotNull(saved);
        assertTrue(saved.isDefault());
        assertEquals(testUser, saved.getUser());
    }

    @Test
    void testAddAddress_WithExistingAndDefaultTrue() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        Address existingAddr = Address.builder().id(9L).user(testUser).isDefault(true).build();
        when(addressRepository.findByUserId(1L)).thenReturn(new ArrayList<>(List.of(existingAddr)));
        when(addressRepository.save(any(Address.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Address newAddress = Address.builder().recipientName("Second").isDefault(true).build();
        ResponseEntity<?> response = addressController.addAddress(newAddress, authentication);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertFalse(existingAddr.isDefault());
    }

    @Test
    void testAddAddress_WithExistingAndDefaultFalse() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        Address existingAddr = Address.builder().id(9L).user(testUser).isDefault(true).build();
        when(addressRepository.findByUserId(1L)).thenReturn(new ArrayList<>(List.of(existingAddr)));
        when(addressRepository.save(any(Address.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Address newAddress = Address.builder().recipientName("Second").isDefault(false).build();
        ResponseEntity<?> response = addressController.addAddress(newAddress, authentication);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        Address saved = (Address) response.getBody();
        assertNotNull(saved);
        assertFalse(saved.isDefault());
    }

    @Test
    void testSetDefaultAddress_Unauthorized() {
        ResponseEntity<?> response = addressController.setDefaultAddress(10L, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testSetDefaultAddress_NotFoundOrDifferentUser() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        when(addressRepository.findById(10L)).thenReturn(Optional.empty());
        ResponseEntity<?> response = addressController.setDefaultAddress(10L, authentication);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());

        User otherUser = User.builder().id(99L).build();
        Address otherAddress = Address.builder().id(10L).user(otherUser).build();
        when(addressRepository.findById(10L)).thenReturn(Optional.of(otherAddress));

        response = addressController.setDefaultAddress(10L, authentication);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testSetDefaultAddress_Success() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        when(addressRepository.findById(10L)).thenReturn(Optional.of(testAddress));
        Address otherAddr = Address.builder().id(11L).user(testUser).isDefault(true).build();
        when(addressRepository.findByUserId(1L)).thenReturn(List.of(testAddress, otherAddr));

        ResponseEntity<?> response = addressController.setDefaultAddress(10L, authentication);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertTrue(testAddress.isDefault());
        assertFalse(otherAddr.isDefault());
    }

    @Test
    void testUpdateAddress_Unauthorized() {
        ResponseEntity<?> response = addressController.updateAddress(10L, testAddress, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testUpdateAddress_NotFoundOrDifferentUser() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        when(addressRepository.findById(10L)).thenReturn(Optional.empty());
        ResponseEntity<?> response = addressController.updateAddress(10L, testAddress, authentication);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testUpdateAddress_SuccessWithDefaultChange() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        Address existing = Address.builder().id(10L).user(testUser).isDefault(false).build();
        Address other = Address.builder().id(11L).user(testUser).isDefault(true).build();
        when(addressRepository.findById(10L)).thenReturn(Optional.of(existing));
        when(addressRepository.findByUserId(1L)).thenReturn(List.of(existing, other));
        when(addressRepository.save(any(Address.class))).thenAnswer(i -> i.getArgument(0));

        Address updateData = Address.builder()
                .recipientName("New Name")
                .phone("0987654321")
                .city("HN")
                .ward("Ward 2")
                .street("456 St")
                .isDefault(true)
                .build();

        ResponseEntity<?> response = addressController.updateAddress(10L, updateData, authentication);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        Address saved = (Address) response.getBody();
        assertNotNull(saved);
        assertEquals("New Name", saved.getRecipientName());
        assertTrue(saved.isDefault());
        assertFalse(other.isDefault());
    }

    @Test
    void testDeleteAddress_Unauthorized() {
        ResponseEntity<?> response = addressController.deleteAddress(10L, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testDeleteAddress_NotFound() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(addressRepository.findById(10L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = addressController.deleteAddress(10L, authentication);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testDeleteAddress_Success_DefaultAddress_SetsNextAsDefault() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        testAddress.setDefault(true);
        when(addressRepository.findById(10L)).thenReturn(Optional.of(testAddress));
        Address remaining = Address.builder().id(11L).user(testUser).isDefault(false).build();
        when(addressRepository.findByUserId(1L)).thenReturn(List.of(remaining));

        ResponseEntity<?> response = addressController.deleteAddress(10L, authentication);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(addressRepository).delete(testAddress);
        assertTrue(remaining.isDefault());
        verify(addressRepository).save(remaining);
    }

    @Test
    void testDeleteAddress_Success_NonDefaultAddress() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        testAddress.setDefault(false);
        when(addressRepository.findById(10L)).thenReturn(Optional.of(testAddress));

        ResponseEntity<?> response = addressController.deleteAddress(10L, authentication);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(addressRepository).delete(testAddress);
        verify(addressRepository, never()).findByUserId(1L);
    }

    @Test
    void testDeleteAddress_Success_DefaultAddress_NoRemaining() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        testAddress.setDefault(true);
        when(addressRepository.findById(10L)).thenReturn(Optional.of(testAddress));
        when(addressRepository.findByUserId(1L)).thenReturn(Collections.emptyList());

        ResponseEntity<?> response = addressController.deleteAddress(10L, authentication);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(addressRepository).delete(testAddress);
        verify(addressRepository, never()).save(any(Address.class));
    }

    @Test
    void testDeleteAddress_DifferentUser_ReturnsNotFound() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        User otherUser = User.builder().id(999L).build();
        Address otherAddress = Address.builder().id(10L).user(otherUser).build();
        when(addressRepository.findById(10L)).thenReturn(Optional.of(otherAddress));

        ResponseEntity<?> response = addressController.deleteAddress(10L, authentication);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testUpdateAddress_DifferentUser_ReturnsNotFound() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        User otherUser = User.builder().id(999L).build();
        Address otherAddress = Address.builder().id(10L).user(otherUser).build();
        when(addressRepository.findById(10L)).thenReturn(Optional.of(otherAddress));

        ResponseEntity<?> response = addressController.updateAddress(10L, testAddress, authentication);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testUpdateAddress_WhenExistingIsDefaultTrueAndUpdatedIsDefaultTrue_DoesNotChangeOtherAddresses() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));

        Address existing = Address.builder().id(10L).user(testUser).isDefault(true).build();
        when(addressRepository.findById(10L)).thenReturn(Optional.of(existing));
        when(addressRepository.save(any(Address.class))).thenAnswer(i -> i.getArgument(0));

        Address updateData = Address.builder().recipientName("New Name").isDefault(true).build();
        ResponseEntity<?> response = addressController.updateAddress(10L, updateData, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(addressRepository, never()).findByUserId(1L);
    }

    @Test
    void testUpdateAddress_WhenBothDefaultsFalse_DoesNotChangeOtherAddresses() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        Address existing = Address.builder().id(10L).user(testUser).isDefault(false).build();
        when(addressRepository.findById(10L)).thenReturn(Optional.of(existing));
        when(addressRepository.save(any(Address.class))).thenAnswer(i -> i.getArgument(0));

        ResponseEntity<?> response = addressController.updateAddress(
                10L, Address.builder().isDefault(false).build(), authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(addressRepository, never()).findByUserId(1L);
    }
}

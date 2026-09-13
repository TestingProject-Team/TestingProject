package com.bookstore.controller;

import com.bookstore.dto.ChangePasswordRequest;
import com.bookstore.dto.ProfileUpdateRequest;
import com.bookstore.entity.User;
import com.bookstore.service.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class UserControllerTest {

    @Mock
    private UserService userService;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private UserController userController;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder().id(1L).username("testuser").email("test@example.com").build();
    }

    @Test
    void testGetProfile() {
        when(authentication.getName()).thenReturn("testuser");
        when(userService.getUserByUsername("testuser")).thenReturn(testUser);

        ResponseEntity<User> response = userController.getProfile(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testUser, response.getBody());
        verify(userService).getUserByUsername("testuser");
    }

    @Test
    void testUpdateProfile() {
        ProfileUpdateRequest request = new ProfileUpdateRequest();
        request.setFullName("New Name");

        when(authentication.getName()).thenReturn("testuser");
        when(userService.updateProfile("testuser", request)).thenReturn(testUser);

        ResponseEntity<User> response = userController.updateProfile(authentication, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testUser, response.getBody());
        verify(userService).updateProfile("testuser", request);
    }

    @Test
    void testChangePassword() {
        ChangePasswordRequest request = new ChangePasswordRequest();
        request.setOldPassword("oldPass");
        request.setNewPassword("newPass");

        when(authentication.getName()).thenReturn("testuser");

        ResponseEntity<?> response = userController.changePassword(authentication, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(userService).changePassword("testuser", request);
    }
}
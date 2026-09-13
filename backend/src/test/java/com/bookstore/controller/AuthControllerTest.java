package com.bookstore.controller;

import com.bookstore.dto.AuthRequest;
import com.bookstore.dto.AuthResponse;
import com.bookstore.dto.RegisterRequest;
import com.bookstore.entity.User;
import com.bookstore.service.AuthService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    @Mock
    private AuthService authService;

    @InjectMocks
    private AuthController authController;

    private AuthResponse authResponse;

    @BeforeEach
    void setUp() {
        User user = new User();
        user.setId(1L);
        user.setEmail("user@example.com");
        authResponse = new AuthResponse("mock-jwt-token", user);
    }

    @Test
    void testRegister() {
        RegisterRequest request = new RegisterRequest();
        request.setEmail("new@example.com");
        request.setPassword("123456");
        request.setName("New User");

        when(authService.register(any(RegisterRequest.class))).thenReturn(authResponse);

        ResponseEntity<AuthResponse> response = authController.register(request);

        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertEquals("mock-jwt-token", response.getBody().getToken());
        verify(authService, times(1)).register(any(RegisterRequest.class));
    }

    @Test
    void testLogin() {
        AuthRequest request = new AuthRequest();
        request.setEmail("user@example.com");
        request.setPassword("123456");

        when(authService.login(any(AuthRequest.class))).thenReturn(authResponse);

        ResponseEntity<AuthResponse> response = authController.login(request);

        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertEquals("mock-jwt-token", response.getBody().getToken());
        verify(authService, times(1)).login(any(AuthRequest.class));
    }
}

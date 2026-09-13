package com.bookstore.controller;

import com.bookstore.entity.Role;
import com.bookstore.entity.User;
import com.bookstore.repository.CartRepository;
import com.bookstore.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Map;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AdminUserControllerTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private CartRepository cartRepository;

    @Mock
    private JdbcTemplate jdbcTemplate;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private AdminUserController adminUserController;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .id(1L)
                .username("testuser")
                .role(Role.USER)
                .build();
    }

    @Test
    void testGetAllUsers() {
        when(userRepository.findAll()).thenReturn(List.of(testUser));

        ResponseEntity<List<User>> response = adminUserController.getAllUsers();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testUser), response.getBody());
        verify(userRepository).findAll();
    }

    @Test
    void testUpdateRole_UserNotFound() {
        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = adminUserController.updateRole(1L, Map.of("role", "ADMIN"));

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testUpdateRole_InvalidRole() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));

        ResponseEntity<?> response = adminUserController.updateRole(1L, Map.of("role", "INVALID_ROLE"));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testUpdateRole_Success() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(userRepository.save(any(User.class))).thenAnswer(i -> i.getArgument(0));

        ResponseEntity<?> response = adminUserController.updateRole(1L, Map.of("role", "ADMIN"));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        User updated = (User) response.getBody();
        assertNotNull(updated);
        assertEquals(Role.ADMIN, updated.getRole());
        verify(userRepository).save(testUser);
    }

    @Test
    void testDeleteUser_UserNotFound() {
        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = adminUserController.deleteUser(authentication, 1L);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testDeleteUser_SelfDeleteForbidden() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(authentication.getName()).thenReturn("testuser");

        ResponseEntity<?> response = adminUserController.deleteUser(authentication, 1L);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertTrue(response.getBody() instanceof Map);
        assertEquals("Không thể tự xóa tài khoản của chính mình!", ((Map<?, ?>) response.getBody()).get("message"));
    }

    @Test
    void testDeleteUser_Success() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(authentication.getName()).thenReturn("admin_user");

        ResponseEntity<?> response = adminUserController.deleteUser(authentication, 1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(jdbcTemplate, atLeastOnce()).update(anyString(), eq(1L));
    }

    @Test
    void testDeleteUser_NullAuth_Success() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));

        ResponseEntity<?> response = adminUserController.deleteUser(null, 1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(jdbcTemplate, atLeastOnce()).update(anyString(), eq(1L));
    }

    @Test
    void testDeleteUser_Exception() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(authentication.getName()).thenReturn("admin_user");
        doThrow(new RuntimeException("DB error")).when(jdbcTemplate).update(anyString(), eq(1L));

        ResponseEntity<?> response = adminUserController.deleteUser(authentication, 1L);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }
}
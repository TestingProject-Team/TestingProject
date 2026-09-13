package com.bookstore.controller;

import com.bookstore.entity.Notification;
import com.bookstore.repository.NotificationRepository;
import com.bookstore.repository.UserRepository;
import com.bookstore.service.NotificationService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class NotificationControllerTest {

    @Mock
    private NotificationService notificationService;

    @Mock
    private NotificationRepository notificationRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private NotificationController notificationController;

    private Notification notification;

    @BeforeEach
    void setUp() {
        notification = Notification.builder()
                .id(1L)
                .title("New Order")
                .content("Order #1 has been placed")
                .type("ORDER")
                .isRead(false)
                .build();
    }

    @Test
    void testGetNotifications_WithAuth() {
        when(authentication.getName()).thenReturn("testuser");
        when(notificationService.getNotificationsByUser("testuser")).thenReturn(List.of(notification));

        ResponseEntity<List<Notification>> response = notificationController.getNotifications(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(notification), response.getBody());
    }

    @Test
    void testGetNotifications_NullAuth() {
        when(notificationService.getNotificationsByUser(null)).thenReturn(List.of(notification));

        ResponseEntity<List<Notification>> response = notificationController.getNotifications(null);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(notification), response.getBody());
    }

    @Test
    void testGetUnreadCount_WithAuth() {
        when(authentication.getName()).thenReturn("testuser");
        when(notificationService.getUnreadCount("testuser")).thenReturn(3L);

        ResponseEntity<Long> response = notificationController.getUnreadCount(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(3L, response.getBody());
    }

    @Test
    void testGetUnreadCount_NullAuth() {
        when(notificationService.getUnreadCount(null)).thenReturn(0L);

        ResponseEntity<Long> response = notificationController.getUnreadCount(null);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(0L, response.getBody());
    }

    @Test
    void testMarkAsRead() {
        when(notificationService.markAsRead(1L)).thenReturn(notification);

        ResponseEntity<Notification> response = notificationController.markAsRead(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(notification, response.getBody());
    }

    @Test
    void testMarkAllAsRead_WithAuth() {
        when(authentication.getName()).thenReturn("testuser");
        doNothing().when(notificationService).markAllAsRead("testuser");

        ResponseEntity<Void> response = notificationController.markAllAsRead(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(notificationService).markAllAsRead("testuser");
    }

    @Test
    void testMarkAllAsRead_NullAuth() {
        ResponseEntity<Void> response = notificationController.markAllAsRead(null);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(notificationService, never()).markAllAsRead(anyString());
    }

    @Test
    void testCreateNotification() {
        when(notificationService.createNotification(notification)).thenReturn(notification);

        ResponseEntity<Notification> response = notificationController.createNotification(notification);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(notification, response.getBody());
    }

    @Test
    void testGetAllNotificationsAdmin() {
        when(notificationRepository.findAll(any(Sort.class))).thenReturn(List.of(notification));

        ResponseEntity<List<Notification>> response = notificationController.getAllNotifications();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(notification), response.getBody());
    }

    @Test
    void testAdminSendNotification() {
        NotificationController.AdminNotificationRequest request = new NotificationController.AdminNotificationRequest();
        request.setTitle("System update");
        request.setContent("Server maintenance tonight");
        request.setType(null); // tests default SYSTEM
        request.setUserId(10L);

        when(notificationService.createNotification(any(Notification.class))).thenReturn(notification);

        ResponseEntity<Notification> response = notificationController.adminSendNotification(request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(notification, response.getBody());

        // Test with non-null type
        request.setType("PROMOTION");
        ResponseEntity<Notification> responsePromo = notificationController.adminSendNotification(request);
        assertEquals(HttpStatus.OK, responsePromo.getStatusCode());
    }

    @Test
    void testDeleteNotification() {
        doNothing().when(notificationRepository).deleteById(1L);

        ResponseEntity<Void> response = notificationController.deleteNotification(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(notificationRepository).deleteById(1L);
    }
}
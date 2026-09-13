package com.bookstore.controller;

import com.bookstore.entity.NewsletterSubscriber;
import com.bookstore.service.NewsletterService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class NewsletterControllerTest {

    @Mock
    private NewsletterService newsletterService;

    @InjectMocks
    private NewsletterController newsletterController;

    private NewsletterSubscriber subscriber;

    @BeforeEach
    void setUp() {
        subscriber = new NewsletterSubscriber();
        subscriber.setId(1L);
        subscriber.setEmail("subscriber@example.com");
        subscriber.setActive(true);
    }

    @Test
    void testSubscribe_Success() {
        doNothing().when(newsletterService).subscribe("test@example.com");

        ResponseEntity<?> response = newsletterController.subscribe(Map.of("email", "test@example.com"));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(newsletterService).subscribe("test@example.com");
    }

    @Test
    void testSubscribe_IllegalArgumentException() {
        doThrow(new IllegalArgumentException("Email invalid")).when(newsletterService).subscribe("invalid");

        ResponseEntity<?> response = newsletterController.subscribe(Map.of("email", "invalid"));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testSubscribe_GenericException() {
        doThrow(new RuntimeException("DB error")).when(newsletterService).subscribe("test@example.com");

        ResponseEntity<?> response = newsletterController.subscribe(Map.of("email", "test@example.com"));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }

    @Test
    void testSendBulkNewsletter_NullSubjectOrBody() {
        ResponseEntity<?> response1 = newsletterController.sendBulkNewsletter(Map.of("body", "Body"));
        assertEquals(HttpStatus.BAD_REQUEST, response1.getStatusCode());

        ResponseEntity<?> response2 = newsletterController.sendBulkNewsletter(Map.of("subject", "Subject"));
        assertEquals(HttpStatus.BAD_REQUEST, response2.getStatusCode());
    }

    @Test
    void testSendBulkNewsletter_Success() {
        doNothing().when(newsletterService).sendBulkNewsletter("Subject", "Body");

        ResponseEntity<?> response = newsletterController.sendBulkNewsletter(Map.of("subject", "Subject", "body", "Body"));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(newsletterService).sendBulkNewsletter("Subject", "Body");
    }

    @Test
    void testSendBulkNewsletter_Exception() {
        doThrow(new RuntimeException("Mail error")).when(newsletterService).sendBulkNewsletter("Subject", "Body");

        ResponseEntity<?> response = newsletterController.sendBulkNewsletter(Map.of("subject", "Subject", "body", "Body"));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }

    @Test
    void testGetAllSubscribers_Success() {
        when(newsletterService.getAllSubscribers()).thenReturn(List.of(subscriber));

        ResponseEntity<?> response = newsletterController.getAllSubscribers();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(subscriber), response.getBody());
    }

    @Test
    void testGetAllSubscribers_Exception() {
        when(newsletterService.getAllSubscribers()).thenThrow(new RuntimeException("DB error"));

        ResponseEntity<?> response = newsletterController.getAllSubscribers();

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }

    @Test
    void testDeleteSubscriber_Success() {
        doNothing().when(newsletterService).deleteSubscriber(1L);

        ResponseEntity<?> response = newsletterController.deleteSubscriber(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(newsletterService).deleteSubscriber(1L);
    }

    @Test
    void testDeleteSubscriber_IllegalArgumentException() {
        doThrow(new IllegalArgumentException("Not found")).when(newsletterService).deleteSubscriber(1L);

        ResponseEntity<?> response = newsletterController.deleteSubscriber(1L);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testDeleteSubscriber_GenericException() {
        doThrow(new RuntimeException("DB error")).when(newsletterService).deleteSubscriber(1L);

        ResponseEntity<?> response = newsletterController.deleteSubscriber(1L);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }
}
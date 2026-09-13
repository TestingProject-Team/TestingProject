package com.bookstore.controller;

import com.bookstore.entity.Contact;
import com.bookstore.service.ContactService;
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
class ContactControllerTest {

    @Mock
    private ContactService contactService;

    @InjectMocks
    private ContactController contactController;

    private Contact testContact;

    @BeforeEach
    void setUp() {
        testContact = Contact.builder()
                .id(1L)
                .fullName("Nguyen Van A")
                .email("a@example.com")
                .content("Great store")
                .status("NEW")
                .build();
    }

    @Test
    void testCreateContact_Success() {
        when(contactService.createContact(testContact)).thenReturn(testContact);

        ResponseEntity<?> response = contactController.createContact(testContact);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(contactService).createContact(testContact);
    }

    @Test
    void testCreateContact_IllegalArgumentException() {
        when(contactService.createContact(testContact)).thenThrow(new IllegalArgumentException("Invalid input"));

        ResponseEntity<?> response = contactController.createContact(testContact);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testCreateContact_GenericException() {
        when(contactService.createContact(testContact)).thenThrow(new RuntimeException("Server error"));

        ResponseEntity<?> response = contactController.createContact(testContact);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }

    @Test
    void testGetAllContacts_Success() {
        when(contactService.getAllContacts()).thenReturn(List.of(testContact));

        ResponseEntity<?> response = contactController.getAllContacts();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testContact), response.getBody());
    }

    @Test
    void testGetAllContacts_Exception() {
        when(contactService.getAllContacts()).thenThrow(new RuntimeException("DB error"));

        ResponseEntity<?> response = contactController.getAllContacts();

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }

    @Test
    void testUpdateContactStatus_Success() {
        when(contactService.updateContactStatus(1L, "PROCESSED")).thenReturn(testContact);

        ResponseEntity<?> response = contactController.updateContactStatus(1L, Map.of("status", "PROCESSED"));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(contactService).updateContactStatus(1L, "PROCESSED");
    }

    @Test
    void testUpdateContactStatus_DefaultStatus() {
        when(contactService.updateContactStatus(1L, "PROCESSED")).thenReturn(testContact);

        ResponseEntity<?> response = contactController.updateContactStatus(1L, Map.of());

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(contactService).updateContactStatus(1L, "PROCESSED");
    }

    @Test
    void testUpdateContactStatus_IllegalArgumentException() {
        when(contactService.updateContactStatus(1L, "INVALID")).thenThrow(new IllegalArgumentException("Invalid status"));

        ResponseEntity<?> response = contactController.updateContactStatus(1L, Map.of("status", "INVALID"));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testUpdateContactStatus_GenericException() {
        when(contactService.updateContactStatus(1L, "PROCESSED")).thenThrow(new RuntimeException("DB error"));

        ResponseEntity<?> response = contactController.updateContactStatus(1L, Map.of("status", "PROCESSED"));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }

    @Test
    void testDeleteContact_Success() {
        doNothing().when(contactService).deleteContact(1L);

        ResponseEntity<?> response = contactController.deleteContact(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(contactService).deleteContact(1L);
    }

    @Test
    void testDeleteContact_IllegalArgumentException() {
        doThrow(new IllegalArgumentException("Not found")).when(contactService).deleteContact(1L);

        ResponseEntity<?> response = contactController.deleteContact(1L);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testDeleteContact_GenericException() {
        doThrow(new RuntimeException("DB error")).when(contactService).deleteContact(1L);

        ResponseEntity<?> response = contactController.deleteContact(1L);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    }
}
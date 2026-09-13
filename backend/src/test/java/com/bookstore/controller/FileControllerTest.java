package com.bookstore.controller;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class FileControllerTest {

    private FileController fileController;

    @BeforeEach
    void setUp() {
        fileController = new FileController();
    }

    @Test
    void testUploadFile_InvalidExtension() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "test.exe",
                "application/octet-stream",
                "malicious".getBytes()
        );

        ResponseEntity<Map<String, String>> response = fileController.uploadFile(file);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().containsKey("message"));
    }

    @Test
    void testUploadFile_ValidImage() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "avatar.png",
                "image/png",
                "fake image bytes".getBytes()
        );

        ResponseEntity<Map<String, String>> response = fileController.uploadFile(file);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().containsKey("url"));
        assertTrue(response.getBody().get("url").startsWith("/uploads/"));
        assertTrue(response.getBody().get("url").endsWith(".png"));
    }

    @Test
    void testUploadFile_ValidPdf() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "document.pdf",
                "application/pdf",
                "fake pdf bytes".getBytes()
        );

        ResponseEntity<Map<String, String>> response = fileController.uploadFile(file);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().get("url").endsWith(".pdf"));
    }

    @Test
    void testUploadFile_NullOriginalFilename_UsesRandomUuid() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                null,
                "application/octet-stream",
                "content".getBytes()
        );

        // fileName will be UUID without extension -> allowedExtensions.contains("") is false -> 400 Bad Request
        ResponseEntity<Map<String, String>> response = fileController.uploadFile(file);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testUploadFile_InvalidPathSequence() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "../test.png",
                "image/png",
                "fake image bytes".getBytes()
        );

        assertThrows(RuntimeException.class, () -> fileController.uploadFile(file));
    }

    @Test
    void testUploadFile_NoExtensionDot_BadRequest() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "nodotfile",
                "application/octet-stream",
                "content".getBytes()
        );

        ResponseEntity<Map<String, String>> response = fileController.uploadFile(file);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testUploadFile_FilenameWithDotAtStart() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                ".hidden",
                "application/octet-stream",
                "content".getBytes()
        );

        ResponseEntity<Map<String, String>> response = fileController.uploadFile(file);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testUploadFile_IOException_ThrowsRuntimeException() throws Exception {
        org.springframework.web.multipart.MultipartFile mockFile = mock(org.springframework.web.multipart.MultipartFile.class);
        when(mockFile.getOriginalFilename()).thenReturn("test.png");
        when(mockFile.getInputStream()).thenThrow(new java.io.IOException("Disk error"));

        assertThrows(RuntimeException.class, () -> fileController.uploadFile(mockFile));
    }

    @Test
    void constructor_WhenUploadDirectoryCannotBeCreated_WrapsFailure() {
        try (org.mockito.MockedStatic<java.nio.file.Files> files = mockStatic(java.nio.file.Files.class)) {
            files.when(() -> java.nio.file.Files.createDirectories(any(java.nio.file.Path.class)))
                    .thenThrow(new java.io.IOException("permission denied"));

            RuntimeException error = assertThrows(RuntimeException.class, FileController::new);
            assertEquals("Could not create the directory where the uploaded files will be stored.", error.getMessage());
            assertEquals("permission denied", error.getCause().getMessage());
        }
    }
}

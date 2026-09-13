package com.bookstore.controller;

import com.bookstore.entity.Book;
import com.bookstore.service.BookService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class BookControllerTest {

    @Mock
    private BookService bookService;

    @InjectMocks
    private BookController bookController;

    private Book testBook;

    @BeforeEach
    void setUp() {
        testBook = Book.builder()
                .id(1L)
                .title("Clean Code")
                .author("Robert C. Martin")
                .price(BigDecimal.valueOf(250000))
                .isFeatured(true)
                .build();
    }

    @Test
    void testGetAllBooks() {
        when(bookService.getAllBooks()).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getAllBooks();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetBookById() {
        when(bookService.getBookById(1L)).thenReturn(testBook);
        ResponseEntity<Book> response = bookController.getBookById(1L);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testBook, response.getBody());
    }

    @Test
    void testCreateBook() {
        when(bookService.createBook(testBook)).thenReturn(testBook);
        ResponseEntity<Book> response = bookController.createBook(testBook);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testBook, response.getBody());
    }

    @Test
    void testGetBooksByCategory() {
        when(bookService.getBooksByCategoryId(2L)).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getBooksByCategory(2L);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetBestsellers() {
        when(bookService.getBestsellers()).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getBestsellers();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetCombos() {
        when(bookService.getCombos()).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getCombos();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetRecommendations() {
        when(bookService.getRecommendations("user1", 1L)).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getRecommendations("user1", 1L);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetLatestBooks() {
        when(bookService.getLatestBooks()).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getLatestBooks();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetFeaturedBooks() {
        when(bookService.getFeaturedBooks()).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getFeaturedBooks();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testToggleFeaturedStatus() {
        when(bookService.toggleFeaturedStatus(1L, true)).thenReturn(testBook);
        ResponseEntity<Book> response = bookController.toggleFeaturedStatus(1L, Map.of("isFeatured", true));
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testBook, response.getBody());
    }

    @Test
    void testGetDiscountedBooks() {
        when(bookService.getDiscountedBooks()).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.getDiscountedBooks();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testUpdateBook() {
        when(bookService.updateBook(1L, testBook)).thenReturn(testBook);
        ResponseEntity<Book> response = bookController.updateBook(1L, testBook);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testBook, response.getBody());
    }

    @Test
    void testDeleteBook() {
        ResponseEntity<Void> response = bookController.deleteBook(1L);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(bookService).deleteBook(1L);
    }

    @Test
    void testSearchBooks() {
        when(bookService.searchBooks("Java")).thenReturn(List.of(testBook));
        ResponseEntity<List<Book>> response = bookController.searchBooks("Java");
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBook), response.getBody());
    }

    @Test
    void testGetImportTemplate() {
        ResponseEntity<Resource> response = bookController.getImportTemplate();
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
    }

    @Test
    void testImportBooks_NonExcelFile() {
        MockMultipartFile file = new MockMultipartFile("file", "test.txt", "text/plain", "data".getBytes());
        ResponseEntity<?> response = bookController.importBooks(file);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testImportBooks_ExcelFile_Success() throws Exception {
        String contentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
        MockMultipartFile file = new MockMultipartFile("file", "test.xlsx", contentType, "data".getBytes());

        doNothing().when(bookService).importBooksFromExcel(file);

        ResponseEntity<?> response = bookController.importBooks(file);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testImportBooks_ExcelFile_Exception() throws Exception {
        String contentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
        MockMultipartFile file = new MockMultipartFile("file", "test.xlsx", contentType, "data".getBytes());

        doThrow(new RuntimeException("Excel error")).when(bookService).importBooksFromExcel(file);

        ResponseEntity<?> response = bookController.importBooks(file);
        assertEquals(HttpStatus.EXPECTATION_FAILED, response.getStatusCode());
    }
}
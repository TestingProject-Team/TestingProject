package com.bookstore.service;

import com.bookstore.entity.Book;
import com.bookstore.entity.Category;
import com.bookstore.repository.BookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private BookService bookService;

    private Book testBook;
    private Category testCategory;

    @BeforeEach
    void setUp() {
        testCategory = Category.builder()
                .id(1L)
                .name("Văn Học")
                .build();

        testBook = Book.builder()
                .id(100L)
                .title("Clean Code")
                .author("Robert C. Martin")
                .price(new BigDecimal("250000"))
                .isFeatured(false)
                .isCombo(false)
                .category(testCategory)
                .build();
    }

    @Test
    void getAllBooks_Success() {
        when(bookRepository.findAll()).thenReturn(List.of(testBook));

        List<Book> result = bookService.getAllBooks();

        assertEquals(1, result.size());
        assertEquals("Clean Code", result.get(0).getTitle());
        verify(bookRepository, times(1)).findAll();
    }

    @Test
    void getBookById_Success() {
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));

        Book result = bookService.getBookById(100L);

        assertNotNull(result);
        assertEquals("Clean Code", result.getTitle());
        verify(bookRepository, times(1)).findById(100L);
    }

    @Test
    void getBookById_NotFound_ThrowsException() {
        when(bookRepository.findById(999L)).thenReturn(Optional.empty());

        Exception exception = assertThrows(RuntimeException.class, () -> {
            bookService.getBookById(999L);
        });

        assertTrue(exception.getMessage().contains("Không tìm thấy sách với ID: 999"));
    }

    @Test
    void createBook_Success() {
        when(bookRepository.findFirstByTitle("Clean Code")).thenReturn(Optional.empty());
        when(bookRepository.save(testBook)).thenReturn(testBook);

        Book created = bookService.createBook(testBook);

        assertNotNull(created);
        assertEquals("Clean Code", created.getTitle());
        verify(bookRepository).save(testBook);
    }

    @Test
    void createBook_DuplicateTitle_ThrowsException() {
        when(bookRepository.findFirstByTitle("Clean Code")).thenReturn(Optional.of(testBook));

        Exception exception = assertThrows(RuntimeException.class, () -> {
            bookService.createBook(testBook);
        });

        assertTrue(exception.getMessage().contains("đã tồn tại trong hệ thống"));
        verify(bookRepository, never()).save(any(Book.class));
    }

    @Test
    void toggleFeaturedStatus_Success() {
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(bookRepository.save(testBook)).thenReturn(testBook);

        Book updated = bookService.toggleFeaturedStatus(100L, true);

        assertTrue(updated.getIsFeatured());
        verify(bookRepository).save(testBook);
    }

    @Test
    void searchBooks_CleanKeyword_RemovesPrefixes() {
        when(bookRepository.searchBooksByKeyword("clean code")).thenReturn(List.of(testBook));

        List<Book> result = bookService.searchBooks("sách Clean Code ");

        assertEquals(1, result.size());
        verify(bookRepository).searchBooksByKeyword("clean code");
    }

    @Test
    void searchBooks_EmptyKeyword_ReturnsEmptyList() {
        List<Book> result1 = bookService.searchBooks("");
        List<Book> result2 = bookService.searchBooks(null);

        assertTrue(result1.isEmpty());
        assertTrue(result2.isEmpty());
        verify(bookRepository, never()).searchBooksByKeyword(anyString());
    }

    @Test
    void deleteBook_Success() {
        doNothing().when(bookRepository).deleteById(100L);

        bookService.deleteBook(100L);

        verify(bookRepository, times(1)).deleteById(100L);
    }

    @Test
    void getBooksByCategoryId_Success() {
        when(bookRepository.findByCategoryId(1L)).thenReturn(List.of(testBook));
        List<Book> result = bookService.getBooksByCategoryId(1L);
        assertEquals(1, result.size());
        verify(bookRepository).findByCategoryId(1L);
    }

    @Test
    void getBestsellers_Success() {
        when(bookRepository.findTop200ByOrderBySalesCountDesc()).thenReturn(List.of(testBook));
        List<Book> result = bookService.getBestsellers();
        assertEquals(1, result.size());
    }

    @Test
    void getCombos_Success() {
        when(bookRepository.findByIsComboTrue()).thenReturn(List.of(testBook));
        List<Book> result = bookService.getCombos();
        assertEquals(1, result.size());
    }

    @Test
    void getLatestBooks_Success() {
        when(bookRepository.findTop200ByOrderByIdDesc()).thenReturn(List.of(testBook));
        List<Book> result = bookService.getLatestBooks();
        assertEquals(1, result.size());
    }

    @Test
    void getDiscountedBooks_Success() {
        when(bookRepository.findDiscountedBooks()).thenReturn(List.of(testBook));
        List<Book> result = bookService.getDiscountedBooks();
        assertEquals(1, result.size());
    }

    @Test
    void getFeaturedBooks_Success() {
        when(bookRepository.findByIsFeaturedTrue()).thenReturn(List.of(testBook));
        List<Book> result = bookService.getFeaturedBooks();
        assertEquals(1, result.size());
    }

    @Test
    void getRecommendations_WithCategory_Found() {
        when(bookRepository.findByCategoryId(1L)).thenReturn(List.of(testBook));
        List<Book> result = bookService.getRecommendations("user1", 1L);
        assertEquals(1, result.size());
    }

    @Test
    void getRecommendations_WithCategory_EmptyOrNullReturnsBestsellers() {
        when(bookRepository.findByCategoryId(1L)).thenReturn(Collections.emptyList());
        when(bookRepository.findTop200ByOrderBySalesCountDesc()).thenReturn(List.of(testBook));
        List<Book> result1 = bookService.getRecommendations("user1", 1L);
        assertEquals(1, result1.size());

        List<Book> result2 = bookService.getRecommendations("user1", null);
        assertEquals(1, result2.size());
    }

    @Test
    void updateBook_Success() {
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(bookRepository.save(any(Book.class))).thenAnswer(i -> i.getArgument(0));

        Book updatePayload = Book.builder()
                .title("New Title")
                .author("New Author")
                .publisher("New Publisher")
                .description("New Desc")
                .price(new BigDecimal("300000"))
                .oldPrice(new BigDecimal("350000"))
                .discount(10)
                .stockQuantity(20)
                .imageUrl("http://new.img")
                .additionalImages(List.of("http://img1.jpg"))
                .isCombo(true)
                .isFeatured(true)
                .category(testCategory)
                .build();

        Book updated = bookService.updateBook(100L, updatePayload);

        assertEquals("New Title", updated.getTitle());
        assertEquals("New Author", updated.getAuthor());
        assertTrue(updated.getIsFeatured());
        assertTrue(updated.getIsCombo());
    }

    @Test
    void updateBook_WithNullFeatured() {
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(bookRepository.save(any(Book.class))).thenAnswer(i -> i.getArgument(0));

        Book updatePayload = Book.builder()
                .title("New Title")
                .isFeatured(null)
                .build();

        Book updated = bookService.updateBook(100L, updatePayload);
        assertEquals("New Title", updated.getTitle());
        assertFalse(updated.getIsFeatured());
    }

    @Test
    void searchBooks_PrefixVariations() {
        when(bookRepository.searchBooksByKeyword(anyString())).thenReturn(List.of(testBook));

        bookService.searchBooks("truyện tranh Conan");
        verify(bookRepository).searchBooksByKeyword("tranh conan");

        bookService.searchBooks("cuốn nhật ký");
        verify(bookRepository).searchBooksByKeyword("nhật ký");

        bookService.searchBooks("tiểu thuyết tuổi trẻ");
        verify(bookRepository).searchBooksByKeyword("tuổi trẻ");

        bookService.searchBooks("sách ");
        verify(bookRepository).searchBooksByKeyword("sách");

        bookService.searchBooks("truyện ");
        bookService.searchBooks("cuốn ");
        bookService.searchBooks("tiểu thuyết ");
    }

    @Test
    void getRecommendations_WithCategory_FoundMoreThan10() {
        List<Book> fifteenBooks = new java.util.ArrayList<>();
        for (int i = 0; i < 15; i++) {
            fifteenBooks.add(Book.builder().id((long) i).title("Book " + i).build());
        }
        when(bookRepository.findByCategoryId(1L)).thenReturn(fifteenBooks);
        List<Book> result = bookService.getRecommendations("user1", 1L);
        assertEquals(10, result.size());
    }

    @Test
    void getRecommendations_NullCategoryResult_FallsBackToBestsellers() {
        when(bookRepository.findByCategoryId(1L)).thenReturn(null);
        when(bookRepository.findTop200ByOrderBySalesCountDesc()).thenReturn(List.of(testBook));

        assertEquals(List.of(testBook), bookService.getRecommendations("user1", 1L));
    }

    @Test
    void importBooksFromExcel_AllFieldsBranches() throws Exception {
        org.apache.poi.ss.usermodel.Workbook wb = new org.apache.poi.xssf.usermodel.XSSFWorkbook();
        org.apache.poi.ss.usermodel.Sheet sheet = wb.createSheet("Books");
        org.apache.poi.ss.usermodel.Row header = sheet.createRow(0);
        for (int i = 0; i < 10; i++) header.createCell(i).setCellValue("Col " + i);

        // Row 1: Existing Book with all fields filled
        org.apache.poi.ss.usermodel.Row row1 = sheet.createRow(1);
        row1.createCell(0).setCellValue("Existing Full");
        row1.createCell(1).setCellValue("Author A");
        row1.createCell(2).setCellValue("Pub A");
        row1.createCell(3).setCellValue("Desc A");
        row1.createCell(4).setCellValue(100000.0);
        row1.createCell(5).setCellValue(120000.0);
        row1.createCell(6).setCellValue(10.0);
        row1.createCell(7).setCellValue(50.0);
        row1.createCell(8).setCellValue(2.0);
        row1.createCell(9).setCellValue("http://imgA.jpg");

        // Row 2: Existing Book with empty/null/zero fields
        org.apache.poi.ss.usermodel.Row row2 = sheet.createRow(2);
        row2.createCell(0).setCellValue("Existing Empty Fields");
        row2.createCell(1).setCellValue(""); // empty author
        row2.createCell(2).setCellValue(""); // empty pub
        row2.createCell(3).setCellValue(""); // empty desc
        row2.createCell(4).setCellValue(0.0); // 0 price
        row2.createCell(5).setBlank(); // null old price
        row2.createCell(6).setBlank(); // default discount 0
        row2.createCell(7).setBlank(); // default stock 0
        row2.createCell(8).setCellValue(0.0); // category id 0
        row2.createCell(9).setCellValue(""); // empty image

        // Row 2b: Existing Book with null Category / null CategoryId
        org.apache.poi.ss.usermodel.Row row2b = sheet.createRow(3);
        row2b.createCell(0).setCellValue("Existing Category Null");
        row2b.createCell(1).setCellValue("Auth");
        row2b.createCell(2).setCellValue("Pub");
        row2b.createCell(3).setCellValue("Desc");
        row2b.createCell(4).setCellValue(100.0);
        row2b.createCell(8).setBlank(); // null category id

        // Row 3: Null title
        org.apache.poi.ss.usermodel.Row row3 = sheet.createRow(4);
        row3.createCell(1).setCellValue("No title book");

        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        wb.write(out);
        wb.close();

        org.springframework.mock.web.MockMultipartFile file = new org.springframework.mock.web.MockMultipartFile(
                "file", "books.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", out.toByteArray()
        );

        Book existingFull = Book.builder().id(201L).title("Existing Full").build();
        when(bookRepository.findFirstByTitle("Existing Full")).thenReturn(Optional.of(existingFull));

        Book existingEmpty = Book.builder().id(202L).title("Existing Empty Fields").build();
        when(bookRepository.findFirstByTitle("Existing Empty Fields")).thenReturn(Optional.of(existingEmpty));

        Book existingCatNull = Book.builder().id(203L).title("Existing Category Null").build();
        when(bookRepository.findFirstByTitle("Existing Category Null")).thenReturn(Optional.of(existingCatNull));

        bookService.importBooksFromExcel(file);
        verify(bookRepository, atLeast(3)).save(any(Book.class));
    }

    @Test
    void importBooksFromExcel_CreateAndExistingBranches() throws Exception {
        org.apache.poi.ss.usermodel.Workbook wb = new org.apache.poi.xssf.usermodel.XSSFWorkbook();
        org.apache.poi.ss.usermodel.Sheet sheet = wb.createSheet("Books");
        org.apache.poi.ss.usermodel.Row header = sheet.createRow(0);
        for (int i = 0; i < 10; i++) header.createCell(i).setCellValue("Col " + i);

        // Row 1: New Book
        org.apache.poi.ss.usermodel.Row row1 = sheet.createRow(1);
        row1.createCell(0).setCellValue("New Book Title");
        row1.createCell(1).setCellValue("New Author");
        row1.createCell(2).setCellValue("New Pub");
        row1.createCell(3).setCellValue("New Desc");
        row1.createCell(4).setCellValue(100000.0);
        row1.createCell(5).setCellValue(120000.0);
        row1.createCell(6).setCellValue(10.0);
        row1.createCell(7).setCellValue(50.0);
        row1.createCell(8).setCellValue(1.0);
        row1.createCell(9).setCellValue("http://img.jpg");

        // Row 2: Existing Book
        org.apache.poi.ss.usermodel.Row row2 = sheet.createRow(2);
        row2.createCell(0).setCellValue("Existing Book");
        row2.createCell(1).setCellValue("Updated Author");
        row2.createCell(2).setCellValue("Updated Pub");
        row2.createCell(3).setCellValue("Updated Desc");
        row2.createCell(4).setCellValue(150000.0);
        row2.createCell(5).setCellValue(180000.0);
        row2.createCell(6).setCellValue(20.0);
        row2.createCell(7).setCellValue(80.0);
        row2.createCell(8).setCellValue(1.0);
        row2.createCell(9).setCellValue("http://updated.jpg");

        // Row 3: Blank title (should be skipped)
        org.apache.poi.ss.usermodel.Row row3 = sheet.createRow(3);
        row3.createCell(0).setCellValue("   ");

        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        wb.write(out);
        wb.close();

        org.springframework.mock.web.MockMultipartFile file = new org.springframework.mock.web.MockMultipartFile(
                "file", "books.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", out.toByteArray()
        );

        when(bookRepository.findFirstByTitle("New Book Title")).thenReturn(Optional.empty());
        Book existingBook = Book.builder().id(200L).title("Existing Book").build();
        when(bookRepository.findFirstByTitle("Existing Book")).thenReturn(Optional.of(existingBook));

        bookService.importBooksFromExcel(file);

        verify(bookRepository, atLeastOnce()).save(any(Book.class));
    }

    @Test
    void importBooksFromExcel_ExceptionThrowsRuntimeException() {
        org.springframework.web.multipart.MultipartFile mockFile = mock(org.springframework.web.multipart.MultipartFile.class);
        try {
            when(mockFile.getInputStream()).thenThrow(new java.io.IOException("File read error"));
        } catch (Exception ignored) {}

        assertThrows(RuntimeException.class, () -> bookService.importBooksFromExcel(mockFile));
    }
}

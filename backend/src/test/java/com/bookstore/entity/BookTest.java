package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class BookTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Book book = new Book();
        Category category = new Category();
        category.setId(10L);
        category.setName("Fiction");

        List<String> images = new ArrayList<>();
        images.add("img1.jpg");
        images.add("img2.jpg");

        book.setId(1L);
        book.setTitle("Clean Code");
        book.setAuthor("Robert C. Martin");
        book.setPublisher("Prentice Hall");
        book.setDescription("A handbook of agile software craftsmanship");
        book.setPrice(new BigDecimal("45.00"));
        book.setOldPrice(new BigDecimal("50.00"));
        book.setDiscount(10);
        book.setStockQuantity(100);
        book.setImageUrl("clean_code.jpg");
        book.setAverageRating(4.8);
        book.setReviewCount(150);
        book.setSalesCount(500);
        book.setIsCombo(true);
        book.setIsFeatured(true);
        book.setCategory(category);
        book.setAdditionalImages(images);

        assertEquals(1L, book.getId());
        assertEquals("Clean Code", book.getTitle());
        assertEquals("Robert C. Martin", book.getAuthor());
        assertEquals("Prentice Hall", book.getPublisher());
        assertEquals("A handbook of agile software craftsmanship", book.getDescription());
        assertEquals(new BigDecimal("45.00"), book.getPrice());
        assertEquals(new BigDecimal("50.00"), book.getOldPrice());
        assertEquals(10, book.getDiscount());
        assertEquals(100, book.getStockQuantity());
        assertEquals("clean_code.jpg", book.getImageUrl());
        assertEquals(4.8, book.getAverageRating());
        assertEquals(150, book.getReviewCount());
        assertEquals(500, book.getSalesCount());
        assertTrue(book.getIsCombo());
        assertTrue(book.getIsFeatured());
        assertEquals(category, book.getCategory());
        assertEquals(images, book.getAdditionalImages());
    }

    @Test
    void testAllArgsConstructor() {
        Category category = new Category();
        List<String> images = List.of("img1.jpg");

        Book book = new Book(
                2L,
                "Refactoring",
                "Martin Fowler",
                "Addison-Wesley",
                "Improving the design of existing code",
                new BigDecimal("55.00"),
                new BigDecimal("60.00"),
                5,
                50,
                "refactoring.jpg",
                4.9,
                80,
                300,
                false,
                true,
                category,
                images
        );

        assertEquals(2L, book.getId());
        assertEquals("Refactoring", book.getTitle());
        assertEquals("Martin Fowler", book.getAuthor());
        assertEquals("Addison-Wesley", book.getPublisher());
        assertEquals("Improving the design of existing code", book.getDescription());
        assertEquals(new BigDecimal("55.00"), book.getPrice());
        assertEquals(new BigDecimal("60.00"), book.getOldPrice());
        assertEquals(5, book.getDiscount());
        assertEquals(50, book.getStockQuantity());
        assertEquals("refactoring.jpg", book.getImageUrl());
        assertEquals(4.9, book.getAverageRating());
        assertEquals(80, book.getReviewCount());
        assertEquals(300, book.getSalesCount());
        assertFalse(book.getIsCombo());
        assertTrue(book.getIsFeatured());
        assertEquals(category, book.getCategory());
        assertEquals(images, book.getAdditionalImages());
    }

    @Test
    void testBuilderDefaults() {
        Book book = Book.builder()
                .title("Default Book")
                .build();

        assertEquals(0, book.getDiscount());
        assertEquals(0, book.getStockQuantity());
        assertEquals(0.0, book.getAverageRating());
        assertEquals(0, book.getReviewCount());
        assertEquals(0, book.getSalesCount());
        assertFalse(book.getIsCombo());
        assertFalse(book.getIsFeatured());
        assertNotNull(book.getAdditionalImages());
        assertTrue(book.getAdditionalImages().isEmpty());
    }

    @Test
    void testEqualsAndHashCode() {
        Book b1 = Book.builder().id(1L).title("Book 1").price(BigDecimal.TEN).build();
        Book b2 = Book.builder().id(1L).title("Book 1").price(BigDecimal.TEN).build();
        Book b3 = Book.builder().id(2L).title("Book 2").price(BigDecimal.ONE).build();

        assertEquals(b1, b2);
        assertEquals(b1.hashCode(), b2.hashCode());
        assertNotEquals(b1, b3);
        assertNotEquals(b1, null);
        assertNotEquals(b1, new Object());
        assertEquals(b1, b1);
        assertTrue(b1.canEqual(b2));
        assertNotNull(b1.toString());
    }
}

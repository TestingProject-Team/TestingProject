package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CategoryTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Category category = new Category();
        List<Book> books = new ArrayList<>();
        books.add(new Book());

        category.setId(1L);
        category.setName("Science Fiction");
        category.setDescription("Sci-Fi books collection");
        category.setImageUrl("scifi.jpg");
        category.setFeatured(true);
        category.setBooks(books);

        assertEquals(1L, category.getId());
        assertEquals("Science Fiction", category.getName());
        assertEquals("Sci-Fi books collection", category.getDescription());
        assertEquals("scifi.jpg", category.getImageUrl());
        assertTrue(category.isFeatured());
        assertEquals(books, category.getBooks());
    }

    @Test
    void testAllArgsConstructor() {
        List<Book> books = new ArrayList<>();
        Category category = new Category(2L, "Literature", "Literature books", "lit.jpg", false, books);

        assertEquals(2L, category.getId());
        assertEquals("Literature", category.getName());
        assertEquals("Literature books", category.getDescription());
        assertEquals("lit.jpg", category.getImageUrl());
        assertFalse(category.isFeatured());
        assertEquals(books, category.getBooks());
    }

    @Test
    void testBuilder() {
        Category category = Category.builder()
                .id(3L)
                .name("Comics")
                .description("Comics books")
                .imageUrl("comics.jpg")
                .isFeatured(true)
                .build();

        assertEquals(3L, category.getId());
        assertEquals("Comics", category.getName());
        assertEquals("Comics books", category.getDescription());
        assertEquals("comics.jpg", category.getImageUrl());
        assertTrue(category.isFeatured());
        assertNotNull(category.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        Category c1 = Category.builder().id(1L).name("Cat1").build();
        Category c2 = Category.builder().id(1L).name("Cat1").build();
        Category c3 = Category.builder().id(2L).name("Cat2").build();

        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
        assertNotEquals(c1, c3);
        assertNotEquals(c1, null);
        assertNotEquals(c1, new Object());
        assertEquals(c1, c1);
        assertTrue(c1.canEqual(c2));
    }
}

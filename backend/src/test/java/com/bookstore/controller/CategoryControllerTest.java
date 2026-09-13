package com.bookstore.controller;

import com.bookstore.entity.Category;
import com.bookstore.service.CategoryService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CategoryControllerTest {

    @Mock
    private CategoryService categoryService;

    @InjectMocks
    private CategoryController categoryController;

    private Category testCategory;

    @BeforeEach
    void setUp() {
        testCategory = Category.builder()
                .id(1L)
                .name("Fiction")
                .description("Fiction books")
                .build();
    }

    @Test
    void testGetAllCategories() {
        when(categoryService.getAllCategories()).thenReturn(List.of(testCategory));

        ResponseEntity<List<Category>> response = categoryController.getAllCategories();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testCategory), response.getBody());
        verify(categoryService).getAllCategories();
    }

    @Test
    void testGetCategoryById() {
        when(categoryService.getCategoryById(1L)).thenReturn(testCategory);

        ResponseEntity<Category> response = categoryController.getCategoryById(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCategory, response.getBody());
        verify(categoryService).getCategoryById(1L);
    }

    @Test
    void testCreateCategory() {
        when(categoryService.createCategory(testCategory)).thenReturn(testCategory);

        ResponseEntity<Category> response = categoryController.createCategory(testCategory);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCategory, response.getBody());
        verify(categoryService).createCategory(testCategory);
    }

    @Test
    void testUpdateCategory() {
        when(categoryService.updateCategory(1L, testCategory)).thenReturn(testCategory);

        ResponseEntity<Category> response = categoryController.updateCategory(1L, testCategory);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCategory, response.getBody());
        verify(categoryService).updateCategory(1L, testCategory);
    }

    @Test
    void testDeleteCategory() {
        ResponseEntity<Void> response = categoryController.deleteCategory(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(categoryService).deleteCategory(1L);
    }
}
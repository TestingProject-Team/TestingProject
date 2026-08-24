package com.bookstore.repository;

import com.bookstore.entity.Category;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class CategoryRepositoryTest {

    @Autowired
    private CategoryRepository categoryRepository;

    @Test
    @DisplayName("Save and find category by ID - Success")
    void testSaveAndFindById() {
        Category category = Category.builder()
                .name("Comics & Manga")
                .description("Comic books and Japanese manga")
                .isFeatured(true)
                .build();

        Category saved = categoryRepository.save(category);
        assertThat(saved.getId()).isNotNull();

        Optional<Category> found = categoryRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Comics & Manga");
        assertThat(found.get().isFeatured()).isTrue();
    }

    @Test
    @DisplayName("Update and Delete category CRUD operations - Success")
    void testUpdateAndDeleteCategory() {
        Category category = categoryRepository.save(Category.builder()
                .name("Old Category")
                .build());

        Long id = category.getId();
        category.setName("Updated Category");
        categoryRepository.save(category);

        Category updated = categoryRepository.findById(id).orElseThrow();
        assertThat(updated.getName()).isEqualTo("Updated Category");

        categoryRepository.deleteById(id);
        assertThat(categoryRepository.findById(id)).isEmpty();
    }

    @Test
    @DisplayName("Find all categories - Success")
    void testFindAll() {
        categoryRepository.save(Category.builder().name("Cat 1").build());
        categoryRepository.save(Category.builder().name("Cat 2").build());

        List<Category> all = categoryRepository.findAll();
        assertThat(all).hasSizeGreaterThanOrEqualTo(2);
    }
}

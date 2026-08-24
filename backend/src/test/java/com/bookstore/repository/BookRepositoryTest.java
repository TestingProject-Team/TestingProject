package com.bookstore.repository;

import com.bookstore.entity.Book;
import com.bookstore.entity.Category;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class BookRepositoryTest {

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private CategoryRepository categoryRepository;

    private Category fictionCategory;
    private Category techCategory;

    private Book book1;
    private Book book2;
    private Book book3;

    @BeforeEach
    void setUp() {
        fictionCategory = categoryRepository.save(Category.builder()
                .name("Fiction")
                .description("Fiction books")
                .build());

        techCategory = categoryRepository.save(Category.builder()
                .name("Technology")
                .description("Tech books")
                .build());

        book1 = Book.builder()
                .title("Java Programming")
                .author("John Doe")
                .publisher("TechPub")
                .price(new BigDecimal("29.99"))
                .oldPrice(new BigDecimal("39.99"))
                .discount(10)
                .stockQuantity(50)
                .salesCount(100)
                .isCombo(false)
                .isFeatured(true)
                .category(techCategory)
                .build();

        book2 = Book.builder()
                .title("Spring Boot in Action")
                .author("Jane Smith")
                .publisher("TechPub")
                .price(new BigDecimal("45.00"))
                .stockQuantity(20)
                .salesCount(250)
                .isCombo(true)
                .isFeatured(false)
                .category(techCategory)
                .build();

        book3 = Book.builder()
                .title("The Great Novel")
                .author("John Doe")
                .publisher("ClassicPub")
                .price(new BigDecimal("15.00"))
                .stockQuantity(10)
                .salesCount(50)
                .isCombo(false)
                .isFeatured(true)
                .category(fictionCategory)
                .build();

        bookRepository.saveAll(List.of(book1, book2, book3));
    }

    @Test
    @DisplayName("Find books by Category ID - Success")
    void testFindByCategoryId() {
        List<Book> techBooks = bookRepository.findByCategoryId(techCategory.getId());
        assertThat(techBooks).hasSize(2);
        assertThat(techBooks).extracting(Book::getTitle)
                .containsExactlyInAnyOrder("Java Programming", "Spring Boot in Action");
    }

    @Test
    @DisplayName("Find first book by title - Success")
    void testFindFirstByTitle() {
        Optional<Book> found = bookRepository.findFirstByTitle("Java Programming");
        assertThat(found).isPresent();
        assertThat(found.get().getAuthor()).isEqualTo("John Doe");

        Optional<Book> notFound = bookRepository.findFirstByTitle("Non Existent Title");
        assertThat(notFound).isEmpty();
    }

    @Test
    @DisplayName("Find top 200 books ordered by sales count desc - Success")
    void testFindTop200ByOrderBySalesCountDesc() {
        List<Book> sortedBooks = bookRepository.findTop200ByOrderBySalesCountDesc();
        assertThat(sortedBooks).hasSize(3);
        assertThat(sortedBooks.get(0).getTitle()).isEqualTo("Spring Boot in Action"); // sales = 250
        assertThat(sortedBooks.get(1).getTitle()).isEqualTo("Java Programming");      // sales = 100
        assertThat(sortedBooks.get(2).getTitle()).isEqualTo("The Great Novel");         // sales = 50
    }

    @Test
    @DisplayName("Find books where isCombo is true - Success")
    void testFindByIsComboTrue() {
        List<Book> comboBooks = bookRepository.findByIsComboTrue();
        assertThat(comboBooks).hasSize(1);
        assertThat(comboBooks.get(0).getTitle()).isEqualTo("Spring Boot in Action");
    }

    @Test
    @DisplayName("Find books where isFeatured is true - Success")
    void testFindByIsFeaturedTrue() {
        List<Book> featuredBooks = bookRepository.findByIsFeaturedTrue();
        assertThat(featuredBooks).hasSize(2);
        assertThat(featuredBooks).extracting(Book::getTitle)
                .containsExactlyInAnyOrder("Java Programming", "The Great Novel");
    }

    @Test
    @DisplayName("Find discounted books via custom JPQL query - Success")
    void testFindDiscountedBooks() {
        List<Book> discountedBooks = bookRepository.findDiscountedBooks();
        assertThat(discountedBooks).hasSize(1);
        assertThat(discountedBooks.get(0).getTitle()).isEqualTo("Java Programming");
    }

    @Test
    @DisplayName("Find by title containing or author containing ignore case - Success")
    void testFindByTitleOrAuthorContainingIgnoreCase() {
        List<Book> johnBooks = bookRepository.findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCase("John", "John");
        assertThat(johnBooks).hasSize(2); // book1 & book3 by John Doe

        List<Book> springBooks = bookRepository.findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCase("spring", "spring");
        assertThat(springBooks).hasSize(1);
        assertThat(springBooks.get(0).getTitle()).isEqualTo("Spring Boot in Action");
    }

    @Test
    @DisplayName("Search books by keyword custom JPQL query across title, author, category - Success")
    void testSearchBooksByKeyword() {
        // Keyword in Title
        List<Book> titleResults = bookRepository.searchBooksByKeyword("Java");
        assertThat(titleResults).hasSize(1);

        // Keyword in Author
        List<Book> authorResults = bookRepository.searchBooksByKeyword("Jane");
        assertThat(authorResults).hasSize(1);

        // Keyword in Category Name
        List<Book> categoryResults = bookRepository.searchBooksByKeyword("Fiction");
        assertThat(categoryResults).hasSize(1);
        assertThat(categoryResults.get(0).getTitle()).isEqualTo("The Great Novel");

        // Keyword with no match
        List<Book> emptyResults = bookRepository.searchBooksByKeyword("NonExistentKeyword");
        assertThat(emptyResults).isEmpty();
    }
}

package com.bookstore.repository;

import com.bookstore.entity.Book;
import com.bookstore.entity.Review;
import com.bookstore.entity.Role;
import com.bookstore.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class ReviewRepositoryTest {

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BookRepository bookRepository;

    private User reviewer;
    private Book reviewedBook;
    private Review review1;
    private Review review2;

    @BeforeEach
    void setUp() {
        reviewer = userRepository.save(User.builder()
                .username("reviewer")
                .password("password")
                .fullName("Reviewer User")
                .email("reviewer@example.com")
                .role(Role.USER)
                .build());

        reviewedBook = bookRepository.save(Book.builder()
                .title("Reviewed Book")
                .price(new BigDecimal("25.00"))
                .stockQuantity(30)
                .build());

        review1 = Review.builder()
                .user(reviewer)
                .book(reviewedBook)
                .rating(5)
                .comment("Excellent book!")
                .createdAt(LocalDateTime.now().minusDays(1))
                .build();

        review2 = Review.builder()
                .user(reviewer)
                .book(reviewedBook)
                .rating(4)
                .comment("Good read.")
                .createdAt(LocalDateTime.now())
                .build();

        reviewRepository.saveAll(List.of(review1, review2));
    }

    @Test
    @DisplayName("Find reviews by Book ID ordered by CreatedAt desc - Success")
    void testFindByBookIdOrderByCreatedAtDesc() {
        List<Review> reviews = reviewRepository.findByBookIdOrderByCreatedAtDesc(reviewedBook.getId());
        assertThat(reviews).hasSize(2);
        assertThat(reviews.get(0).getRating()).isEqualTo(4); // latest review
    }

    @Test
    @DisplayName("Find reviews by User ID ordered by CreatedAt desc - Success")
    void testFindByUserIdOrderByCreatedAtDesc() {
        List<Review> userReviews = reviewRepository.findByUserIdOrderByCreatedAtDesc(reviewer.getId());
        assertThat(userReviews).hasSize(2);
    }

    @Test
    @DisplayName("Check if review exists by User ID and Book ID - Success")
    void testExistsByUserIdAndBookId() {
        boolean exists = reviewRepository.existsByUserIdAndBookId(reviewer.getId(), reviewedBook.getId());
        assertThat(exists).isTrue();

        boolean notExists = reviewRepository.existsByUserIdAndBookId(reviewer.getId(), 9999L);
        assertThat(notExists).isFalse();
    }

    @Test
    @DisplayName("Count reviews by User ID and Book ID - Success")
    void testCountByUserIdAndBookId() {
        long count = reviewRepository.countByUserIdAndBookId(reviewer.getId(), reviewedBook.getId());
        assertThat(count).isEqualTo(2L);

        long nonExistentCount = reviewRepository.countByUserIdAndBookId(reviewer.getId(), 9999L);
        assertThat(nonExistentCount).isEqualTo(0L);
    }
}

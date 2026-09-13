package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class ReviewCommentTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        ReviewComment rc = new ReviewComment();
        Review review = new Review();
        review.setId(1L);
        User user = new User();
        user.setId(2L);
        LocalDateTime now = LocalDateTime.now();

        rc.setId(10L);
        rc.setReview(review);
        rc.setUser(user);
        rc.setContent("I agree with your review");
        rc.setCreatedAt(now);

        assertEquals(10L, rc.getId());
        assertEquals(review, rc.getReview());
        assertEquals(user, rc.getUser());
        assertEquals("I agree with your review", rc.getContent());
        assertEquals(now, rc.getCreatedAt());
    }

    @Test
    void testAllArgsConstructor() {
        Review review = new Review();
        User user = new User();
        LocalDateTime now = LocalDateTime.now();

        ReviewComment rc = new ReviewComment(20L, review, user, "Great points!", now);

        assertEquals(20L, rc.getId());
        assertEquals(review, rc.getReview());
        assertEquals(user, rc.getUser());
        assertEquals("Great points!", rc.getContent());
        assertEquals(now, rc.getCreatedAt());
    }

    @Test
    void testBuilder() {
        Review review = new Review();
        User user = new User();
        LocalDateTime now = LocalDateTime.now();

        ReviewComment rc = ReviewComment.builder()
                .id(30L)
                .review(review)
                .user(user)
                .content("Thanks for sharing")
                .createdAt(now)
                .build();

        assertEquals(30L, rc.getId());
        assertEquals(review, rc.getReview());
        assertEquals(user, rc.getUser());
        assertEquals("Thanks for sharing", rc.getContent());
        assertEquals(now, rc.getCreatedAt());
        assertNotNull(rc.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        ReviewComment rc1 = ReviewComment.builder().id(1L).content("A").build();
        ReviewComment rc2 = ReviewComment.builder().id(1L).content("A").build();
        ReviewComment rc3 = ReviewComment.builder().id(2L).content("B").build();

        assertEquals(rc1, rc2);
        assertEquals(rc1.hashCode(), rc2.hashCode());
        assertNotEquals(rc1, rc3);
        assertNotEquals(rc1, null);
        assertNotEquals(rc1, new Object());
        assertEquals(rc1, rc1);
        assertTrue(rc1.canEqual(rc2));
    }
}

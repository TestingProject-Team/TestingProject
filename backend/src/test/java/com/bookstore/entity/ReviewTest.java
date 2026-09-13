package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class ReviewTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Review review = new Review();
        User user = new User();
        user.setId(1L);
        Book book = new Book();
        book.setId(2L);
        LocalDateTime now = LocalDateTime.now();
        List<ReviewComment> comments = new ArrayList<>();
        comments.add(new ReviewComment());
        Set<User> likedUsers = new HashSet<>();
        likedUsers.add(user);

        review.setId(10L);
        review.setUser(user);
        review.setBook(book);
        review.setRating(5);
        review.setComment("Excellent book!");
        review.setLikesCount(10);
        review.setImageUrl("review.jpg");
        review.setCreatedAt(now);
        review.setIsReported(true);
        review.setComments(comments);
        review.setLikedByUsers(likedUsers);

        assertEquals(10L, review.getId());
        assertEquals(user, review.getUser());
        assertEquals(book, review.getBook());
        assertEquals(5, review.getRating());
        assertEquals("Excellent book!", review.getComment());
        assertEquals(10, review.getLikesCount());
        assertEquals("review.jpg", review.getImageUrl());
        assertEquals(now, review.getCreatedAt());
        assertTrue(review.getIsReported());
        assertEquals(comments, review.getComments());
        assertEquals(likedUsers, review.getLikedByUsers());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        Book book = new Book();
        LocalDateTime now = LocalDateTime.now();
        List<ReviewComment> comments = new ArrayList<>();
        Set<User> likedUsers = new HashSet<>();

        Review review = new Review(
                20L,
                user,
                book,
                4,
                "Good read",
                3,
                "photo.png",
                now,
                false,
                comments,
                likedUsers
        );

        assertEquals(20L, review.getId());
        assertEquals(user, review.getUser());
        assertEquals(book, review.getBook());
        assertEquals(4, review.getRating());
        assertEquals("Good read", review.getComment());
        assertEquals(3, review.getLikesCount());
        assertEquals("photo.png", review.getImageUrl());
        assertEquals(now, review.getCreatedAt());
        assertFalse(review.getIsReported());
        assertEquals(comments, review.getComments());
        assertEquals(likedUsers, review.getLikedByUsers());
    }

    @Test
    void testBuilderDefaults() {
        Review review = Review.builder().build();

        assertEquals(0, review.getLikesCount());
        assertFalse(review.getIsReported());
        assertNotNull(review.getLikedByUsers());
        assertTrue(review.getLikedByUsers().isEmpty());
    }

    @Test
    void testEqualsAndHashCode() {
        Review r1 = Review.builder().id(1L).rating(5).build();
        Review r2 = Review.builder().id(1L).rating(5).build();
        Review r3 = Review.builder().id(2L).rating(3).build();

        assertEquals(r1, r2);
        assertEquals(r1.hashCode(), r2.hashCode());
        assertNotEquals(r1, r3);
        assertNotEquals(r1, null);
        assertNotEquals(r1, new Object());
        assertEquals(r1, r1);
        assertTrue(r1.canEqual(r2));
        assertNotNull(r1.toString());
    }
}

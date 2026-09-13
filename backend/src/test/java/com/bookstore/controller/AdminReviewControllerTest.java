package com.bookstore.controller;

import com.bookstore.entity.Review;
import com.bookstore.service.ReviewService;
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
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class AdminReviewControllerTest {

    @Mock
    private ReviewService reviewService;

    @InjectMocks
    private AdminReviewController adminReviewController;

    private Review testReview;

    @BeforeEach
    void setUp() {
        testReview = Review.builder()
                .id(1L)
                .rating(5)
                .comment("Great book!")
                .build();
    }

    @Test
    void testGetAllReviews() {
        when(reviewService.getAllReviews()).thenReturn(List.of(testReview));

        ResponseEntity<List<Review>> response = adminReviewController.getAllReviews();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testReview), response.getBody());
        verify(reviewService).getAllReviews();
    }

    @Test
    void testUpdateReview() {
        AdminReviewController.UpdateReviewRequest request = new AdminReviewController.UpdateReviewRequest();
        request.setComment("Updated comment");
        request.setRating(4);

        Review updatedReview = Review.builder()
                .id(1L)
                .rating(4)
                .comment("Updated comment")
                .build();

        when(reviewService.updateReview(1L, "Updated comment", 4)).thenReturn(updatedReview);

        ResponseEntity<Review> response = adminReviewController.updateReview(1L, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("Updated comment", response.getBody().getComment());
        assertEquals(4, response.getBody().getRating());
        verify(reviewService).updateReview(1L, "Updated comment", 4);
    }

    @Test
    void testDeleteReview() {
        ResponseEntity<Void> response = adminReviewController.deleteReview(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(reviewService).deleteReview(1L);
    }

    @Test
    void testDismissReport() {
        when(reviewService.dismissReport(1L)).thenReturn(testReview);

        ResponseEntity<Review> response = adminReviewController.dismissReport(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testReview, response.getBody());
        verify(reviewService).dismissReport(1L);
    }
}
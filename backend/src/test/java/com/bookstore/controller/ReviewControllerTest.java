package com.bookstore.controller;

import com.bookstore.entity.Review;
import com.bookstore.entity.ReviewComment;
import com.bookstore.service.ReviewService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ReviewControllerTest {

    @Mock
    private ReviewService reviewService;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private ReviewController reviewController;

    private Review testReview;

    @BeforeEach
    void setUp() {
        testReview = Review.builder().id(1L).rating(5).comment("Great!").build();
    }

    @Test
    void testGetReviewsByBook() {
        when(reviewService.getReviewsByBookId(10L)).thenReturn(List.of(testReview));

        ResponseEntity<List<Review>> response = reviewController.getReviewsByBook(10L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testReview), response.getBody());
    }

    @Test
    void testGetMyReviews_Unauthenticated() {
        ResponseEntity<List<Review>> response1 = reviewController.getMyReviews(null);
        assertEquals(HttpStatus.UNAUTHORIZED, response1.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<List<Review>> response2 = reviewController.getMyReviews(authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response2.getStatusCode());
    }

    @Test
    void testGetMyReviews_Success() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(reviewService.getReviewsByUsername("testuser")).thenReturn(List.of(testReview));

        ResponseEntity<List<Review>> response = reviewController.getMyReviews(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testReview), response.getBody());
    }

    @Test
    void testCreateReview() {
        ReviewController.ReviewRequest request = new ReviewController.ReviewRequest();
        request.setRating(5);
        request.setComment("Awesome book");
        request.setImageUrl("https://example.com/img.jpg");

        when(authentication.getName()).thenReturn("testuser");
        when(reviewService.createReview("testuser", 10L, 5, "Awesome book", "https://example.com/img.jpg"))
                .thenReturn(testReview);

        ResponseEntity<Review> response = reviewController.createReview(authentication, 10L, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testReview, response.getBody());
    }

    @Test
    void testLikeReview_Unauthenticated() {
        ResponseEntity<Review> response = reviewController.likeReview(1L, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<Review> response2 = reviewController.likeReview(1L, authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response2.getStatusCode());
    }

    @Test
    void testLikeReview_Success() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(reviewService.likeReview(1L, "testuser")).thenReturn(testReview);

        ResponseEntity<Review> response = reviewController.likeReview(1L, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testReview, response.getBody());
    }

    @Test
    void testAddComment_Unauthenticated() {
        ReviewController.CommentRequest req = new ReviewController.CommentRequest();
        ResponseEntity<ReviewComment> response = reviewController.addComment(1L, null, req);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<ReviewComment> response2 = reviewController.addComment(1L, authentication, req);
        assertEquals(HttpStatus.UNAUTHORIZED, response2.getStatusCode());
    }

    @Test
    void testAddComment_Success() {
        ReviewController.CommentRequest req = new ReviewController.CommentRequest();
        req.setContent("I agree");

        ReviewComment comment = ReviewComment.builder().id(2L).content("I agree").build();
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(reviewService.addComment(1L, "testuser", "I agree")).thenReturn(comment);

        ResponseEntity<ReviewComment> response = reviewController.addComment(1L, authentication, req);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(comment, response.getBody());
    }

    @Test
    void testReportReview_Unauthenticated() {
        ResponseEntity<Review> response = reviewController.reportReview(1L, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<Review> response2 = reviewController.reportReview(1L, authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response2.getStatusCode());
    }

    @Test
    void testReportReview_Success() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(reviewService.reportReview(1L)).thenReturn(testReview);

        ResponseEntity<Review> response = reviewController.reportReview(1L, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testReview, response.getBody());
    }

    @Test
    void testCheckEligibility_Unauthenticated() {
        ResponseEntity<Map<String, Object>> response = reviewController.checkEligibility(10L, null);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(false, response.getBody().get("eligible"));

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<Map<String, Object>> response2 = reviewController.checkEligibility(10L, authentication);
        assertEquals(false, response2.getBody().get("eligible"));
    }

    @Test
    void testCheckEligibility_Authenticated() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(reviewService.getReviewEligibilityReason("testuser", 10L)).thenReturn(Map.of("eligible", true));

        ResponseEntity<Map<String, Object>> response = reviewController.checkEligibility(10L, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(true, response.getBody().get("eligible"));
    }

    @Test
    void testGetComments() {
        ReviewComment comment = ReviewComment.builder().id(2L).content("Nice").build();
        when(reviewService.getComments(1L)).thenReturn(List.of(comment));

        ResponseEntity<List<ReviewComment>> response = reviewController.getComments(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(comment), response.getBody());
    }

    @Test
    void testHandleRuntimeException() {
        ResponseEntity<Map<String, String>> response = reviewController.handleRuntimeException(new RuntimeException("Something failed"));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("Something failed", response.getBody().get("message"));
    }
}
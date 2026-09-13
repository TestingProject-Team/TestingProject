package com.bookstore.controller;

import com.bookstore.entity.Book;
import com.bookstore.entity.User;
import com.bookstore.entity.Wishlist;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.UserRepository;
import com.bookstore.repository.WishlistRepository;
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
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class WishlistControllerTest {

    @Mock
    private WishlistRepository wishlistRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private BookRepository bookRepository;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private WishlistController wishlistController;

    private User testUser;
    private Book testBook;
    private Wishlist testWishlist;

    @BeforeEach
    void setUp() {
        testUser = User.builder().id(1L).username("testuser").build();
        testBook = Book.builder().id(10L).title("Test Book").build();
        testWishlist = Wishlist.builder().id(100L).user(testUser).book(testBook).build();
    }

    @Test
    void testGetMyWishlist_Unauthorized() {
        ResponseEntity<?> response1 = wishlistController.getMyWishlist(null);
        assertEquals(HttpStatus.UNAUTHORIZED, response1.getStatusCode());

        when(authentication.isAuthenticated()).thenReturn(false);
        ResponseEntity<?> response2 = wishlistController.getMyWishlist(authentication);
        assertEquals(HttpStatus.UNAUTHORIZED, response2.getStatusCode());
    }

    @Test
    void testGetMyWishlist_Success() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(wishlistRepository.findByUserIdOrderByCreatedAtDesc(1L)).thenReturn(List.of(testWishlist));

        ResponseEntity<?> response = wishlistController.getMyWishlist(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testWishlist), response.getBody());
    }

    @Test
    void testToggleWishlist_Unauthorized() {
        ResponseEntity<?> response = wishlistController.toggleWishlist(10L, null);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void testToggleWishlist_BookNotFound() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(10L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = wishlistController.toggleWishlist(10L, authentication);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testToggleWishlist_RemoveFromWishlist() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(10L)).thenReturn(Optional.of(testBook));
        when(wishlistRepository.findByUserIdAndBookId(1L, 10L)).thenReturn(Optional.of(testWishlist));

        ResponseEntity<?> response = wishlistController.toggleWishlist(10L, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertTrue(response.getBody() instanceof Map);
        assertEquals(false, ((Map<?, ?>) response.getBody()).get("isLiked"));
        verify(wishlistRepository).delete(testWishlist);
    }

    @Test
    void testToggleWishlist_AddToWishlist() {
        when(authentication.isAuthenticated()).thenReturn(true);
        when(authentication.getName()).thenReturn("testuser");
        when(userRepository.findByUsername("testuser")).thenReturn(Optional.of(testUser));
        when(bookRepository.findById(10L)).thenReturn(Optional.of(testBook));
        when(wishlistRepository.findByUserIdAndBookId(1L, 10L)).thenReturn(Optional.empty());

        ResponseEntity<?> response = wishlistController.toggleWishlist(10L, authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertTrue(response.getBody() instanceof Map);
        assertEquals(true, ((Map<?, ?>) response.getBody()).get("isLiked"));
        verify(wishlistRepository).save(any(Wishlist.class));
    }
}
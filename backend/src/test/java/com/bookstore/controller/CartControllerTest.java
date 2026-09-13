package com.bookstore.controller;

import com.bookstore.dto.CartRequest;
import com.bookstore.entity.Cart;
import com.bookstore.service.CartService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CartControllerTest {

    @Mock
    private CartService cartService;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private CartController cartController;

    private Cart testCart;

    @BeforeEach
    void setUp() {
        testCart = Cart.builder().id(1L).build();
    }

    @Test
    void testGetCart() {
        when(authentication.getName()).thenReturn("testuser");
        when(cartService.getCartByUser("testuser")).thenReturn(testCart);

        ResponseEntity<Cart> response = cartController.getCart(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCart, response.getBody());
        verify(cartService).getCartByUser("testuser");
    }

    @Test
    void testAddToCart() {
        CartRequest request = new CartRequest();
        request.setBookId(10L);
        request.setQuantity(2);

        when(authentication.getName()).thenReturn("testuser");
        when(cartService.addToCart("testuser", request)).thenReturn(testCart);

        ResponseEntity<Cart> response = cartController.addToCart(authentication, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCart, response.getBody());
        verify(cartService).addToCart("testuser", request);
    }

    @Test
    void testUpdateCartItem() {
        CartRequest request = new CartRequest();
        request.setQuantity(3);

        when(authentication.getName()).thenReturn("testuser");
        when(cartService.updateCartItem("testuser", 10L, request)).thenReturn(testCart);

        ResponseEntity<Cart> response = cartController.updateCartItem(authentication, 10L, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCart, response.getBody());
        verify(cartService).updateCartItem("testuser", 10L, request);
    }

    @Test
    void testRemoveCartItem() {
        when(authentication.getName()).thenReturn("testuser");
        when(cartService.removeCartItem("testuser", 10L)).thenReturn(testCart);

        ResponseEntity<Cart> response = cartController.removeCartItem(authentication, 10L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testCart, response.getBody());
        verify(cartService).removeCartItem("testuser", 10L);
    }

    @Test
    void testClearCart() {
        when(authentication.getName()).thenReturn("testuser");

        ResponseEntity<Void> response = cartController.clearCart(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(cartService).clearCart("testuser");
    }
}
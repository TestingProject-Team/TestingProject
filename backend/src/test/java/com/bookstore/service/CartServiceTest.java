package com.bookstore.service;

import com.bookstore.dto.CartRequest;
import com.bookstore.entity.Book;
import com.bookstore.entity.Cart;
import com.bookstore.entity.CartItem;
import com.bookstore.entity.User;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.CartRepository;
import com.bookstore.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class CartServiceTest {

    @Mock
    private CartRepository cartRepository;

    @Mock
    private BookRepository bookRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private CartService cartService;

    private User testUser;
    private Cart testCart;
    private Book testBook;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
                .id(1L)
                .username("cartuser")
                .build();

        testCart = Cart.builder()
                .id(10L)
                .user(testUser)
                .items(new ArrayList<>())
                .build();

        testBook = Book.builder()
                .id(100L)
                .title("Tối Ưu Hóa Code")
                .stockQuantity(100)
                .build();
    }

    @Test
    void getCartByUser_ExistingCart() {
        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));

        Cart cart = cartService.getCartByUser("cartuser");

        assertNotNull(cart);
        assertEquals(10L, cart.getId());
    }

    @Test
    void addToCart_NewItem() {
        CartRequest request = new CartRequest();
        request.setBookId(100L);
        request.setQuantity(2);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(cartRepository.save(any(Cart.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Cart result = cartService.addToCart("cartuser", request);

        assertEquals(1, result.getItems().size());
        assertEquals(2, result.getItems().get(0).getQuantity());
        assertEquals(testBook, result.getItems().get(0).getBook());
    }

    @Test
    void addToCart_ExistingItem_IncrementsQuantity() {
        CartItem existingItem = CartItem.builder()
                .id(50L)
                .cart(testCart)
                .book(testBook)
                .quantity(1)
                .build();
        testCart.getItems().add(existingItem);

        CartRequest request = new CartRequest();
        request.setBookId(100L);
        request.setQuantity(3);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(cartRepository.save(any(Cart.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Cart result = cartService.addToCart("cartuser", request);

        assertEquals(1, result.getItems().size());
        assertEquals(4, result.getItems().get(0).getQuantity());
    }

    @Test
    void removeCartItem_Success() {
        CartItem item = CartItem.builder().id(50L).cart(testCart).book(testBook).quantity(2).build();
        testCart.getItems().add(item);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(cartRepository.save(any(Cart.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Cart result = cartService.removeCartItem("cartuser", 100L);

        assertTrue(result.getItems().isEmpty());
    }

    @Test
    void addToCart_BookStockQuantityNull() {
        testBook.setStockQuantity(null);
        CartRequest request = new CartRequest();
        request.setBookId(100L);
        request.setQuantity(2);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(cartRepository.save(any(Cart.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Cart result = cartService.addToCart("cartuser", request);
        assertNotNull(result);
    }

    @Test
    void updateCartItem_BookStockQuantityNull() {
        testBook.setStockQuantity(null);
        CartRequest validReq = new CartRequest();
        validReq.setQuantity(5);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        when(cartRepository.save(any(Cart.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Cart result = cartService.updateCartItem("cartuser", 100L, validReq);
        assertNotNull(result);
    }

    @Test
    void getCartByUser_NotFound_ThrowsException() {
        when(userRepository.findByUsername("unknown")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> cartService.getCartByUser("unknown"));
    }

    @Test
    void getCartByUser_CartNotExists_CreatesNewCart() {
        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.empty());
        when(cartRepository.save(any(Cart.class))).thenAnswer(i -> i.getArgument(0));

        Cart created = cartService.getCartByUser("cartuser");
        assertNotNull(created);
        assertEquals(testUser, created.getUser());
    }

    @Test
    void addToCart_InvalidQuantityOrRequest_ThrowsException() {
        CartRequest req1 = null;
        CartRequest reqNullQty = new CartRequest();
        reqNullQty.setQuantity(null);
        CartRequest req2 = new CartRequest();
        req2.setQuantity(0);

        assertThrows(RuntimeException.class, () -> cartService.addToCart("cartuser", req1));
        assertThrows(RuntimeException.class, () -> cartService.addToCart("cartuser", reqNullQty));
        assertThrows(RuntimeException.class, () -> cartService.addToCart("cartuser", req2));
    }

    @Test
    void addToCart_BookNotFound_ThrowsException() {
        CartRequest req = new CartRequest();
        req.setBookId(999L);
        req.setQuantity(1);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(bookRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(RuntimeException.class, () -> cartService.addToCart("cartuser", req));
    }

    @Test
    void addToCart_StockExceeded_ThrowsException() {
        testBook.setStockQuantity(5);
        CartRequest req = new CartRequest();
        req.setBookId(100L);
        req.setQuantity(10);

        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));

        assertThrows(RuntimeException.class, () -> cartService.addToCart("cartuser", req));
    }

    @Test
    void updateCartItem_Scenarios() {
        // Invalid request or quantity < 0
        assertThrows(RuntimeException.class, () -> cartService.updateCartItem("cartuser", 100L, null));
        CartRequest reqNullQty = new CartRequest();
        reqNullQty.setQuantity(null);
        assertThrows(RuntimeException.class, () -> cartService.updateCartItem("cartuser", 100L, reqNullQty));
        CartRequest negReq = new CartRequest();
        negReq.setQuantity(-1);
        assertThrows(RuntimeException.class, () -> cartService.updateCartItem("cartuser", 100L, negReq));

        // Quantity == 0 calls removeCartItem
        CartRequest zeroReq = new CartRequest();
        zeroReq.setQuantity(0);
        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(testCart));
        when(cartRepository.save(any(Cart.class))).thenAnswer(i -> i.getArgument(0));

        Cart resZero = cartService.updateCartItem("cartuser", 100L, zeroReq);
        assertNotNull(resZero);

        // Book not found
        CartRequest validReq = new CartRequest();
        validReq.setQuantity(2);
        when(bookRepository.findById(999L)).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> cartService.updateCartItem("cartuser", 999L, validReq));

        // Stock exceeded
        testBook.setStockQuantity(2);
        validReq.setQuantity(5);
        when(bookRepository.findById(100L)).thenReturn(Optional.of(testBook));
        assertThrows(RuntimeException.class, () -> cartService.updateCartItem("cartuser", 100L, validReq));

        // Normal update
        testBook.setStockQuantity(20);
        validReq.setQuantity(5);
        CartItem item = CartItem.builder().id(50L).cart(testCart).book(testBook).quantity(1).build();
        testCart.getItems().add(item);

        Cart updatedCart = cartService.updateCartItem("cartuser", 100L, validReq);
        assertEquals(5, updatedCart.getItems().get(0).getQuantity());
    }

    @Test
    void clearCart_RemovesAllItemsAndPersistsCart() {
        testCart.getItems().add(CartItem.builder().cart(testCart).book(testBook).quantity(2).build());
        when(userRepository.findByUsername("cartuser")).thenReturn(Optional.of(testUser));
        when(cartRepository.findByUserId(testUser.getId())).thenReturn(Optional.of(testCart));

        cartService.clearCart("cartuser");

        assertTrue(testCart.getItems().isEmpty());
        verify(cartRepository).save(testCart);
    }
}

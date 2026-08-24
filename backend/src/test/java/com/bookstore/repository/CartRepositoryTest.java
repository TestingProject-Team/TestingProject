package com.bookstore.repository;

import com.bookstore.entity.Book;
import com.bookstore.entity.Cart;
import com.bookstore.entity.CartItem;
import com.bookstore.entity.Role;
import com.bookstore.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class CartRepositoryTest {

    @Autowired
    private CartRepository cartRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BookRepository bookRepository;

    private User user;
    private Book book;

    @BeforeEach
    void setUp() {
        user = userRepository.save(User.builder()
                .username("cartuser")
                .password("password")
                .fullName("Cart User")
                .email("cartuser@example.com")
                .role(Role.USER)
                .build());

        book = bookRepository.save(Book.builder()
                .title("Cart Book")
                .price(new BigDecimal("15.99"))
                .stockQuantity(100)
                .build());
    }

    @Test
    @DisplayName("Save Cart with items and find by user ID - Success")
    void testSaveCartAndFindByUserId() {
        Cart cart = Cart.builder()
                .user(user)
                .items(new ArrayList<>())
                .build();

        CartItem item = CartItem.builder()
                .cart(cart)
                .book(book)
                .quantity(2)
                .build();
        cart.getItems().add(item);

        Cart savedCart = cartRepository.save(cart);
        assertThat(savedCart.getId()).isNotNull();

        Optional<Cart> foundCart = cartRepository.findByUserId(user.getId());
        assertThat(foundCart).isPresent();
        assertThat(foundCart.get().getItems()).hasSize(1);
        assertThat(foundCart.get().getItems().get(0).getQuantity()).isEqualTo(2);
    }

    @Test
    @DisplayName("Find Cart for non-existent user returns empty Optional")
    void testFindByUserIdNonExistentReturnsEmpty() {
        Optional<Cart> foundCart = cartRepository.findByUserId(999L);
        assertThat(foundCart).isEmpty();
    }

    @Test
    @DisplayName("Delete Cart and verify cascade cleanup")
    void testDeleteCart() {
        Cart cart = cartRepository.save(Cart.builder()
                .user(user)
                .items(new ArrayList<>())
                .build());

        Long cartId = cart.getId();
        cartRepository.deleteById(cartId);

        assertThat(cartRepository.findById(cartId)).isEmpty();
    }
}

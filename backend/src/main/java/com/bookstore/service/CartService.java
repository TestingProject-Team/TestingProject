package com.bookstore.service;

import com.bookstore.dto.CartRequest;
import com.bookstore.entity.Book;
import com.bookstore.entity.Cart;
import com.bookstore.entity.CartItem;
import com.bookstore.entity.User;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.CartRepository;
import com.bookstore.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional
public class CartService {
    private final CartRepository cartRepository;
    private final BookRepository bookRepository;
    private final UserRepository userRepository;

    public Cart getCartByUser(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("Tài khoản không tồn tại hoặc phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!"));
        return cartRepository.findByUserId(user.getId())
                .orElseGet(() -> createNewCart(user));
    }

    private Cart createNewCart(User user) {
        Cart cart = Cart.builder().user(user).build();
        return cartRepository.save(cart);
    }

    public Cart addToCart(String username, CartRequest request) {
        if (request == null || request.getQuantity() == null || request.getQuantity() <= 0) {
            throw new RuntimeException("Số lượng sản phẩm không hợp lệ!");
        }

        Cart cart = getCartByUser(username);
        Book book = bookRepository.findById(request.getBookId())
                .orElseThrow(() -> new RuntimeException("Sách (ID: " + request.getBookId() + ") không tồn tại hoặc đã ngừng kinh doanh!"));

        Optional<CartItem> existingItem = cart.getItems().stream()
                .filter(item -> item.getBook().getId().equals(book.getId()))
                .findFirst();

        int targetQuantity = request.getQuantity();
        if (existingItem.isPresent()) {
            targetQuantity += existingItem.get().getQuantity();
        }

        if (book.getStockQuantity() != null && targetQuantity > book.getStockQuantity()) {
            throw new RuntimeException("Số lượng yêu cầu vượt quá tồn kho hiện có (" + book.getStockQuantity() + ")!");
        }

        if (existingItem.isPresent()) {
            CartItem item = existingItem.get();
            item.setQuantity(targetQuantity);
        } else {
            CartItem newItem = CartItem.builder()
                    .cart(cart)
                    .book(book)
                    .quantity(request.getQuantity())
                    .build();
            cart.getItems().add(newItem);
        }

        return cartRepository.save(cart);
    }

    public Cart updateCartItem(String username, Long bookId, CartRequest request) {
        if (request == null || request.getQuantity() == null || request.getQuantity() < 0) {
            throw new RuntimeException("Số lượng sản phẩm không hợp lệ!");
        }

        if (request.getQuantity() == 0) {
            return removeCartItem(username, bookId);
        }

        Cart cart = getCartByUser(username);
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new RuntimeException("Sách không tồn tại!"));

        if (book.getStockQuantity() != null && request.getQuantity() > book.getStockQuantity()) {
            throw new RuntimeException("Số lượng yêu cầu vượt quá tồn kho hiện có (" + book.getStockQuantity() + ")!");
        }

        cart.getItems().stream()
                .filter(item -> item.getBook().getId().equals(bookId))
                .findFirst()
                .ifPresent(item -> item.setQuantity(request.getQuantity()));
        
        return cartRepository.save(cart);
    }

    public Cart removeCartItem(String username, Long bookId) {
        Cart cart = getCartByUser(username);
        cart.getItems().removeIf(item -> item.getBook().getId().equals(bookId));
        return cartRepository.save(cart);
    }

    public void clearCart(String username) {
        Cart cart = getCartByUser(username);
        cart.getItems().clear();
        cartRepository.save(cart);
    }
}

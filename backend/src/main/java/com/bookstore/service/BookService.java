package com.bookstore.service;

import com.bookstore.entity.Book;
import com.bookstore.repository.BookRepository;
import com.bookstore.utils.ExcelHelper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class BookService {

    private final BookRepository bookRepository;

    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    public Book getBookById(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy sách với ID: " + id));
    }

    @Transactional
    @org.springframework.cache.annotation.CacheEvict(value = {"books_bestsellers", "books_latest", "books_discounted", "books_featured", "books_combos"}, allEntries = true)
    public Book createBook(Book book) {
        if (bookRepository.findFirstByTitle(book.getTitle().trim()).isPresent()) {
            throw new RuntimeException("Sách với tiêu đề '" + book.getTitle() + "' đã tồn tại trong hệ thống.");
        }
        return bookRepository.save(book);
    }

    public List<Book> getBooksByCategoryId(Long categoryId) {
        return bookRepository.findByCategoryId(categoryId);
    }

    @org.springframework.cache.annotation.Cacheable("books_bestsellers")
    public List<Book> getBestsellers() {
        return bookRepository.findTop200ByOrderBySalesCountDesc();
    }

    @org.springframework.cache.annotation.Cacheable("books_combos")
    public List<Book> getCombos() {
        return bookRepository.findByIsComboTrue();
    }

    public List<Book> getRecommendations(String userId, Long categoryId) {
        if (categoryId != null) {
            List<Book> books = bookRepository.findByCategoryId(categoryId);
            if (books != null && !books.isEmpty()) {
                // Return top 10 from category
                return books.subList(0, Math.min(books.size(), 10));
            }
        }
        return getBestsellers();
    }

    @org.springframework.cache.annotation.Cacheable("books_latest")
    public List<Book> getLatestBooks() {
        return bookRepository.findTop200ByOrderByIdDesc();
    }

    @org.springframework.cache.annotation.Cacheable("books_discounted")
    public List<Book> getDiscountedBooks() {
        return bookRepository.findDiscountedBooks();
    }

    @org.springframework.cache.annotation.Cacheable("books_featured")
    public List<Book> getFeaturedBooks() {
        return bookRepository.findByIsFeaturedTrue();
    }

    @Transactional
    @org.springframework.cache.annotation.CacheEvict(value = {"books_bestsellers", "books_latest", "books_discounted", "books_featured", "books_combos"}, allEntries = true)
    public Book toggleFeaturedStatus(Long id, boolean isFeatured) {
        Book book = getBookById(id);
        book.setIsFeatured(isFeatured);
        return bookRepository.save(book);
    }

    @Transactional
    @org.springframework.cache.annotation.CacheEvict(value = {"books_bestsellers", "books_latest", "books_discounted", "books_featured", "books_combos"}, allEntries = true)
    public Book updateBook(Long id, Book updatedBook) {
        Book book = getBookById(id);
        book.setTitle(updatedBook.getTitle());
        book.setAuthor(updatedBook.getAuthor());
        book.setPublisher(updatedBook.getPublisher());
        book.setDescription(updatedBook.getDescription());
        book.setPrice(updatedBook.getPrice());
        book.setOldPrice(updatedBook.getOldPrice());
        book.setDiscount(updatedBook.getDiscount());
        book.setStockQuantity(updatedBook.getStockQuantity());
        book.setImageUrl(updatedBook.getImageUrl());
        book.setAdditionalImages(updatedBook.getAdditionalImages());
        book.setIsCombo(updatedBook.getIsCombo());
        if (updatedBook.getIsFeatured() != null) {
            book.setIsFeatured(updatedBook.getIsFeatured());
        }
        book.setCategory(updatedBook.getCategory());
        return bookRepository.save(book);
    }

    @Transactional
    @org.springframework.cache.annotation.CacheEvict(value = {"books_bestsellers", "books_latest", "books_discounted", "books_featured", "books_combos"}, allEntries = true)
    public void deleteBook(Long id) {
        bookRepository.deleteById(id);
    }

    public List<Book> searchBooks(String keyword) {
        if (keyword == null || keyword.trim().isEmpty()) {
            return java.util.Collections.emptyList();
        }
        
        String cleanKeyword = keyword.trim().toLowerCase();
        
        // Loại bỏ các từ khóa thừa
        if (cleanKeyword.startsWith("sách ")) {
            cleanKeyword = cleanKeyword.substring(5).trim();
        } else if (cleanKeyword.startsWith("truyện ")) {
            cleanKeyword = cleanKeyword.substring(7).trim();
        } else if (cleanKeyword.startsWith("cuốn ")) {
            cleanKeyword = cleanKeyword.substring(5).trim();
        } else if (cleanKeyword.startsWith("tiểu thuyết ")) {
            cleanKeyword = cleanKeyword.substring(12).trim();
        }
        
        return bookRepository.searchBooksByKeyword(cleanKeyword);
    }

    @Transactional
    @org.springframework.cache.annotation.CacheEvict(value = {"books_bestsellers", "books_latest", "books_discounted", "books_featured", "books_combos"}, allEntries = true)
    public void importBooksFromExcel(MultipartFile file) {
        try {
            List<Book> books = ExcelHelper.excelToBooks(file.getInputStream());
            for (Book newBook : books) {
                if (!org.springframework.util.StringUtils.hasText(newBook.getTitle())) {
                    continue; // Bỏ qua sách không có tên
                }
                
                java.util.Optional<Book> existingOpt = bookRepository.findFirstByTitle(newBook.getTitle().trim());
                if (existingOpt.isPresent()) {
                    Book existing = existingOpt.get();
                    if (org.springframework.util.StringUtils.hasLength(newBook.getAuthor())) existing.setAuthor(newBook.getAuthor());
                    if (org.springframework.util.StringUtils.hasLength(newBook.getPublisher())) existing.setPublisher(newBook.getPublisher());
                    if (org.springframework.util.StringUtils.hasLength(newBook.getDescription())) existing.setDescription(newBook.getDescription());
                    if (java.util.Optional.ofNullable(newBook.getPrice()).orElse(java.math.BigDecimal.ZERO).signum() > 0) existing.setPrice(newBook.getPrice());
                    if (newBook.getOldPrice() != null) existing.setOldPrice(newBook.getOldPrice());
                    existing.setDiscount(newBook.getDiscount());
                    existing.setStockQuantity(newBook.getStockQuantity());
                    java.util.Optional.ofNullable(newBook.getCategory())
                            .map(com.bookstore.entity.Category::getId)
                            .filter(categoryId -> categoryId != 0)
                            .ifPresent(categoryId -> existing.setCategory(newBook.getCategory()));
                    if (org.springframework.util.StringUtils.hasLength(newBook.getImageUrl())) existing.setImageUrl(newBook.getImageUrl());
                    bookRepository.save(existing);
                } else {
                    bookRepository.save(newBook);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("Lỗi khi import file: " + e.getMessage());
        }
    }
}

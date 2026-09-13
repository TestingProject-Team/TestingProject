package com.bookstore.config;

import com.bookstore.entity.Book;
import com.bookstore.entity.Category;
import com.bookstore.entity.User;
import com.bookstore.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DataSeederTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private CategoryRepository categoryRepository;

    @Mock
    private BookRepository bookRepository;

    @Mock
    private BannerRepository bannerRepository;

    @Mock
    private NotificationRepository notificationRepository;

    @Mock
    private CouponRepository couponRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    private DataSeeder dataSeeder;

    @BeforeEach
    void setUp() {
        dataSeeder = new DataSeeder(
                userRepository,
                categoryRepository,
                bookRepository,
                bannerRepository,
                notificationRepository,
                couponRepository,
                passwordEncoder
        );
    }

    @Test
    void testRun_WhenDatabaseIsEmpty_ShouldSeedAllData() throws Exception {
        when(userRepository.count()).thenReturn(0L);
        when(bannerRepository.count()).thenReturn(0L);
        when(notificationRepository.count()).thenReturn(0L);
        when(couponRepository.count()).thenReturn(0L);
        when(passwordEncoder.encode(anyString())).thenReturn("encodedPassword");

        when(categoryRepository.findAll()).thenReturn(new ArrayList<>());
        when(categoryRepository.save(any(Category.class))).thenAnswer(invocation -> {
            Category cat = invocation.getArgument(0);
            return new Category(1L, cat.getName(), cat.getDescription(), cat.getImageUrl(), false, null);
        });

        when(bookRepository.findAll()).thenReturn(new ArrayList<>());

        dataSeeder.run();

        verify(userRepository, times(2)).save(any(User.class));
        verify(bannerRepository, times(1)).saveAll(anyList());
        verify(notificationRepository, times(1)).saveAll(anyList());
        verify(couponRepository, times(1)).saveAll(anyList());
        verify(categoryRepository, times(10)).save(any(Category.class));
        verify(bookRepository, times(10)).save(any(Book.class));
    }

    @Test
    void testRun_WhenDatabaseIsAlreadySeeded_ShouldNotSeedDuplicateData() throws Exception {
        when(userRepository.count()).thenReturn(2L);
        when(bannerRepository.count()).thenReturn(5L);
        when(notificationRepository.count()).thenReturn(3L);
        when(couponRepository.count()).thenReturn(3L);

        List<Category> existingCategories = List.of(
                new Category(1L, "Sách Thiếu Nhi", "desc", "img", false, null),
                new Category(2L, "Tiểu Thuyết", "desc", "img", false, null),
                new Category(3L, "Khoa Học Công Nghệ", "desc", "img", false, null),
                new Category(4L, "Combo Sách", "desc", "img", false, null),
                new Category(5L, "Văn phòng phẩm", "desc", "img", false, null),
                new Category(6L, "Đồ chơi", "desc", "img", false, null),
                new Category(7L, "Manga-Comic", "desc", "img", false, null),
                new Category(8L, "Sách ngoại văn", "desc", "img", false, null),
                new Category(9L, "Quà lưu niệm", "desc", "img", false, null),
                new Category(10L, "Bách hóa", "desc", "img", false, null)
        );
        when(categoryRepository.findAll()).thenReturn(existingCategories);

        List<Book> existingBooks = List.of(
                Book.builder().title("Dế Mèn Phiêu Lưu Ký").build(),
                Book.builder().title("Clean Code").build(),
                Book.builder().title("Nhà Giả Kim").build(),
                Book.builder().title("Combo Harry Potter (7 Tập)").build(),
                Book.builder().title("Bút Bi Thiên Long FO-03").build(),
                Book.builder().title("Đồ chơi Lego City Cảnh sát tuần tra").build(),
                Book.builder().title("Doraemon Truyện Ngắn - Tập 1").build(),
                Book.builder().title("Harry Potter and the Philosopher's Stone").build(),
                Book.builder().title("Móc Khóa Gỗ Anime Chibi").build(),
                Book.builder().title("Bình Nước Thủy Tinh Có Bao Silicon 450ml").build()
        );
        when(bookRepository.findAll()).thenReturn(existingBooks);

        dataSeeder.run();

        verify(userRepository, never()).save(any(User.class));
        verify(bannerRepository, never()).saveAll(anyList());
        verify(notificationRepository, never()).saveAll(anyList());
        verify(couponRepository, never()).saveAll(anyList());
        verify(categoryRepository, never()).save(any(Category.class));
        verify(bookRepository, never()).save(any(Book.class));
    }
}

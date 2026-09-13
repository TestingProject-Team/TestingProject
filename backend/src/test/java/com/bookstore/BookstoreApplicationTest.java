package com.bookstore;

import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;
import org.springframework.boot.SpringApplication;

import java.util.TimeZone;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;

class BookstoreApplicationTest {

    @Test
    void testInit() {
        BookstoreApplication app = new BookstoreApplication();
        app.init();
        assertEquals("Asia/Ho_Chi_Minh", TimeZone.getDefault().getID());
    }

    @Test
    void testMain() {
        try (MockedStatic<SpringApplication> mockedSpringApplication = Mockito.mockStatic(SpringApplication.class)) {
            mockedSpringApplication.when(() -> SpringApplication.run(eq(BookstoreApplication.class), any(String[].class)))
                    .thenReturn(null);

            String[] args = new String[]{};
            BookstoreApplication.main(args);

            mockedSpringApplication.verify(() -> SpringApplication.run(BookstoreApplication.class, args));
        }
    }

    @Test
    void testConstructor() {
        BookstoreApplication app = new BookstoreApplication();
        assertNotNull(app);
    }
}

package com.bookstore.config;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.context.ApplicationContext;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class SpringContextTest {

    private SpringContext springContext;

    @BeforeEach
    void setUp() {
        springContext = new SpringContext();
    }

    @Test
    void testGetBean_WhenContextIsNull() {
        springContext.setApplicationContext(null);

        String bean = SpringContext.getBean(String.class);
        assertNull(bean);
    }

    @Test
    void testSetApplicationContextAndGetBean() {
        ApplicationContext context = mock(ApplicationContext.class);
        String expectedBean = "TestBean";
        when(context.getBean(String.class)).thenReturn(expectedBean);

        springContext.setApplicationContext(context);

        String actualBean = SpringContext.getBean(String.class);
        assertEquals(expectedBean, actualBean);
        verify(context, times(1)).getBean(String.class);
    }
}

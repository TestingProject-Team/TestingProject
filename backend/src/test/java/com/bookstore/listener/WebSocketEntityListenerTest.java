package com.bookstore.listener;

import com.bookstore.config.SpringContext;
import com.bookstore.service.WebSocketService;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.mockito.Mockito.*;

class WebSocketEntityListenerTest {

    private WebSocketEntityListener listener;
    private MockedStatic<SpringContext> mockedSpringContext;
    private WebSocketService webSocketService;

    @BeforeEach
    void setUp() {
        listener = new WebSocketEntityListener();
        mockedSpringContext = Mockito.mockStatic(SpringContext.class);
        webSocketService = mock(WebSocketService.class);
    }

    @AfterEach
    void tearDown() {
        if (mockedSpringContext != null && !mockedSpringContext.isClosed()) {
            mockedSpringContext.close();
        }
    }

    @Test
    void testOnEntityChange_WithValidWebSocketService() {
        mockedSpringContext.when(() -> SpringContext.getBean(WebSocketService.class))
                .thenReturn(webSocketService);

        String dummyEntity = "SampleEntity";
        listener.onEntityChange(dummyEntity);

        verify(webSocketService, times(1)).broadcastDataChange("STRING");
    }

    @Test
    void testOnEntityChange_WithNullWebSocketService() {
        mockedSpringContext.when(() -> SpringContext.getBean(WebSocketService.class))
                .thenReturn(null);

        String dummyEntity = "SampleEntity";
        assertDoesNotThrow(() -> listener.onEntityChange(dummyEntity));
        verifyNoInteractions(webSocketService);
    }

    @Test
    void testOnEntityChange_WhenExceptionThrown_ShouldCatchAndNotBreak() {
        mockedSpringContext.when(() -> SpringContext.getBean(WebSocketService.class))
                .thenThrow(new RuntimeException("Context error"));

        String dummyEntity = "SampleEntity";
        assertDoesNotThrow(() -> listener.onEntityChange(dummyEntity));
    }
}

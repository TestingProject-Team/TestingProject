package com.bookstore.config;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.StompWebSocketEndpointRegistration;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

class WebSocketConfigTest {

    private WebSocketConfig webSocketConfig;

    @BeforeEach
    void setUp() {
        webSocketConfig = new WebSocketConfig();
    }

    @Test
    void testConfigureMessageBroker() {
        MessageBrokerRegistry registry = mock(MessageBrokerRegistry.class);

        webSocketConfig.configureMessageBroker(registry);

        verify(registry, times(1)).enableSimpleBroker("/topic");
        verify(registry, times(1)).setApplicationDestinationPrefixes("/app");
    }

    @Test
    void testRegisterStompEndpoints() {
        StompEndpointRegistry registry = mock(StompEndpointRegistry.class);
        StompWebSocketEndpointRegistration registration = mock(StompWebSocketEndpointRegistration.class);

        when(registry.addEndpoint("/ws")).thenReturn(registration);
        when(registration.setAllowedOriginPatterns(anyString())).thenReturn(registration);

        webSocketConfig.registerStompEndpoints(registry);

        verify(registry, times(1)).addEndpoint("/ws");
        verify(registration, times(1)).setAllowedOriginPatterns("*");
        verify(registration, times(1)).withSockJS();
    }
}

package com.bookstore.config;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;

import java.nio.file.Paths;

import static org.mockito.Mockito.*;

class WebConfigTest {

    private WebConfig webConfig;

    @BeforeEach
    void setUp() {
        webConfig = new WebConfig();
    }

    @Test
    void testAddResourceHandlers() {
        ResourceHandlerRegistry registry = mock(ResourceHandlerRegistry.class);
        ResourceHandlerRegistration registration = mock(ResourceHandlerRegistration.class);

        when(registry.addResourceHandler("/uploads/**")).thenReturn(registration);
        when(registration.addResourceLocations(anyString())).thenReturn(registration);

        webConfig.addResourceHandlers(registry);

        verify(registry, times(1)).addResourceHandler("/uploads/**");
        String expectedPath = "file:" + Paths.get("uploads").toFile().getAbsolutePath() + "/";
        verify(registration, times(1)).addResourceLocations(expectedPath);
    }
}

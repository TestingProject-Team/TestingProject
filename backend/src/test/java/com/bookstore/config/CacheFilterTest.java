package com.bookstore.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.IOException;

import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CacheFilterTest {

    @Mock
    private HttpServletRequest request;

    @Mock
    private HttpServletResponse response;

    @Mock
    private FilterChain filterChain;

    private CacheFilter cacheFilter;

    @BeforeEach
    void setUp() {
        cacheFilter = new CacheFilter();
    }

    @Test
    void testDoFilterInternal_GetBooks_SetsCacheControlHeader() throws ServletException, IOException {
        when(request.getMethod()).thenReturn("GET");
        when(request.getRequestURI()).thenReturn("/api/books/123");

        cacheFilter.doFilterInternal(request, response, filterChain);

        verify(response, times(1)).setHeader("Cache-Control", "public, max-age=300");
        verify(filterChain, times(1)).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_GetCategories_SetsCacheControlHeader() throws ServletException, IOException {
        when(request.getMethod()).thenReturn("GET");
        when(request.getRequestURI()).thenReturn("/api/categories");

        cacheFilter.doFilterInternal(request, response, filterChain);

        verify(response, times(1)).setHeader("Cache-Control", "public, max-age=300");
        verify(filterChain, times(1)).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_GetBanners_SetsCacheControlHeader() throws ServletException, IOException {
        when(request.getMethod()).thenReturn("GET");
        when(request.getRequestURI()).thenReturn("/api/banners");

        cacheFilter.doFilterInternal(request, response, filterChain);

        verify(response, times(1)).setHeader("Cache-Control", "public, max-age=300");
        verify(filterChain, times(1)).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_GetSettings_SetsCacheControlHeader() throws ServletException, IOException {
        when(request.getMethod()).thenReturn("GET");
        when(request.getRequestURI()).thenReturn("/api/settings");

        cacheFilter.doFilterInternal(request, response, filterChain);

        verify(response, times(1)).setHeader("Cache-Control", "public, max-age=300");
        verify(filterChain, times(1)).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_PostRequest_DoesNotSetHeader() throws ServletException, IOException {
        when(request.getMethod()).thenReturn("POST");
        when(request.getRequestURI()).thenReturn("/api/books");

        cacheFilter.doFilterInternal(request, response, filterChain);

        verify(response, never()).setHeader(anyString(), anyString());
        verify(filterChain, times(1)).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_NonMatchedGetUri_DoesNotSetHeader() throws ServletException, IOException {
        when(request.getMethod()).thenReturn("GET");
        when(request.getRequestURI()).thenReturn("/api/orders");

        cacheFilter.doFilterInternal(request, response, filterChain);

        verify(response, never()).setHeader(anyString(), anyString());
        verify(filterChain, times(1)).doFilter(request, response);
    }
}

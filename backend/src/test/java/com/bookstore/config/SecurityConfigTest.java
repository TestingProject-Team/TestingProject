package com.bookstore.config;

import com.bookstore.security.JwtAuthFilter;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.context.ApplicationContext;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.config.annotation.ObjectPostProcessor;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.servlet.handler.HandlerMappingIntrospector;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class SecurityConfigTest {

    @Mock
    private JwtAuthFilter jwtAuthFilter;

    @Mock
    private AuthenticationProvider authenticationProvider;

    @Mock
    private ApplicationContext applicationContext;

    private SecurityConfig securityConfig;

    @BeforeEach
    void setUp() {
        securityConfig = new SecurityConfig(jwtAuthFilter, authenticationProvider);
    }

    @Test
    void testCorsConfigurationSource() {
        CorsConfigurationSource corsSource = securityConfig.corsConfigurationSource();
        assertNotNull(corsSource);

        MockHttpServletRequest request = new MockHttpServletRequest();
        request.setRequestURI("/api/books");

        CorsConfiguration config = corsSource.getCorsConfiguration(request);
        assertNotNull(config);
        assertEquals(List.of("*"), config.getAllowedOriginPatterns());
        assertEquals(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"), config.getAllowedMethods());
        assertEquals(List.of("*"), config.getAllowedHeaders());
        assertTrue(config.getAllowCredentials());
    }

    @Test
    void testSecurityFilterChain() throws Exception {
        ObjectPostProcessor<Object> objectPostProcessor = new ObjectPostProcessor<>() {
            @Override
            public <T> T postProcess(T object) {
                return object;
            }
        };

        AuthenticationManagerBuilder authBuilder = new AuthenticationManagerBuilder(objectPostProcessor);
        Map<Class<?>, Object> sharedObjects = new HashMap<>();
        sharedObjects.put(AuthenticationManagerBuilder.class, authBuilder);
        sharedObjects.put(ApplicationContext.class, applicationContext);

        HandlerMappingIntrospector introspector = new HandlerMappingIntrospector();
        lenient().when(applicationContext.getBeanNamesForType(any(Class.class))).thenReturn(new String[]{});
        lenient().when(applicationContext.containsBean("mvcHandlerMappingIntrospector")).thenReturn(true);
        lenient().when(applicationContext.getBean("mvcHandlerMappingIntrospector", HandlerMappingIntrospector.class)).thenReturn(introspector);

        HttpSecurity http = new HttpSecurity(objectPostProcessor, authBuilder, sharedObjects);

        SecurityFilterChain filterChain = securityConfig.securityFilterChain(http);
        assertNotNull(filterChain);
    }
}

package com.bookstore.config;

import com.bookstore.entity.Role;
import com.bookstore.entity.User;
import com.bookstore.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ApplicationConfigTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private AuthenticationConfiguration authenticationConfiguration;

    @Mock
    private AuthenticationManager authenticationManager;

    private ApplicationConfig applicationConfig;

    @BeforeEach
    void setUp() {
        applicationConfig = new ApplicationConfig(userRepository);
    }

    @Test
    void testUserDetailsService_UserFound() {
        User mockUser = User.builder()
                .username("test@example.com")
                .email("test@example.com")
                .password("encoded_pass")
                .role(Role.USER)
                .build();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(mockUser));

        UserDetailsService userDetailsService = applicationConfig.userDetailsService();
        UserDetails userDetails = userDetailsService.loadUserByUsername("test@example.com");

        assertNotNull(userDetails);
        assertEquals("test@example.com", userDetails.getUsername());
    }

    @Test
    void testUserDetailsService_UserNotFound() {
        when(userRepository.findByEmail("notfound@example.com")).thenReturn(Optional.empty());

        UserDetailsService userDetailsService = applicationConfig.userDetailsService();

        assertThrows(UsernameNotFoundException.class, () ->
                userDetailsService.loadUserByUsername("notfound@example.com"));
    }

    @Test
    void testAuthenticationProvider() {
        AuthenticationProvider authProvider = applicationConfig.authenticationProvider();
        assertNotNull(authProvider);
        assertInstanceOf(DaoAuthenticationProvider.class, authProvider);
    }

    @Test
    void testPasswordEncoder() {
        PasswordEncoder passwordEncoder = applicationConfig.passwordEncoder();
        assertNotNull(passwordEncoder);
        String rawPassword = "password123";
        String encoded = passwordEncoder.encode(rawPassword);
        assertTrue(passwordEncoder.matches(rawPassword, encoded));
    }

    @Test
    void testAuthenticationManager() throws Exception {
        when(authenticationConfiguration.getAuthenticationManager()).thenReturn(authenticationManager);

        AuthenticationManager manager = applicationConfig.authenticationManager(authenticationConfiguration);

        assertNotNull(manager);
        assertEquals(authenticationManager, manager);
        verify(authenticationConfiguration, times(1)).getAuthenticationManager();
    }
}

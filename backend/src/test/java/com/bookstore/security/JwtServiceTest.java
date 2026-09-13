package com.bookstore.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.Collections;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class JwtServiceTest {

    private JwtService jwtService;
    private UserDetails userDetails;

    @BeforeEach
    void setUp() {
        jwtService = new JwtService();
        // 256-bit secret key in Base64
        ReflectionTestUtils.setField(jwtService, "secretKey", "404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970");
        ReflectionTestUtils.setField(jwtService, "jwtExpiration", 86400000L); // 1 day

        userDetails = new User("testuser", "password", Collections.emptyList());
    }

    @Test
    void testGenerateTokenAndExtractUsername() {
        String token = jwtService.generateToken(userDetails);
        assertNotNull(token);

        String username = jwtService.extractUsername(token);
        assertEquals("testuser", username);
    }

    @Test
    void testGenerateTokenWithExtraClaims() {
        String token = jwtService.generateToken(Map.of("role", "ADMIN"), userDetails);
        assertNotNull(token);

        String username = jwtService.extractUsername(token);
        assertEquals("testuser", username);
    }

    @Test
    void testIsTokenValid_Success() {
        String token = jwtService.generateToken(userDetails);
        boolean isValid = jwtService.isTokenValid(token, userDetails);
        assertTrue(isValid);
    }

    @Test
    void testIsTokenValid_FalseWhenUsernameDoesNotMatch() {
        String token = jwtService.generateToken(userDetails);
        UserDetails nonMatchingUser = new User("other_name", "password", Collections.emptyList());
        boolean isValid = jwtService.isTokenValid(token, nonMatchingUser);
        assertFalse(isValid);
    }

    @Test
    void testIsTokenValid_DifferentUsername() {
        String token = jwtService.generateToken(userDetails);
        UserDetails otherUser = new User("differentuser", "password", Collections.emptyList());
        boolean isValid = jwtService.isTokenValid(token, otherUser);
        assertFalse(isValid);
    }

    @Test
    void testIsTokenValid_WrongUser() {
        String token = jwtService.generateToken(userDetails);
        UserDetails otherUser = new User("otheruser", "password", Collections.emptyList());
        boolean isValid = jwtService.isTokenValid(token, otherUser);
        assertFalse(isValid);
    }

    @Test
    void testIsTokenValid_ExpiredToken() {
        // Set negative expiration to create an expired token immediately
        ReflectionTestUtils.setField(jwtService, "jwtExpiration", -10000L);
        String expiredToken = jwtService.generateToken(userDetails);

        assertFalse(jwtService.isTokenValid(expiredToken, userDetails));
    }

    @Test
    void testExtractClaim() {
        String token = jwtService.generateToken(Map.of("role", "ADMIN"), userDetails);
        String subject = jwtService.extractClaim(token, claims -> claims.getSubject());
        assertEquals("testuser", subject);
    }
}

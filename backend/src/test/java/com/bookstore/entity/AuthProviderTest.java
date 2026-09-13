package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AuthProviderTest {

    @Test
    void testEnumValues() {
        AuthProvider[] providers = AuthProvider.values();
        assertEquals(4, providers.length);
        assertArrayEquals(new AuthProvider[]{
                AuthProvider.LOCAL,
                AuthProvider.GOOGLE,
                AuthProvider.APPLE,
                AuthProvider.FACEBOOK
        }, providers);
    }

    @Test
    void testEnumValueOf() {
        assertEquals(AuthProvider.LOCAL, AuthProvider.valueOf("LOCAL"));
        assertEquals(AuthProvider.GOOGLE, AuthProvider.valueOf("GOOGLE"));
        assertEquals(AuthProvider.APPLE, AuthProvider.valueOf("APPLE"));
        assertEquals(AuthProvider.FACEBOOK, AuthProvider.valueOf("FACEBOOK"));
    }
}

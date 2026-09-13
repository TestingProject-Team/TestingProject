package com.bookstore.entity;

import org.junit.jupiter.api.Test;
import org.springframework.security.core.GrantedAuthority;

import java.time.LocalDateTime;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.*;

class UserTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        User user = new User();
        LocalDateTime now = LocalDateTime.now();

        user.setId(1L);
        user.setUsername("john_doe");
        user.setPassword("secret123");
        user.setFullName("John Doe");
        user.setEmail("john@example.com");
        user.setPhone("0987654321");
        user.setGender("MALE");
        user.setBirthday("1995-05-15");
        user.setYPoints(100);
        user.setAccumulatedPoints(500);
        user.setTotalSpent(1500000.0);
        user.setFreeShipCoupons(2);
        user.setAiPreferences("Likes sci-fi and tech books");
        user.setProvider(AuthProvider.GOOGLE);
        user.setProviderId("google-12345");
        user.setRole(Role.USER);
        user.setCreatedAt(now);

        assertEquals(1L, user.getId());
        assertEquals("john_doe", user.getUsername());
        assertEquals("secret123", user.getPassword());
        assertEquals("John Doe", user.getFullName());
        assertEquals("john@example.com", user.getEmail());
        assertEquals("0987654321", user.getPhone());
        assertEquals("MALE", user.getGender());
        assertEquals("1995-05-15", user.getBirthday());
        assertEquals(100, user.getYPoints());
        assertEquals(500, user.getAccumulatedPoints());
        assertEquals(1500000.0, user.getTotalSpent());
        assertEquals(2, user.getFreeShipCoupons());
        assertEquals("Likes sci-fi and tech books", user.getAiPreferences());
        assertEquals(AuthProvider.GOOGLE, user.getProvider());
        assertEquals("google-12345", user.getProviderId());
        assertEquals(Role.USER, user.getRole());
        assertEquals(now, user.getCreatedAt());
    }

    @Test
    void testAllArgsConstructor() {
        LocalDateTime now = LocalDateTime.now();

        User user = new User(
                2L,
                "jane_admin",
                "adminPass",
                "Jane Admin",
                "jane@example.com",
                "0911222333",
                "FEMALE",
                "1990-01-01",
                200,
                1000,
                5000000.0,
                5,
                "Prefers business books",
                AuthProvider.LOCAL,
                null,
                Role.ADMIN,
                now
        );

        assertEquals(2L, user.getId());
        assertEquals("jane_admin", user.getUsername());
        assertEquals("adminPass", user.getPassword());
        assertEquals("Jane Admin", user.getFullName());
        assertEquals("jane@example.com", user.getEmail());
        assertEquals("0911222333", user.getPhone());
        assertEquals("FEMALE", user.getGender());
        assertEquals("1990-01-01", user.getBirthday());
        assertEquals(200, user.getYPoints());
        assertEquals(1000, user.getAccumulatedPoints());
        assertEquals(5000000.0, user.getTotalSpent());
        assertEquals(5, user.getFreeShipCoupons());
        assertEquals("Prefers business books", user.getAiPreferences());
        assertEquals(AuthProvider.LOCAL, user.getProvider());
        assertNull(user.getProviderId());
        assertEquals(Role.ADMIN, user.getRole());
        assertEquals(now, user.getCreatedAt());
    }

    @Test
    void testBuilderDefaults() {
        User user = User.builder()
                .username("default_user")
                .role(Role.USER)
                .build();

        assertEquals(0, user.getYPoints());
        assertEquals(0, user.getAccumulatedPoints());
        assertEquals(0.0, user.getTotalSpent());
        assertEquals(0, user.getFreeShipCoupons());
        assertEquals(AuthProvider.LOCAL, user.getProvider());
    }

    @Test
    void testUserDetailsMethods() {
        User user = User.builder()
                .username("test_user")
                .role(Role.ADMIN)
                .build();

        Collection<? extends GrantedAuthority> authorities = user.getAuthorities();
        assertNotNull(authorities);
        assertEquals(1, authorities.size());
        assertTrue(authorities.stream().anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN")));

        user.setRole(Role.USER);
        Collection<? extends GrantedAuthority> userAuthorities = user.getAuthorities();
        assertTrue(userAuthorities.stream().anyMatch(a -> a.getAuthority().equals("ROLE_USER")));

        assertTrue(user.isAccountNonExpired());
        assertTrue(user.isAccountNonLocked());
        assertTrue(user.isCredentialsNonExpired());
        assertTrue(user.isEnabled());
    }

    @Test
    void testOnCreate() {
        User user = new User();
        assertNull(user.getCreatedAt());

        user.onCreate();
        assertNotNull(user.getCreatedAt());

        LocalDateTime specificTime = LocalDateTime.of(2025, 1, 1, 0, 0);
        user.setCreatedAt(specificTime);
        user.onCreate();
        assertEquals(specificTime, user.getCreatedAt());
    }

    @Test
    void testEqualsAndHashCode() {
        User u1 = User.builder().id(1L).username("u1").role(Role.USER).build();
        User u2 = User.builder().id(1L).username("u1").role(Role.USER).build();
        User u3 = User.builder().id(2L).username("u2").role(Role.ADMIN).build();

        assertEquals(u1, u2);
        assertEquals(u1.hashCode(), u2.hashCode());
        assertNotEquals(u1, u3);
        assertNotEquals(u1, null);
        assertNotEquals(u1, new Object());
        assertEquals(u1, u1);
        assertTrue(u1.canEqual(u2));
        assertNotNull(u1.toString());
    }
}

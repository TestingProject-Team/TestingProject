package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RoleTest {

    @Test
    void testEnumValues() {
        Role[] roles = Role.values();
        assertEquals(2, roles.length);
        assertArrayEquals(new Role[]{
                Role.USER,
                Role.ADMIN
        }, roles);
    }

    @Test
    void testEnumValueOf() {
        assertEquals(Role.USER, Role.valueOf("USER"));
        assertEquals(Role.ADMIN, Role.valueOf("ADMIN"));
    }
}

package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BannerTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Banner banner = new Banner();
        banner.setId(1L);
        banner.setImageUrl("https://example.com/banner.jpg");
        banner.setTitle("Summer Sale");
        banner.setLinkUrl("https://example.com/sale");
        banner.setPosition("MAIN");

        assertEquals(1L, banner.getId());
        assertEquals("https://example.com/banner.jpg", banner.getImageUrl());
        assertEquals("Summer Sale", banner.getTitle());
        assertEquals("https://example.com/sale", banner.getLinkUrl());
        assertEquals("MAIN", banner.getPosition());
    }

    @Test
    void testAllArgsConstructor() {
        Banner banner = new Banner(2L, "https://example.com/banner2.jpg", "Winter Sale", "https://example.com/winter", "SIDE");

        assertEquals(2L, banner.getId());
        assertEquals("https://example.com/banner2.jpg", banner.getImageUrl());
        assertEquals("Winter Sale", banner.getTitle());
        assertEquals("https://example.com/winter", banner.getLinkUrl());
        assertEquals("SIDE", banner.getPosition());
    }

    @Test
    void testBuilder() {
        Banner banner = Banner.builder()
                .id(3L)
                .imageUrl("https://example.com/banner3.jpg")
                .title("Flash Sale")
                .linkUrl("https://example.com/flash")
                .position("TOP")
                .build();

        assertEquals(3L, banner.getId());
        assertEquals("https://example.com/banner3.jpg", banner.getImageUrl());
        assertEquals("Flash Sale", banner.getTitle());
        assertEquals("https://example.com/flash", banner.getLinkUrl());
        assertEquals("TOP", banner.getPosition());
        assertNotNull(banner.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        Banner b1 = Banner.builder().id(1L).imageUrl("img").title("title").linkUrl("link").position("MAIN").build();
        Banner b2 = Banner.builder().id(1L).imageUrl("img").title("title").linkUrl("link").position("MAIN").build();
        Banner b3 = Banner.builder().id(2L).imageUrl("img2").title("title2").linkUrl("link2").position("SIDE").build();

        assertEquals(b1, b2);
        assertEquals(b1.hashCode(), b2.hashCode());
        assertNotEquals(b1, b3);
        assertNotEquals(b1, null);
        assertNotEquals(b1, new Object());
        assertEquals(b1, b1);
        assertTrue(b1.canEqual(b2));
    }
}

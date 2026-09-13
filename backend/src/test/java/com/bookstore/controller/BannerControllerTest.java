package com.bookstore.controller;

import com.bookstore.entity.Banner;
import com.bookstore.service.BannerService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class BannerControllerTest {

    @Mock
    private BannerService bannerService;

    @InjectMocks
    private BannerController bannerController;

    private Banner testBanner;

    @BeforeEach
    void setUp() {
        testBanner = Banner.builder()
                .id(1L)
                .title("Special Offer")
                .imageUrl("https://example.com/banner.jpg")
                .linkUrl("https://example.com/books")
                .position("HOME_TOP")
                .build();
    }

    @Test
    void testGetAllBanners() {
        when(bannerService.getAllBanners()).thenReturn(List.of(testBanner));

        ResponseEntity<List<Banner>> response = bannerController.getAllBanners();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBanner), response.getBody());
        verify(bannerService).getAllBanners();
    }

    @Test
    void testGetBannersByPosition() {
        when(bannerService.getBannersByPosition("HOME_TOP")).thenReturn(List.of(testBanner));

        ResponseEntity<List<Banner>> response = bannerController.getBannersByPosition("HOME_TOP");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testBanner), response.getBody());
        verify(bannerService).getBannersByPosition("HOME_TOP");
    }

    @Test
    void testCreateBanner() {
        when(bannerService.createBanner(testBanner)).thenReturn(testBanner);

        ResponseEntity<Banner> response = bannerController.createBanner(testBanner);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testBanner, response.getBody());
        verify(bannerService).createBanner(testBanner);
    }

    @Test
    void testUpdateBanner() {
        when(bannerService.updateBanner(1L, testBanner)).thenReturn(testBanner);

        ResponseEntity<Banner> response = bannerController.updateBanner(1L, testBanner);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testBanner, response.getBody());
        verify(bannerService).updateBanner(1L, testBanner);
    }

    @Test
    void testDeleteBanner() {
        ResponseEntity<Void> response = bannerController.deleteBanner(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(bannerService).deleteBanner(1L);
    }
}
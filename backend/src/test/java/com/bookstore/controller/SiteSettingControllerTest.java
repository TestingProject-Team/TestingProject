package com.bookstore.controller;

import com.bookstore.service.SiteSettingService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class SiteSettingControllerTest {

    @Mock
    private SiteSettingService siteSettingService;

    @InjectMocks
    private SiteSettingController siteSettingController;

    @Test
    void testGetAllSettings() {
        Map<String, String> settings = Map.of("site_name", "YiYi Bookstore");
        when(siteSettingService.getSettingsAsMap()).thenReturn(settings);

        ResponseEntity<Map<String, String>> response = siteSettingController.getAllSettings();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(settings, response.getBody());
        verify(siteSettingService).getSettingsAsMap();
    }

    @Test
    void testSaveSettings() {
        Map<String, String> settings = Map.of("site_name", "YiYi Bookstore");

        ResponseEntity<?> response = siteSettingController.saveSettings(settings);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(siteSettingService).saveAllSettings(settings);
    }
}
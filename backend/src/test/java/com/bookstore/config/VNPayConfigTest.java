package com.bookstore.config;

import jakarta.servlet.http.HttpServletRequest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class VNPayConfigTest {

    @Mock
    private HttpServletRequest request;

    private VNPayConfig vnPayConfig;

    @BeforeEach
    void setUp() {
        vnPayConfig = new VNPayConfig();
    }

    @Test
    void testSettersAndGetters() {
        vnPayConfig.setTmnCode("NEW_TMN");
        assertEquals("NEW_TMN", VNPayConfig.vnp_TmnCode);

        vnPayConfig.setTmnCode(null);
        assertEquals("NEW_TMN", VNPayConfig.vnp_TmnCode);

        vnPayConfig.setTmnCode("   ");
        assertEquals("NEW_TMN", VNPayConfig.vnp_TmnCode);

        vnPayConfig.setSecretKey("NEW_SECRET");
        assertEquals("NEW_SECRET", VNPayConfig.secretKey);

        vnPayConfig.setSecretKey(null);
        assertEquals("NEW_SECRET", VNPayConfig.secretKey);

        vnPayConfig.setSecretKey("  ");
        assertEquals("NEW_SECRET", VNPayConfig.secretKey);

        vnPayConfig.setPayUrl("https://new.url");
        assertEquals("https://new.url", VNPayConfig.vnp_PayUrl);

        vnPayConfig.setPayUrl(null);
        assertEquals("https://new.url", VNPayConfig.vnp_PayUrl);

        vnPayConfig.setPayUrl("   ");
        assertEquals("https://new.url", VNPayConfig.vnp_PayUrl);
    }

    @Test
    void testHmacSHA512_Success() {
        String key = "secret_key";
        String data = "sample_data_to_hash";

        String hash = VNPayConfig.hmacSHA512(key, data);

        assertNotNull(hash);
        assertEquals(128, hash.length());
    }

    @Test
    void testHmacSHA512_NullKeyOrData_ReturnsEmptyString() {
        String hash1 = VNPayConfig.hmacSHA512(null, "data");
        assertEquals("", hash1);

        String hash2 = VNPayConfig.hmacSHA512("key", null);
        assertEquals("", hash2);
    }

    @Test
    void testGetIpAddress_WithHeader() {
        when(request.getHeader("X-FORWARDED-FOR")).thenReturn("192.168.1.100");

        String ip = VNPayConfig.getIpAddress(request);
        assertEquals("192.168.1.100", ip);
    }

    @Test
    void testGetIpAddress_WithoutHeader() {
        when(request.getHeader("X-FORWARDED-FOR")).thenReturn(null);
        when(request.getRemoteAddr()).thenReturn("127.0.0.1");

        String ip = VNPayConfig.getIpAddress(request);
        assertEquals("127.0.0.1", ip);
    }

    @Test
    void testGetIpAddress_Exception() {
        when(request.getHeader("X-FORWARDED-FOR")).thenThrow(new RuntimeException("Request error"));

        String ip = VNPayConfig.getIpAddress(request);
        assertEquals("Invalid IP", ip);
    }

    @Test
    void testGetRandomNumber() {
        int length = 8;
        String randomStr = VNPayConfig.getRandomNumber(length);

        assertNotNull(randomStr);
        assertEquals(length, randomStr.length());
        assertTrue(randomStr.matches("\\d+"));
    }
}

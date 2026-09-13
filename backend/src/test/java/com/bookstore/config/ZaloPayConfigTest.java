package com.bookstore.config;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ZaloPayConfigTest {

    @Test
    void testConstants() {
        assertEquals("2553", ZaloPayConfig.APP_ID);
        assertEquals("***REMOVED_ZALOPAY_KEY1***", ZaloPayConfig.KEY1);
        assertEquals("kLtgPl8YESD1XcgX5IQOZIbdzVmWVPNI", ZaloPayConfig.KEY2);
        assertEquals("https://sb-openapi.zalopay.vn/v2/create", ZaloPayConfig.CREATE_ORDER_URL);
        assertEquals("https://sb-openapi.zalopay.vn/v2/query", ZaloPayConfig.QUERY_ORDER_URL);
    }

    @Test
    void testHmacSHA256_ValidData() {
        String data = "app_id=2553&app_trans_id=123456";
        String key = "test_key";

        String hash = ZaloPayConfig.hmacSHA256(data, key);

        assertNotNull(hash);
        assertFalse(hash.isEmpty());
        assertEquals(64, hash.length());
    }

    @Test
    void testHmacSHA256_ExceptionHandling() {
        assertThrows(RuntimeException.class, () -> ZaloPayConfig.hmacSHA256(null, "key"));
    }

    @Test
    void testConstructor() {
        ZaloPayConfig config = new ZaloPayConfig();
        assertNotNull(config);
    }
}

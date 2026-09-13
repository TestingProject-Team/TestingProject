package com.bookstore.config;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MoMoConfigTest {

    @Test
    void testConstants() {
        assertEquals("MOMOBKUN20180529", MoMoConfig.PARTNER_CODE);
        assertEquals("klm05TvNBzhg7h7j", MoMoConfig.ACCESS_KEY);
        assertEquals("at67qH6mk8w5Y1nAyMoYKMWACiEi2bsa", MoMoConfig.SECRET_KEY);
        assertEquals("https://test-payment.momo.vn/v2/gateway/api/create", MoMoConfig.ENDPOINT);
        assertEquals("http://localhost:5173/payment-result", MoMoConfig.RETURN_URL);
        assertEquals("http://localhost:8081/api/payment/momo-ipn", MoMoConfig.NOTIFY_URL);
    }

    @Test
    void testHmacSHA256_ValidData() {
        String data = "partnerCode=MOMOBKUN20180529&orderId=123456";
        String key = "secret_key_test";

        String hash = MoMoConfig.hmacSHA256(data, key);

        assertNotNull(hash);
        assertFalse(hash.isEmpty());
        assertEquals(64, hash.length());
    }

    @Test
    void testHmacSHA256_ExceptionHandling() {
        assertThrows(RuntimeException.class, () -> MoMoConfig.hmacSHA256(null, "key"));
    }

    @Test
    void testConstructor() {
        MoMoConfig config = new MoMoConfig();
        assertNotNull(config);
    }
}

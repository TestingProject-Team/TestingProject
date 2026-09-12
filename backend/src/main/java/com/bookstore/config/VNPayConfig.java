package com.bookstore.config;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Random;

@Configuration
public class VNPayConfig {
    public static String vnp_PayUrl = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html";
    public static String vnp_ReturnUrl = "http://localhost:5173/payment-result";
    public static String vnp_TmnCode = "CGXZLS0Z";
    public static String secretKey = "***REMOVED_VNPAY_HASH_SECRET***";
    public static String vnp_ApiUrl = "https://sandbox.vnpayment.vn/merchant_webapi/api/transaction";

    @Value("${vnpay.tmnCode:CGXZLS0Z}")
    public void setTmnCode(String tmnCode) {
        if (tmnCode != null && !tmnCode.trim().isEmpty()) {
            VNPayConfig.vnp_TmnCode = tmnCode.trim();
        }
    }

    @Value("${vnpay.hashSecret:***REMOVED_VNPAY_HASH_SECRET***}")
    public void setSecretKey(String hashSecret) {
        if (hashSecret != null && !hashSecret.trim().isEmpty()) {
            VNPayConfig.secretKey = hashSecret.trim();
        }
    }

    @Value("${vnpay.url:https://sandbox.vnpayment.vn/paymentv2/vpcpay.html}")
    public void setPayUrl(String url) {
        if (url != null && !url.trim().isEmpty()) {
            VNPayConfig.vnp_PayUrl = url.trim();
        }
    }

    public static String hmacSHA512(final String key, final String data) {
        try {
            if (key == null || data == null) {
                throw new NullPointerException();
            }
            final Mac hmac512 = Mac.getInstance("HmacSHA512");
            byte[] hmacKeyBytes = key.getBytes(StandardCharsets.UTF_8);
            final SecretKeySpec secretKeySpec = new SecretKeySpec(hmacKeyBytes, "HmacSHA512");
            hmac512.init(secretKeySpec);
            byte[] dataBytes = data.getBytes(StandardCharsets.UTF_8);
            byte[] result = hmac512.doFinal(dataBytes);
            StringBuilder sb = new StringBuilder(2 * result.length);
            for (byte b : result) {
                sb.append(String.format("%02x", b & 0xff));
            }
            return sb.toString();

        } catch (Exception ex) {
            return "";
        }
    }

    public static String getIpAddress(HttpServletRequest request) {
        String ipAdress;
        try {
            ipAdress = request.getHeader("X-FORWARDED-FOR");
            if (ipAdress == null) {
                ipAdress = request.getRemoteAddr();
            }
        } catch (Exception e) {
            ipAdress = "Invalid IP";
        }
        return ipAdress;
    }

    public static String getRandomNumber(int len) {
        Random rnd = new Random();
        String chars = "0123456789";
        StringBuilder sb = new StringBuilder(len);
        for (int i = 0; i < len; i++) {
            sb.append(chars.charAt(rnd.nextInt(chars.length())));
        }
        return sb.toString();
    }
}

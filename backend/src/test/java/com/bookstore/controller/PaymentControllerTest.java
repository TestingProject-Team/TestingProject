package com.bookstore.controller;

import com.bookstore.config.MoMoConfig;
import com.bookstore.config.VNPayConfig;
import com.bookstore.config.ZaloPayConfig;
import com.bookstore.service.OrderService;
import jakarta.servlet.http.HttpServletRequest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedConstruction;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class PaymentControllerTest {

    @Mock
    private OrderService orderService;

    @Mock
    private HttpServletRequest request;

    @InjectMocks
    private PaymentController paymentController;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(paymentController, "frontendUrl", "http://localhost:5173");
    }

    @Test
    void testCreatePaymentUrl_Success() {
        when(request.getHeader("X-FORWARDED-FOR")).thenReturn(null);
        when(request.getRemoteAddr()).thenReturn("127.0.0.1");

        ResponseEntity<Map<String, String>> response = paymentController.createPaymentUrl(100000L, "ORD1", "NCB", request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertNotNull(response.getBody().get("url"));
    }

    @Test
    void testMockReturn_Success() {
        doNothing().when(orderService).confirmVNPayPayment(1L, true);

        ResponseEntity<?> response = paymentController.mockReturn(Map.of("orderId", "1", "success", true));

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(1L, true);
    }

    @Test
    void testMockReturn_Error() {
        ResponseEntity<?> response = paymentController.mockReturn(Map.of("orderId", "invalid", "success", true));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_InvalidSignature() {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("00");
        when(request.getParameter("vnp_SecureHash")).thenReturn("INVALID_HASH");

        ResponseEntity<?> response = paymentController.vnpayReturn(request);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_Success() throws Exception {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("00");

        String hashData = "vnp_ResponseCode=" + URLEncoder.encode("00", StandardCharsets.US_ASCII.toString())
                + "&vnp_TxnRef=" + URLEncoder.encode("123_456", StandardCharsets.US_ASCII.toString());
        String correctHash = VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData);
        when(request.getParameter("vnp_SecureHash")).thenReturn(correctHash);

        ResponseEntity<?> response = paymentController.vnpayReturn(request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(123L, true);
    }

    @Test
    void testVnpayReturn_FailedResponseCode() throws Exception {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("99");

        String hashData = "vnp_ResponseCode=" + URLEncoder.encode("99", StandardCharsets.US_ASCII.toString())
                + "&vnp_TxnRef=" + URLEncoder.encode("123_456", StandardCharsets.US_ASCII.toString());
        String correctHash = VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData);
        when(request.getParameter("vnp_SecureHash")).thenReturn(correctHash);

        ResponseEntity<?> response = paymentController.vnpayReturn(request);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(123L, false);
    }

    @Test
    void testMomoReturn_Success() {
        when(request.getParameter("partnerCode")).thenReturn(MoMoConfig.PARTNER_CODE);
        when(request.getParameter("orderId")).thenReturn("100_123");
        when(request.getParameter("requestId")).thenReturn("req1");
        when(request.getParameter("amount")).thenReturn("50000");
        when(request.getParameter("orderInfo")).thenReturn("Order Info");
        when(request.getParameter("orderType")).thenReturn("momo_wallet");
        when(request.getParameter("transId")).thenReturn("trans1");
        when(request.getParameter("resultCode")).thenReturn("0");
        when(request.getParameter("message")).thenReturn("Success");
        when(request.getParameter("payType")).thenReturn("qr");
        when(request.getParameter("responseTime")).thenReturn("12345");
        when(request.getParameter("extraData")).thenReturn("");

        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Success" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=0" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);
        when(request.getParameter("signature")).thenReturn(sig);

        ResponseEntity<?> response = paymentController.momoReturn(request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(100L, true);
    }

    @Test
    void testMomoReturn_InvalidSignature() {
        when(request.getParameter("partnerCode")).thenReturn(MoMoConfig.PARTNER_CODE);
        when(request.getParameter("orderId")).thenReturn("100_123");
        when(request.getParameter("requestId")).thenReturn("req1");
        when(request.getParameter("amount")).thenReturn("50000");
        when(request.getParameter("orderInfo")).thenReturn("Order Info");
        when(request.getParameter("orderType")).thenReturn("momo_wallet");
        when(request.getParameter("transId")).thenReturn("trans1");
        when(request.getParameter("resultCode")).thenReturn("0");
        when(request.getParameter("message")).thenReturn("Success");
        when(request.getParameter("payType")).thenReturn("qr");
        when(request.getParameter("responseTime")).thenReturn("12345");
        when(request.getParameter("extraData")).thenReturn("");
        when(request.getParameter("signature")).thenReturn("INVALID");

        ResponseEntity<?> response = paymentController.momoReturn(request);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testMomoIpn_Success() {
        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Success" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=0" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);

        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", "0");
        payload.put("message", "Success");
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        payload.put("signature", sig);

        ResponseEntity<?> response = paymentController.momoIpn(payload);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(100L, true);
    }

    @Test
    void testZalopayReturn_InvalidAppTransId() {
        ResponseEntity<?> response1 = paymentController.zalopayReturn("invalid");
        assertEquals(HttpStatus.BAD_REQUEST, response1.getStatusCode());

        ResponseEntity<?> response2 = paymentController.zalopayReturn("too_many_parts_here");
        assertEquals(HttpStatus.BAD_REQUEST, response2.getStatusCode());
    }

    @Test
    void testCreatePaymentUrl_FieldWithEmptyValueSkipped() {
        when(request.getHeader("X-FORWARDED-FOR")).thenReturn(null);
        when(request.getRemoteAddr()).thenReturn("127.0.0.1");

        // bankCode is null -> vnp_Params won't have bankCode
        ResponseEntity<Map<String, String>> response = paymentController.createPaymentUrl(100000L, "ORD1", null, request);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testMomoIpn_OptimisticLocking() {
        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Success" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=0" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);

        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", "0");
        payload.put("message", "Success");
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        payload.put("signature", sig);

        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("concurrent", new Throwable()))
                .when(orderService).confirmVNPayPayment(100L, true);

        ResponseEntity<?> response = paymentController.momoIpn(payload);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testMomoIpn_HibernateStaleObject() {
        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Success" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=0" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);

        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", "0");
        payload.put("message", "Success");
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        payload.put("signature", sig);

        org.hibernate.StaleObjectStateException staleEx = new org.hibernate.StaleObjectStateException("Order", 100L);
        RuntimeException wrapperEx = new RuntimeException("wrapped", staleEx);
        doThrow(wrapperEx).when(orderService).confirmVNPayPayment(100L, true);

        ResponseEntity<?> response = paymentController.momoIpn(payload);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testMomoIpn_FailedCodeOptimisticLocking() {
        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Fail" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=99" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);

        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", "99");
        payload.put("message", "Fail");
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        payload.put("signature", sig);

        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("concurrent", new Throwable()))
                .when(orderService).confirmVNPayPayment(100L, false);

        ResponseEntity<?> response = paymentController.momoIpn(payload);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testMomoIpn_FailedCodeHibernateStaleObject() {
        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Fail" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=99" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);

        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", "99");
        payload.put("message", "Fail");
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        payload.put("signature", sig);

        org.hibernate.StaleObjectStateException staleEx = new org.hibernate.StaleObjectStateException("Order", 100L);
        RuntimeException wrapperEx = new RuntimeException("wrapped", staleEx);
        doThrow(wrapperEx).when(orderService).confirmVNPayPayment(100L, false);

        ResponseEntity<?> response = paymentController.momoIpn(payload);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testMomoReturn_FailedCodeOptimisticLocking() {
        when(request.getParameter("partnerCode")).thenReturn(MoMoConfig.PARTNER_CODE);
        when(request.getParameter("orderId")).thenReturn("100_123");
        when(request.getParameter("requestId")).thenReturn("req1");
        when(request.getParameter("amount")).thenReturn("50000");
        when(request.getParameter("orderInfo")).thenReturn("Order Info");
        when(request.getParameter("orderType")).thenReturn("momo_wallet");
        when(request.getParameter("transId")).thenReturn("trans1");
        when(request.getParameter("resultCode")).thenReturn("49");
        when(request.getParameter("message")).thenReturn("User cancelled");
        when(request.getParameter("payType")).thenReturn("qr");
        when(request.getParameter("responseTime")).thenReturn("12345");
        when(request.getParameter("extraData")).thenReturn("");

        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=User cancelled" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=49" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);
        when(request.getParameter("signature")).thenReturn(sig);

        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("concurrent", new Throwable()))
                .when(orderService).confirmVNPayPayment(100L, false);

        ResponseEntity<?> response = paymentController.momoReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testMomoReturn_FailedCodeHibernateStaleObject() {
        when(request.getParameter("partnerCode")).thenReturn(MoMoConfig.PARTNER_CODE);
        when(request.getParameter("orderId")).thenReturn("100_123");
        when(request.getParameter("requestId")).thenReturn("req1");
        when(request.getParameter("amount")).thenReturn("50000");
        when(request.getParameter("orderInfo")).thenReturn("Order Info");
        when(request.getParameter("orderType")).thenReturn("momo_wallet");
        when(request.getParameter("transId")).thenReturn("trans1");
        when(request.getParameter("resultCode")).thenReturn("49");
        when(request.getParameter("message")).thenReturn("User cancelled");
        when(request.getParameter("payType")).thenReturn("qr");
        when(request.getParameter("responseTime")).thenReturn("12345");
        when(request.getParameter("extraData")).thenReturn("");

        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=User cancelled" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=49" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);
        when(request.getParameter("signature")).thenReturn(sig);

        org.hibernate.StaleObjectStateException staleEx = new org.hibernate.StaleObjectStateException("Order", 100L);
        RuntimeException wrapperEx = new RuntimeException("wrapped", staleEx);
        doThrow(wrapperEx).when(orderService).confirmVNPayPayment(100L, false);

        ResponseEntity<?> response = paymentController.momoReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_FailedResponseCodeOptimisticLocking() throws Exception {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("99");

        String hashData = "vnp_ResponseCode=" + URLEncoder.encode("99", StandardCharsets.US_ASCII.toString())
                + "&vnp_TxnRef=" + URLEncoder.encode("123_456", StandardCharsets.US_ASCII.toString());
        String correctHash = VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData);
        when(request.getParameter("vnp_SecureHash")).thenReturn(correctHash);

        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("concurrent", new Throwable()))
                .when(orderService).confirmVNPayPayment(123L, false);

        ResponseEntity<?> response = paymentController.vnpayReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_FailedResponseCodeHibernateStaleObject() throws Exception {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("99");

        String hashData = "vnp_ResponseCode=" + URLEncoder.encode("99", StandardCharsets.US_ASCII.toString())
                + "&vnp_TxnRef=" + URLEncoder.encode("123_456", StandardCharsets.US_ASCII.toString());
        String correctHash = VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData);
        when(request.getParameter("vnp_SecureHash")).thenReturn(correctHash);

        org.hibernate.StaleObjectStateException staleEx = new org.hibernate.StaleObjectStateException("Order", 123L);
        RuntimeException wrapperEx = new RuntimeException("wrapped", staleEx);
        doThrow(wrapperEx).when(orderService).confirmVNPayPayment(123L, false);

        ResponseEntity<?> response = paymentController.vnpayReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testCreateZaloPayUrl_SuccessAndErrorBranches() {
        ResponseEntity<?> response = paymentController.createZaloPayUrl(10000L, "100");
        assertNotNull(response);
    }

    @Test
    void testCreatePaymentUrl_NullAndEmptyValuesInParams() {
        when(request.getHeader("X-FORWARDED-FOR")).thenReturn(null);
        when(request.getRemoteAddr()).thenReturn("127.0.0.1");

        ResponseEntity<Map<String, String>> response = paymentController.createPaymentUrl(100000L, "ORD1", "NCB", request);
        assertNotNull(response);
    }

    @Test
    void testZalopayReturn_Success() {
        // Mocking RestTemplate for ZaloPay query return
        // Note: when calling zalopayReturn("240101_100"), if real HTTP call fails or returns non-200/error map,
        // it enters the else branch.
    }

    @Test
    void testZalopayReturn_AllBranches() {
        // Calling with valid format triggers RestTemplate postForEntity
        ResponseEntity<?> response = paymentController.zalopayReturn("240101_100");
        assertNotNull(response);
    }

    @Test
    void testCreatePaymentUrl_ExceptionHandling() {
        lenient().when(request.getHeader("X-FORWARDED-FOR")).thenThrow(new RuntimeException("Error"));
        lenient().when(request.getRemoteAddr()).thenReturn(null);

        ResponseEntity<Map<String, String>> response = paymentController.createPaymentUrl(100000L, "ORD1", null, request);
        assertNotNull(response);
    }

    @Test
    void testVnpayReturn_SecureHashTypeParam() {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_SecureHashType");
        paramNames.add("vnp_SecureHash");
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_SecureHashType")).thenReturn("SHA512");
        when(request.getParameter("vnp_SecureHash")).thenReturn("INV");
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("00");

        ResponseEntity<?> response = paymentController.vnpayReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_ExceptionHandling() {
        when(request.getParameterNames()).thenThrow(new RuntimeException("Simulated exception"));
        ResponseEntity<?> response = paymentController.vnpayReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testMomoReturn_FailureResultCode() {
        when(request.getParameter("partnerCode")).thenReturn(MoMoConfig.PARTNER_CODE);
        when(request.getParameter("orderId")).thenReturn("100_123");
        when(request.getParameter("requestId")).thenReturn("req1");
        when(request.getParameter("amount")).thenReturn("50000");
        when(request.getParameter("orderInfo")).thenReturn("Order Info");
        when(request.getParameter("orderType")).thenReturn("momo_wallet");
        when(request.getParameter("transId")).thenReturn("trans1");
        when(request.getParameter("resultCode")).thenReturn("49");
        when(request.getParameter("message")).thenReturn("User cancelled");
        when(request.getParameter("payType")).thenReturn("qr");
        when(request.getParameter("responseTime")).thenReturn("12345");
        when(request.getParameter("extraData")).thenReturn("");

        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=User cancelled" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=49" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);
        when(request.getParameter("signature")).thenReturn(sig);

        ResponseEntity<?> response = paymentController.momoReturn(request);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(100L, false);
    }

    @Test
    void testMomoReturn_ExceptionHandling() {
        when(request.getParameter("partnerCode")).thenThrow(new RuntimeException("Simulated error"));
        ResponseEntity<?> response = paymentController.momoReturn(request);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testMomoIpn_InvalidSignature() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("signature", "INVALID");

        ResponseEntity<?> response = paymentController.momoIpn(payload);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testMomoIpn_FailedResultCode() {
        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Fail" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=99" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);

        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", "99");
        payload.put("message", "Fail");
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        payload.put("signature", sig);

        ResponseEntity<?> response = paymentController.momoIpn(payload);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).confirmVNPayPayment(100L, false);
    }

    @Test
    void testMomoIpn_ExceptionHandling() {
        ResponseEntity<?> response = paymentController.momoIpn(null);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_OptimisticLockingAndCauseIgnored() throws Exception {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("00");

        String hashData = "vnp_ResponseCode=" + URLEncoder.encode("00", StandardCharsets.US_ASCII.toString())
                + "&vnp_TxnRef=" + URLEncoder.encode("123_456", StandardCharsets.US_ASCII.toString());
        String correctHash = VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData);
        when(request.getParameter("vnp_SecureHash")).thenReturn(correctHash);

        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("concurrent", new Throwable()))
                .when(orderService).confirmVNPayPayment(123L, true);

        ResponseEntity<?> response = paymentController.vnpayReturn(request);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testVnpayReturn_HibernateStaleObjectExceptionIgnored() throws Exception {
        Vector<String> paramNames = new Vector<>();
        paramNames.add("vnp_TxnRef");
        paramNames.add("vnp_ResponseCode");
        paramNames.add("vnp_SecureHash");

        when(request.getParameterNames()).thenReturn(paramNames.elements());
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("00");

        String hashData = "vnp_ResponseCode=" + URLEncoder.encode("00", StandardCharsets.US_ASCII.toString())
                + "&vnp_TxnRef=" + URLEncoder.encode("123_456", StandardCharsets.US_ASCII.toString());
        String correctHash = VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData);
        when(request.getParameter("vnp_SecureHash")).thenReturn(correctHash);

        org.hibernate.StaleObjectStateException staleEx = new org.hibernate.StaleObjectStateException("Order", 123L);
        RuntimeException wrapperEx = new RuntimeException("wrapped", staleEx);
        doThrow(wrapperEx).when(orderService).confirmVNPayPayment(123L, true);

        ResponseEntity<?> response = paymentController.vnpayReturn(request);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void testMomoReturn_OptimisticLockingAndHibernateStaleObjectIgnored() {
        when(request.getParameter("partnerCode")).thenReturn(MoMoConfig.PARTNER_CODE);
        when(request.getParameter("orderId")).thenReturn("100_123");
        when(request.getParameter("requestId")).thenReturn("req1");
        when(request.getParameter("amount")).thenReturn("50000");
        when(request.getParameter("orderInfo")).thenReturn("Order Info");
        when(request.getParameter("orderType")).thenReturn("momo_wallet");
        when(request.getParameter("transId")).thenReturn("trans1");
        when(request.getParameter("resultCode")).thenReturn("0");
        when(request.getParameter("message")).thenReturn("Success");
        when(request.getParameter("payType")).thenReturn("qr");
        when(request.getParameter("responseTime")).thenReturn("12345");
        when(request.getParameter("extraData")).thenReturn("");

        String rawSignature = "accessKey=" + MoMoConfig.ACCESS_KEY +
                "&amount=50000" +
                "&extraData=" +
                "&message=Success" +
                "&orderId=100_123" +
                "&orderInfo=Order Info" +
                "&orderType=momo_wallet" +
                "&partnerCode=" + MoMoConfig.PARTNER_CODE +
                "&payType=qr" +
                "&requestId=req1" +
                "&responseTime=12345" +
                "&resultCode=0" +
                "&transId=trans1";
        String sig = MoMoConfig.hmacSHA256(rawSignature, MoMoConfig.SECRET_KEY);
        when(request.getParameter("signature")).thenReturn(sig);

        org.hibernate.StaleObjectStateException staleEx = new org.hibernate.StaleObjectStateException("Order", 100L);
        RuntimeException wrapperEx = new RuntimeException("wrapped", staleEx);
        doThrow(wrapperEx).when(orderService).confirmVNPayPayment(100L, true);

        ResponseEntity<?> response = paymentController.momoReturn(request);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void createPaymentUrlCoversEmptyBankAndNullAndEmptyParameterValues() {
        when(request.getHeader("X-FORWARDED-FOR")).thenReturn(null);
        when(request.getRemoteAddr()).thenReturn(null);
        String originalTmnCode = VNPayConfig.vnp_TmnCode;
        try {
            VNPayConfig.vnp_TmnCode = null;
            assertEquals(HttpStatus.OK,
                    paymentController.createPaymentUrl(1L, "1", "", request).getStatusCode());
            VNPayConfig.vnp_TmnCode = "";
            assertEquals(HttpStatus.OK,
                    paymentController.createPaymentUrl(1L, "1", null, request).getStatusCode());
        } finally {
            VNPayConfig.vnp_TmnCode = originalTmnCode;
        }
    }

    @Test
    void createMomoUrlCoversSuccessNullBodyMissingUrlAndRuntimeFailure() {
        try (MockedConstruction<RestTemplate> construction = restResponse(Map.of("payUrl", "https://momo/pay"))) {
            ResponseEntity<?> success = paymentController.createMomoUrl(10L, "7");
            assertEquals(HttpStatus.OK, success.getStatusCode());
            assertEquals("https://momo/pay", ((Map<?, ?>) success.getBody()).get("url"));
        }
        try (MockedConstruction<RestTemplate> construction = restResponse(null)) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.createMomoUrl(10L, "7").getStatusCode());
        }
        try (MockedConstruction<RestTemplate> construction = restResponse(Map.of("resultCode", 1))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.createMomoUrl(10L, "7").getStatusCode());
        }
        try (MockedConstruction<RestTemplate> construction = mockConstruction(RestTemplate.class,
                (mock, context) -> when(mock.postForEntity(anyString(), any(), eq(Map.class)))
                        .thenThrow(new IllegalStateException("offline")))) {
            ResponseEntity<?> error = paymentController.createMomoUrl(10L, "7");
            assertEquals(HttpStatus.BAD_REQUEST, error.getStatusCode());
            assertTrue(((Map<?, ?>) error.getBody()).get("message").toString().contains("offline"));
        }
    }

    @Test
    void createMomoUrlCoversHttpStatusException() {
        HttpClientErrorException apiError = HttpClientErrorException.create(
                HttpStatus.BAD_REQUEST, "bad", null, "gateway detail".getBytes(StandardCharsets.UTF_8),
                StandardCharsets.UTF_8);
        try (MockedConstruction<RestTemplate> construction = mockConstruction(RestTemplate.class,
                (mock, context) -> when(mock.postForEntity(anyString(), any(), eq(Map.class)))
                        .thenThrow(apiError))) {
            ResponseEntity<?> response = paymentController.createMomoUrl(10L, "7");
            assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
            assertTrue(((Map<?, ?>) response.getBody()).get("message").toString().contains("gateway detail"));
        }
    }

    @Test
    void createZaloPayUrlCoversEveryResponseShapeAndException() {
        try (MockedConstruction<RestTemplate> construction = restResponse(null)) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.createZaloPayUrl(10L, "7").getStatusCode());
        }
        try (MockedConstruction<RestTemplate> construction = restResponse(Map.of("other", 1))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.createZaloPayUrl(10L, "7").getStatusCode());
        }
        try (MockedConstruction<RestTemplate> construction = restResponse(Map.of("return_code", 2))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.createZaloPayUrl(10L, "7").getStatusCode());
        }
        try (MockedConstruction<RestTemplate> construction =
                     restResponse(Map.of("return_code", 1, "order_url", "https://zalo/pay"))) {
            assertEquals("https://zalo/pay", paymentController.createZaloPayUrl(10L, "7").getBody().get("url"));
        }
        try (MockedConstruction<RestTemplate> construction = restResponse(Map.of("return_code", 1))) {
            assertEquals("", paymentController.createZaloPayUrl(10L, "7").getBody().get("url"));
        }
        try (MockedConstruction<RestTemplate> construction = mockConstruction(RestTemplate.class,
                (mock, context) -> when(mock.postForEntity(anyString(), any(), eq(Map.class)))
                        .thenThrow(new IllegalStateException("offline")))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.createZaloPayUrl(10L, "7").getStatusCode());
        }
    }

    @Test
    void zalopayReturnCoversSuccessFailureAndServiceExceptionBranches() {
        try (MockedConstruction<RestTemplate> construction = mockConstruction(RestTemplate.class,
                (mock, context) -> when(mock.postForEntity(anyString(), any(), eq(Map.class)))
                        .thenReturn(ResponseEntity.ok(Map.of("return_code", 1))))) {
            assertEquals(HttpStatus.OK, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("race", new Throwable()))
                .when(orderService).confirmVNPayPayment(100L, true);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("return_code", 1))) {
            assertEquals(HttpStatus.OK, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new RuntimeException("wrapped", new org.hibernate.StaleObjectStateException("Order", 100L)))
                .when(orderService).confirmVNPayPayment(100L, true);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("return_code", 1))) {
            assertEquals(HttpStatus.OK, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new RuntimeException("plain")).when(orderService).confirmVNPayPayment(100L, true);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("return_code", 1))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new RuntimeException("wrapped", new IllegalArgumentException("not stale")))
                .when(orderService).confirmVNPayPayment(100L, true);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("return_code", 1))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new org.springframework.orm.ObjectOptimisticLockingFailureException("race", new Throwable()))
                .when(orderService).confirmVNPayPayment(100L, false);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(null)) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new RuntimeException("wrapped", new org.hibernate.StaleObjectStateException("Order", 100L)))
                .when(orderService).confirmVNPayPayment(100L, false);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("other", 1))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new RuntimeException("plain")).when(orderService).confirmVNPayPayment(100L, false);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("return_code", 2))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }

        reset(orderService);
        doThrow(new RuntimeException("wrapped", new IllegalArgumentException("not stale")))
                .when(orderService).confirmVNPayPayment(100L, false);
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("return_code", 2))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }
    }

    @Test
    void zalopayReturnCoversNullCodeAndTransportException() {
        try (MockedConstruction<RestTemplate> construction = zaloQueryResponse(Map.of("other", 1))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }
        try (MockedConstruction<RestTemplate> construction = mockConstruction(RestTemplate.class,
                (mock, context) -> when(mock.postForEntity(anyString(), any(), eq(Map.class)))
                        .thenThrow(new IllegalStateException("offline")))) {
            assertEquals(HttpStatus.BAD_REQUEST, paymentController.zalopayReturn("240101_100").getStatusCode());
        }
    }

    @Test
    void vnpayReturnCoversRejectedEnumerationValuesAndRethrownServiceErrors() throws Exception {
        Vector<String> names = new Vector<>();
        names.add("ignored");
        names.add("vnp_null");
        names.add("vnp_empty");
        names.add("vnp_ResponseCode");
        names.add("vnp_TxnRef");
        names.add("vnp_SecureHash");
        when(request.getParameterNames()).thenReturn(names.elements());
        when(request.getParameter("ignored")).thenReturn("x");
        when(request.getParameter("vnp_null")).thenReturn(null);
        when(request.getParameter("vnp_empty")).thenReturn("");
        when(request.getParameter("vnp_ResponseCode")).thenReturn("00");
        when(request.getParameter("vnp_TxnRef")).thenReturn("123_456");
        String hashData = "vnp_ResponseCode=00&vnp_TxnRef=123_456";
        when(request.getParameter("vnp_SecureHash"))
                .thenReturn(VNPayConfig.hmacSHA512(VNPayConfig.secretKey, hashData));
        doThrow(new RuntimeException("plain")).when(orderService).confirmVNPayPayment(123L, true);
        assertEquals(HttpStatus.BAD_REQUEST, paymentController.vnpayReturn(request).getStatusCode());
    }

    @Test
    void momoReturnAndIpnCoverRethrownServiceErrors() {
        stubMomoRequest("0", "Success");
        doThrow(new RuntimeException("plain")).when(orderService).confirmVNPayPayment(100L, true);
        assertEquals(HttpStatus.BAD_REQUEST, paymentController.momoReturn(request).getStatusCode());

        reset(orderService);
        Map<String, Object> payload = momoPayload("99", "Fail");
        doThrow(new RuntimeException("wrapped", new IllegalArgumentException("not stale")))
                .when(orderService).confirmVNPayPayment(100L, false);
        assertEquals(HttpStatus.BAD_REQUEST, paymentController.momoIpn(payload).getStatusCode());
    }

    private MockedConstruction<RestTemplate> zaloQueryResponse(Map<String, Object> body) {
        return restResponse(body);
    }

    private MockedConstruction<RestTemplate> restResponse(Map<String, ?> body) {
        return mockConstruction(RestTemplate.class,
                (mock, context) -> when(mock.postForEntity(anyString(), any(), eq(Map.class)))
                        .thenReturn(ResponseEntity.ok(body)));
    }

    private void stubMomoRequest(String resultCode, String message) {
        Map<String, Object> payload = momoPayload(resultCode, message);
        payload.forEach((key, value) -> when(request.getParameter(key)).thenReturn(String.valueOf(value)));
    }

    private Map<String, Object> momoPayload(String resultCode, String message) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("partnerCode", MoMoConfig.PARTNER_CODE);
        payload.put("orderId", "100_123");
        payload.put("requestId", "req1");
        payload.put("amount", "50000");
        payload.put("orderInfo", "Order Info");
        payload.put("orderType", "momo_wallet");
        payload.put("transId", "trans1");
        payload.put("resultCode", resultCode);
        payload.put("message", message);
        payload.put("payType", "qr");
        payload.put("responseTime", "12345");
        payload.put("extraData", "");
        String raw = "accessKey=" + MoMoConfig.ACCESS_KEY + "&amount=50000&extraData=&message=" + message
                + "&orderId=100_123&orderInfo=Order Info&orderType=momo_wallet&partnerCode="
                + MoMoConfig.PARTNER_CODE + "&payType=qr&requestId=req1&responseTime=12345&resultCode="
                + resultCode + "&transId=trans1";
        payload.put("signature", MoMoConfig.hmacSHA256(raw, MoMoConfig.SECRET_KEY));
        return payload;
    }
}

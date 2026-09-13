package com.bookstore.controller;

import com.bookstore.dto.OrderRequest;
import com.bookstore.dto.ReturnRequest;
import com.bookstore.entity.Order;
import com.bookstore.entity.User;
import com.bookstore.service.OrderService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderControllerTest {

    @Mock
    private OrderService orderService;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private OrderController orderController;

    private Order testOrder;
    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder().id(1L).username("testuser").build();
        testOrder = Order.builder().id(100L).user(testUser).build();
    }

    @Test
    void testCreateOrder() {
        OrderRequest request = new OrderRequest();
        when(authentication.getName()).thenReturn("testuser");
        when(orderService.createOrder("testuser", request)).thenReturn(testOrder);

        ResponseEntity<Order> response = orderController.createOrder(authentication, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testOrder, response.getBody());
    }

    @Test
    void testGetMyOrders() {
        when(authentication.getName()).thenReturn("testuser");
        when(orderService.getOrdersByUser("testuser")).thenReturn(List.of(testOrder));

        ResponseEntity<List<Order>> response = orderController.getMyOrders(authentication);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testOrder), response.getBody());
    }

    @Test
    void testGetAllOrders() {
        when(orderService.getAllOrders()).thenReturn(List.of(testOrder));

        ResponseEntity<List<Order>> response = orderController.getAllOrders();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(List.of(testOrder), response.getBody());
    }

    @Test
    void testGetOrderById_Forbidden() {
        when(orderService.getOrderById(100L)).thenReturn(testOrder);
        doReturn(Collections.emptyList()).when(authentication).getAuthorities();
        when(authentication.getName()).thenReturn("otheruser");

        ResponseEntity<Order> response = orderController.getOrderById(authentication, 100L);

        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());

        // Test with null authentication
        ResponseEntity<Order> respNullAuth = orderController.getOrderById(null, 100L);
        assertEquals(HttpStatus.FORBIDDEN, respNullAuth.getStatusCode());

        // Test with order.getUser() == null
        Order orderNoUser = Order.builder().id(200L).user(null).build();
        when(orderService.getOrderById(200L)).thenReturn(orderNoUser);
        ResponseEntity<Order> respNoUser = orderController.getOrderById(authentication, 200L);
        assertEquals(HttpStatus.FORBIDDEN, respNoUser.getStatusCode());
    }

    @Test
    void testGetOrderById_Success_Owner() {
        when(orderService.getOrderById(100L)).thenReturn(testOrder);
        doReturn(Collections.emptyList()).when(authentication).getAuthorities();
        when(authentication.getName()).thenReturn("testuser");

        ResponseEntity<Order> response = orderController.getOrderById(authentication, 100L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testOrder, response.getBody());
    }

    @Test
    void testGetOrderById_Success_Admin() {
        when(orderService.getOrderById(100L)).thenReturn(testOrder);
        doReturn(List.of(new SimpleGrantedAuthority("ROLE_ADMIN"))).when(authentication).getAuthorities();

        ResponseEntity<Order> response = orderController.getOrderById(authentication, 100L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testOrder, response.getBody());
    }

    @Test
    void testUpdateOrderShipping() {
        when(orderService.updateOrderShipping(100L, "DELIVERED", "VNPost", "VN123")).thenReturn(testOrder);

        ResponseEntity<Order> response = orderController.updateOrderShipping(100L, "DELIVERED", "VNPost", "VN123");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testOrder, response.getBody());
    }

    @Test
    void testCancelOrder() {
        when(authentication.getName()).thenReturn("testuser");
        doNothing().when(orderService).userCancelOrder(100L, "testuser");

        ResponseEntity<Void> response = orderController.cancelOrder(authentication, 100L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).userCancelOrder(100L, "testuser");
    }

    @Test
    void testUpdatePaymentMethod() {
        when(authentication.getName()).thenReturn("testuser");
        when(orderService.updatePaymentMethod(100L, "COD", "testuser")).thenReturn(testOrder);

        ResponseEntity<Order> response = orderController.updatePaymentMethod(authentication, 100L, "COD");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(testOrder, response.getBody());
    }

    @Test
    void testReturnOrder() {
        ReturnRequest req = new ReturnRequest();
        when(authentication.getName()).thenReturn("testuser");
        doNothing().when(orderService).userReturnOrder(100L, "testuser", req);

        ResponseEntity<Void> response = orderController.returnOrder(authentication, 100L, req);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).userReturnOrder(100L, "testuser", req);
    }

    @Test
    void testConfirmReceived() {
        when(authentication.getName()).thenReturn("testuser");
        doNothing().when(orderService).confirmOrderReceived(100L, "testuser");

        ResponseEntity<Void> response = orderController.confirmReceived(authentication, 100L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).confirmOrderReceived(100L, "testuser");
    }

    @Test
    void testApproveReturnOrder() {
        doNothing().when(orderService).adminApproveReturn(100L);

        ResponseEntity<Void> response = orderController.approveReturnOrder(100L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).adminApproveReturn(100L);
    }

    @Test
    void testRejectReturnOrder() {
        doNothing().when(orderService).adminRejectReturn(100L);

        ResponseEntity<Void> response = orderController.rejectReturnOrder(100L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(orderService).adminRejectReturn(100L);
    }

    @Test
    void testDeleteOrder() {
        doNothing().when(orderService).deleteOrder(100L);

        ResponseEntity<Void> response = orderController.deleteOrder(100L);

        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
        verify(orderService).deleteOrder(100L);
    }

    @Test
    void testDeleteMultipleOrders() {
        doNothing().when(orderService).deleteMultipleOrders(List.of(1L, 2L));

        ResponseEntity<Void> response = orderController.deleteMultipleOrders(List.of(1L, 2L));

        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
        verify(orderService).deleteMultipleOrders(List.of(1L, 2L));
    }
}
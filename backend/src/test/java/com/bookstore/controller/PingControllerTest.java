package com.bookstore.controller;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PingControllerTest {

    private final PingController pingController = new PingController();

    @Test
    void testPing() {
        ResponseEntity<String> response = pingController.ping();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("pong", response.getBody());
    }
}
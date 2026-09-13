package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class VatInvoiceTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        VatInvoice invoice = new VatInvoice();
        User user = new User();
        user.setId(1L);

        invoice.setId(10L);
        invoice.setUser(user);
        invoice.setType("DOANH_NGHIEP");
        invoice.setCompanyName("Cong Ty TNHH ABC");
        invoice.setCompanyAddress("123 Duong ABC, Quan 1, TP HCM");
        invoice.setTaxCode("0101234567");
        invoice.setEmail("tax@abc.com");

        assertEquals(10L, invoice.getId());
        assertEquals(user, invoice.getUser());
        assertEquals("DOANH_NGHIEP", invoice.getType());
        assertEquals("Cong Ty TNHH ABC", invoice.getCompanyName());
        assertEquals("123 Duong ABC, Quan 1, TP HCM", invoice.getCompanyAddress());
        assertEquals("0101234567", invoice.getTaxCode());
        assertEquals("tax@abc.com", invoice.getEmail());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        VatInvoice invoice = new VatInvoice(
                20L,
                user,
                "CA_NHAN",
                "Nguyen Van A",
                "456 Duong XYZ, Ha Noi",
                "8001234567",
                "personal@example.com"
        );

        assertEquals(20L, invoice.getId());
        assertEquals(user, invoice.getUser());
        assertEquals("CA_NHAN", invoice.getType());
        assertEquals("Nguyen Van A", invoice.getCompanyName());
        assertEquals("456 Duong XYZ, Ha Noi", invoice.getCompanyAddress());
        assertEquals("8001234567", invoice.getTaxCode());
        assertEquals("personal@example.com", invoice.getEmail());
    }

    @Test
    void testBuilder() {
        User user = new User();
        VatInvoice invoice = VatInvoice.builder()
                .id(30L)
                .user(user)
                .type("DOANH_NGHIEP")
                .companyName("Tech Corp")
                .companyAddress("Tech Park")
                .taxCode("0312345678")
                .email("contact@techcorp.com")
                .build();

        assertEquals(30L, invoice.getId());
        assertEquals(user, invoice.getUser());
        assertEquals("DOANH_NGHIEP", invoice.getType());
        assertEquals("Tech Corp", invoice.getCompanyName());
        assertEquals("Tech Park", invoice.getCompanyAddress());
        assertEquals("0312345678", invoice.getTaxCode());
        assertEquals("contact@techcorp.com", invoice.getEmail());
        assertNotNull(invoice.toString());
    }

    @Test
    void testEqualsAndHashCode() {
        VatInvoice v1 = VatInvoice.builder().id(1L).taxCode("0101").build();
        VatInvoice v2 = VatInvoice.builder().id(1L).taxCode("0101").build();
        VatInvoice v3 = VatInvoice.builder().id(2L).taxCode("0202").build();

        assertEquals(v1, v2);
        assertEquals(v1.hashCode(), v2.hashCode());
        assertNotEquals(v1, v3);
        assertNotEquals(v1, null);
        assertNotEquals(v1, new Object());
        assertEquals(v1, v1);
        assertTrue(v1.canEqual(v2));
    }
}

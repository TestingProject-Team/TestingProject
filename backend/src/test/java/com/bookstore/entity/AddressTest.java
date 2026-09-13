package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AddressTest {

    @Test
    void testNoArgsConstructorAndSettersGetters() {
        Address address = new Address();
        User user = new User();
        user.setId(1L);

        address.setId(10L);
        address.setUser(user);
        address.setRecipientName("Nguyen Van A");
        address.setPhone("0123456789");
        address.setStreet("123 Le Loi");
        address.setWard("Ben Nghe");
        address.setDistrict("Quan 1");
        address.setCity("TP Ho Chi Minh");
        address.setDefault(true);

        assertEquals(10L, address.getId());
        assertEquals(user, address.getUser());
        assertEquals("Nguyen Van A", address.getRecipientName());
        assertEquals("0123456789", address.getPhone());
        assertEquals("123 Le Loi", address.getStreet());
        assertEquals("Ben Nghe", address.getWard());
        assertEquals("Quan 1", address.getDistrict());
        assertEquals("TP Ho Chi Minh", address.getCity());
        assertTrue(address.isDefault());
    }

    @Test
    void testAllArgsConstructor() {
        User user = new User();
        user.setId(2L);

        Address address = new Address(
                20L,
                user,
                "Tran Thi B",
                "0987654321",
                "456 Nguyen Hue",
                "Ben Thanh",
                "Quan 1",
                "TP Ho Chi Minh",
                false
        );

        assertEquals(20L, address.getId());
        assertEquals(user, address.getUser());
        assertEquals("Tran Thi B", address.getRecipientName());
        assertEquals("0987654321", address.getPhone());
        assertEquals("456 Nguyen Hue", address.getStreet());
        assertEquals("Ben Thanh", address.getWard());
        assertEquals("Quan 1", address.getDistrict());
        assertEquals("TP Ho Chi Minh", address.getCity());
        assertFalse(address.isDefault());
    }

    @Test
    void testBuilder() {
        User user = new User();
        user.setId(3L);

        Address address = Address.builder()
                .id(30L)
                .user(user)
                .recipientName("Le Van C")
                .phone("0912345678")
                .street("789 Hai Ba Trung")
                .ward("Vo Thi Sau")
                .district("Quan 3")
                .city("TP Ho Chi Minh")
                .isDefault(true)
                .build();

        assertEquals(30L, address.getId());
        assertEquals(user, address.getUser());
        assertEquals("Le Van C", address.getRecipientName());
        assertEquals("0912345678", address.getPhone());
        assertEquals("789 Hai Ba Trung", address.getStreet());
        assertEquals("Vo Thi Sau", address.getWard());
        assertEquals("Quan 3", address.getDistrict());
        assertEquals("TP Ho Chi Minh", address.getCity());
        assertTrue(address.isDefault());
        assertNotNull(address.toString());
    }

    @Test
    void testBuilderDefaults() {
        Address address = Address.builder()
                .recipientName("Test")
                .build();

        assertEquals("", address.getDistrict());
        assertFalse(address.isDefault());
    }

    @Test
    void testEqualsAndHashCode() {
        User user = new User();
        user.setId(1L);

        Address addr1 = Address.builder()
                .id(1L)
                .user(user)
                .recipientName("Name")
                .phone("123")
                .street("Street")
                .ward("Ward")
                .district("District")
                .city("City")
                .isDefault(true)
                .build();

        Address addr2 = Address.builder()
                .id(1L)
                .user(user)
                .recipientName("Name")
                .phone("123")
                .street("Street")
                .ward("Ward")
                .district("District")
                .city("City")
                .isDefault(true)
                .build();

        Address addr3 = Address.builder()
                .id(2L)
                .recipientName("Different")
                .build();

        assertEquals(addr1, addr2);
        assertEquals(addr1.hashCode(), addr2.hashCode());
        assertNotEquals(addr1, addr3);
        assertNotEquals(addr1, null);
        assertNotEquals(addr1, new Object());
        assertEquals(addr1, addr1);
        assertTrue(addr1.canEqual(addr2));
    }
}

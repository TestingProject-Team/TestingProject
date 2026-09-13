package com.bookstore.entity;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SiteSettingTest {

    @Test
    void testSettersAndGetters() {
        SiteSetting setting = new SiteSetting();
        setting.setSettingKey("site_title");
        setting.setSettingValue("YiYi Bookstore");

        assertEquals("site_title", setting.getSettingKey());
        assertEquals("YiYi Bookstore", setting.getSettingValue());
    }

    @Test
    void testEqualsAndHashCode() {
        SiteSetting s1 = new SiteSetting();
        s1.setSettingKey("key1");
        s1.setSettingValue("val1");

        SiteSetting s2 = new SiteSetting();
        s2.setSettingKey("key1");
        s2.setSettingValue("val1");

        SiteSetting s3 = new SiteSetting();
        s3.setSettingKey("key2");
        s3.setSettingValue("val2");

        assertEquals(s1, s2);
        assertEquals(s1.hashCode(), s2.hashCode());
        assertNotEquals(s1, s3);
        assertNotEquals(s1, null);
        assertNotEquals(s1, new Object());
        assertEquals(s1, s1);
        assertTrue(s1.canEqual(s2));
        assertNotNull(s1.toString());
    }
}

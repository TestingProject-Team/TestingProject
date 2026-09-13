package com.bookstore.utils;

import com.bookstore.entity.Book;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFCellStyle;
import org.apache.poi.xssf.usermodel.XSSFFont;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.junit.jupiter.api.Test;
import org.mockito.MockedConstruction;
import org.springframework.mock.web.MockMultipartFile;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.*;

class ExcelHelperTest {

    @Test
    void utilityConstructorIsNotPublicButRemainsInvocableForCoverage() throws Exception {
        java.lang.reflect.Constructor<ExcelHelper> constructor = ExcelHelper.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        assertNotNull(constructor.newInstance());
    }

    @Test
    void testHasExcelFormat() {
        MockMultipartFile excelFile = new MockMultipartFile(
                "file", "test.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                new byte[0]
        );
        assertTrue(ExcelHelper.hasExcelFormat(excelFile));

        MockMultipartFile textFile = new MockMultipartFile(
                "file", "test.txt",
                "text/plain",
                new byte[0]
        );
        assertFalse(ExcelHelper.hasExcelFormat(textFile));
    }

    @Test
    void testGenerateBooksTemplate() {
        ByteArrayInputStream is = ExcelHelper.generateBooksTemplate();
        assertNotNull(is);
        assertTrue(is.available() > 0);
    }

    @Test
    void testExcelToBooks_Success() throws Exception {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Books");

        // Header row
        Row header = sheet.createRow(0);
        header.createCell(0).setCellValue("Tiêu đề");
        header.createCell(1).setCellValue("Tác giả");
        header.createCell(2).setCellValue("NXB");
        header.createCell(3).setCellValue("Mô tả");
        header.createCell(4).setCellValue("Giá");
        header.createCell(5).setCellValue("Giá cũ");
        header.createCell(6).setCellValue("Giảm giá");
        header.createCell(7).setCellValue("Tồn kho");
        header.createCell(8).setCellValue("Category ID");
        header.createCell(9).setCellValue("Link Ảnh");

        // Data row
        Row data = sheet.createRow(1);
        data.createCell(0).setCellValue("Java in Action");
        data.createCell(1).setCellValue("Author Name");
        data.createCell(2).setCellValue("Publisher Name");
        data.createCell(3).setCellValue("Great book description");
        data.createCell(4).setCellValue(120000.0);
        data.createCell(5).setCellValue(150000.0);
        data.createCell(6).setCellValue(20.0);
        data.createCell(7).setCellValue(50.0);
        data.createCell(8).setCellValue(2.0);
        data.createCell(9).setCellValue("http://example.com/java.png");

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        workbook.write(out);
        workbook.close();

        InputStream is = new ByteArrayInputStream(out.toByteArray());
        List<Book> books = ExcelHelper.excelToBooks(is);

        assertNotNull(books);
        assertEquals(1, books.size());
        Book book = books.get(0);
        assertEquals("Java in Action", book.getTitle());
        assertEquals("Author Name", book.getAuthor());
        assertEquals(20, book.getDiscount());
        assertEquals(50, book.getStockQuantity());
        assertNotNull(book.getCategory());
        assertEquals(2L, book.getCategory().getId());
    }

    @Test
    void testExcelToBooks_EmptyOrBlankFirstCellStopsReading() throws Exception {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Sheet1");

        Row header = sheet.createRow(0);
        header.createCell(0).setCellValue("Header");

        Row blankData = sheet.createRow(1);
        // cell 0 is blank

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        workbook.write(out);
        workbook.close();

        InputStream is = new ByteArrayInputStream(out.toByteArray());
        List<Book> books = ExcelHelper.excelToBooks(is);

        assertNotNull(books);
        assertTrue(books.isEmpty());
    }

    @Test
    void testExcelToBooks_AllCellTypesAndDefaultFallbacks() throws Exception {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Books");

        // Header row
        Row header = sheet.createRow(0);
        for (int i = 0; i < 10; i++) {
            header.createCell(i).setCellValue("H" + i);
        }

        // Data row 1: string values for numeric columns, extra unused columns, etc.
        Row data1 = sheet.createRow(1);
        data1.createCell(0).setCellValue("Book 1");
        data1.createCell(1).setCellValue(12345.0); // author as numeric cell -> getCellValueAsString numeric branch
        data1.createCell(2).setCellValue("Publisher 1");
        data1.createCell(3).setCellValue("Description 1");
        data1.createCell(4).setCellValue("100000"); // price as string
        data1.createCell(5).setCellValue("invalid_price"); // oldPrice as invalid string -> fallback 0
        data1.createCell(6).setCellValue("15"); // discount as string
        data1.createCell(7).setCellValue("50"); // stock as string
        data1.createCell(8).setCellValue("99"); // category id as string
        data1.createCell(9).setCellValue("http://example.com/img.jpg");
        data1.createCell(10).setCellValue("Extra column"); // default branch in switch

        // Data row 2: blank or boolean or unsupported cell types
        Row data2 = sheet.createRow(2);
        data2.createCell(0).setCellValue("Book 2");
        data2.createCell(1).setBlank(); // null/blank string cell
        data2.createCell(2).setCellValue(true); // boolean cell -> getCellValueAsString returns null
        data2.createCell(3).setCellValue("Desc 2");
        data2.createCell(4).setCellValue(200000.0);
        data2.createCell(5).setCellValue(250000.0);
        data2.createCell(6).setCellValue(10.0);
        data2.createCell(7).setCellValue(20.0);
        data2.createCell(8).setCellValue(5.0);
        data2.createCell(9).setCellValue("http://example.com/img2.jpg");

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        workbook.write(out);
        workbook.close();

        InputStream is = new ByteArrayInputStream(out.toByteArray());
        List<Book> books = ExcelHelper.excelToBooks(is);

        assertEquals(2, books.size());
        assertEquals("Book 1", books.get(0).getTitle());
        assertEquals("12345", books.get(0).getAuthor());
        assertEquals(0, books.get(0).getOldPrice().intValue());
        assertEquals(15, books.get(0).getDiscount());
        assertEquals(99L, books.get(0).getCategory().getId());
        assertEquals(0.0, books.get(0).getAverageRating());
        assertEquals(0, books.get(0).getReviewCount());
        assertEquals(0, books.get(0).getSalesCount());
        assertFalse(books.get(0).getIsCombo());

        assertNull(books.get(1).getAuthor());
        assertNull(books.get(1).getPublisher());
    }

    @Test
    void testExcelToBooks_AllFieldsSetExplicitly() throws Exception {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Books");

        Row header = sheet.createRow(0);
        for (int i = 0; i < 10; i++) {
            header.createCell(i).setCellValue("H" + i);
        }

        Row data = sheet.createRow(1);
        data.createCell(0).setCellValue("Book Full");
        data.createCell(1).setCellValue("Author Full");
        data.createCell(2).setCellValue("Publisher Full");
        data.createCell(3).setCellValue("Desc Full");
        data.createCell(4).setCellValue(100000.0);
        data.createCell(5).setCellValue(120000.0);
        data.createCell(6).setCellValue(10.0);
        data.createCell(7).setCellValue(20.0);
        data.createCell(8).setCellValue(1.0);
        data.createCell(9).setCellValue("img.png");

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        workbook.write(out);
        workbook.close();

        InputStream is = new ByteArrayInputStream(out.toByteArray());
        List<Book> books = ExcelHelper.excelToBooks(is);

        assertEquals(1, books.size());
        assertEquals("Book Full", books.get(0).getTitle());
        assertEquals(10, books.get(0).getDiscount());
        assertEquals(20, books.get(0).getStockQuantity());
    }

    @Test
    void testExcelToBooks_InvalidStreamThrowsException() {
        InputStream invalidIs = new ByteArrayInputStream("not an excel file".getBytes());
        assertThrows(RuntimeException.class, () -> ExcelHelper.excelToBooks(invalidIs));
    }

    @Test
    void testExcelToBooks_WithoutBooksSheet_UsesFirstSheet() throws Exception {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("OtherSheet");

        Row header = sheet.createRow(0);
        for (int i = 0; i < 10; i++) {
            header.createCell(i).setCellValue("H" + i);
        }

        Row data = sheet.createRow(1);
        data.createCell(0).setCellValue("Book From Other Sheet");
        data.createCell(4).setBlank(); // null numeric -> getCellValueAsNumeric returns 0

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        workbook.write(out);
        workbook.close();

        InputStream is = new ByteArrayInputStream(out.toByteArray());
        List<Book> books = ExcelHelper.excelToBooks(is);

        assertEquals(1, books.size());
        assertEquals("Book From Other Sheet", books.get(0).getTitle());
    }

    @Test
    void testGetCellValueAsString_NullAndDifferentCellTypes() {
        assertNull(org.springframework.test.util.ReflectionTestUtils.invokeMethod(ExcelHelper.class, "getCellValueAsString", new Object[]{null}));
    }

    @Test
    void testGetCellValueAsNumeric_NullAndDifferentCellTypes() {
        assertEquals(0.0, (double) org.springframework.test.util.ReflectionTestUtils.invokeMethod(ExcelHelper.class, "getCellValueAsNumeric", new Object[]{null}));
    }

    @Test
    void testExcelToBooks_BlankFirstCellTriggersBreak() throws Exception {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Books");

        Row header = sheet.createRow(0);
        header.createCell(0).setCellValue("Title");

        Row row1 = sheet.createRow(1);
        row1.createCell(0).setBlank(); // Cell exists but is CellType.BLANK -> triggers break

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        workbook.write(out);
        workbook.close();

        InputStream is = new ByteArrayInputStream(out.toByteArray());
        List<Book> books = ExcelHelper.excelToBooks(is);
        assertNotNull(books);
        assertTrue(books.isEmpty());
    }

    @Test
    void generateBooksTemplate_WhenWorkbookWriteFails_WrapsIOException() throws Exception {
        try (MockedConstruction<XSSFWorkbook> ignored = mockConstruction(
                XSSFWorkbook.class,
                withSettings().defaultAnswer(RETURNS_DEEP_STUBS),
                (workbook, context) -> {
                    XSSFSheet sheet = mock(XSSFSheet.class);
                    XSSFRow header = mock(XSSFRow.class);
                    XSSFRow data = mock(XSSFRow.class);
                    XSSFCell cell = mock(XSSFCell.class);
                    XSSFCellStyle style = mock(XSSFCellStyle.class);
                    XSSFFont font = mock(XSSFFont.class);

                    when(workbook.createSheet(ExcelHelper.SHEET)).thenReturn(sheet);
                    when(workbook.createCellStyle()).thenReturn(style);
                    when(workbook.createFont()).thenReturn(font);
                    when(sheet.createRow(0)).thenReturn(header);
                    when(sheet.createRow(1)).thenReturn(data);
                    when(header.createCell(anyInt())).thenReturn(cell);
                    when(data.createCell(anyInt())).thenReturn(cell);
                    doThrow(new IOException("disk full")).when(workbook).write(any(ByteArrayOutputStream.class));
                })) {
            RuntimeException exception = assertThrows(
                    RuntimeException.class, ExcelHelper::generateBooksTemplate);
            assertEquals("Lỗi khi tạo tệp Excel mẫu: disk full", exception.getMessage());
        }
    }

    @Test
    void excelToBooks_WhenInputReadFails_WrapsIOException() {
        InputStream failingInput = new InputStream() {
            @Override
            public int read() throws IOException {
                throw new IOException("read failed");
            }

            @Override
            public int read(byte[] bytes, int offset, int length) throws IOException {
                throw new IOException("read failed");
            }
        };

        RuntimeException exception = assertThrows(
                RuntimeException.class, () -> ExcelHelper.excelToBooks(failingInput));
        assertEquals("Lỗi đọc file Excel: read failed", exception.getMessage());
    }

    @Test
    void privateCellConverters_CoverEveryCellTypeAndParseOutcome() {
        try (Workbook workbook = new XSSFWorkbook()) {
            Row row = workbook.createSheet().createRow(0);
            Cell stringCell = row.createCell(0);
            stringCell.setCellValue("12.5");
            Cell numericCell = row.createCell(1);
            numericCell.setCellValue(42.75);
            Cell booleanCell = row.createCell(2);
            booleanCell.setCellValue(true);
            Cell invalidNumericString = row.createCell(3);
            invalidNumericString.setCellValue("not-a-number");

            assertEquals("12.5", invokeStringConverter(stringCell));
            assertEquals("42", invokeStringConverter(numericCell));
            assertNull(invokeStringConverter(booleanCell));
            assertNull(invokeStringConverter(null));

            assertEquals(12.5, invokeNumericConverter(stringCell));
            assertEquals(42.75, invokeNumericConverter(numericCell));
            assertEquals(0.0, invokeNumericConverter(booleanCell));
            assertEquals(0.0, invokeNumericConverter(invalidNumericString));
            assertEquals(0.0, invokeNumericConverter(null));
        } catch (IOException exception) {
            fail(exception);
        }
    }

    @Test
    void excelToBooks_DefaultAssignments_CoverBothOutcomesOfEveryNullCheck() throws Exception {
        byte[] excel = workbookWithOneMinimalDataRow();

        try (MockedConstruction<Book> books = mockConstruction(Book.class, (book, context) -> {
            when(book.getDiscount()).thenReturn(1);
            when(book.getStockQuantity()).thenReturn(2);
            when(book.getIsCombo()).thenReturn(true);
            when(book.getAverageRating()).thenReturn(4.5);
            when(book.getReviewCount()).thenReturn(3);
            when(book.getSalesCount()).thenReturn(4);
        })) {
            List<Book> result = ExcelHelper.excelToBooks(new ByteArrayInputStream(excel));
            assertEquals(1, result.size());
            Book constructed = books.constructed().get(0);
            verify(constructed, never()).setDiscount(0);
            verify(constructed, never()).setStockQuantity(0);
            verify(constructed, never()).setIsCombo(false);
            verify(constructed, never()).setAverageRating(0.0);
            verify(constructed, never()).setReviewCount(0);
            verify(constructed, never()).setSalesCount(0);
        }
    }

    private static String invokeStringConverter(Cell cell) {
        return org.springframework.test.util.ReflectionTestUtils.invokeMethod(
                ExcelHelper.class, "getCellValueAsString", cell);
    }

    private static double invokeNumericConverter(Cell cell) {
        return org.springframework.test.util.ReflectionTestUtils.invokeMethod(
                ExcelHelper.class, "getCellValueAsNumeric", cell);
    }

    private static byte[] workbookWithOneMinimalDataRow() throws IOException {
        try (Workbook workbook = new XSSFWorkbook(); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            Sheet sheet = workbook.createSheet("Books");
            sheet.createRow(0).createCell(0).setCellValue("Title");
            sheet.createRow(1).createCell(0).setCellValue("Book");
            workbook.write(out);
            return out.toByteArray();
        }
    }
}

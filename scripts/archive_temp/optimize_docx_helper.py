import zipfile
import io
import os
from PIL import Image
import xml.etree.ElementTree as ET
import docx

def optimize_docx(input_path, output_path):
    print(f"Starting optimization for: {input_path}")
    with zipfile.ZipFile(input_path, 'r') as zin, zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            # 1. Loại bỏ các font chữ nhúng dư thừa (Calibri, Cambria, Noto Sans) gây lag máy khi mở Word
            if item.filename.startswith('word/fonts/'):
                continue
            
            # 2. Loại bỏ thumbnail EMF dung lượng lớn (2.4MB)
            if item.filename == 'docProps/thumbnail.emf':
                continue
            
            # 3. Cập nhật _rels/.rels (gỡ bỏ relationship tới thumbnail)
            if item.filename == '_rels/.rels':
                content = zin.read(item.filename).decode('utf-8')
                root = ET.fromstring(content)
                for child in list(root):
                    if 'thumbnail' in child.attrib.get('Type', '').lower() or 'thumbnail' in child.attrib.get('Target', '').lower():
                        root.remove(child)
                new_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)
                zout.writestr(item.filename, new_xml)
                continue

            # 4. Tối ưu ảnh nhưng vẫn giữ định dạng PNG chất lượng cao, sắc nét (chuẩn in ấn 300 DPI)
            if item.filename.startswith('word/media/'):
                data = zin.read(item.filename)
                try:
                    img = Image.open(io.BytesIO(data))
                    w, h = img.size
                    # Giới hạn chiều rộng tối đa 1400px (đầy đủ chi tiết cho văn bản A4 chiều ngang 6 inch)
                    if w > 1400:
                        new_w = 1400
                        new_h = int(h * (1400 / w))
                        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                    # Nếu ảnh RGBA nhưng thực tế không có pixel trong suốt, chuyển sang RGB để giảm 25% bộ nhớ render
                    if img.mode == 'RGBA':
                        extrema = img.getextrema()
                        if not (len(extrema) == 4 and extrema[3][0] < 255):
                            img = img.convert('RGB')
                    
                    buf = io.BytesIO()
                    img.save(buf, format='PNG', optimize=True, compress_level=9)
                    zout.writestr(item.filename, buf.getvalue())
                    continue
                except Exception as e:
                    print(f"Could not process {item.filename}: {e}")
                    zout.writestr(item.filename, data)
                    continue
            
            # 5. Cập nhật fontTable.xml (gỡ bỏ các khai báo embed font)
            if item.filename == 'word/fontTable.xml':
                content = zin.read(item.filename)
                root = ET.fromstring(content)
                for font in root:
                    for child in list(font):
                        if 'embed' in child.tag.lower():
                            font.remove(child)
                new_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)
                zout.writestr(item.filename, new_xml)
                continue
                
            # 6. Cập nhật fontTable.xml.rels (làm rỗng relationship fonts)
            if item.filename == 'word/_rels/fontTable.xml.rels':
                empty_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'
                zout.writestr(item.filename, empty_rels.encode('utf-8'))
                continue

            # 7. Xử lý settings.xml (tắt embedTrueTypeFonts, savePreviewPicture)
            if item.filename == 'word/settings.xml':
                content = zin.read(item.filename).decode('utf-8')
                content = content.replace('<w:embedTrueTypeFonts/>', '')
                content = content.replace('<w:savePreviewPicture/>', '')
                zout.writestr(item.filename, content.encode('utf-8'))
                continue

            # 8. Cập nhật [Content_Types].xml
            if item.filename == '[Content_Types].xml':
                content = zin.read(item.filename).decode('utf-8')
                content = content.replace('<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/>', '')
                content = content.replace('<Default Extension="emf" ContentType="image/x-emf"/>', '')
                zout.writestr(item.filename, content.encode('utf-8'))
                continue

            # Các file khác giữ nguyên
            zout.writestr(item, zin.read(item.filename))

    orig_size = os.path.getsize(input_path)
    new_size = os.path.getsize(output_path)
    print(f"Original: {orig_size / (1024*1024):.2f} MB")
    print(f"Optimized: {new_size / (1024*1024):.2f} MB")
    print(f"Reduced by: {(1 - new_size/orig_size)*100:.1f}%")

if __name__ == '__main__':
    targets = [
        r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full_REVIEWED.docx',
        r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full.docx',
        r'E:\TestingProject\docs yiyi\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full.docx'
    ]
    
    for doc_path in targets:
        temp_path = doc_path + '.tmp'
        optimize_docx(doc_path, temp_path)
        
        # Kiểm tra tính toàn vẹn với python-docx trước khi ghi đè
        doc = docx.Document(temp_path)
        print(f"Validation successful for {os.path.basename(doc_path)}! Paragraphs: {len(doc.paragraphs)}, Tables: {len(doc.tables)}")
        
        os.replace(temp_path, doc_path)
        print(f"Replaced {doc_path} with optimized version.\n")

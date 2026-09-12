import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

# 1. Fix P398 "Hãy"
p398 = doc.paragraphs[398]
if 'Hãy xác nhận' in p398.text:
    p398.text = p398.text.replace('Hãy xác nhận provider và topology thực tế trước khi hoàn thiện diagram triển khai.', 'Cấu hình provider và topology thực tế cần được đối chiếu trước khi hoàn thiện diagram triển khai chính thức.')

# 2. Fix P817: Port 8080 -> 8081
p817 = doc.paragraphs[817]
if 'cổng 8080' in p817.text:
    p817.text = p817.text.replace('cổng 8080', 'cổng 8081 [CẦN XÁC MINH PORT TỪ application.properties]')

doc.save(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')
print("Successfully modified without printing unicode strings.")

import docx

doc = docx.Document(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')

for idx, p in enumerate(doc.paragraphs):
    if 'Hãy' in p.text:
        print(f"P{idx} has 'Hãy':")
        # replace any occurrences of 'hãy' or 'Hãy'
        p.text = p.text.replace('Hãy ', '').replace('hãy ', '')

doc.save(r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Tieng_Viet_Refined_Full(1).docx')
print("Replaced all 'Hãy'.")

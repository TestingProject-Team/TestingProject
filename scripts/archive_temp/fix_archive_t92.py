import docx

doc_path = r'E:\TestingProject\YiYi_Book_Capstone_Project_Report_Content_Final.docx'
doc = docx.Document(doc_path)

# Table 92: check row 1 cell 2
t92 = doc.tables[92]
for row in t92.rows:
    for cell in row.cells:
        if 'Archive / repository' in cell.text:
            cell.text = cell.text.replace('Archive / repository', 'Mã nguồn / Git Repository')

doc.save(doc_path)
print("Table 92 archive replaced successfully.")

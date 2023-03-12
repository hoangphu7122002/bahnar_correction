import docx

doc = docx.Document('Pages from Diong Sen Gren 1-150.pdf.docx')
all_paras = doc.paragraphs

mydoc = docx.Document()
lines = []
for para in all_paras:
    lines.append(para.text)
    
    
    
# with open('a.docx', 'w', encoding='utf-8') as f:
#     f.writelines(lines) 

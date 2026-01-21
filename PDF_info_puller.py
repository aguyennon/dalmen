# Tester file for PDFs

import pdfplumber

# Enter whatever path to check any PDF
pdf_path = "G:/Alexis/QUINCAILERIE LION/CONFIRMATION/Dalmen3029.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"\n{'='*60}")
        print(f"PAGE {i+1}")
        print('='*60)
        print(text)









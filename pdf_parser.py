import fitz  # PyMuPDF
import re
import logging

def extrair_texto_do_pdf(pdf_content):
    try:
        
        pdf_document = fitz.open("pdf", pdf_content)
        num_pages = pdf_document.page_count

        
        text_content = ""
        for page_number in range(num_pages):
            page = pdf_document[page_number]
            text_content += page.get_text()

        
        text_content = ''.join(char for char in text_content if char.isprintable() or char.isspace())

        
        return text_content, {'num_pages': num_pages}

    except Exception as e:
        
        logging.error(f"Erro durante a extração do PDF: {str(e)}")
        return "", {'num_pages': 0}  

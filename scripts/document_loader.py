import PyPDF2

def load_documents(file_1, file_2):
    """
    Loads two PDF documents and returns a dictionary with page numbers as keys and page text as values.
    """
    def extract_text_by_page(file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page_texts = {}
            for i, page in enumerate(pdf_reader.pages):
                page_texts[f"Page {i + 1}"] = page.extract_text()
        return page_texts

    doc1_pages = extract_text_by_page(file_1)
    doc2_pages = extract_text_by_page(file_2)
    
    return doc1_pages, doc2_pages

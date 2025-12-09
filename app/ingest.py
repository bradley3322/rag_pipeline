from pypdf import PdfReader
import re

def load_raw_pdf_data():
    reader = PdfReader("../data/raw_docs/test_two.pdf")

    for page in range(len(reader.pages)):
        currentPage = reader.pages[page]
        print(currentPage.extract_text())
        print("----- cleaned text -----")
        cleanedText = clean_text(currentPage.extract_text())
        print(cleanedText)
        print("----- chunked text -----")
        chunkedText = chunk_text(cleanedText)
        print(chunkedText)



def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-\'\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text):
    return re.split(r'(?<=[.!?]) +', text)

    

load_raw_pdf_data()

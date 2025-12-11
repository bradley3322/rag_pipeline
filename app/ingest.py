from pypdf import PdfReader
import re
import uuid

MAX_CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_raw_pdf_data():
    reader = PdfReader("../data/raw_docs/test_two.pdf")
    return reader.pages

def clean_text(page):
    text = page.lower()
    text = text.replace('\xa0', ' ')
    text = re.sub(r'[^a-z0-9\s\-\'\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(sentence):
    sentences_to_process = split_into_sentences(sentence)
    final_chunks = []
    current_chunk = ""

    for current_sentence in sentences_to_process:
        if len(current_chunk) + len(current_sentence) + 1 > MAX_CHUNK_SIZE:
            final_chunks.append(current_chunk.strip())
            current_chunk = current_chunk[-CHUNK_OVERLAP:].strip() + " " + current_sentence
        else:
            if current_chunk:
                current_chunk += " " + current_sentence
            else: 
                current_chunk = current_sentence

    if current_chunk:
        final_chunks.append(current_chunk.strip())
    return final_chunks

def split_into_sentences(text):
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    return sentences

def build_chunks():
    raw_document_text = ""
    cleaned_document_text = ""
    chunked_document_text_list = ""
    dict_chunk_list = []

    loaded_pages = load_raw_pdf_data()
    for page in loaded_pages:
        raw_document_text += page.extract_text() + " "


    cleaned_document_text = clean_text(raw_document_text)
    chunked_document_text_list = chunk_text(cleaned_document_text)
    
    for chunk in chunked_document_text_list:
        print(chunk)
        dict_chunk_list.append(dict(id = uuid.uuid4(), text = chunk, metadata = {}))

    # print(dict_chunk_list)    

    return ""

def index_chunks():
    return ""

    

build_chunks()

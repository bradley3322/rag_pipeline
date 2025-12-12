
import logging
from datetime import datetime
from pypdf import PdfReader
import re
import uuid

from app.embeddings import get_embeddings
from app.vectorstore import add_chunks_to_db


MAX_CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
DOCUMENT_NAME = "test_one"
DOCUMENT_PATH = "data/raw_docs/test_one.pdf"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_raw_pdf_data():
    logging.info(f"Loading PDF data from {DOCUMENT_PATH}")
    reader = PdfReader(DOCUMENT_PATH)
    logging.info(f"Loaded {len(reader.pages)} pages from PDF.")
    return reader.pages

def clean_text(page):
    logging.info("Cleaning text.")
    text = page.lower()
    text = text.replace('\xa0', ' ')
    text = re.sub(r'[^a-z0-9\s\-\'\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    cleaned = text.strip()
    logging.info(f"Cleaned text length: {len(cleaned)}")
    return cleaned

def chunk_text(sentence):
    logging.info("Chunking text.")
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
    logging.info(f"Chunked into {len(final_chunks)} chunks.")
    return final_chunks

def split_into_sentences(text):
    logging.info("Splitting text into sentences.")
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    logging.info(f"Split into {len(sentences)} sentences.")
    return sentences

def build_chunks():
    logging.info("Building chunks from document.")
    raw_document_text = ""
    cleaned_document_text = ""
    chunked_document_text_list = ""
    dict_chunk_list = []

    loaded_pages = load_raw_pdf_data()
    logging.info(f"Processing {len(loaded_pages)} pages.")
    for pn, page in enumerate(loaded_pages):
        raw_text = page.extract_text()
        logging.info(f"Extracted text from page {pn}, length: {len(raw_text) if raw_text else 0}")
        raw_document_text += raw_text + " "

    cleaned_document_text = clean_text(raw_document_text)
    chunked_document_text_list = chunk_text(cleaned_document_text)

    for i, chunk in enumerate(chunked_document_text_list):
        dict_chunk_list.append(dict(id=str(uuid.uuid4()), text=chunk, metadata={'source_file': DOCUMENT_NAME, 'date_issued': str(datetime.now()), 'page_number': str(pn), 'chunk_index': str(i)}))

    logging.info(f"Built {len(dict_chunk_list)} chunk dictionaries.")
    return dict_chunk_list

def index_chunks():
    logging.info("Indexing chunks.")
    id_list = []
    documents_list = []
    metadata_list = []
    embeddings_list = []

    dict_chunk_list = build_chunks()

    for chunk in dict_chunk_list:
        id_list.append(chunk['id'])
        documents_list.append(chunk['text'])
        metadata_list.append(chunk['metadata'])
        logging.info(f"Getting embedding for chunk id {chunk['id']} (length: {len(chunk['text'])})")
        embeddings_list.append(get_embeddings(chunk['text']))
    logging.info(f"Generated embeddings for {len(embeddings_list)} chunks.")
    
    add_chunks_to_db(id_list, documents_list, metadata_list, embeddings_list)

    return ""

    

index_chunks()

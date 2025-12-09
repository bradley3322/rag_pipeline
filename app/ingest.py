from pypdf import PdfReader
import re

MAX_CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_raw_pdf_data():
    reader = PdfReader("../data/raw_docs/test_two.pdf")

    for page in range(len(reader.pages)):
        current_page = reader.pages[page]
        # print(current_page.extract_text())
        print("----- cleaned text -----")
        cleaned_text = clean_text(current_page.extract_text())
        # print(cleaned_text)
        print("----- chunked text -----")
        chunked_text = chunk_text(cleaned_text)
        print(chunked_text)

def clean_text(text):
    # add compiling the regex patterns for efficiency
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-\'\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text):
    sentences_to_process = split_into_sentences(text)
    final_chunks = []
    current_chunk = ""

    for current_sentence in sentences_to_process:
        if len(current_chunk) + len(current_sentence) > MAX_CHUNK_SIZE:
            final_chunks.append(current_chunk)
            current_chunk = current_chunk[-CHUNK_OVERLAP:] + " " + current_sentence
            print('current_chunk: ', len(current_chunk))
        else:
            current_chunk += " " + current_sentence

    if current_chunk:
        final_chunks.append(current_chunk.strip())
    print(len(final_chunks))
    return final_chunks

def split_into_sentences(text):
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    return sentences
    

load_raw_pdf_data()

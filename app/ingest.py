import logging
from datetime import datetime
from typing import List, Dict, Any
from pypdf import PdfReader
import re

from app.embeddings import get_embeddings
from app.vectorstore import add_chunks_to_db, query_texts_from_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFIngestor:
    def __init__(self, document_path: str, document_name: str, max_chunk_size: int = 1000, chunk_overlap: int = 50):
        self.document_path = document_path
        self.document_name = document_name
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap

    def load_raw_pdf_data(self) -> List[Any]:
        try:
            logging.info(f"Loading PDF data from {self.document_path}")
            reader = PdfReader(self.document_path)
            logging.info(f"Loaded {len(reader.pages)} pages from PDF.")
            return reader.pages
        except Exception as e:
            logging.error(f"Failed to load PDF: {e}")
            raise

    @staticmethod
    def clean_text(text: str) -> str:
        logging.info("Cleaning text.")
        if not isinstance(text, str):
            logging.error("Input to clean_text must be a string.")
            raise ValueError("Input to clean_text must be a string.")
        text = text.lower()
        text = text.replace('\xa0', ' ')
        text = re.sub(r'[^a-z0-9\s\-\'\.]', ' ', text)
        text = re.sub(r'[ \t\r\f\v]+', ' ', text)
        cleaned = text.strip()
        logging.info(f"Cleaned text length: {len(cleaned)}")
        return cleaned

    def recursive_chunk(self, text: str) -> List[str]:
        paragraphs = re.split(r'\n{2,}', text)
        final_chunks = []
        for para in paragraphs:
            if len(para) <= self.max_chunk_size:
                final_chunks.append(para.strip())
            else:
                lines = re.split(r'\n', para)
                current = ""
                for line in lines:
                    if len(current) + len(line) + 1 > self.max_chunk_size:
                        if current:
                            final_chunks.append(current.strip())
                        current = line
                    else:
                        if current:
                            current += "\n" + line
                        else:
                            current = line
                if current:
                    final_chunks.append(current.strip())
        return [chunk for chunk in final_chunks if chunk]

    def build_chunks(self) -> List[Dict[str, Any]]:
        try:
            logging.info("Building chunks from document.")
            raw_document_text = ""
            dict_chunk_list = []
            loaded_pages = self.load_raw_pdf_data()
            logging.info(f"Processing {len(loaded_pages)} pages.")
            for pn, page in enumerate(loaded_pages):
                try:
                    raw_text = page.extract_text()
                except Exception as e:
                    logging.warning(f"Failed to extract text from page {pn}: {e}")
                    raw_text = ""
                logging.info(f"Extracted text from page {pn}, length: {len(raw_text) if raw_text else 0}")
                raw_document_text += (raw_text or "") + " "

            cleaned_document_text = self.clean_text(raw_document_text)
            chunked_document_text_list = self.recursive_chunk(cleaned_document_text)

            for i, chunk in enumerate(chunked_document_text_list):
                dict_chunk_list.append({
                    'id': f"{self.document_name}_{i}",
                    'text': chunk,
                    'metadata': {
                        'source_file': self.document_name,
                        'date_issued': str(datetime.now()),
                        'chunk_index': str(i)
                    }
                })
            logging.info(f"Built {len(dict_chunk_list)} chunk dictionaries.")
            return dict_chunk_list
        except Exception as e:
            logging.error(f"Failed to build chunks: {e}")
            raise

    def index_chunks(self) -> None:
        try:
            logging.info("Indexing chunks.")
            id_list: List[str] = []
            documents_list: List[str] = []
            metadata_list: List[Dict[str, Any]] = []
            embeddings_list: List[Any] = []
            dict_chunk_list = self.build_chunks()
            logging.info(f"Generated {len(dict_chunk_list)} chunks to index.")
            # print(dict_chunk_list)  # Remove or comment out for production

            for chunk in dict_chunk_list:
                id_list.append(chunk['id'])
                documents_list.append(chunk['text'])
                metadata_list.append(chunk['metadata'])
                logging.info(f"Getting embedding for chunk id {chunk['id']} (length: {len(chunk['text'])})")
                try:
                    embeddings_list.append(get_embeddings(chunk['text']))
                except Exception as e:
                    logging.error(f"Failed to get embedding for chunk {chunk['id']}: {e}")
                    embeddings_list.append([])
            logging.info(f"Generated embeddings for {len(embeddings_list)} chunks.")
            add_chunks_to_db(id_list, documents_list, metadata_list, embeddings_list)
            # TODO: currently testing query right after indexing, will move to separate call when API is set up
            response = query_texts_from_db("what if you had a complaint about your leadership?", n_results=5)
            logging.info(f"Query response: {str(response)}")
        except Exception as e:
            logging.error(f"Failed to index chunks: {e}")
            raise


if __name__ == "__main__":
    # Configurable parameters
    DOCUMENT_NAME = "test_one"
    DOCUMENT_PATH = "data/raw_docs/test_one.pdf"
    MAX_CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 50

    ingestor = PDFIngestor(
        document_path=DOCUMENT_PATH,
        document_name=DOCUMENT_NAME,
        max_chunk_size=MAX_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    ingestor.index_chunks()


import logging
from sentence_transformers import SentenceTransformer

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model = SentenceTransformer('all-MiniLM-L6-v2')
logging.info("SentenceTransformer model loaded.")

def get_embeddings(data):
    logging.info(f"Encoding data of type {type(data)} and length {len(data) if hasattr(data, '__len__') else 'N/A'}.")
    embeddings = model.encode(data)
    logging.info(f"Generated embeddings of type {type(embeddings)}.")
    return embeddings

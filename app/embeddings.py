
import logging
from typing import Any, List, Union, Optional
from sentence_transformers import SentenceTransformer

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Embeddings:
    _model_name: str = 'all-MiniLM-L6-v2'
    _model: Optional[SentenceTransformer] = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            try:
                cls._model = SentenceTransformer(cls._model_name)
                logging.info(f"SentenceTransformer model '{cls._model_name}' loaded.")
            except Exception as e:
                logging.error(f"Failed to load SentenceTransformer model: {e}")
                raise
        return cls._model

    @classmethod
    def get_embeddings(cls, data: Union[str, List[str]]) -> Any:
        if not isinstance(data, (str, list)):
            logging.error(f"Input data must be a string or list of strings, got {type(data)}.")
            raise ValueError("Input data must be a string or list of strings.")
        try:
            model = cls.get_model()
            logging.info(f"Encoding data of type {type(data)} and length {len(data) if hasattr(data, '__len__') else 'N/A'}.")
            embeddings = model.encode(data)
            logging.info(f"Generated embeddings of type {type(embeddings)}.")
            return embeddings
        except Exception as e:
            logging.error(f"Failed to generate embeddings: {e}")
            raise

# Convenience function for backward compatibility
def get_embeddings(data: Union[str, List[str]]) -> Any:
    return Embeddings.get_embeddings(data)

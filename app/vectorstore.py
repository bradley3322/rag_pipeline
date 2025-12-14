import chromadb
import logging
from typing import List, Dict, Any, Optional

class VectorStore:
    _client: Optional[chromadb.PersistentClient] = None
    _collection: Optional[Any] = None
    _collection_name: str = "test_collection" # TODO: Make this configurable

    @classmethod
    def _get_client(cls) -> chromadb.PersistentClient:
        if cls._client is None:
            try:
                cls._client = chromadb.PersistentClient(path="./chroma" )
                logging.info("ChromaDB client initialized.")
            except Exception as e:
                logging.error(f"Failed to initialize ChromaDB client: {e}")
                raise
        return cls._client

    @classmethod
    def get_collection(cls) -> Any:
        if cls._collection is None:
            try:
                client = cls._get_client()
                cls._collection = client.get_or_create_collection(name=cls._collection_name)
                logging.info(f"ChromaDB collection '{cls._collection_name}' initialized.")
            except Exception as e:
                logging.error(f"Failed to get or create collection: {e}")
                raise
        return cls._collection

    @classmethod
    def add_chunks_to_db(
        cls,
        id_list: List[str],
        documents_list: List[str],
        metadata_list: List[Dict[str, Any]],
        embeddings_list: List[Any]
    ) -> None:
        if not (id_list and documents_list and metadata_list and embeddings_list):
            logging.error("Input lists must not be empty.")
            raise ValueError("All input lists must be non-empty.")
        if not (len(id_list) == len(documents_list) == len(metadata_list) == len(embeddings_list)):
            logging.error("Input lists must be of equal length.")
            raise ValueError("All input lists must be of equal length.")
        try:
            collection = cls.get_collection()
            collection.upsert(
                ids=id_list,
                documents=documents_list,
                metadatas=metadata_list,
                embeddings=embeddings_list
            )
            logging.info(f"Added {len(id_list)} chunks to ChromaDB.")
        except Exception as e:
            logging.error(f"Failed to add chunks to DB: {e}")
            raise

    @classmethod
    def delete_collection(cls, collection_name: Optional[str] = None) -> None:
        name = collection_name or cls._collection_name
        try:
            client = cls._get_client()
            client.delete_collection(name=name)
            logging.info(f"Deleted collection: {name}")
            if name == cls._collection_name:
                cls._collection = None
        except Exception as e:
            logging.error(f"Failed to delete collection '{name}': {e}")
            raise

    @classmethod
    def delete_collection_data(cls) -> None:
        try:
            collection = cls.get_collection()
            collection.delete(ids=[], where={})
            logging.info(f"Deleted all data in collection '{cls._collection_name}'.")
        except Exception as e:
            logging.error(f"Failed to delete collection data: {e}")
            raise

    @classmethod
    def query_texts_from_db(cls, query_text: str, n_results: int = 1) -> Dict[str, Any]:
        if not query_text:
            logging.error("Query text must not be empty.")
            raise ValueError("Query text must not be empty.")
        try:
            collection = cls.get_collection()
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            logging.info(f"Retrieved {len(results['ids'][0]) if results and 'ids' in results and results['ids'] else 0} results from query.")
            return results
        except Exception as e:
            logging.error(f"Failed to query texts from DB: {e}")
            raise

    @classmethod
    def id_exists(cls, id_value: str) -> bool:
        try:
            collection = cls.get_collection()
            result = collection.get(ids=[id_value])
            exists = bool(result and result.get('ids') and id_value in result['ids'])
            logging.info(f"ID '{id_value}' exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Failed to check if ID exists: {e}")
            raise

# Convenience functions for backward compatibility
def add_chunks_to_db(id_list: List[str], documents_list: List[str], metadata_list: List[Dict[str, Any]], embeddings_list: List[Any]) -> None:
    VectorStore.add_chunks_to_db(id_list, documents_list, metadata_list, embeddings_list)

def delete_collection(collection_name: Optional[str] = None) -> None:
    VectorStore.delete_collection(collection_name)

def delete_collection_data() -> None:
    VectorStore.delete_collection_data()

def query_texts_from_db(query_text: str, n_results: int = 1) -> Dict[str, Any]:
    return VectorStore.query_texts_from_db(query_text, n_results)

def id_exists(id_value: str) -> bool:
    return VectorStore.id_exists(id_value)

import chromadb
chroma_client = chromadb.chromadb.PersistentClient()
import logging

def add_chunks_to_db(id_list, documents_list, metadata_list, embeddings_list):
    logging.info("Adding chunks to ChromaDB.")
    collection = chroma_client.get_or_create_collection(name="test_collection")
    collection.add(
        ids=id_list,
        documents=documents_list,
        metadatas=metadata_list,
        embeddings=embeddings_list)
    print(collection.peek())

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
    print(documents_list)
    
def delete_all_db_data():
    logging.info("deleting all db data.")
    collection = chroma_client.get_or_create_collection(name="test_collection")
    collection.delete(where={'source_file': 'test_one'})
    
def query_texts_from_db(query_texts, n_results=1):
    logging.info("Querying texts from ChromaDB: " + query_texts)
    collection = chroma_client.get_or_create_collection(name="test_collection")
    results = collection.query(
        query_texts=[query_texts],
        n_results=n_results
    )
    logging.info(f"Retrieved {len(results['ids'][0])} results from query.")
    return results

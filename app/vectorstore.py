import chromadb
import logging
chroma_client = chromadb.chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection(name="test_collection")


def add_chunks_to_db(id_list, documents_list, metadata_list, embeddings_list):
    logging.info("Adding chunks to ChromaDB.")
    collection.upsert(
        ids=id_list,
        documents=documents_list,
        metadatas=metadata_list,
        embeddings=embeddings_list)
    print(documents_list)
        
def delete_collection(collection_name):
    logging.info("deleting collection: " + collection_name)
    chroma_client.delete_collection(name=collection_name)

# TODO: Implement proper deletion of all data in the DB with POST FastAPI endpoint
def delete_collection_data():
    collection.delete(
        ids=[],
        where={},
        )

    
def query_texts_from_db(query_text, n_results=1):
    logging.info("Querying texts from ChromaDB: " + query_text)
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    logging.info(f"Retrieved {len(results['ids'][0])} results from query.")
    return results

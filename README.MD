# RAG Pipeline Project

This project implements a Retrieval-Augmented Generation (RAG) pipeline using FastAPI, ChromaDB, and Ollama for local LLM inference. It allows you to ingest PDF documents, store and query them using vector search, and generate answers to user queries using a local LLM.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Ollama LLM Setup](#2-ollama-llm-setup)
  - [3. Data Preparation](#3-data-preparation)
  - [4. Ingesting Documents](#4-ingesting-documents)
  - [5. Running the API](#5-running-the-api)
- [API Usage](#api-usage)
- [Notes](#notes)

---

## Features

- **PDF Ingestion:** Extracts and chunks text from PDF files.
- **Vector Store:** Stores document chunks and metadata in ChromaDB for similarity search.
- **API:** FastAPI endpoints for querying the vector store and health checks.
- **RAG with Ollama:** Uses retrieved context to generate answers from a local LLM via Ollama.

---

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── api.py           # FastAPI app and endpoints
│   ├── config.py        # (Configurable settings)
│   ├── embeddings.py    # Embedding generation logic
│   ├── ingest.py        # PDF ingestion and chunking
│   ├── schemas.py       # Pydantic schemas
│   ├── vectorstore.py   # ChromaDB vector store logic
│   ├── ollama.py        # Ollama LLM prompt/response
├── chroma/              # ChromaDB persistent storage
├── data/
│   └── raw_docs/        # Place your PDF files here
├── notebooks/
│   └── 01_explore_docs.ipynb
├── README.MD
```

---

## Setup Instructions

### 1. Environment Setup

- Python 3.11+
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Install [ChromaDB](https://docs.trychroma.com/) and [Ollama](https://ollama.com/):

```bash
pip install chromadb pypdf fastapi uvicorn requests
```

- (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Ollama LLM Setup

- [Install Ollama](https://ollama.com/download) and start the Ollama server locally:

```bash
ollama serve
```

- Pull the required model (e.g., llama3:8b):

```bash
ollama pull llama3:8b
```

- The API expects Ollama to be running at `http://localhost:11434`.

### 3. Data Preparation

- Place your PDF files in the `data/raw_docs/` directory.

### 4. Ingesting Documents

- Run the ingestion script to process and index your PDFs:

```bash
python -m app.ingest
```

- This will extract, chunk, embed, and store your documents in ChromaDB.

### 5. Running the API

- Start the FastAPI server:

```bash
uvicorn app.api:app --reload
```

- The API will be available at `http://localhost:8000/api/`

---

## API Usage

### Query Endpoint

- **POST** `/api/query/`
- **Body:**

```json
{
  "query": "your question here",
  "n_results": 5
}
```

- **Response:**

```json
"Yet to be confirmed"
```

### Health Check

- **GET** `/api/health/`

---

## Notes

- The vector store uses ChromaDB with persistent storage in the `chroma/` directory.
- Embeddings are generated for each chunk during ingestion (see `app/embeddings.py`).
- The RAG prompt is constructed using the top retrieved document chunks and sent to Ollama for answer generation.
- You can modify chunking, embedding, and model settings in the respective files.

### Notes on Testing

- Current testing is being conducted using the Dungeons & Dragons Player's Handbook (2014 edition) as the primary document. This ensures the pipeline processes complex and structured text effectively.

---

## Troubleshooting

- Ensure Ollama is running and the model is pulled before querying the API.
- Check logs for errors during ingestion or querying.
- For large PDFs, adjust chunk size and overlap in `app/ingest.py` as needed.

---

## License

MIT License

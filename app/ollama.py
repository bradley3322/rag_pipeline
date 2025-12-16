from ollama import Client

import requests
import json
from typing import List

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma:2b" 

def generate_rag_prompt(query: str, retrieved_context: List[str]) -> str:
    context_text = "\n---\n".join(retrieved_context)

    prompt = f"""
    You are a helpful and knowledgeable assistant. Use ONLY the following provided context
    to answer the user's question. Do not use any external knowledge.
    If the context does not contain the answer, state clearly that the information is not available
    in the provided documents.

    CONTEXT:
    {context_text}

    QUESTION: {query}

    ANSWER:
    """
    return prompt

def generate_response_ollama(rag_prompt: str) -> str:

    payload = {
        "model": MODEL_NAME,
        "prompt": rag_prompt,
        "stream": False, 
        "options": {
            "temperature": 0.2, 
            "num_predict": 1024 
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status() 
        return response.json().get("response", "Error: No response content found.")
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}. Is the 'ollama serve' running?"





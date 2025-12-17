from ollama import Client

import requests
import json
from typing import List

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b" 

def generate_rag_prompt(query: str, retrieved_context: List[str]) -> str:
    context_text = "\n---\n".join(retrieved_context)

    prompt = f"""
    You are a **Literal Text Extractor**. Your sole purpose is to find a direct, single-sentence answer to the QUESTION within the CONTEXT.

    **CONTEXT:**
    {context_text}

    **QUESTION:** {query}

    # Updated INSTRUCTIONS for Maximum Safety

    **INSTRUCTIONS:**
    1. Read the QUESTION and the CONTEXT.
    2. **First, check if the subject of the QUESTION (e.g., 'Fighter', 'Asbestos') is explicitly mentioned in the CONTEXT.**
    3. If the subject is **NOT** mentioned, immediately output ONLY: `RULE_NOT_FOUND`.
    4. If the subject **IS** mentioned, proceed to search for the specific rule.
    5. Search for the single sentence that provides the most absolute rule about the QUESTION (using keywords like 'only when,' 'otherwise don\'t,' or 'cannot'). **OUTPUT THAT EXACT SENTENCE**.
    6. Do NOT output any spell descriptions, long paragraphs, or synthesis.

**ANSWER (Start immediately with the extracted sentence or the token):**
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

    print(str(payload))
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status() 
        return response.json().get("response", "Error: No response content found.")
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}. Is the 'ollama serve' running?"





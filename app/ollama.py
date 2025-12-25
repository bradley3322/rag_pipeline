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

    **INSTRUCTIONS:**
    1. Read the QUESTION and the CONTEXT.
    2. **Subject Check:** If the subject (e.g., 'Fighter') is NOT mentioned, but the action (e.g., 'summoning') IS mentioned for other subjects (e.g., 'Wizard'):
    - Output: `SUBJECT_MISSING: The context discusses [Action] but only in relation to [Other Subjects].`
    3. If the subject IS mentioned but the specific rule isn't there:
    - Output: `RULE_NOT_FOUND`.
    4. If the subject and rule are both found:
    - Output ONLY the exact sentence.

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
            "num_predict": 5120 
        }
    }

    print(str(payload))
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status() 
        return response.json().get("response", "Error: No response content found.")
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}. Is the 'ollama serve' running?"





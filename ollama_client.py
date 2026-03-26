import requests

OLLAMA_MODEL = "MODEL_NAME"  # Deepseek-r1 recommended 
OLLAMA_URL = "OLLAMA_API"

def call_ollama(prompt: str, model: str, temperature=0.7) -> str:
    payload = {
        "model": model,
        "prompt": prompt.strip(),
        "temperature": temperature,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"].strip()

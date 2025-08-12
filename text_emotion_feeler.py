import requests

# Ollama server URL
OLLAMA_URL = "http://localhost:11434/api/generate"

def detect_category(user_text: str) -> str:
    """
    Detects the category of the given text using LLaMA 3.2 via Ollama.
    Categories:
    - open youtube
    - open desktop app
    Returns only the category string.
    """
    prompt = f"""
You are a sentence feeling detector.
Whenever any text comes to you, you just tell me which category it goes:
- open youtube
- open desktop app
- open music
Do not give me any extra words without category.

Text: {user_text}
"""

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Example usage
if __name__ == "__main__":
    text_input = "my moode is off so i need to listen something beautiful "
    category = detect_category(text_input)
    print( category)

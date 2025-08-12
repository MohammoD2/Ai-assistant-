import requests

# Ollama server URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Input text to classify
user_text = "i have a good idea in my mind so i need some thing for write"

# Prompt for LLaMA 3.2
prompt = f"""
You are a sentence feeling detector.
Whenever any text comes to you, you just tell me which category it goes:
- open youtube
- open desktop app
Do not give me any extra words without category.

Text: {user_text}
"""

# Send request to Ollama
payload = {
    "model": "llama3.2",
    "prompt": prompt,
    "stream": False  # We want the full result at once
}

response = requests.post(OLLAMA_URL, json=payload)

if response.status_code == 200:
    result = response.json()
    # 'response' key contains the model's output
    category = result.get("response", "").strip()
    print(category)
else:
    print(f"Error: {response.status_code}, {response.text}")

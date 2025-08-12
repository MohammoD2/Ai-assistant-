import requests

# Ollama server URL
OLLAMA_URL = "http://localhost:11434/api/generate"

def detect_category(user_text: str) -> str:
    """
    Detects the category of the given text using LLaMA 3.2 via Ollama.
    Returns only the category string.
    """
    prompt = f"""
You are an advanced action intent detector for a Data Scientist / ML Engineer / AI Engineer.
Whenever any text comes to you, you must tell me which category it belongs to from the list below.
Return only the category name — no extra words, no punctuation, no explanations.

Categories:
- open youtube
- open facebook
- open clock
- open important professional website
- file opener
- file management
- write code
- find file
- search information
- open email
- schedule event
- play music
- read document
- translate text
- send message
- take screenshot
- system settings
- shut down system
- restart system
- open calculator
- weather update
- news update
- run terminal command
- open camera
- open notes
- open calendar
- open chat app
- browse internet
- manage tasks
- open microsoft word
- open microsoft excel
- open microsoft powerpoint
- open microsoft outlook
- open microsoft teams
- open visual studio
- open visual studio code
- open pycharm
- open intellij idea
- open eclipse
- open photoshop
- open illustrator
- open premiere pro
- open after effects
- open figma
- open slack
- open zoom
- open discord
- open notepad
- open notepad++
- open sublime text
- open firefox
- open google chrome
- open microsoft edge
- open opera
- open vlc media player
- open spotify
- open skype
- open file explorer
- open terminal
- open command prompt
- open powershell
- open git bash
- open onedrive
- open dropbox
- open jupyter notebook
- open jupyter lab
- open anaconda navigator
- open spyder ide
- open rstudio
- open matlab
- open tableau
- open power bi
- open datagrip
- open dbeaver
- open postman
- open docker desktop
- open kubernetes dashboard
- open airflow ui
- open mlflow ui
- open tensorboard
- open azure data studio
- open aws console
- open gcp console
- open azure ml studio
- open hugging face
- open kaggle
- open colab
- open github desktop
- open gitlab
- open bitbucket
- open elasticsearch
- open kibana
- open grafana
- open neo4j browser
- open faiss dashboard (if available)
- open vsphere
- open putty
- open winSCP
- open cyberduck

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
        return result.get("response", "").strip().lower()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Example usage
if __name__ == "__main__":
    text_input = "i think i need some things like hugging face "
    category = detect_category(text_input)
    print("Detected category:", category)

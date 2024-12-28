import requests
import time

from fastapi import FastAPI

time.sleep(5)

def generate_content(prompt_raw):
    url = "http://ollama:11434/api/generate"
    payload = {
        "model": "llama3.2",
        "prompt": prompt_raw,
        "stream": False,
    }
    response = requests.post(url, json=payload)
    return response.json()["response"]

def get_ollama_model():
    url = "http://ollama:11434/api/tags"
    response = requests.get(url)
    return str(response.content)

def pull_ollama():
    url = "http://ollama:11434/api/pull"
    payload = {
        "model": "llama3.2",
    }
    response = requests.post(url, json=payload)

modellist = get_ollama_model()
if "llama3.2" not in modellist:
    pull_ollama()
else:
    print(modellist)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Binance RAG"}

@app.get("/rq/{key}")
async def get_value(key: str):
    response = generate_content(key)
    return {"Question": key, "Answer": response}

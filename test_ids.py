
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def test_manual(model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    print(f"Testing: {model}")
    print(f"URL: {url}")
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Result: {r.text[:200]}")

test_manual("gemini-1.5-flash")
test_manual("gemini-1.5-flash-latest")
test_manual("gemini-pro")

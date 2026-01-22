
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def test_full_path(model_path):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    print(f"Testing: {model_path}")
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Result: {r.text[:200]}")

test_full_path("models/gemini-1.5-flash")
test_full_path("models/gemini-pro")

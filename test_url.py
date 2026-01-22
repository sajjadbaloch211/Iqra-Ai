
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def test_manual(url_part):
    url = f"https://generativelanguage.googleapis.com/{url_part}?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    print(f"Testing: {url}")
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Result: {r.text[:200]}")

test_manual("v1beta/models/gemini-1.5-flash:generateContent")
test_manual("v1/models/gemini-1.5-flash:generateContent")

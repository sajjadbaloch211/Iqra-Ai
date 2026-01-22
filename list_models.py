
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def list_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    r = requests.get(url)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        models = r.json()
        for m in models.get('models', []):
            print(m['name'])
    else:
        print(r.text)

list_models()

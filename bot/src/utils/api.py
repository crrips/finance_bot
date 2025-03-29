import os

import requests

API_URL = os.getenv("API_URL", "http://backend:8000")

def fetch_expenses():
    response = requests.get(f"{API_URL}/expenses")
    response.raise_for_status()
    return response.json()
    
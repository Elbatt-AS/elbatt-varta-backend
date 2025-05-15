import json

def load_token():
    with open('config.json', 'r') as f:
        data = json.load(f)
        return data.get('API_TOKEN')

from config import API_TOKEN

print(f"API token loaded: {API_TOKEN[:10]}...")


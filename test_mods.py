import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get('GEMINI_API_KEY').strip()

print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
print("\nChecking available models...\n")

# Try v1 API
print("=== Trying v1 API ===")
url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
response = requests.get(url)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    models = response.json()
    print("Available models:")
    for model in models.get('models', []):
        print(f"  - {model.get('name')}")
        print(f"    Methods: {model.get('supportedGenerationMethods', [])}")
else:
    print(response.text)

print("\n=== Trying v1beta API ===")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    models = response.json()
    print("Available models:")
    for model in models.get('models', []):
        print(f"  - {model.get('name')}")
        print(f"    Methods: {model.get('supportedGenerationMethods', [])}")
else:
    print(response.text)
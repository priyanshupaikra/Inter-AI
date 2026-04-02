"""
List available Gemini models
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("API Key not found")
    exit(1)

client = genai.Client(api_key=api_key)

print("Fetching available models...")
try:
    # models.list returns an iterator
    print("Models found:")
    for m in client.models.list():
        # Try to print name, otherwise print the object
        try:
            print(f"- {m.name}")
        except:
            print(f"- {m}")
            
except Exception as e:
    print(f"Error listing models: {e}")

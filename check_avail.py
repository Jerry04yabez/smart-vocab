import google.generativeai as genai
import os
import sys

# Hardcode API key check from env to avoid dotenv issues if any
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    with open('avail.txt', 'w') as f:
        f.write("NO_API_KEY")
    sys.exit(1)

genai.configure(api_key=api_key)

try:
    with open('avail.txt', 'w', encoding='utf-8') as f:
        f.write(f"VERSION: {genai.__version__}\n")
        f.write("MODELS:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
except Exception as e:
    with open('avail.txt', 'w') as f:
        f.write(f"ERROR: {e}")

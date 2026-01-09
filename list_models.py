import google.generativeai as genai
import os
import sys

# Hardcode API key check from env to avoid dotenv issues if any
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("NO_API_KEY")
    sys.exit(1)

genai.configure(api_key=api_key)

try:
    print(f"VERSION: {genai.__version__}")
    
    print("MODELS_START")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"MODEL: {m.name}")
    print("MODELS_END")
except Exception as e:
    print(f"ERROR: {e}")

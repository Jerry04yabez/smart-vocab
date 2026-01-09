import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("No API Key found")
    exit(1)

genai.configure(api_key=api_key)

models_to_try = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-001',
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-1.0-pro'
]

print(f"Testing models with lib version: {genai.__version__}")

for model_name in models_to_try:
    print(f"Testing {model_name}...", end=" ")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        if response and response.text:
            print("SUCCESS")
        else:
            print("FAILED (Empty response)")
    except Exception as e:
        print(f"FAILED: {e}")

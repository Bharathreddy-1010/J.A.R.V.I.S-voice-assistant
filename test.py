import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
GEMINI_API_KEY = "AIzaSyDNcsXp20v_1i18DSUSucFTAYm2MXzW8wU"

if not GEMINI_API_KEY:
    print("API Key not found in .env file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

    print("Listing available models...\n")
    for model in genai.list_models():
        # Check if the model supports the 'generateContent' method
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
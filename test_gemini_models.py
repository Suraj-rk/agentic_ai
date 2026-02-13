import os
from dotenv import load_dotenv
import google.generativeai as genai

# 🔑 Load .env explicitly
load_dotenv()

# Debug check
print("API KEY:", os.getenv("GOOGLE_API_KEY"))

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

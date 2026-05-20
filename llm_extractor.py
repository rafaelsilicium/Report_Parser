import os
from dotenv import load_dotenv

load_dotenv()

api_gemini_key = os.environ.get("AI_API_KEY")
print(f"chave API: {api_gemini_key}")
import os
from dotenv import load_dotenv

load_dotenv()

print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))
print("LLM_API_KEY:", os.getenv("LLM_API_KEY"))
print("LLM_PROVIDER:", os.getenv("LLM_PROVIDER"))
print("LLM_MODEL:", os.getenv("LLM_MODEL"))

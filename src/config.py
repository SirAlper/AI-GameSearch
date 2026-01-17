import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("HATA: Api key bulunamadi")

MODEL_NAME = "gemini-3-flash-preview"
TEMPERATURE = 0.5
SEARCH_MAX_RESULTS = 5
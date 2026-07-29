from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

AI_DAILY_REQUEST_LIMIT = int(
    os.getenv("AI_DAILY_REQUEST_LIMIT", "3")
)
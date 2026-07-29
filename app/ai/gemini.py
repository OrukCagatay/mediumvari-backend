from google import genai
from google.genai import types

from app.core.config import GEMINI_API_KEY
from app.ai.exceptions import (
    GeminiAPIError,
    GeminiTimeoutError,
    GeminiEmptyResponseError,
)

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

    except TimeoutError:
        raise GeminiTimeoutError()

    except Exception as e:
        raise GeminiAPIError(str(e))

    if not response.text:
        raise GeminiEmptyResponseError()

    return response.text

import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def _clean_json(text: str) -> str:
    """
    Remove markdown code fences like ```json ... ```
    """
    text = text.strip()

    # Remove starting ```json or ```
    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```", "", text)

    # Remove ending ```
    text = re.sub(r"```$", "", text)

    return text.strip()


def generate_structured_payload(prompt: str) -> dict:
    """
    Calls Gemini and returns a STRICT Python dict.
    Cleans markdown and parses JSON safely.
    """
    response = model.generate_content(prompt)
    raw_text = response.text

    try:
        cleaned = _clean_json(raw_text)
        return json.loads(cleaned)
    except Exception:
        raise ValueError(
            f"LLM returned invalid JSON.\nRaw output:\n{raw_text}"
        )

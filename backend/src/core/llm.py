import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)


def get_gemini_response(query: str) -> str:
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(query)
        return response.text
    except Exception as error:
        try:
            model = genai.GenerativeModel("models/gemini-flash-latest")
            response = model.generate_content(query)
            return response.text
        except Exception:
            return f"Error: {str(error)}"

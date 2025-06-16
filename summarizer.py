import requests
import os
from dotenv import load_dotenv
from langdetect import detect
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import re

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return ' '.join([p.text for p in soup.find_all('p')])

def is_url(text):
    return re.match(r'^https?:\/\/', text.strip())

def get_summary(input_data, tone="formal", length="medium", file_type=None):
    """
    Generate a summary using DeepSeek via OpenRouter.

    Args:
        input_data (str): Text, PDF path, or URL to summarize.
        tone (str): Summary tone.
        length (str): Summary length.
        file_type (str): 'pdf' if input is PDF. Otherwise, detect text/URL.

    Returns:
        str: Summary text or error message.
    """
    try:
        # 🔍 Source detection
        if file_type == "pdf":
            raw_text = extract_text_from_pdf(input_data)
        elif is_url(input_data):
            raw_text = extract_text_from_url(input_data)
        else:
            raw_text = input_data

        # 🌍 Language detection
        try:
            lang = detect(raw_text)
        except:
            lang = "en"

        # 🧠 Prompt engineering
        prompt = f"Summarize this text in a {tone} tone and {length} length. The text is in {lang} language:\n\n{raw_text}"

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI summarizer."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
        )

        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: {result.get('error', {}).get('message', 'Unknown error')}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"

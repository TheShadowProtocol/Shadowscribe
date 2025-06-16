import PyPDF2
from docx import Document
import fitz  # PyMuPDF (for better PDF support)
from bs4 import BeautifulSoup
import requests
import re

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == "txt":
            uploaded_file.seek(0)
            return uploaded_file.read().decode("utf-8", errors="ignore")

        elif file_type == "pdf":
            try:
                # Try PyMuPDF for better layout retention
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = "\n".join([page.get_text() for page in doc])
                if text.strip():
                    return text
            except:
                # Fallback to PyPDF2
                uploaded_file.seek(0)
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                return text

        elif file_type == "docx":
            uploaded_file.seek(0)
            doc = Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])

    except Exception as e:
        print(f"Error extracting file: {e}")

    return None

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join(p.get_text() for p in paragraphs if p.get_text())
    except Exception as e:
        print(f"URL extract error: {e}")
        return None

def is_url(text):
    return re.match(r'^https?://', text.strip()) is not None

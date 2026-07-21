import fitz
import requests
from io import BytesIO

def extract_text_from_pdf(file_url: str) -> str:
    response = requests.get(file_url)
    response.raise_for_status()

    if not response.content:
        raise ValueError("Downloaded file is empty")

    pdf_bytes = BytesIO(response.content)

    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return text.strip()
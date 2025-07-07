import io
from PyPDF2 import PdfReader

def read_pdf_text(content):
    reader = PdfReader(io.BytesIO(content))  # Correct use of io.BytesIO
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

import fitz  # PyMuPDF for handling PDFs
import logging

def extract_text(file_path):
    """Extracts text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF {file_path}: {e}")
        raise ValueError(f"Failed to extract text from PDF {file_path}: {e}")

import docx  # python-docx for handling DOCX files
import logging

def extract_text(file_path):
    """Extracts text from a DOCX file using python-docx."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        logging.error(f"Error extracting text from DOCX {file_path}: {e}")
        raise ValueError(f"Failed to extract text from DOCX {file_path}: {e}")

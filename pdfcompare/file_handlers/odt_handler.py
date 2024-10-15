from odf.opendocument import load
from odf.text import P

def extract_text(file_path):
    """Extracts text from an ODT file."""
    try:
        doc = load(file_path)
        paragraphs = [p.text for p in doc.getElementsByType(P)]
        text = "\n".join(paragraphs)
        if not text:
            raise ValueError("No text found in ODT file.")
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from ODT file: {e}")

from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text(file_path):
    """Extracts text from an EPUB file."""
    try:
        book = epub.read_epub(file_path)
        text = []
        for item in book.get_items():
            if item.get_type() == epub.EpubHtml:
                soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                text.append(soup.get_text())
        full_text = "\n".join(text)
        if not full_text:
            raise ValueError("No text found in EPUB file.")
        return full_text
    except Exception as e:
        raise ValueError(f"Failed to extract text from EPUB file: {e}")

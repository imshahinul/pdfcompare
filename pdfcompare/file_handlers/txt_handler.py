def extract_text(file_path):
    """Extracts text from a plain text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise ValueError("No text found in TXT file.")
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from TXT file: {e}")

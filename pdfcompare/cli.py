import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


# Function to extract text from a PDF (scanned or non-scanned PDFs)
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Try to extract text from PDF
        extracted_text = page.get_text("text")
        if extracted_text.strip():
            text += extracted_text
        else:
            # If the page seems to be empty, it's likely scanned; use OCR
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text += pytesseract.image_to_string(img)

    return text

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import docx
import mimetypes
from difflib import unified_diff


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


# Function to extract text from .docx files
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# Function to extract text from image files (for scanned images)
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


# Function to dynamically detect file type and extract text
def extract_text_from_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        raise ValueError(f"Cannot determine file type for: {file_path}")

    if mime_type == "application/pdf":
        return extract_text_from_pdf(file_path)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_path)
    elif mime_type.startswith("image/"):
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")


# Function to compare two texts and output differences
def compare_texts(text1, text2):
    diff = unified_diff(text1.splitlines(), text2.splitlines(), lineterm="")
    return "\n".join(list(diff))

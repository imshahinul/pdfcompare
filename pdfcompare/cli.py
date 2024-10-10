import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import docx
import mimetypes
from difflib import unified_diff
from pathlib import Path
import pdfkit


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


# Function to generate readable HTML format of the comparison report
def generate_html_report(differences_report, file_names):
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h2 {{ color: #333; }}
            .difference {{ background-color: #f9f9f9; padding: 10px; margin-bottom: 20px; }}
            pre {{ background-color: #eee; padding: 10px; border-left: 5px solid #ccc; }}
        </style>
        <title>Comparison Report</title>
    </head>
    <body>
        <h2>File Comparison Report</h2>
        <p><strong>Compared Files:</strong> {', '.join(file_names)}</p>
        <div class="difference">
            <h3>Differences</h3>
            <pre>{differences_report}</pre>
        </div>
    </body>
    </html>
    """
    return html_content


# Function to dynamically handle multiple files and comparison
def compare_files(files):
    if len(files) < 2:
        raise ValueError("At least two files are required for comparison.")

    # Extract text from all files
    texts = []
    for file_path in files:
        print(f"Extracting text from {file_path}...")
        text = extract_text_from_file(file_path)
        texts.append(text)

    # Compare each file with the next one
    all_differences = []
    for i in range(len(texts) - 1):
        print(f"Comparing {Path(files[i]).name} with {Path(files[i + 1]).name}...")
        differences = compare_texts(texts[i], texts[i + 1])
        if differences:
            all_differences.append(f"Differences between {files[i]} and {files[i + 1]}:\n{differences}")
        else:
            all_differences.append(f"No differences between {files[i]} and {files[i + 1]}")

    # Return the differences as a single report string
    return "\n\n".join(all_differences)


# Function to save the plain text report
def save_text_report(differences_report, output_file="comparison_report.txt"):
    with open(output_file, "w") as f:
        f.write(differences_report)
    print(f"Text report saved to {output_file}")

# Function to save HTML report as a text file
def save_html_report(html_content, output_file="comparison_report.html"):
    with open(output_file, "w") as f:
        f.write(html_content)
    print(f"HTML report saved to {output_file}")

# Function to save HTML report as a PDF file
def save_html_as_pdf(html_content, output_pdf="comparison_report.pdf"):
    pdfkit.from_string(html_content, output_pdf)
    print(f"PDF report saved to {output_pdf}")
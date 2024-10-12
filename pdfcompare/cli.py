import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import docx
import mimetypes
from difflib import unified_diff
from pathlib import Path
import pdfkit
import argparse
import os
import logging


def validate_file(file_path):
    """Checks if a file exists and is not empty."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File is empty: {file_path}")
    logging.info(f"File {file_path} validated successfully.")


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    try:
        validate_file(pdf_path)
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        if not text:
            raise ValueError("No text found in PDF file.")
        logging.info(f"Text extracted from PDF {pdf_path} successfully.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF {pdf_path}: {e}")
        raise ValueError(f"Failed to extract text from PDF: {e}")


def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        validate_file(docx_path)
        doc = docx.Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        if not text:
            raise ValueError("No text found in DOCX file.")
        logging.info(f"Text extracted from DOCX {docx_path} successfully.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from DOCX {docx_path}: {e}")
        raise ValueError(f"Failed to extract text from DOCX: {e}")


def extract_text_from_image(image_path):
    """Extracts text from an image file using Tesseract OCR."""
    try:
        validate_file(image_path)
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        if not text:
            raise ValueError("No text found in image file.")
        logging.info(f"Text extracted from image {image_path} successfully.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from image {image_path}: {e}")
        raise ValueError(f"Failed to extract text from image: {e}")


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


def compare_texts(text1, text2):
    """Compares two texts and returns the differences."""
    try:
        diff = list(unified_diff(text1.splitlines(), text2.splitlines()))
        if not diff:
            return "No differences found."
        logging.info("Text comparison completed with differences found.")
        return "\n".join(diff)
    except Exception as e:
        logging.error(f"Error comparing texts: {e}")
        raise ValueError(f"Failed to compare texts: {e}")


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


# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Compare text content from multiple files.")
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='Files to be compared, separated by spaces.')
    parser.add_argument('--output-txt', '-otxt', type=str, default=None,
                        help='Optional output text file to save the comparison report as plain text.')
    parser.add_argument('--output-html', '-ohtml', type=str, default=None,
                        help='Optional output HTML file to save the comparison report as readable HTML.')
    parser.add_argument('--output-pdf', '-opdf', type=str, default=None,
                        help='Optional output PDF file to save the comparison report as a PDF.')

    args = parser.parse_args()

    # Perform the comparison
    differences_report = compare_files(args.files)

    # Print the differences in plain text format to the console
    print(differences_report)

    # If output file is specified for text, generate and save the text report
    if args.output_txt:
        save_text_report(differences_report, args.output_txt)

    # If output file is specified for HTML, generate and save the HTML report
    if args.output_html:
        html_content = generate_html_report(differences_report, args.files)
        save_html_report(html_content, args.output_html)

    # If output file is specified for PDF, generate and save the PDF report
    if args.output_pdf:
        html_content = generate_html_report(differences_report, args.files)
        save_html_as_pdf(html_content, args.output_pdf)


if __name__ == "__main__":
    main()

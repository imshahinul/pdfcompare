import unittest
import tempfile
import os
from pdfcompare.cli import extract_text, compare_texts, generate_report
from pdfcompare.file_handlers import load_handler
from reportlab.pdfgen import canvas
from docx import Document
from PIL import Image, ImageDraw, ImageFont


class TestPDFCompare(unittest.TestCase):

    def setUp(self):
        """Create temporary files for testing purposes."""
        # Create temp PDF file
        self.test_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        c = canvas.Canvas(self.test_pdf.name)
        c.drawString(100, 750, "This is a test PDF file.")
        c.save()

        # Create temp DOCX file
        self.test_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        doc = Document()
        doc.add_paragraph("This is a test DOCX file.")
        doc.save(self.test_docx.name)

        # Create temp plain text file
        self.test_txt = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        with open(self.test_txt.name, 'w') as f:
            f.write("This is a test TXT file.")

        # Create temp image file with text for OCR
        self.test_image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        image = Image.new('RGB', (300, 100), color='white')  # Increased size
        draw = ImageDraw.Draw(image)

        # Use an OCR-friendly font
        try:
            font = ImageFont.truetype("Tahoma.ttf", 40)  # Or any clear monospace font
        except IOError:
            font = ImageFont.load_default()

        draw.text((10, 25), "Test OCR text", font=font, fill='black')  # Improved contrast
        image.save(self.test_image.name)

    def tearDown(self):
        """Clean up temporary files after tests."""
        os.remove(self.test_pdf.name)
        os.remove(self.test_docx.name)
        os.remove(self.test_txt.name)
        os.remove(self.test_image.name)

    def test_extract_text_from_pdf(self):
        """Test text extraction from PDF file."""
        text = extract_text(self.test_pdf.name)
        self.assertIn("This is a test PDF file.", text)

    def test_extract_text_from_docx(self):
        """Test text extraction from DOCX file."""
        text = extract_text(self.test_docx.name)
        self.assertIn("This is a test DOCX file.", text)

    def test_extract_text_from_txt(self):
        """Test text extraction from TXT file."""
        text = extract_text(self.test_txt.name)
        self.assertIn("This is a test TXT file.", text)

    def test_extract_text_from_image(self):
        """Test text extraction from image file using OCR."""
        text = extract_text(self.test_image.name)
        print(f"OCR extracted text: '{text}'")  # Log the OCR output

        # Normalize the extracted text by stripping spaces and converting to lowercase
        normalized_text = text.replace(" ", "").lower()

        # Perform a relaxed assertion to check for the expected text
        self.assertIn("testocrtext", normalized_text, "OCR did not match expected text.")

    def test_compare_texts(self):
        """Test comparing two texts for differences."""
        text1 = "This is a test."
        text2 = "This is another test."
        result = compare_texts(text1, text2)
        self.assertIn('-This is a test.', result)
        self.assertIn('+This is another test.', result)

    def test_generate_report_txt(self):
        """Test generating a comparison report in TXT format."""
        text1 = "This is a test."
        text2 = "This is another test."
        result = compare_texts(text1, text2)
        report_path = generate_report(self.test_txt.name, self.test_pdf.name, result, 'txt')
        self.assertTrue(os.path.exists(report_path))
        with open(report_path, 'r') as report_file:
            content = report_file.read()
            self.assertIn('-This is a test.', content)
        os.remove(report_path)

    def test_generate_report_html(self):
        """Test generating a comparison report in HTML format."""
        text1 = "This is a test."
        text2 = "This is another test."
        result = compare_texts(text1, text2)
        report_path = generate_report(self.test_txt.name, self.test_pdf.name, result, 'html')
        self.assertTrue(os.path.exists(report_path))
        os.remove(report_path)

    def test_generate_report_pdf(self):
        """Test generating a comparison report in PDF format."""
        text1 = "This is a test."
        text2 = "This is another test."
        result = compare_texts(text1, text2)
        report_path = generate_report(self.test_txt.name, self.test_pdf.name, result, 'pdf')
        self.assertTrue(os.path.exists(report_path))
        os.remove(report_path)


if __name__ == '__main__':
    unittest.main()

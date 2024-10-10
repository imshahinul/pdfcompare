import unittest
from pdfcompare.cli import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image, compare_texts, generate_html_report
import os
import tempfile
from PIL import Image, ImageDraw
import fitz
import docx

class TestPDFCompare(unittest.TestCase):

    def setUp(self):
        # Create a valid test PDF with some text
        self.test_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = fitz.open()
        page = doc.new_page()  # Create a blank page
        page.insert_text((72, 72), "Sample text for PDF")  # Insert some sample text
        doc.save(self.test_pdf.name)
        doc.close()

        # Create a valid DOCX file with some text
        self.test_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc = docx.Document()
        doc.add_paragraph("Sample text for DOCX")
        doc.save(self.test_docx.name)

        # Create a valid image with some text
        self.test_image = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img = Image.new('RGB', (200, 100), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), "Sample Text", fill=(255, 255, 0))
        img.save(self.test_image.name)

        # Temporary output files for reports
        self.test_txt_output = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.test_html_output = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        self.test_pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    def tearDown(self):
        # Clean up all temporary files
        try:
            os.unlink(self.test_pdf.name)
            os.unlink(self.test_docx.name)
            os.unlink(self.test_image.name)
            os.unlink(self.test_txt_output.name)
            os.unlink(self.test_html_output.name)
            os.unlink(self.test_pdf_output.name)
        except OSError:
            pass

    def test_extract_text_from_pdf(self):
        # Assuming a simple PDF with some text for testing
        text = extract_text_from_pdf(self.test_pdf.name)
        self.assertIsNotNone(text)
        self.assertIsInstance(text, str)

    def test_extract_text_from_docx(self):
        # Assuming a simple DOCX file with some text for testing
        text = extract_text_from_docx(self.test_docx.name)
        self.assertIsNotNone(text)
        self.assertIsInstance(text, str)

    def test_extract_text_from_image(self):
        # Assuming a simple image file with some text for testing
        text = extract_text_from_image(self.test_image.name)
        self.assertIsNotNone(text)
        self.assertIsInstance(text, str)

    def test_compare_texts(self):
        # Test comparison of two similar texts
        text1 = "This is a test."
        text2 = "This is a test."
        result = compare_texts(text1, text2)
        self.assertEqual(result.strip(), "No differences found.")  # Assuming this is the output of no differences

        # Test comparison of two different texts
        text1 = "This is a test."
        text2 = "This is another test."
        result = compare_texts(text1, text2)
        self.assertIn('- This is a test.', result)
        self.assertIn('+ This is another test.', result)

    def test_generate_html_report(self):
        # Generate an HTML report from a comparison report
        differences_report = "No differences found."
        file_names = ['file1.pdf', 'file2.docx']
        html_report = generate_html_report(differences_report, file_names)

        self.assertIsNotNone(html_report)
        self.assertIn('<html>', html_report)
        self.assertIn('<body>', html_report)
        self.assertIn('No differences found.', html_report)

    def test_save_text_report(self):
        from pdfcompare.cli import save_text_report

        # Test saving the text report
        differences_report = "No differences found."
        save_text_report(differences_report, self.test_txt_output.name)

        # Check if file was created and has the correct content
        with open(self.test_txt_output.name, 'r') as f:
            content = f.read()
            self.assertIn("No differences found.", content)

    def test_save_html_report(self):
        from pdfcompare.cli import save_html_report

        # Test saving the HTML report
        differences_report = "No differences found."
        file_names = ['file1.pdf', 'file2.docx']
        html_content = generate_html_report(differences_report, file_names)
        save_html_report(html_content, self.test_html_output.name)

        # Check if file was created and has the correct content
        with open(self.test_html_output.name, 'r') as f:
            content = f.read()
            self.assertIn("<html>", content)
            self.assertIn("No differences found.", content)

    def test_save_html_as_pdf(self):
        from pdfcompare.cli import save_html_as_pdf

        # Test saving the PDF report
        differences_report = "No differences found."
        file_names = ['file1.pdf', 'file2.docx']
        html_content = generate_html_report(differences_report, file_names)
        save_html_as_pdf(html_content, self.test_pdf_output.name)

        # Check if the PDF file was created
        self.assertTrue(os.path.exists(self.test_pdf_output.name))
        self.assertTrue(os.path.getsize(self.test_pdf_output.name) > 0)

if __name__ == '__main__':
    unittest.main()

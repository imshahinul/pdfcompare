import unittest
import tempfile
import os

class TestPDFCompare(unittest.TestCase):

    def setUp(self):
        # Setup temporary test files
        self.test_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        self.test_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        self.test_image = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self.test_txt_output = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.test_html_output = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        self.test_pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    def tearDown(self):
        # Remove temporary test files
        try:
            os.unlink(self.test_pdf.name)
            os.unlink(self.test_docx.name)
            os.unlink(self.test_image.name)
            os.unlink(self.test_txt_output.name)
            os.unlink(self.test_html_output.name)
            os.unlink(self.test_pdf_output.name)
        except OSError:
            pass
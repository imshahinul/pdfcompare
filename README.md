
# PDFCompare

`PDFCompare` is a Python package for comparing two files (PDF, DOCX, or scanned images) and generating a difference report. It provides options for exporting the comparison report in three formats: plain text, HTML, and PDF. The package uses `PyMuPDF` for PDF parsing, `pytesseract` for OCR on images, and `python-docx` for DOCX parsing.

## Features

- Compare PDF, DOCX, or scanned image files.
- Generate and save comparison reports in **TXT**, **HTML**, and **PDF** formats.
- Supports text extraction from scanned PDFs or images using `pytesseract`.
- Simple CLI for running comparisons.

## Installation

### Python Requirements

- Python 3.6+

### Dependency Installation

The following external dependencies are required to handle PDF and image OCR:

1. **Tesseract OCR**: Required for extracting text from images or scanned PDFs.
2. **wkhtmltopdf**: Required for converting HTML reports into PDFs.

#### Tesseract Installation

##### **Linux (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

##### **MacOS**
If you have Homebrew installed, use the following command:
```bash
brew install tesseract
```

##### **Windows**
Download the Tesseract installer from the official repository [here](https://github.com/tesseract-ocr/tesseract/wiki) and follow the installation instructions.

#### wkhtmltopdf Installation

##### **Linux (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

##### **MacOS**
If you have Homebrew installed, use the following command:
```bash
brew install wkhtmltopdf
```

##### **Windows**
Download the Windows installer from [here](https://wkhtmltopdf.org/downloads.html) and install it.

### Installing the `pdfcompare` Package

Once the dependencies are installed, you can install `pdfcompare` using `pip`:

```bash
pip install pdfcompare
```

## Usage

### Command-Line Interface (CLI)

`pdfcompare` provides a command-line interface to compare files and generate reports.

#### Basic Syntax

```bash
pdfcompare file1 file2 --output txt
pdfcompare file1 file2 --output html
pdfcompare file1 file2 --output pdf
```

### Example

```bash
pdfcompare document1.pdf document2.docx --output html
```

This command compares `document1.pdf` and `document2.docx` and saves the output as an HTML report.

### Options

- `file1`, `file2`: Paths to the two files you want to compare.
- `--output`: Specify the format for the report (options: `txt`, `html`, `pdf`).

### Programmatic Usage

You can also use `pdfcompare` as a Python module in your own code.

```python
from pdfcompare.cli import compare_files

file1 = "path/to/file1.pdf"
file2 = "path/to/file2.docx"
output_format = "pdf"  # Choose between 'txt', 'html', or 'pdf'

compare_files(file1, file2, output_format)
```

## Testing

To run unit tests, simply run the following command after installing the dependencies:

```bash
python -m unittest discover tests/
```

The tests cover:
- Text extraction from PDFs, DOCX, and images.
- File comparison logic.
- Report generation in TXT, HTML, and PDF formats.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
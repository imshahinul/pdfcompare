# PDFCompare

`PDFCompare` is a Python package designed for comparing multiple file types, including **PDF**, **DOCX**, and **scanned images**. It generates detailed difference reports that can be exported in **TXT**, **HTML**, and **PDF** formats. The package utilizes `PyMuPDF` for parsing PDFs, `pytesseract` for OCR on images, and `python-docx` for DOCX parsing. Additionally, it now includes **advanced image preprocessing** for improved OCR accuracy using **OpenCV**.

## Features

- **Compare multiple file types**: PDF, DOCX, and scanned image files.
- **Export comparison reports**: Generate and save reports in **TXT**, **HTML**, or **PDF** formats.
- **OCR for image files**: Supports text extraction from scanned PDFs or images using `pytesseract` with advanced preprocessing.
- **Advanced image preprocessing**: Leverage `OpenCV` for binarization, noise removal, and other image enhancements to improve OCR accuracy.
- **Easy-to-use CLI**: Run comparisons via the command line or integrate into your own Python applications.

## Installation

### Python Requirements

- Python 3.7+

### External Dependencies

The following external dependencies are required for handling PDF parsing and OCR:

1. **Tesseract OCR**: For extracting text from images or scanned PDFs.
2. **wkhtmltopdf**: For converting HTML reports into PDFs.
3. **OpenCV**: For image preprocessing before OCR.

#### Installing Tesseract

##### **Linux (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

##### **MacOS**
If you have Homebrew installed, run:
```bash
brew install tesseract
```

##### **Windows**
Download the Tesseract installer from the official repository [here](https://github.com/tesseract-ocr/tesseract/wiki) and follow the installation instructions.

#### Installing wkhtmltopdf

##### **Linux (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

##### **MacOS**
Using Homebrew:
```bash
brew install wkhtmltopdf
```

##### **Windows**
Download the Windows installer from [here](https://wkhtmltopdf.org/downloads.html) and install it.

#### Installing OpenCV

To install OpenCV for image preprocessing, run:

```bash
pip install opencv-python
```

### Installing the `pdfcompare` Package

Once all dependencies are installed, you can install `pdfcompare` via `pip`:

```bash
pip install pdfcompare
```

## Usage

### Command-Line Interface (CLI)

`pdfcompare` provides an intuitive command-line interface for comparing files and generating reports.

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

This command compares `document1.pdf` and `document2.docx`, and saves the comparison result as an HTML report.

### Options

- `file1`, `file2`: Paths to the files you want to compare.
- `--output`: Specify the format for the report (options: `txt`, `html`, `pdf`).

### Advanced Image Preprocessing for OCR

The `pdfcompare` package now supports advanced image preprocessing using OpenCV to improve OCR accuracy. This includes steps like binarization, noise removal, and other enhancements before performing text extraction.

### Programmatic Usage

`pdfcompare` can be used as a Python module within your code.

```python
from pdfcompare.cli import compare_files

file1 = "path/to/file1.pdf"
file2 = "path/to/file2.docx"
output_format = "pdf"  # Choose from 'txt', 'html', or 'pdf'

compare_files(file1, file2, output_format)
```

```python
from pdfcompare.file_handlers.image_handler import extract_text

text = extract_text("path/to/your/image.png")
print(text)
```

## Testing

To run unit tests, first install the development dependencies, and then use:

```bash
python -m unittest discover tests/
```

### Coverage of Tests:

- **Text extraction**: From PDFs, DOCX files, and images.
- **File comparison logic**: Ensures accurate and consistent differences between file contents.
- **Report generation**: Tests for TXT, HTML, and PDF formats.
- **Image preprocessing**: Tests the effectiveness of OpenCV preprocessing for OCR.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Key Changes and Additions:
1. **Advanced Image Preprocessing**: Added details about preprocessing images using OpenCV before performing OCR to improve accuracy.
2. **Python Version Requirement**: Updated to require Python 3.7+.
3. **Installation Section**: Included OpenCV installation instructions.
4. **Testing**: Added specifics about testing image preprocessing with OpenCV and OCR.
5. **Programmatic Usage**: Clarified how to use the package as a Python module.


## Changelog

### Version 0.2.0
- Added advanced image preprocessing (grayscale, binarization, and noise removal) using OpenCV to improve OCR accuracy.
- Modularized the `extract_text` function for better maintainability.

### Installation

To install the latest version:

```bash
pip install pdfcompare --upgrade

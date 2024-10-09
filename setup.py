from setuptools import setup, find_packages

setup(
    name="pdfcompare",  # Name of the package
    version="0.1.0",  # Initial version
    author="S M Shahinul Islam",
    author_email="s.m.shahinul.islam@gmail.com",
    description="A Python package to compare files (PDF, docx, images) and generate reports in txt, html, or PDF format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/imshahinul/pdfcompare",  # Optional, your GitHub URL
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        "pytesseract",
        "pillow",
        "fitz",
        "python-docx",
        "pdfkit",
        "argparse"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pdfcompare=pdfcompare.cli:main",  # Create a CLI command
        ],
    },
)
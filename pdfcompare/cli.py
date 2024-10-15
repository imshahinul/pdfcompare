import os
import sys
import click
import logging
import tempfile
from pdfcompare.file_handlers import load_handler
from difflib import unified_diff
from itertools import combinations

# Set up logging
logging.basicConfig(filename="pdfcompare.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def extract_text(file_path):
    """Extracts text from a file based on its extension."""
    _, ext = os.path.splitext(file_path)
    try:
        handler_module = load_handler(ext)
        return handler_module.extract_text(file_path)
    except Exception as e:
        logging.error(f"Error extracting text from {file_path}: {e}")
        raise ValueError(f"Failed to extract text from {file_path}: {e}")


def compare_texts(text1, text2):
    """Compares two texts and returns the differences."""
    try:
        diff = list(unified_diff(text1.splitlines(), text2.splitlines()))
        if not diff:
            return "No differences found."
        return "\n".join(diff)
    except Exception as e:
        logging.error(f"Error comparing texts: {e}")
        raise ValueError(f"Failed to compare texts: {e}")


def generate_report(file1, file2, result, output_format):
    """Generates a comparison report in the specified format."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as tmp_file:
        tmp_file.write(result.encode())
        report_path = tmp_file.name
        logging.info(f"{output_format.upper()} report saved to {report_path}.")
        return report_path


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Choice(['txt', 'html', 'pdf']), default='txt', help='Specify output format.')
def compare_files(files, output):
    """Compare multiple files and generate comparison reports."""
    try:
        # Ensure at least two files are provided
        if len(files) < 2:
            print("Please provide at least two files for comparison.")
            sys.exit(1)

        # Compare each pair of files
        reports = []
        for file1, file2 in combinations(files, 2):
            # Extract text from both files
            text1 = extract_text(file1)
            text2 = extract_text(file2)

            # Compare the texts
            result = compare_texts(text1, text2)

            # Generate and store the report
            report_path = generate_report(file1, file2, result, output)
            reports.append((file1, file2, report_path))

        # Output the paths of all generated reports
        for file1, file2, report_path in reports:
            print(f"Comparison report for {file1} and {file2} saved to: {report_path}")

    except Exception as e:
        logging.error(f"Error during file comparison: {e}")
        print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    compare_files()

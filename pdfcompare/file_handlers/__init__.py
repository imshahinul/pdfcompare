import importlib
import os

# List of available file format handlers
AVAILABLE_HANDLERS = {
    '.pdf': 'pdf_handler',
    '.docx': 'docx_handler',
    '.png': 'image_handler',
    '.jpg': 'image_handler',
    '.jpeg': 'image_handler',
    '.txt': 'txt_handler',
    '.epub': 'epub_handler',
    '.odt': 'odt_handler'
}

def load_handler(extension):
    """Dynamically loads the appropriate handler module for the given extension."""
    handler_module_name = AVAILABLE_HANDLERS.get(extension.lower())
    if not handler_module_name:
        raise ValueError(f"Unsupported file type: {extension}")

    module = importlib.import_module(f'pdfcompare.file_handlers.{handler_module_name}')
    return module

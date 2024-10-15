import pytesseract  # For OCR on images
import cv2  # OpenCV for image processing
import numpy as np
from PIL import Image  # Pillow for image handling
import logging

def preprocess_image(image):
    """Preprocess the image to improve OCR accuracy."""
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binarization (thresholding) - you can experiment with different threshold values
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Morphological operations to remove small noise (e.g., closing operation)
    kernel = np.ones((2, 2), np.uint8)
    processed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    return processed_image

def extract_text(file_path):
    """Extracts text from an image file using pytesseract with preprocessing."""
    try:
        # Read the image using OpenCV
        img_cv = cv2.imread(file_path)

        if img_cv is None:
            raise ValueError(f"Unable to read image file {file_path}")

        # Preprocess the image
        preprocessed_img = preprocess_image(img_cv)

        # Convert the processed OpenCV image back to a PIL image for pytesseract
        pil_image = Image.fromarray(preprocessed_img)

        # Run OCR on the preprocessed image
        text = pytesseract.image_to_string(pil_image)

        # Clean up the extracted text
        text = text.strip()  # Strip any extra whitespace
        return text
    except Exception as e:
        logging.error(f"Error extracting text from image {file_path}: {e}")
        raise ValueError(f"Failed to extract text from image {file_path}: {e}")

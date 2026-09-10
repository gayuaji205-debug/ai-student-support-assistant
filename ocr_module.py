"""Optional OCR support for scanned student notices."""

from pathlib import Path

try:
    from PIL import Image
    import pytesseract

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image with Tesseract, with friendly errors."""
    path = Path(image_path).expanduser()

    if not path.exists():
        return f"OCR error: file not found - {path}"

    if not OCR_AVAILABLE:
        return (
            "OCR is not installed. Run 'pip install -r requirements.txt' "
            "and install the Tesseract OCR application."
        )

    try:
        text = pytesseract.image_to_string(Image.open(path)).strip()
    except Exception as error:
        return f"OCR error: {error}"

    return text or "OCR completed, but no readable text was found."
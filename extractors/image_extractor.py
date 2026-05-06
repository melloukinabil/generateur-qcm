from PIL import Image
import pytesseract


def extract_text_from_image(file) -> str:
    """Extrait le texte d'une image via OCR (Tesseract)."""
    image = Image.open(file)
    text = pytesseract.image_to_string(image, lang="fra")
    return text.strip()

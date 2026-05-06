from PyPDF2 import PdfReader


def extract_text_from_pdf(file) -> str:
    """Extrait le texte d'un fichier PDF."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

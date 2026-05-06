from docx import Document


def extract_text_from_word(file) -> str:
    """Extrait le texte d'un fichier Word (.docx)."""
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text.strip()

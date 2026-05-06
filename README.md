# 📝 Générateur de QCM

Application web qui génère automatiquement des Questions à Choix Multiples (QCM) à partir de documents PDF, Word ou images.

## Fonctionnalités

- 📄 **PDF** : Extraction de texte depuis des fichiers PDF
- 📝 **Word** : Extraction depuis des fichiers .docx
- 🖼️ **Images** : Extraction via OCR (reconnaissance optique de caractères)
- 🤖 **IA** : Génération intelligente de QCM avec OpenAI GPT
- ⚙️ **Paramétrable** : Nombre de questions et niveau de difficulté ajustables

## Prérequis

- Python 3.9+
- Une clé API OpenAI
- Tesseract OCR (pour l'extraction depuis les images)

### Installation de Tesseract (pour les images)

- **Windows** : Télécharger depuis https://github.com/UB-Mannheim/tesseract/wiki
- **macOS** : `brew install tesseract`
- **Linux** : `sudo apt install tesseract-ocr tesseract-ocr-fra`

## Installation

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Configurer la clé API :
   - Copier `.env.example` en `.env`
   - Ajouter votre clé API OpenAI dans le fichier `.env`

## Lancement

```bash
streamlit run app.py
```

L'application sera accessible sur http://localhost:8501

## Utilisation

1. Téléversez un document (PDF, Word ou image)
2. Ajustez les paramètres (nombre de questions, difficulté)
3. Cliquez sur "Générer le QCM"
4. Consultez les questions générées avec les réponses et explications

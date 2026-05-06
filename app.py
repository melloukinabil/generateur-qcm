import streamlit as st
from extractors import extract_text_from_pdf, extract_text_from_word, extract_text_from_image
from generator import generate_qcm

st.set_page_config(page_title="Générateur de QCM", page_icon="📝", layout="wide")

st.title("📝 Générateur de QCM")
st.markdown("Générez automatiquement des questions à choix multiples à partir de vos documents (PDF, Word, Image).")

st.divider()

# --- Sidebar : paramètres ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    num_questions = st.slider("Nombre de questions", min_value=3, max_value=20, value=5)
    difficulty = st.selectbox("Niveau de difficulté", ["facile", "moyen", "difficile"])
    st.divider()
    st.header("🤖 Provider IA")
    st.markdown("""
    - **Ollama** : 100% local et gratuit ([ollama.com](https://ollama.com))
    - **Groq** : Cloud gratuit (clé sur [console.groq.com](https://console.groq.com))
    """)

# --- Upload de fichier ---
st.subheader("📂 Téléversez votre document")
uploaded_file = st.file_uploader(
    "Choisissez un fichier (PDF, DOCX ou Image)",
    type=["pdf", "docx", "png", "jpg", "jpeg"],
)

if uploaded_file is not None:
    file_type = uploaded_file.type
    st.success(f"Fichier chargé : **{uploaded_file.name}**")

    # --- Extraction du texte ---
    with st.spinner("Extraction du texte en cours..."):
        try:
            if file_type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_word(uploaded_file)
            elif file_type in ["image/png", "image/jpeg"]:
                text = extract_text_from_image(uploaded_file)
            else:
                st.error("Type de fichier non supporté.")
                st.stop()
        except Exception as e:
            st.error(f"Erreur lors de l'extraction : {e}")
            st.stop()

    if not text:
        st.warning("Aucun texte n'a pu être extrait du document.")
        st.stop()

    # --- Affichage du texte extrait ---
    with st.expander("📄 Texte extrait (aperçu)"):
        st.text(text[:2000] + ("..." if len(text) > 2000 else ""))

    # --- Génération du QCM ---
    if st.button("🚀 Générer le QCM", type="primary"):
        with st.spinner("Génération des questions en cours..."):
            try:
                qcm = generate_qcm(text, num_questions=num_questions, difficulty=difficulty)
                st.divider()
                st.subheader("📋 QCM Généré")
                st.markdown(qcm)
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")

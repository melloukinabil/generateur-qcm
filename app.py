import streamlit as st
from extractors import extract_text_from_pdf, extract_text_from_word, extract_text_from_image
from generator import generate_qcm

st.set_page_config(page_title="Générateur de QCM", page_icon="📝", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .block-container {
        padding-top: 2rem;
    }
    h1 {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.05);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📝 Générateur de QCM")
st.markdown('<p class="subtitle">Générez automatiquement des questions à choix multiples à partir de vos documents</p>', unsafe_allow_html=True)

# --- Feature cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <strong>PDF</strong><br>
        <small>Importez vos cours en PDF</small>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <strong>Word</strong><br>
        <small>Supportez les fichiers .docx</small>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🖼️</div>
        <strong>Images</strong><br>
        <small>OCR pour extraire le texte</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Sidebar : paramètres ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/quiz.png", width=80)
    st.header("⚙️ Paramètres")
    st.markdown("---")
    num_questions = st.slider("🔢 Nombre de questions", min_value=3, max_value=20, value=5)
    difficulty = st.selectbox("📊 Niveau de difficulté", ["facile", "moyen", "difficile"])
    st.markdown("---")
    st.markdown("💡 *Powered by AI open source*")

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

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Groq (gratuit) - clé gratuite sur https://console.groq.com
# En local: utilise .env | Sur Streamlit Cloud: utilise st.secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

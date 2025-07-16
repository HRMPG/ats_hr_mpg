
import streamlit as st
import os

st.set_page_config(page_title="Upload CV Kandidat", layout="centered")
st.title("📤 Upload CV untuk Lamaran Kerja")

uploaded_file = st.file_uploader("Silakan upload CV Anda (PDF atau DOCX)", type=["pdf", "docx"])

if uploaded_file:
    os.makedirs("uploaded_cvs", exist_ok=True)
    with open(f"uploaded_cvs/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("CV berhasil diupload! ✅")
    st.info("Terima kasih sudah melamar. Tim HR kami akan segera meninjau CV Anda.")

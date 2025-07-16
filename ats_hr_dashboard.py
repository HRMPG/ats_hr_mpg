
import streamlit as st
import os
import fitz  # PyMuPDF
import docx2txt
import pandas as pd

st.set_page_config(page_title="HR ATS Dashboard", layout="wide")
st.sidebar.title("🔐 HR Login")

USER_CREDENTIALS = {"admin": "hr123"}
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
    st.sidebar.success("Login Berhasil ✅")
    st.title("📊 HR ATS Dashboard - Filter & Penilaian CV")

    uploaded_files = st.file_uploader("Upload CV kandidat (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    keywords = st.text_input("Masukkan kata kunci pencarian (pisahkan dengan koma):")

    def extract_text(file):
        if file.name.endswith(".pdf"):
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                return "".join(page.get_text() for page in doc)
        elif file.name.endswith(".docx"):
            return docx2txt.process(file)
        return ""

    if uploaded_files and keywords:
        keys = [k.strip().lower() for k in keywords.split(",")]
        result_data = []

        for file in uploaded_files:
            content = extract_text(file)
            score = sum(1 for k in keys if k in content.lower())
            status = "Lolos" if score >= len(keys) // 2 else "Tidak Lolos"
            data = {"Nama File": file.name, "Skor": score, "Status": status}
            for k in keys:
                data[k] = "✅" if k in content.lower() else "❌"
            result_data.append(data)

        df = pd.DataFrame(result_data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Hasil sebagai CSV", csv, "hasil_ats.csv", "text/csv")
else:
    st.warning("Masukkan username dan password untuk akses dashboard HR.")
    st.stop()

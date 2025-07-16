
import streamlit as st
import os
import base64
import fitz  # PyMuPDF
import docx2txt
import pandas as pd

# ========== LOGIN SECTION ==========
st.set_page_config(page_title="HR ATS Dashboard", layout="centered")

st.sidebar.title("🔐 HR Login")

# Dummy credentials
USER_CREDENTIALS = {
    "admin": "hr123",  # kamu bisa ganti sesuai kebutuhan
}

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# ========== LOGIN CHECK ==========
if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
    st.sidebar.success("Login Berhasil ✅")

    # ========== ATS DASHBOARD ==========
    st.title("📄 Applicant Tracking System (ATS) - HR Dashboard")

    uploaded_files = st.file_uploader(
        "Upload CV files (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True
    )

    keywords = st.text_input("Masukkan kata kunci (pisahkan dengan koma):")
    st.markdown("---")

    def extract_text_from_file(file):
        if file.name.endswith(".pdf"):
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                return text
        elif file.name.endswith(".docx"):
            return docx2txt.process(file)
        return ""

    if uploaded_files and keywords:
        keyword_list = [k.strip().lower() for k in keywords.split(",")]
        st.subheader("📊 Hasil Pencarian")
        results = []

        for file in uploaded_files:
            text = extract_text_from_file(file)
            row = {"Nama File": file.name}
            for kw in keyword_list:
                row[kw] = "✅" if kw.lower() in text.lower() else "❌"
            results.append(row)

        df = pd.DataFrame(results)
        st.dataframe(df)

        # Download hasil sebagai CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Hasil sebagai CSV",
            data=csv,
            file_name="hasil_filter_ats.csv",
            mime="text/csv",
        )

else:
    st.warning("Masukkan username dan password untuk akses dashboard HR.")
    st.stop()

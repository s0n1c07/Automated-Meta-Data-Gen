import streamlit as st
from generate import generate_metadata

st.title("📄 Automated Metadata Generator")

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded!")

    with st.spinner("Generating metadata..."):
        metadata = generate_metadata(uploaded_file.name)

    st.subheader("📦 Extracted Metadata")
    st.json(metadata)

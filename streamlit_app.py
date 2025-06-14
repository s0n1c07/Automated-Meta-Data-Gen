import streamlit as st
import requests

st.title("Automated Metadata Generator")
uploaded = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf","docx","txt"])
if uploaded:
    # Assuming backend runs at localhost:8000
    files = {"file": (uploaded.name, uploaded.getvalue())}
    with st.spinner("Generating metadata..."):
        res = requests.post("http://localhost:8000/upload/", files=files)
    if res.status_code == 200:
        metadata = res.json()
        st.json(metadata)
    else:
        st.error(f"Error: {res.text}")

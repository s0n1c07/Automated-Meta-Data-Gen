# 📄 Automated Metadata Generator

This Streamlit web app lets you upload a document (PDF, DOCX, or TXT), extract its text using OCR (if needed), and generate useful metadata including:

- 🔍 Summary sections
- 🗝️ Keywords
- 🧠 Named Entities

It uses NLP techniques and pretrained models like `SentenceTransformer`, `spaCy`, and `RAKE` to extract meaningful insights.

---

## 🚀 Demo

Try it live on [Streamlit Cloud](https://share.streamlit.io/)  
*(Replace with your actual app link once deployed.)*

---

## 🛠️ Features

- **Text extraction** using `PyMuPDF`, `python-docx`, or `EasyOCR`
- **OCR fallback** for scanned PDFs
- **RAKE-based** keyword extraction
- **Sentence embeddings** for semantic summaries
- **Named entity recognition** using `spaCy`

---

## 🧠 Tech Stack
- Streamlit

- spaCy

- EasyOCR

- SentenceTransformers

- RAKE-NLTK

- PyMuPDF

---

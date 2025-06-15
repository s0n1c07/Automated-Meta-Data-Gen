# 📄 Automated Metadata Generator

A Streamlit‑based web app that automatically extracts rich, structured metadata from documents (PDF, DOCX, TXT) using OCR and NLP.

---

## 🚀 Features

- **Smart Text Extraction**  
  - Fast parsing of text‑based PDFs via PyMuPDF  
  - OCR fallback for scanned PDFs using EasyOCR  
  - DOCX & TXT support :contentReference[oaicite:10]{index=10}  

- **Semantic Summarization**  
  - Sentence‑transformer embeddings to pick the most representative sentences :contentReference[oaicite:11]{index=11}  

- **Entity Recognition & Profiling**  
  - spaCy for named‑entity extraction (PERSON, DATE, GPE, etc.) :contentReference[oaicite:12]{index=12}  
  - Language detection (langdetect) & timezone‑aware timestamps (pytz)  

- **Document Statistics**  
  - Character & word counts  
  - Estimated reading time  
  - Paragraph count  

- **Downloadable Plain‑Text Report**  
  - Read‑only report in the UI with one‑click download :contentReference[oaicite:13]{index=13}  

---

## 📁 Repository Structure

```text
.
├── generate.py          # Core logic: text extraction, summarization, NER, report assembly :contentReference[oaicite:14]{index=14}  
├── streamlit_app.py     # Streamlit UI: uploader, report display, download button :contentReference[oaicite:15]{index=15}  
├── requirements.txt     # Python dependencies :contentReference[oaicite:16]{index=16}  
├── Procfile             # (for platforms like Heroku/Render): start command :contentReference[oaicite:17]{index=17}  
└── README.md            # This documentation  

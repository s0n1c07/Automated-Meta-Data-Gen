import io
import fitz                        # PyMuPDF for fast PDF text
import easyocr                     # pure‑Python OCR for Streamlit Cloud
from pdf2image import convert_from_bytes
from docx import Document

# initialize the EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(path: str) -> str:
    ext = path.lower().split('.')[-1]
    if ext == 'txt':
        return open(path, 'r', encoding='utf-8').read()

    if ext == 'docx':
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == 'pdf':
        # 1) try the fast, text‑based extraction
        pdf = fitz.open(path)
        text = "".join(page.get_text() for page in pdf)

        # 2) if it came out almost empty, assume scanned → OCR with EasyOCR
        if len(text.strip()) < 50:
            # read the raw bytes of the PDF and convert to PIL images
            with open(path, 'rb') as f:
                pdf_bytes = f.read()
            images = convert_from_bytes(pdf_bytes)

            # run EasyOCR on each page image
            text = ""
            for img in images:
                # detail=0 returns only the text strings, paragraph=True tries to group lines
                page_text = reader.readtext(img, detail=0, paragraph=True)
                text += "\n".join(page_text) + "\n\n"

        return text

    raise ValueError(f"Unsupported file type: {ext}")
# ——————————————————————————————————————————————
# Make sure NLTK data and spaCy model are available
import nltk
from spacy.cli import download as spacy_download
import spacy

# Download NLTK corpora for RAKE
nltk.download('stopwords')
nltk.download('punkt')

# Load or download spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy_download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
# ——————————————————————————————————————————————
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rake_nltk import Rake

# These were initialized above:
# nlp
# (You could also move this line below if you prefer, but keep it after the download logic.)
sentencemodel = SentenceTransformer('all-MiniLM-L6-v2')
rake = Rake()

def semantic_sections(raw_text: str, top_n: int = 5):
    docs = [sent for sent in raw_text.split('\n') if len(sent) > 20]
    embeddings = sentencemodel.encode(docs)
    avg_emb = embeddings.mean(axis=0, keepdims=True)
    sims = cosine_similarity(embeddings, avg_emb).flatten()
    idx = sims.argsort()[-top_n:][::-1]
    return [docs[i] for i in idx]

def extract_keywords(raw_text: str, max_words: int = 20):
    rake.extract_keywords_from_text(raw_text)
    return [kw for kw, score in rake.get_ranked_phrases_with_scores()[:max_words]]
from pathlib import Path
import json
from datetime import datetime

def generate_metadata(path: str) -> dict:
    """
    Extract text, select semantic sections, keywords, and entities from the document at `path`,
    then serialize the metadata to a sidecar JSON file (filename_meta.json).
    Returns the metadata dict (or an error dict if something goes wrong).
    """
    p = Path(path)
    try:
        # 1. Raw text
        text = extract_text(str(p))

        # 2. Semantic summary & keywords
        summary_sections = semantic_sections(text, top_n=3)
        keywords = extract_keywords(text, max_words=15)

        # 3. Named entities (using spaCy)
        doc = nlp(text[:500])  # sample first 500 chars for quick heuristics
        entities = {
            ent.label_: list({e.text for e in doc.ents if e.label_ == ent.label_})
            for ent in doc.ents
        }

        # 4. Build metadata dict
        meta = {
            "filename": p.name,
            "extracted_on": datetime.utcnow().isoformat() + "Z",
            "length_chars": len(text),
            "summary_sections": summary_sections,
            "keywords": keywords,
            "entities": entities,
        }

        # 5. Write out to JSON next to original file
        out_path = p.with_name(p.stem + "_meta.json")
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return meta

    except Exception as e:
        # don’t crash your app—return the error message as metadata
        return {
            "filename": p.name,
            "error": str(e),
        }

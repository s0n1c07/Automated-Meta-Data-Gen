import io
import fitz                        # PyMuPDF for fast PDF text
import easyocr                     # OCR (models already cached at build time)
from pdf2image import convert_from_bytes
from docx import Document
from pathlib import Path
import json
from datetime import datetime

# initialize the EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

# spaCy model (already installed in your image)
import spacy
nlp = spacy.load("en_core_web_sm")

# sentence-transformers & RAKE (nltk data already in image)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rake_nltk import Rake

sentencemodel = SentenceTransformer('all-MiniLM-L6-v2')
rake = Rake()

def extract_text(path: str) -> str:
    ext = path.lower().split('.')[-1]
    if ext == 'txt':
        return Path(path).read_text(encoding='utf-8')

    if ext == 'docx':
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == 'pdf':
        pdf = fitz.open(path)
        text = "".join(page.get_text() for page in pdf)

        # if nearly empty, fall back to OCR
        if len(text.strip()) < 50:
            pdf_bytes = Path(path).read_bytes()
            images = convert_from_bytes(pdf_bytes)
            text = ""
            for img in images:
                page_text = reader.readtext(img, detail=0, paragraph=True)
                text += "\n".join(page_text) + "\n\n"

        return text

    raise ValueError(f"Unsupported file type: {ext}")


def semantic_sections(raw_text: str, top_n: int = 5):
    docs = [sent for sent in raw_text.split('\n') if len(sent) > 20]
    embeddings = sentencemodel.encode(docs)
    avg_emb = embeddings.mean(axis=0, keepdims=True)
    sims = cosine_similarity(embeddings, avg_emb).flatten()
    idx = sims.argsort()[-top_n:][::-1]
    return [docs[i] for i in idx]


def extract_keywords(raw_text: str, max_words: int = 20):
    rake.extract_keywords_from_text(raw_text)
    return [kw for kw, _ in rake.get_ranked_phrases_with_scores()[:max_words]]


def generate_metadata(path: str) -> dict:
    p = Path(path)
    try:
        # 1. Extract text from file
        text = extract_text(str(p))

        # 2. Semantic summary & keyword extraction
        summary_sections = semantic_sections(text, top_n=3)
        keywords = extract_keywords(text, max_words=15)

        # 3. Named-entity extraction
        doc = nlp(text[:500])  # sample first 500 chars
        entities = {
            ent.label_: list({e.text for e in doc.ents if e.label_ == ent.label_})
            for ent in doc.ents
        }

        # 4. Build metadata payload
        meta = {
            "filename": p.name,
            "extracted_on": datetime.utcnow().isoformat() + "Z",
            "length_chars": len(text),
            "summary_sections": summary_sections,
            "keywords": keywords,
            "entities": entities,
        }

        # 5. Write sidecar JSON
        out_path = p.with_name(p.stem + "_meta.json")
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return meta

    except Exception as e:
        # Return an error payload instead of crashing
        return {"filename": p.name, "error": str(e)}

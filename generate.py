import io
import fitz                        # PyMuPDF for fast PDF text
import easyocr                    # OCR
from docx import Document
from pathlib import Path
from datetime import datetime
from PIL import Image
import numpy as np

# spaCy and NLTK setup
import spacy
from spacy.cli import download as spacy_download
import nltk

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy_download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# Semantic similarity
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# sentencemodel = SentenceTransformer('all-MiniLM-L6-v2')
SentenceTransformer("paraphrase-albert-small-v2")

def extract_text(path: str) -> str:
    ext = path.lower().split('.')[-1]
    if ext == 'txt':
        return Path(path).read_text(encoding='utf-8')

        return Path(path).read_text(encoding='utf-8')

    if ext == 'docx':
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)


    if ext == 'pdf':
        pdf = fitz.open(path)
        text = "".join(page.get_text() for page in pdf)

        if len(text.strip()) < 50:
            text = ""
            for page in pdf:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csRGB)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_array = np.array(img)
                page_text = reader.readtext(img_array, detail=0, paragraph=True)
                text += "\n".join(str(seg) for seg in page_text) + "\n\n"
        return text


    raise ValueError(f"Unsupported file type: {ext}")


def semantic_sections(raw_text: str, top_n: int = 5) -> list[str]:
    docs = [sent.text.strip() for sent in nlp(raw_text).sents if len(sent.text.strip()) > 20]
    embeddings = sentencemodel.encode(docs)
    avg_emb = embeddings.mean(axis=0, keepdims=True)
    sims = cosine_similarity(embeddings, avg_emb).flatten()
    idx = sims.argsort()[-top_n:][::-1]
    return [docs[i] for i in idx]


def generate_metadata(path: str) -> str:
    from langdetect import detect
    from pytz import timezone

    p = Path(path)
    try:
        # 1. Extract text
        text = extract_text(str(p))

        # 2. Semantic summary & keywords
        summary_sections = semantic_sections(text, top_n=3)

        doc = nlp(text[:1000])
        entities_map: dict[str, set[str]] = {}
        for ent in doc.ents:
            entities_map.setdefault(ent.label_, set()).add(ent.text)
        entities = {label: sorted([str(v) for v in vals]) for label, vals in entities_map.items()}

        # Meta analysis
        language = detect(text)
        paragraphs = [p for p in text.split('\n') if p.strip()]
        doc_length = len(text)
        word_count = len(text.split())
        reading_time = word_count // 200 + 1
        dominant_entity = max(entities.items(), key=lambda x: len(x[1]))[0] if entities else "N/A"

        # Assemble report
        lines: list[str] = []
        lines.append(f"Filename: {p.name}")
        lines.append(f"Extracted on: {datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST')}")
        lines.append(f"Document length: {doc_length} characters")
        lines.append(f"Word count: {word_count}")
        lines.append(f"Approx. Reading Time: {reading_time} min")
        lines.append(f"Paragraphs: {len(paragraphs)}")
        lines.append(f"Detected Language: {language.upper()}")
        lines.append(f"Dominant Entity Type: {dominant_entity}")

        lines.append("\n=== Summary Sections ===")
        for i, sec in enumerate(summary_sections, 1):
            snippet = str(sec).strip().replace("\n", " ")
            if len(snippet) > 200:
                snippet = snippet[:197].rsplit(" ", 1)[0] + "..."
            lines.append(f"{i}. {snippet}")

        lines.append("\n=== Named Entities ===")
        for label, vals in entities.items():
            lines.append(f"{label}: {', '.join(vals)}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error processing {p.name}:\n{str(e)}"

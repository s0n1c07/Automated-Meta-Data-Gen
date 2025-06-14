import streamlit as st

st.write("Starting app…")

# ——————————————————————————————————————————————
# Load and cache all heavy models & readers
@st.cache_resource
def load_models():
    import easyocr
    import spacy
    from spacy.cli import download as spacy_download
    from sentence_transformers import SentenceTransformer
    from rake_nltk import Rake
    import nltk

    # NLTK requirements for RAKE
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    # EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    # SpaCy model (download if missing)
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        spacy_download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # Sentence embedding model
    sentencemodel = SentenceTransformer('all-MiniLM-L6-v2')

    # RAKE keyword extractor
    rake = Rake()

    return reader, nlp, sentencemodel, rake

reader, nlp, sentencemodel, rake = load_models()
# ——————————————————————————————————————————————

# Now import your pipeline function
from generate import generate_metadata

st.title("📄 Automated Metadata Generator")

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    # save upload to a temp file
    tmp_path = f"{uploaded_file.name}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded!")

    with st.spinner("Generating metadata..."):
        metadata = generate_metadata(tmp_path)

    st.subheader("📦 Extracted Metadata")
    st.json(metadata)

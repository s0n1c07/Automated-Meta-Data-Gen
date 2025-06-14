# predownload.py

# 1. spaCy
import spacy
from spacy.cli import download as spacy_download

try:
    spacy.load("en_core_web_sm")
except OSError:
    spacy_download("en_core_web_sm")
    spacy.load("en_core_web_sm")

# 2. Sentence‐transformers
from sentence_transformers import SentenceTransformer
_ = SentenceTransformer('all-MiniLM-L6-v2')

# 3. EasyOCR
import easyocr
_ = easyocr.Reader(['en'], gpu=False)

# 4. (Optional) Pre‐warm RAKE’s NLTK corpora
import nltk
nltk.download('punkt')
nltk.download('stopwords')
print("All models downloaded and cached.")

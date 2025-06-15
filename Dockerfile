# 1. Start from a slim Python base
FROM python:3.10-slim

# 2. Install OS‑level deps needed for PDF/OCR
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      tesseract-ocr \
      poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# 3. Set working dir
WORKDIR /app

# 4. Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy predownload script and run it at build time
COPY predownload.py .
RUN python predownload.py

# 6. Copy the rest of your app code
COPY . .

# 7. Expose Streamlit’s port and start the app
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

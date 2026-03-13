FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the HuggingFace model at build time so first request isn't slow
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

COPY . .

EXPOSE 7860

CMD ["gunicorn", "backend.core.app:app", "--bind", "0.0.0.0:7860", "--timeout", "120"]

# GCIQS — Genomic Compression & Intelligent Query System

A research prototype for hybrid retrieval-augmented genomic QnA,
powered by Groq LLM inference.

## Architecture

```
┌──────────────┐       ┌──────────────────────────┐       ┌─────────────┐
│   Frontend   │──SSE──│   FastAPI Backend         │──API──│  Groq LLM   │
│  HTML/JS/CSS │       │                          │       │ (llama-3)   │
└──────────────┘       │  ┌─────────┐ ┌────────┐  │       └─────────────┘
                       │  │ FAISS   │ │Symbolic│  │
                       │  │ Vector  │ │ Index  │  │
                       │  │ Store   │ │(BM25)  │  │
                       │  └────┬────┘ └───┬────┘  │
                       │       └────┬─────┘       │
                       │       Hybrid Retriever    │
                       └──────────────────────────┘
```

**Query pipeline:**
1. User submits genomic query from the frontend.
2. Backend runs hybrid retrieval: BM25 keyword matching + FAISS cosine similarity.
3. Top-k documents are merged via reciprocal rank fusion (RRF).
4. Context + query sent to Groq (llama-3-70b) with a genomics system prompt.
5. Response streamed back via SSE to the frontend.

## Quick Start

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
python main.py
```

Then open `frontend/index.html` in a browser (or serve via `python -m http.server 8080` from the frontend dir).

## Folder Structure

```
gciqs/
├── README.md
├── backend/
│   ├── main.py              # FastAPI app, endpoints
│   ├── retriever.py         # Hybrid retrieval (FAISS + BM25)
│   ├── groq_client.py       # Groq API integration, streaming
│   ├── genomic_db.py        # Mock genomic knowledge base
│   ├── embeddings.py        # Sentence embeddings via all-MiniLM
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── data/
    └── (FAISS index files, auto-generated on first run)
```

## Environment Variables

```
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=2048
```

## Docker (optional)

```bash
cd backend
docker build -t gciqs-backend .
docker run -p 8000:8000 --env-file .env gciqs-backend
```

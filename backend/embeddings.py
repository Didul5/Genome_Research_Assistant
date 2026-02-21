"""
embeddings.py — Thin wrapper around sentence-transformers.

Uses all-MiniLM-L6-v2 (384-dim) because it's small, fast, and
good enough for a prototype. In production you'd swap for a
domain-specific biomedical model (e.g., BioLinkBERT, PubMedBERT).
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# lazy-load so the import doesn't block if we just need types
_model = None

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


def _get_model():
    global _model
    if _model is None:
        print(f"[embeddings] loading {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
        print(f"[embeddings] model loaded ({EMBEDDING_DIM}-dim)")
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    """Encode a list of strings into an (N, 384) float32 array."""
    model = _get_model()
    vecs = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return vecs.astype(np.float32)


def embed_query(query: str) -> np.ndarray:
    """Encode a single query string. Returns shape (1, 384)."""
    return embed_texts([query])

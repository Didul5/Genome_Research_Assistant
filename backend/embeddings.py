"""
embeddings.py — Lightweight TF-IDF vectorizer.

Replaces sentence-transformers + FAISS for Vercel deployment.
sentence-transformers pulls in pytorch (~2GB) which blows past
Vercel's 250MB function size limit. TF-IDF is ~0 extra deps
and still works well for our small curated knowledge base where
exact keyword overlap matters more than deep semantic similarity.

The hybrid retrieval (TF-IDF + BM25 with RRF) still gives solid
results because our corpus is domain-specific and queries use
the same vocabulary as the documents.
"""

import math
import re
from collections import defaultdict


def _tokenize(text: str) -> list[str]:
    """Lowercased alphanumeric tokens."""
    return re.findall(r"[a-z0-9]+", text.lower())


class TfidfVectorizer:
    """Minimal TF-IDF vectorizer. No sklearn needed."""

    def __init__(self):
        self.vocab: dict[str, int] = {}  # token -> index
        self.idf: dict[str, float] = {}
        self.doc_vectors: list[dict[str, float]] = []  # sparse vectors

    def fit(self, texts: list[str]):
        """Build vocabulary and IDF weights from corpus."""
        n_docs = len(texts)
        doc_freq: dict[str, int] = defaultdict(int)
        all_tokens_per_doc = []

        for text in texts:
            tokens = _tokenize(text)
            all_tokens_per_doc.append(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                doc_freq[t] += 1

        # build vocab from all tokens that appear
        all_tokens = sorted(doc_freq.keys())
        self.vocab = {t: i for i, t in enumerate(all_tokens)}

        # IDF: log(N / df) + 1  (smoothed)
        self.idf = {}
        for token, df in doc_freq.items():
            self.idf[token] = math.log(n_docs / (df + 1)) + 1.0

        # compute sparse TF-IDF vectors for each doc
        self.doc_vectors = []
        for tokens in all_tokens_per_doc:
            tf: dict[str, float] = defaultdict(float)
            for t in tokens:
                tf[t] += 1.0
            # normalize TF by doc length
            length = len(tokens) or 1
            vec = {}
            for t, count in tf.items():
                if t in self.idf:
                    vec[t] = (count / length) * self.idf[t]
            # L2 normalize
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            vec = {t: v / norm for t, v in vec.items()}
            self.doc_vectors.append(vec)

    def query(self, text: str, top_k: int = 10) -> list[tuple[int, float]]:
        """Return (doc_idx, cosine_similarity) for top_k matches."""
        tokens = _tokenize(text)
        tf: dict[str, float] = defaultdict(float)
        for t in tokens:
            tf[t] += 1.0
        length = len(tokens) or 1

        # build query vector
        q_vec = {}
        for t, count in tf.items():
            if t in self.idf:
                q_vec[t] = (count / length) * self.idf[t]
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
        q_vec = {t: v / norm for t, v in q_vec.items()}

        # cosine similarity against all docs (sparse dot product)
        scores = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            sim = sum(q_vec.get(t, 0) * doc_vec.get(t, 0) for t in q_vec)
            if sim > 0:
                scores.append((idx, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
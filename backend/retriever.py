"""
retriever.py — Hybrid retrieval: TF-IDF (dense-ish) + BM25 (sparse).

Merges results with Reciprocal Rank Fusion (RRF). Replaced FAISS +
sentence-transformers with a lightweight TF-IDF vectorizer so the
whole backend fits in Vercel's 250MB serverless function limit.

BM25 catches exact gene names and mutation codes.
TF-IDF catches broader topical similarity.
RRF fuses both rankings into a single score.
"""

import math
import re
from collections import defaultdict

from embeddings import TfidfVectorizer
from genomic_db import get_all_documents

# ── BM25 (minimal implementation, no external dep) ────────

def _tokenize(text: str) -> list[str]:
    """Lowercased alphanumeric tokens. Good enough for gene names."""
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    """Okapi BM25 scorer. k1=1.5, b=0.75 — standard defaults."""

    def __init__(self, corpus_tokens: list[list[str]], k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus_tokens)
        self.doc_lens = [len(d) for d in corpus_tokens]
        self.avgdl = sum(self.doc_lens) / max(self.corpus_size, 1)

        # inverted index: token -> {doc_idx: term_freq}
        self.inv_index: dict[str, dict[int, int]] = defaultdict(dict)
        for idx, tokens in enumerate(corpus_tokens):
            freq: dict[str, int] = defaultdict(int)
            for t in tokens:
                freq[t] += 1
            for t, f in freq.items():
                self.inv_index[t][idx] = f

        # IDF cache
        self.idf: dict[str, float] = {}
        for token, postings in self.inv_index.items():
            df = len(postings)
            self.idf[token] = math.log(
                (self.corpus_size - df + 0.5) / (df + 0.5) + 1.0
            )

    def score(self, query_tokens: list[str], top_k: int = 10) -> list[tuple[int, float]]:
        """Return list of (doc_idx, score) sorted descending."""
        scores = defaultdict(float)
        for qt in query_tokens:
            if qt not in self.inv_index:
                continue
            for doc_idx, tf in self.inv_index[qt].items():
                dl = self.doc_lens[doc_idx]
                num = tf * (self.k1 + 1)
                denom = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                scores[doc_idx] += self.idf[qt] * num / denom
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


# ── Hybrid Retriever ──────────────────────────────────────

class HybridRetriever:
    """
    Combines TF-IDF (cosine similarity) and BM25 (keyword matching)
    using reciprocal rank fusion.
    """

    def __init__(self):
        self.documents = []
        self.tfidf = None
        self.bm25 = None
        self._built = False
        self.index_size = 0

    def build_index(self):
        """Load documents, build both indexes."""
        self.documents = get_all_documents()
        texts = [self._doc_text(d) for d in self.documents]

        # TF-IDF vectorizer (replaces FAISS + sentence-transformers)
        print("[retriever] building TF-IDF index ...")
        self.tfidf = TfidfVectorizer()
        self.tfidf.fit(texts)
        print(f"[retriever] TF-IDF index built: {len(texts)} docs, {len(self.tfidf.vocab)} terms")

        # BM25
        corpus_tokens = [_tokenize(t) for t in texts]
        self.bm25 = BM25(corpus_tokens)
        print(f"[retriever] BM25 index built: {len(corpus_tokens)} docs")

        self.index_size = len(self.documents)
        self._built = True

    @staticmethod
    def _doc_text(doc: dict) -> str:
        """Concatenate searchable fields into one string."""
        return f"{doc['title']} {doc.get('gene', '')} {doc['content']}"

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Run hybrid search and return top_k documents with scores.
        """
        if not self._built:
            self.build_index()

        # ── dense-ish retrieval (TF-IDF cosine) ───────────
        dense_ranking = self.tfidf.query(query, top_k=top_k * 2)

        # ── sparse retrieval (BM25) ───────────────────────
        q_tokens = _tokenize(query)
        sparse_ranking = self.bm25.score(q_tokens, top_k=top_k * 2)

        # ── reciprocal rank fusion ─────────────────────────
        fused = self._rrf(dense_ranking, sparse_ranking, k=60)

        # assemble results
        results = []
        for doc_idx, rrf_score in fused[:top_k]:
            if 0 <= doc_idx < len(self.documents):
                doc = self.documents[doc_idx].copy()
                doc["score"] = round(rrf_score, 4)
                results.append(doc)
        return results

    @staticmethod
    def _rrf(
        *rankings: list[tuple[int, float]], k: int = 60
    ) -> list[tuple[int, float]]:
        """
        Reciprocal Rank Fusion.
        score(d) = sum over rankings of 1 / (k + rank(d))
        """
        fused_scores: dict[int, float] = defaultdict(float)
        for ranking in rankings:
            for rank, (doc_idx, _score) in enumerate(ranking):
                fused_scores[doc_idx] += 1.0 / (k + rank + 1)
        return sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)


# module-level singleton
retriever = HybridRetriever()
"""
groq_client.py — Groq API integration for LLM-based genomic reasoning.

Uses raw httpx instead of the groq SDK to avoid version conflicts
(groq SDK passes `proxies=` which httpx>=0.28 removed).
This is also more transparent — you can see exactly what hits the wire.
"""

import json
import os
from typing import Generator

import httpx

# ── config ─────────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "2048"))
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ── system prompt ──────────────────────────────────────────

GENOMICS_SYSTEM_PROMPT = """\
You are a genomics and molecular biology research assistant with deep expertise
in cancer genetics, variant interpretation, CRISPR technology, and clinical
oncology. You have access to a curated knowledge base of genomic annotations,
pathway descriptions, and clinical guidelines.

When answering questions:
1. Ground your response in the provided reference documents. Cite them by
   their document IDs (e.g., [DOC-001]) when you use information from them.
2. Distinguish between well-established facts and emerging research.
3. Use precise molecular biology terminology but explain complex concepts
   when appropriate.
4. For clinical questions, note that your answers are informational and
   should not replace professional medical advice.
5. If the provided context is insufficient to fully answer the question,
   say so explicitly — do not fabricate information.
6. Structure your answer clearly: start with a direct answer, then provide
   supporting detail and mechanism where relevant.
7. When discussing mutations, include the standard nomenclature (HGVS)
   and note the functional consequence (gain/loss of function, etc.).
"""


def _format_context(documents: list[dict]) -> str:
    """Format retrieved documents into a context block for the LLM."""
    if not documents:
        return "No relevant documents were retrieved."

    parts = []
    for doc in documents:
        refs = "; ".join(doc.get("references", []))
        parts.append(
            f"--- [{doc['id']}] {doc['title']} ---\n"
            f"Type: {doc['type']} | Gene: {doc.get('gene', 'N/A')}\n"
            f"{doc['content']}\n"
            f"References: {refs}\n"
        )
    return "\n".join(parts)


def _build_messages(query: str, context_docs: list[dict]) -> list[dict]:
    """Assemble the chat messages array for the Groq API."""
    context_block = _format_context(context_docs)

    return [
        {"role": "system", "content": GENOMICS_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"## Retrieved Context\n\n{context_block}\n\n"
                f"## Question\n\n{query}\n\n"
                "Please provide a thorough, well-cited answer based on the "
                "context above."
            ),
        },
    ]


# ── streaming completion (raw httpx, no SDK) ───────────────

def stream_genomic_answer(
    query: str,
    context_docs: list[dict],
) -> Generator[str, None, None]:
    """
    Send query + context to Groq's OpenAI-compatible endpoint
    and yield response tokens as they arrive.

    Uses httpx directly to avoid the groq SDK's proxies= bug
    with httpx>=0.28.
    """
    if not GROQ_API_KEY:
        yield "[ERROR] GROQ_API_KEY not configured. Set it in .env.\n"
        return

    messages = _build_messages(query, context_docs)

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": GROQ_TEMPERATURE,
        "max_tokens": GROQ_MAX_TOKENS,
        "stream": True,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # use httpx streaming — works with any httpx version
    with httpx.Client(timeout=60.0) as client:
        with client.stream(
            "POST",
            GROQ_API_URL,
            json=payload,
            headers=headers,
        ) as response:
            if response.status_code != 200:
                # read full error body
                response.read()
                error_text = response.text
                yield f"[ERROR] Groq API returned {response.status_code}: {error_text}\n"
                return

            # parse SSE lines from the Groq response stream
            for line in response.iter_lines():
                if not line or not line.startswith("data: "):
                    continue

                data_str = line[6:]  # strip "data: "

                if data_str.strip() == "[DONE]":
                    break

                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
                except (json.JSONDecodeError, KeyError, IndexError):
                    # malformed chunk, skip
                    continue


def get_genomic_answer(query: str, context_docs: list[dict]) -> str:
    """Non-streaming version. Useful for testing."""
    parts = list(stream_genomic_answer(query, context_docs))
    return "".join(parts)
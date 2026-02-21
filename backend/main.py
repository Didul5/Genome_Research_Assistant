

import json
import os
import sys
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse


# so that `from retriever import ...` works regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retriever import retriever
from groq_client import stream_genomic_answer

load_dotenv()


# ── app lifecycle ──────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: build retrieval indexes
    print("[main] building indexes on startup ...")
    retriever.build_index()
    print("[main] ready.")
    yield


app = FastAPI(
    title="GCIQS",
    description="Genomic Compression & Intelligent Query System",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — wide open for dev, tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── health check ───────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "index_size": retriever.index_size,
        "timestamp": time.time(),
    }


# ── query endpoint (SSE) ──────────────────────────────────

@app.post("/query")
async def query_endpoint(request: Request):
    body = await request.json()
    user_query = body.get("query", "").strip()

    if not user_query:
        return JSONResponse(
            status_code=400,
            content={"error": "query field is required"},
        )

    top_k = min(int(body.get("top_k", 5)), 10)

    # step 1: hybrid retrieval
    retrieved_docs = retriever.search(user_query, top_k=top_k)

    # step 2: stream LLM response as SSE
    def event_stream():
        # first, emit the retrieved references so the frontend can show them
        refs_payload = []
        for doc in retrieved_docs:
            refs_payload.append({
                "id": doc["id"],
                "title": doc["title"],
                "type": doc["type"],
                "gene": doc.get("gene", ""),
                "score": doc.get("score", 0),
                "references": doc.get("references", []),
            })
        yield f"data: {json.dumps({'type': 'references', 'data': refs_payload})}\n\n"

        # then stream the LLM answer token by token
        try:
            for token in stream_genomic_answer(user_query, retrieved_docs):
                yield f"data: {json.dumps({'type': 'token', 'data': token})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"

        # signal completion
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ── run directly for local development ─────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

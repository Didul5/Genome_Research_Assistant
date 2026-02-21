📘 Genome Research Assistant – Complete Project Documentation
1️⃣ Project Overview

The Genome Research Assistant is a Retrieval-Augmented Generation (RAG) based AI system that:

Accepts genomic research queries

Retrieves relevant genomic knowledge

Generates contextual AI-powered responses using Groq LLM

Deploys frontend on Vercel

Runs backend as API service (FastAPI)

2️⃣ System Architecture
High-Level Flow
User (Frontend)
      ↓
FastAPI Backend (main.py)
      ↓
Retriever (retriever.py)
      ↓
Embeddings (embeddings.py)
      ↓
Genomic Database (genomic_db.py)
      ↓
Groq LLM (groq_client.py)
      ↓
Response to Frontend
3️⃣ Frontend Documentation

Location: /frontend

📄 index.html
Purpose

Defines the UI structure of the application.

Responsibilities:

Provides input box for genomic queries

Contains chat display container

Connects to script.js

Loads styles.css

Key Components:

Input field (user question)

Submit button

Chat response display area

📄 script.js
Purpose

Handles frontend logic and API communication.

Responsibilities:

Captures user input

Sends POST request to backend API

Displays AI response dynamically

Handles loading states / errors

Likely Flow:
fetch("/api/query", {
  method: "POST",
  body: JSON.stringify({ question: userInput })
})
Key Features:

Asynchronous request handling

JSON parsing

DOM manipulation

📄 styles.css
Purpose

Defines visual design and layout.

Responsibilities:

Chat bubble styling

Button design

Responsive layout

Fonts and color scheme

4️⃣ Backend Documentation

Location: /backend

Framework: FastAPI

📄 main.py
Purpose

Main API entry point.

Responsibilities:

Creates FastAPI app

Defines API routes

Handles incoming requests

Calls retriever + Groq client

Returns response

Likely Endpoint:
@app.post("/query")
async def query(data: QueryRequest):
Workflow Inside main.py:

Receive user question

Pass question to retriever

Get relevant genomic context

Send context + question to Groq

Return generated answer

📄 groq_client.py
Purpose

Handles communication with Groq API.

Responsibilities:

Initializes Groq client

Sends prompt to LLM

Handles response parsing

Manages API key from .env

Key Concepts:

Uses Groq SDK

Model likely: llama-3-70b or similar

Constructs prompt with context

Security:

API key loaded via:

os.getenv("GROQ_API_KEY")
📄 retriever.py
Purpose

Implements retrieval mechanism (RAG component).

Responsibilities:

Accepts user query

Converts query into embedding

Searches genomic database

Returns most relevant chunks

Core Idea:

Similarity search between:

Query embedding

Stored genomic embeddings

📄 embeddings.py
Purpose

Handles text embedding generation.

Responsibilities:

Converts genomic text into vectors

Converts user query into embedding

Uses embedding model (possibly HuggingFace)

Likely Flow:
embedding_model.encode(text)

Embeddings are used by retriever.py.

📄 genomic_db.py
Purpose

Stores genomic knowledge base.

Responsibilities:

Loads genomic dataset

Structures data into chunks

Stores embeddings

Provides searchable interface

Could Include:

Gene information

DNA sequence explanations

Mutation data

Research abstracts

This acts as your local vector database layer.

📄 requirements.txt
Purpose

Lists Python dependencies.

Expected Dependencies:

fastapi

uvicorn

groq

numpy

sentence-transformers

pydantic

python-dotenv

Used during:

pip install -r requirements.txt
📄 .env
Purpose

Stores environment variables.

Example:

GROQ_API_KEY=your_api_key

⚠️ Should not be committed to GitHub.

📄 .env.example

Template file for developers to know required variables.

📄 Dockerfile
Purpose

Containerizes backend.

Responsibilities:

Defines Python base image

Installs dependencies

Copies backend code

Runs FastAPI server

Typical Structure:
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Enables Docker deployment.

5️⃣ vercel.json
Purpose

Configures Vercel deployment.

Responsibilities:

Defines routing rules

Connects frontend with backend

Sets API rewrites

Example use:

Redirect /api/* to backend service

6️⃣ api.txt

Likely contains:

API endpoint documentation

Example request/response format

Used for:

Developer reference

Postman testing

7️⃣ .gitignore
Purpose

Prevents committing:

.env

venv

pycache

node_modules

Critical for security.

8️⃣ RAG Pipeline Explanation

Your system uses Retrieval-Augmented Generation:

Step 1 – User Query

User asks genomic question.

Step 2 – Query Embedding

Converted into vector representation.

Step 3 – Similarity Search

Searches genomic knowledge base.

Step 4 – Context Assembly

Top-k relevant chunks selected.

Step 5 – Prompt Construction

Prompt = Context + User Question

Step 6 – Groq LLM

LLM generates scientific response.

Step 7 – Return Answer
9️⃣ Deployment Architecture
Frontend

Hosted on Vercel

Static HTML/CSS/JS

Backend

FastAPI service

Can run:

Docker

Railway

Render

VPS

Groq API is external inference engine.

🔟 Security Considerations

API key hidden in backend

No direct frontend LLM access

Environment variables protected

.env excluded via .gitignore

1️⃣1️⃣ Strengths of Your Project

✅ Modular architecture
✅ Clean separation frontend/backend
✅ RAG implementation
✅ Production-ready Groq integration
✅ Docker support
✅ Vercel deployment compatible

1️⃣2️⃣ Suggested Improvements

Add vector database (FAISS / Chroma)

Add streaming responses

Add citation references in output

Add rate limiting

Add logging middleware

Add scientific source attribution

Add async embedding batching

1️⃣3️⃣ How to Run Locally
Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Frontend

Open:

frontend/index.html
1️⃣4️⃣ Future Scope

CRISPR gene editing assistant

Research paper summarization

DNA sequence analyzer

Mutation impact predictor

Biomedical RAG over PubMed

---
id: 004
title: Build RAG Chatbot Backend Service
stage: green
date: 2025-12-24
surface: agent
model: claude-code
feature: rag-chatbot-backend
branch: 001-rag-chatbot-backend
user: Mudasir Ali
command: Build RAG chatbot backend for textbook Q&A
labels: ["backend", "rag", "fastapi", "ai"]
links:
  spec: specs/001-rag-chatbot-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/requirements.txt
  - backend/src/services/rag_service.py
  - backend/src/services/qdrant_service.py
  - backend/src/services/cohere_service.py
  - backend/src/services/gemini_service.py
  - backend/src/api/rag_routes.py
tests:
  - pytest tests/ -v
---

## Prompt

Build a RAG (Retrieval Augmented Generation) chatbot backend service that answers questions about the Physical AI textbook content using vector embeddings and LLM.

## Response snapshot

Implemented complete RAG chatbot backend:

### Architecture
- FastAPI application with uvicorn server
- Qdrant vector database for embeddings storage
- Cohere for text embeddings (embed-english-v3.0)
- Gemini/OpenAI for response generation
- Optional PostgreSQL for chat history

### Key Services
1. **RAG Service**: Main orchestration service
2. **Qdrant Service**: Vector database operations
3. **Cohere Service**: Embedding generation
4. **Gemini Service**: Google's LLM for responses
5. **OpenAI Agents RAG**: Alternative LLM via OpenRouter

### API Endpoints
- POST /rag/query - Process user questions
- GET /health - Health check

### Document Processing
- process_textbook_content.py scripts indexes all markdown files
- Chunks text into manageable pieces
- Generates and stores embeddings in Qdrant

### Configuration
- OpenRouter API key (cost-effective OpenAI access)
- Cohere API key (embeddings)
- Qdrant URL and API key
- Optional DATABASE_URL for chat history

## Outcome

- ✅ Impact: Full RAG chatbot backend implemented
- 🧪 Tests: Backend starts successfully, API endpoints functional
- 📁 Files: Complete backend/ directory with services, API routes, models
- 🔁 Next prompts: Integrate chatbot UI with Docusaurus frontend
- 🧠 Reflection: Modular service architecture enables easy swapping of LLM providers

## Evaluation notes (flywheel)

- Failure modes observed: Initial startup issues with missing API keys - added graceful handling
- Graders run and results: Backend starts with warnings when API keys missing
- Prompt variant: N/A
- Next experiment: Frontend integration

# Physical AI & Humanoid Robotics RAG Backend

This is the backend service for the Retrieval-Augmented Generation (RAG) chatbot that answers questions about the Physical AI & Humanoid Robotics textbook content. The system uses OpenAI Agents, Cohere embeddings, and Qdrant vector database to provide accurate, context-aware responses.

## Overview

The RAG Chatbot Backend is a FastAPI application that:
- Accepts user questions and optional selected text as input
- Retrieves relevant text chunks from Qdrant vector database
- Generates answers using OpenAI via OpenRouter (cost-effective)
- Ensures responses are grounded only in retrieved textbook content
- Automatically indexes all textbook content from the docs/ directory
- Logs retrieval metrics and performance data

## API Endpoints

- `POST /rag/query` - Process user queries against textbook content
- `GET /health` - Health check endpoint

### Query Endpoint

Request body:
```json
{
  "question": "Your question about textbook content",
  "selected_text": "Optional selected text for additional context (can be null)",
  "query_id": "Optional query ID (auto-generated if not provided)"
}
```

Response:
```json
{
  "response": "Generated answer based on retrieved content",
  "query_id": "Unique query identifier",
  "retrieval_score": "Average similarity score of retrieved chunks (0.0-1.0)",
  "chunks_count": "Number of chunks used to generate the response",
  "timestamp": "ISO 8601 timestamp"
}
```

## Configuration

The service is configured through environment variables:

- `OPENROUTER_API_KEY`: OpenRouter API key (required for RAG functionality - cost-effective option)
- `QDRANT_URL`: Qdrant database URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the collection to use (default: "textbook-content")
- `COHERE_API_KEY`: Cohere API key (for embeddings)
- `USE_OPENROUTER`: Set to "true" to use OpenRouter backend (default: "true" for cost-effective operation)
- `USE_OPENAI_AGENTS`: Set to "true" to use OpenAI Agents SDK with OpenRouter (default: "false")

## How to Use with the Textbook

This backend powers the chatbot on the [Physical AI & Humanoid Robotics Textbook](https://mudasiralilaghari.github.io/hackathon-physical-ai-humanoid-textbook/). When you ask questions on the textbook site, they are processed by this backend service.

## Environment Variables Setup

To run this service, you need to set up the following secrets in your Hugging Face Space:

1. `OPENROUTER_API_KEY` - Your OpenRouter API key
2. `COHERE_API_KEY` - Your Cohere API key
3. `QDRANT_URL` - Your Qdrant database URL
4. `QDRANT_API_KEY` - Your Qdrant API key (if using cloud version)
5. `DATABASE_URL` - Your Postgres database URL (optional, for chat history)

## Architecture

The service follows a modular architecture with the following components:

- `app.py`: Hugging Face Space entry point
- `main.py`: FastAPI application entry point
- `src/models/`: Data models and Pydantic schemas
- `src/services/`: Core business logic services
  - `rag_service.py`: Main orchestration service
  - `qdrant_service.py`: Vector database integration
  - `cohere_service.py`: Embedding generation
  - `openrouter_service.py`: OpenRouter integration
- `src/agents/`: AI agent implementations
- `src/api/`: API routes and endpoints
- `src/utils/`: Utility functions and logging
- `process_textbook_content.py`: Script to process and index textbook content
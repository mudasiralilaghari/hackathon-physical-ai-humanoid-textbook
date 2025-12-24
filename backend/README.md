# RAG Chatbot Backend

This is the backend service for the Retrieval-Augmented Generation (RAG) chatbot that answers questions about the Physical AI & Humanoid Robotics textbook content. The system uses OpenAI Agents, Cohere embeddings, and Qdrant vector database to provide accurate, context-aware responses.

## Overview

The RAG Chatbot Backend is a FastAPI application that:
- Accepts user questions and optional selected text as input
- Retrieves relevant text chunks from Qdrant vector database
- Generates answers using OpenAI Agents via OpenRouter (cost-effective)
- Ensures responses are grounded only in retrieved textbook content
- Automatically indexes all textbook content from the docs/ directory
- Logs retrieval metrics and performance data

## Architecture

The service follows a modular architecture with the following components:

- `main.py`: FastAPI application entry point
- `src/models/`: Data models and Pydantic schemas
- `src/services/`: Core business logic services
  - `rag_service.py`: Main orchestration service
  - `qdrant_service.py`: Vector database integration
  - `cohere_service.py`: Embedding generation
  - `gemini_service.py`: AI response generation
  - `openai_agents_rag_service.py`: OpenAI Agents integration
- `src/agents/`: AI agent implementations
  - `openai_agents_rag_agent.py`: OpenAI Agents RAG implementation
- `src/api/`: API routes and endpoints
- `src/utils/`: Utility functions and logging
- `process_textbook_content.py`: Script to process and index textbook content

## Requirements

- Python 3.11+
- uv package manager
- Access to Qdrant vector database
- OpenRouter API key (for OpenAI access)
- Cohere API key

## Setup

1. **Install uv package manager** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

4. **Process textbook content**:
   ```bash
   python process_textbook_content.py
   ```
   This script will process all Markdown files in the docs/ directory and store them in Qdrant.

## Running the Service

1. **Start the API server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

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

## Testing

Run tests using pytest:
```bash
pytest tests/ -v
```

## Configuration

The service is configured through environment variables in the `.env` file:

- `OPENROUTER_API_KEY`: OpenRouter API key (required for RAG functionality - cost-effective option)
- `QDRANT_URL`: Qdrant database URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the collection to use (default: "textbook-content")
- `COHERE_API_KEY`: Cohere API key (for embeddings)
- `EMBEDDING_MODEL`: Cohere embedding model
- `APP_ENV`: Application environment (development/production)
- `LOG_LEVEL`: Logging level (info/debug/warning/error)
- `USE_OPENROUTER`: Set to "true" to use OpenRouter backend (default: "true" for cost-effective operation)
- `USE_OPENAI_AGENTS`: Set to "true" to use OpenAI Agents SDK with OpenRouter (default: "true")
- `OPENROUTER_MODEL`: Specific OpenRouter model to use (default: "openai/gpt-4o")
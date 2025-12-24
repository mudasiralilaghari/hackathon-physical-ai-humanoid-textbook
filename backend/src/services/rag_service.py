from src.services.cohere_service import get_cohere_service
from src.services.qdrant_service import qdrant_service
from src.services.gemini_service import get_gemini_service
from src.services.openrouter_service import get_openrouter_service
from src.models.rag_models import QueryRequest, QueryResponse, RetrievedChunk
from src.utils.logger import get_logger
from datetime import datetime
import uuid
import os

logger = get_logger(__name__)

class RAGService:
    def __init__(self):
        self.cohere_service = get_cohere_service()
        self.qdrant_service = qdrant_service
        self.gemini_service = get_gemini_service()
        if self.gemini_service is None:
            logger.warning("Gemini service is not available. Using other backends.")
        self.openrouter_service = get_openrouter_service()

        # Determine which backend to use based on configuration
        # By default, prioritize OpenRouter for cost reasons
        self.use_openrouter = os.getenv("USE_OPENROUTER", "true").lower() == "true"
        self.use_openai_agents = os.getenv("USE_OPENAI_AGENTS", "false").lower() == "true"

        # Use the textbook content collection by default
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "textbook-content")

    def query(self, request: QueryRequest) -> QueryResponse:
        if self.use_openai_agents:
            # Use OpenAI Agents SDK with OpenRouter approach
            return self._query_with_openai_agents(request)
        elif self.use_openrouter:
            # Use OpenRouter approach (default for cost reasons)
            return self._query_with_openrouter(request)
        else:
            # Fallback to Gemini approach
            return self._query_with_gemini(request)

    def _query_with_gemini(self, request: QueryRequest) -> QueryResponse:
        try:
            # Check if gemini service is available
            if self.gemini_service is None:
                logger.warning("Gemini service not available, falling back to OpenRouter")
                return self._query_with_openrouter(request)

            logger.info(f"Received query (Gemini backend): {request.question}")

            # 1. Get embeddings for the query
            query_embedding = self.cohere_service.embed_query(request.question)

            # 2. Search for relevant chunks in Qdrant
            retrieved_chunks = self.qdrant_service.search(vector=query_embedding, collection_name=self.collection_name)

            # 3. Generate a response using Gemini
            response_text = self.gemini_service.generate_response(
                question=request.question,
                chunks=retrieved_chunks,
                selected_text=request.selected_text
            )

            # 4. Log and prepare the response
            query_id = request.query_id or str(uuid.uuid4())

            # Calculate retrieval score and chunks count
            retrieval_score = sum(chunk.score for chunk in retrieved_chunks) / len(retrieved_chunks) if retrieved_chunks else 0.0
            chunks_count = len(retrieved_chunks)

            logger.info(f"Query ID: {query_id}, Retrieval Score: {retrieval_score}, Chunks Count: {chunks_count}")

            return QueryResponse(
                response=response_text,
                query_id=query_id,
                retrieval_score=retrieval_score,
                chunks_count=chunks_count,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Error processing query with Gemini: {e}")
            query_id = request.query_id or str(uuid.uuid4())
            return QueryResponse(
                response="outside book scope",
                query_id=query_id,
                retrieval_score=None,
                chunks_count=0,
                timestamp=datetime.now()
            )

    def _query_with_openrouter(self, request: QueryRequest) -> QueryResponse:
        try:
            logger.info(f"Received query (OpenRouter backend): {request.question}")

            # 1. Get embeddings for the query
            query_embedding = self.cohere_service.embed_query(request.question)

            # 2. Search for relevant chunks in Qdrant
            retrieved_chunks = self.qdrant_service.search(vector=query_embedding, collection_name=self.collection_name)

            # 3. Generate a response using OpenRouter
            response_text = self.openrouter_service.generate_response(
                question=request.question,
                chunks=retrieved_chunks,
                selected_text=request.selected_text
            )

            # 4. Log and prepare the response
            query_id = request.query_id or str(uuid.uuid4())

            # Calculate retrieval score and chunks count
            retrieval_score = sum(chunk.score for chunk in retrieved_chunks) / len(retrieved_chunks) if retrieved_chunks else 0.0
            chunks_count = len(retrieved_chunks)

            logger.info(f"Query ID: {query_id}, Retrieval Score: {retrieval_score}, Chunks Count: {chunks_count}")

            return QueryResponse(
                response=response_text,
                query_id=query_id,
                retrieval_score=retrieval_score,
                chunks_count=chunks_count,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Error processing query with OpenRouter: {e}")
            query_id = request.query_id or str(uuid.uuid4())
            return QueryResponse(
                response="outside book scope",
                query_id=query_id,
                retrieval_score=None,
                chunks_count=0,
                timestamp=datetime.now()
            )

    def _query_with_openai_agents(self, request: QueryRequest) -> QueryResponse:
        # Import here to avoid circular dependencies
        from .openai_agents_rag_service import openai_agents_rag_service
        return openai_agents_rag_service.query(request)

rag_service = RAGService()

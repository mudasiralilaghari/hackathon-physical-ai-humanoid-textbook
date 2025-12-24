import uuid
import time
from typing import List, Optional
from src.models.rag_models import QueryRequest, QueryResponse, RetrievedChunk
from src.services.qdrant_service import get_qdrant_service
from src.services.cohere_service import get_cohere_service # Use Cohere for embeddings
from src.services.openai_service import get_openai_service # Use OpenAI for generation
from src.services.postgres_service import get_postgres_service
from src.utils.logger import get_logger, log_query_event, log_retrieval_event, log_error_event
from datetime import datetime
from .base import Agent


logger = get_logger(__name__)


class OpenAI_RAG_Agent(Agent):
    @property
    def qdrant_service(self):
        return get_qdrant_service()

    @property
    def cohere_service(self): # Use cohere for embeddings
        return get_cohere_service()

    @property
    def openai_service(self): # Use openai for generation
        return get_openai_service()

    @property
    def postgres_service(self):
        return get_postgres_service()

    async def answer(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a user query through the RAG pipeline using Cohere for embeddings and OpenAI for generation
        """
        start_time = time.time()

        # Generate query_id if not provided
        query_id = query_request.query_id or str(uuid.uuid4())
        session_id = query_request.session_id or query_id

        try:
            logger.info(f"Processing query {query_id} with OpenAI RAG Agent (Cohere Embeddings): {query_request.question[:50]}...")

            # Retrieve chat history
            chat_history = await self.postgres_service.get_chat_history(session_id)

            # Embed the user question using Cohere
            query_embedding = self.cohere_service.embed_query(query_request.question)

            # Search for relevant chunks in Qdrant
            retrieved_chunks = self.qdrant_service.search_chunks(query_embedding, limit=5)

            # Log retrieval metrics
            if retrieved_chunks:
                avg_score = self.qdrant_service.get_average_score(retrieved_chunks)
                top_score = max(chunk.score for chunk in retrieved_chunks) if retrieved_chunks else None
                log_retrieval_event(
                    query_id=query_id,
                    query=query_request.question,
                    chunks_count=len(retrieved_chunks),
                    avg_score=avg_score,
                    top_score=top_score
                )
            else:
                log_retrieval_event(
                    query_id=query_id,
                    query=query_request.question,
                    chunks_count=0
                )

            # Generate response using OpenAI
            response_text = await self.openai_service.generate_response(
                question=query_request.question,
                chunks=retrieved_chunks,
                selected_text=query_request.selected_text,
                history=chat_history
            )

            # Save chat history
            await self.postgres_service.add_chat_history(
                session_id=session_id,
                user_message=query_request.question,
                assistant_message=response_text
            )

            # Calculate duration
            duration = time.time() - start_time

            # Check if response time exceeds the 2.5s constraint
            if duration > 2.5:
                logger.warning(f"Query {query_id} exceeded 2.5s limit: {duration:.2f}s")

            # Calculate average retrieval score if chunks were found
            retrieval_score = None
            if retrieved_chunks:
                retrieval_score = self.qdrant_service.get_average_score(retrieved_chunks)

            # Create response object
            response = QueryResponse(
                response=response_text,
                query_id=query_id,
                retrieval_score=retrieval_score,
                chunks_count=len(retrieved_chunks),
                timestamp=datetime.utcnow().isoformat(),
                session_id=session_id
            )

            # Log query event
            log_query_event(
                query_id=query_id,
                question=query_request.question,
                chunks_count=len(retrieved_chunks),
                retrieval_score=retrieval_score,
                response=response_text,
                duration=duration
            )

            logger.info(f"Query {query_id} processed successfully in {duration:.2f}s")
            return response

        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            logger.error(f"Error processing query {query_id}: {error_msg}")

            # Log error event
            log_error_event(
                error_code="RAG_001",
                error_message=error_msg,
                query_id=query_id
            )

            # Return error response as per requirements
            return QueryResponse(
                response="outside book scope",
                query_id=query_id,
                retrieval_score=None,
                chunks_count=0,
                timestamp=datetime.utcnow().isoformat()
            )

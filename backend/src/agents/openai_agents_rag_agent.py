import asyncio
import os
from typing import List, Optional
from openai import OpenAI
from src.models.rag_models import QueryRequest, QueryResponse, RetrievedChunk
from src.services.qdrant_service import qdrant_service
from src.services.cohere_service import get_cohere_service
from src.utils.logger import get_logger
from datetime import datetime
import uuid
import time
from .base import Agent as BaseAgent


logger = get_logger(__name__)


class OpenAI_Agents_RAG_Agent(BaseAgent):
    def __init__(self):
        self.cohere_service = get_cohere_service()
        self.qdrant_service = qdrant_service
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_KEY")

        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_KEY environment variable is required")

        # Create OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openrouter_api_key
        )

        # Set the API key and base URL for OpenRouter in environment
        os.environ["OPENAI_API_KEY"] = self.openrouter_api_key
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    async def retrieve_context(self, question: str) -> str:
        """
        Retrieve relevant context chunks from the vector database based on the question
        """
        try:
            logger.info(f"Retrieving context for question: {question[:100]}...")

            # Get embeddings for the query
            query_embedding = self.cohere_service.embed_query(question)

            # Search for relevant chunks in Qdrant
            retrieved_chunks = self.qdrant_service.search(vector=query_embedding)

            if not retrieved_chunks:
                logger.info("No relevant chunks found in vector database")
                return "No relevant context found in the knowledge base."

            # Combine the content of retrieved chunks
            context = "\n\n".join([f"Context {i+1}: {chunk.content}" for i, chunk in enumerate(retrieved_chunks)])

            # Log retrieval metrics
            avg_score = sum(chunk.score for chunk in retrieved_chunks) / len(retrieved_chunks) if retrieved_chunks else 0.0
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks with average score: {avg_score:.3f}")

            return context

        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return "Error retrieving context from knowledge base."

    async def answer(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a user query through the OpenAI RAG pipeline using OpenAI's Assistant API
        """
        start_time = time.time()

        # Generate query_id if not provided
        query_id = query_request.query_id or str(uuid.uuid4())

        try:
            logger.info(f"Processing query {query_id} with OpenAI Agents RAG Agent: {query_request.question[:50]}...")

            # Retrieve context from vector database
            context = await self.retrieve_context(query_request.question)

            # Prepare the messages for the chat completion
            messages = [
                {
                    "role": "system",
                    "content": "You are a Retrieval-Augmented Generation (RAG) assistant. Your task is to answer questions based ONLY on the provided context information. Do not use any external knowledge or make up information. If the question cannot be answered using the provided context, respond with 'outside book scope'. Always be helpful and provide accurate answers based on the context."
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {query_request.question}"
                }
            ]

            # Include selected text if provided
            if query_request.selected_text:
                messages.append({
                    "role": "user",
                    "content": f"Additional context provided by user: {query_request.selected_text}"
                })

            # Call the OpenAI API via OpenRouter
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",  # Using a more cost-effective model via OpenRouter
                messages=messages,
                temperature=0.1,  # Lower temperature for more consistent answers
                max_tokens=500
            )

            response_text = response.choices[0].message.content

            # Calculate duration
            duration = time.time() - start_time

            # Check if response time exceeds the 2.5s constraint
            if duration > 2.5:
                logger.warning(f"Query {query_id} exceeded 2.5s limit: {duration:.2f}s")

            # Since we used the retrieve_context tool, we can extract some metrics
            # For now, we'll return basic metrics - in a real implementation, we'd extract more detailed info
            chunks_count = len(response_text.split()) // 50 if response_text else 0  # Rough estimate
            retrieval_score = None  # This would be more complex to extract from the agent response

            # Create response object
            response_obj = QueryResponse(
                response=response_text,
                query_id=query_id,
                retrieval_score=retrieval_score,
                chunks_count=chunks_count,
                timestamp=datetime.now()
            )

            logger.info(f"Query {query_id} processed successfully in {duration:.2f}s")
            return response_obj

        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            logger.error(f"Error processing query {query_id} with OpenAI Agents: {error_msg}")

            # Return error response as per requirements
            return QueryResponse(
                response="outside book scope",
                query_id=query_id,
                retrieval_score=None,
                chunks_count=0,
                timestamp=datetime.now()
            )
from src.services.cohere_service import get_cohere_service
from src.services.qdrant_service import qdrant_service
from src.models.rag_models import QueryRequest, QueryResponse
from src.utils.logger import get_logger
from src.agents.openai_agents_rag_agent import OpenAI_Agents_RAG_Agent
from datetime import datetime
import uuid
import asyncio
import nest_asyncio
import os

# Apply nest_asyncio to handle nested event loops in FastAPI
nest_asyncio.apply()

logger = get_logger(__name__)

class OpenAI_Agents_RAGService:
    def __init__(self):
        # Ensure OpenRouter configuration is set before initializing the agent
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_KEY environment variable is required")

        os.environ["OPENAI_API_KEY"] = openrouter_api_key
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

        self.agent = OpenAI_Agents_RAG_Agent()

    def query(self, request: QueryRequest) -> QueryResponse:
        try:
            logger.info(f"Received query for OpenAI Agents RAG: {request.question}")

            # Generate query_id if not provided
            if not request.query_id:
                request.query_id = str(uuid.uuid4())

            # Use nest_asyncio to run the async method
            response = asyncio.run(self.agent.answer(request))

            return response

        except Exception as e:
            logger.error(f"Error processing query with OpenAI Agents RAG: {e}")
            # Return error response as per requirements
            query_id = request.query_id or str(uuid.uuid4())
            return QueryResponse(
                response="outside book scope",
                query_id=query_id,
                retrieval_score=None,
                chunks_count=0,
                timestamp=datetime.now()
            )

openai_agents_rag_service = OpenAI_Agents_RAGService()
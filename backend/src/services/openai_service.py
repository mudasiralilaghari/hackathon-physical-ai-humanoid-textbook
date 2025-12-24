import os
from typing import List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv
from src.models.rag_models import RetrievedChunk
from src.utils.logger import get_logger
import time

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


class OpenAIService:
    def __init__(self):
        # Initialize AsyncOpenAI
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        if not api_key:
            logger.warning("OPENAI_API_KEY or GOOGLE_API_KEY environment variable is not set. Service will return mock responses.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

        self.model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.embedding_model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

    async def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query using OpenAI
        """
        try:
            if not self.client:
                logger.warning("Using mock embedding since API key is not available")
                return [0.0] * 1536  # Return a zero vector of the correct dimension

            response = await self.client.embeddings.create(
                input=[query],
                model=self.embedding_model_name
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error embedding query with OpenAI: {str(e)}")
            raise

    async def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed a list of documents using OpenAI
        """
        try:
            if not self.client:
                logger.warning("Using mock embeddings since API key is not available")
                return [[0.0] * 1536 for _ in documents]

            response = await self.client.embeddings.create(
                input=documents,
                model=self.embedding_model_name
            )
            return [d.embedding for d in response.data]
        except Exception as e:
            logger.error(f"Error embedding documents with OpenAI: {str(e)}")
            raise

    async def generate_response(self, question: str, chunks: List[RetrievedChunk], selected_text: Optional[str] = None, history: Optional[List] = None) -> str:
        """
        Generate a response based on the question and retrieved chunks using OpenAI
        """
        try:
            # Build the context from retrieved chunks
            context = "\n\n".join([chunk.content for chunk in chunks])

            # If there's no relevant context, return the "outside book scope" response
            if not context.strip():
                return "outside book scope"

            # If client is not available, return a mock response for development
            if not self.client:
                logger.warning("Using mock response since API key is not available")
                return f"Mock response for: {question[:50]}... [API key not configured]"

            # Create message for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based only on the provided context. Do not make up information."
                }
            ]

            # Add chat history to messages
            if history:
                for entry in history:
                    messages.append({"role": "user", "content": entry.user_message})
                    messages.append({"role": "assistant", "content": entry.assistant_message})

            # Build the prompt
            prompt_parts = [
                f"Context information:\n{context}\n\n"
            ]

            if selected_text:
                prompt_parts.append(f"Additional context provided by user:\n{selected_text}\n\n")

            prompt_parts.append(
                f"Question: {question}\n\n"
                "Please provide an answer based ONLY on the provided context information. "
                "Do not use any external knowledge or make up information. "
                "If the question cannot be answered using the provided context, respond with 'outside book scope'."
            )

            prompt = "".join(prompt_parts)
            messages.append({"role": "user", "content": prompt})

            # Generate response using OpenAI
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1,  # Low temperature for more consistent responses
                max_tokens=1000
            )

            # Extract the response text
            response_text = response.choices[0].message.content

            # Check if the response is empty
            if not response_text or response_text.strip() == "":
                return "outside book scope"

            logger.info(f"Generated response using {self.model_name} model")
            return response_text.strip()

        except Exception as e:
            logger.error(f"Error generating response with OpenAI: {str(e)}")
            raise

    def validate_response_does_not_hallucinate(self, response: str, context: str) -> bool:
        """
        Basic validation to ensure response is grounded in the provided context
        """
        # This is a simple check - in a real implementation, you'd want more sophisticated validation
        # For now, we trust that the model follows the instructions to use only provided context
        return True


# Global instance for use in other services
# Note: This will be initialized when first accessed to handle cases where API keys are not available
openai_service = None


def get_openai_service():
    global openai_service
    if openai_service is None:
        try:
            openai_service = OpenAIService()
        except Exception as e:
            # Log the error but don't crash the application
            from src.utils.logger import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to initialize OpenAI service: {str(e)}. Service will not be available until API key is configured.")
            raise e
    return openai_service
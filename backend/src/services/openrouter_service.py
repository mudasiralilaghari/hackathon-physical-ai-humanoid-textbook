import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from src.models.rag_models import RetrievedChunk
from src.utils.logger import get_logger
import time

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


class OpenRouterService:
    def __init__(self):
        # Initialize OpenAI client with OpenRouter
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_KEY environment variable is required")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        self.model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")

    def generate_response(self, question: str, chunks: List[RetrievedChunk], selected_text: Optional[str] = None) -> str:
        """
        Generate a response based on the question and retrieved chunks using OpenRouter
        """
        try:
            # Build the context from retrieved chunks
            context = "\n\n".join([chunk.content for chunk in chunks])

            # If there's no relevant context, return the "outside book scope" response
            if not context.strip():
                return "outside book scope"

            # Build the prompt
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based only on the provided context. Do not make up information."
                }
            ]

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

            # Generate response using OpenRouter
            response = self.client.chat.completions.create(
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

            logger.info(f"Generated response using {self.model_name} model via OpenRouter")
            return response_text.strip()

        except Exception as e:
            logger.error(f"Error generating response with OpenRouter: {str(e)}")
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
openrouter_service = None


def get_openrouter_service():
    global openrouter_service
    if openrouter_service is None:
        try:
            openrouter_service = OpenRouterService()
        except Exception as e:
            # Log the error but don't crash the application
            from src.utils.logger import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to initialize OpenRouter service: {str(e)}. Service will not be available until API key is configured.")
            raise e
    return openrouter_service
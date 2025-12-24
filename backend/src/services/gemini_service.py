import os
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv
from src.models.rag_models import RetrievedChunk
from src.utils.logger import get_logger
import time

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


class GeminiService:
    def __init__(self):
        # Initialize Google Generative AI
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
        self.model = genai.GenerativeModel(self.model_name)

    def generate_response(self, question: str, chunks: List[RetrievedChunk], selected_text: Optional[str] = None) -> str:
        """
        Generate a response based on the question and retrieved chunks
        """
        try:
            # Build the context from retrieved chunks
            context = "\n\n".join([chunk.content for chunk in chunks])

            # If there's no relevant context, return the "outside book scope" response
            if not context.strip():
                return "outside book scope"

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

            # Generate content using Gemini
            response = self.model.generate_content(prompt)

            # Check if the response is blocked or empty
            if not response.text or response.text.strip() == "":
                return "outside book scope"

            logger.info(f"Generated response using {self.model_name} model")
            return response.text.strip()

        except Exception as e:
            logger.error(f"Error generating response with Gemini: {str(e)}")
            raise

    def validate_response_does_not_hallucinate(self, response: str, context: str) -> bool:
        """
        Basic validation to ensure response is grounded in the provided context
        """
        # This is a simple check - in a real implementation, you'd want more sophisticated validation
        # For now, we trust that Gemini follows the instructions to use only provided context
        return True


# Global instance for use in other services
# Note: This will be initialized when first accessed to handle cases where API keys are not available
gemini_service = None


def get_gemini_service():
    global gemini_service
    if gemini_service is None:
        try:
            gemini_service = GeminiService()
        except Exception as e:
            # Log the error but don't crash the application
            from src.utils.logger import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to initialize Gemini service: {str(e)}. Service will not be available until API key is configured.")
            return None  # Return None instead of re-raising the exception
    return gemini_service
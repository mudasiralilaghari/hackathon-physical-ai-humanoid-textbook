import os
from typing import List
import cohere
from dotenv import load_dotenv
from src.utils.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


class CohereEmbeddingService:
    def __init__(self):
        # Initialize Cohere client
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)
        self.model = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")

    def get_embeddings(self, texts: List[str], input_type: str = "search_query") -> List[List[float]]:
        """
        Get embeddings for a list of texts using Cohere
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type=input_type
            )

            logger.info(f"Generated embeddings for {len(texts)} texts using {self.model}")
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def embed_text(self, text: str, input_type: str = "search_query") -> List[float]:
        """
        Get embedding for a single text
        """
        embeddings = self.get_embeddings([text], input_type)
        return embeddings[0] if embeddings else []

    def embed_query(self, query: str) -> List[float]:
        """
        Get embedding for a search query
        """
        return self.embed_text(query, input_type="search_query")

    def embed_document(self, document: str) -> List[float]:
        """
        Get embedding for a document chunk
        """
        return self.embed_text(document, input_type="search_document")


# Global instance for use in other services
# Note: This will be initialized when first accessed to handle cases where API keys are not available
cohere_service = None

def get_cohere_service():
    global cohere_service
    if cohere_service is None:
        try:
            cohere_service = CohereEmbeddingService()
        except Exception as e:
            # Log the error but don't crash the application
            from src.utils.logger import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to initialize Cohere service: {str(e)}. Service will not be available until API key is configured.")
            raise e
    return cohere_service
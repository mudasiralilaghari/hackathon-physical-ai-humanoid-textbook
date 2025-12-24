import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.utils.logger import get_logger
from src.models.rag_models import RetrievedChunk

logger = get_logger(__name__)

class QdrantService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")

        if not all([self.qdrant_url, self.qdrant_api_key, self.collection_name]):
            raise ValueError("QDRANT_URL, QDRANT_API_KEY, and QDRANT_COLLECTION_NAME must be set in the environment.")

        self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        logger.info("Qdrant client initialized.")

    def search(self, vector: list[float], limit: int = 5, collection_name: str = None) -> list[RetrievedChunk]:
        # Use the provided collection name or fall back to the default
        collection = collection_name or self.collection_name
        logger.info(f"Searching in collection '{collection}' with a vector of dimension {len(vector)}.")

        try:
            # This is a placeholder. The actual implementation will depend on the specifics of the Cohere embeddings
            # and how the search needs to be performed.
            search_result = self.client.search(
                collection_name=collection,
                query_vector=vector,
                limit=limit
            )

            retrieved_chunks = [
                RetrievedChunk(
                    content=hit.payload['text'],
                    score=hit.score,
                    metadata=hit.payload.get('metadata')
                ) for hit in search_result
            ]

            logger.info(f"Retrieved {len(retrieved_chunks)} chunks from Qdrant.")
            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            return []

    def store_embedding(self, collection_name: str, point_id: str, vector: list[float], payload: dict):
        """
        Store an embedding in Qdrant with the given payload
        """
        try:
            # Check if collection exists, if not create it
            try:
                self.client.get_collection(collection_name)
            except:
                # Create collection if it doesn't exist
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(size=len(vector), distance=models.Distance.COSINE),
                )
                logger.info(f"Created new collection: {collection_name}")

            # Generate a valid point ID (integer or UUID)
            # We'll use a hash of the original point_id and convert to int
            import uuid
            try:
                # Try to convert the point_id to int if it's already an int string
                valid_point_id = int(point_id)
            except ValueError:
                # If it's not an integer string, create a UUID
                # Use the original point_id as input to generate a consistent UUID
                import hashlib
                hash_object = hashlib.md5(point_id.encode())
                hex_dig = hash_object.hexdigest()
                # Take the first 8 hex characters and convert to int
                valid_point_id = int(hex_dig[:8], 16)

            # Prepare the point to be stored
            point = models.PointStruct(
                id=valid_point_id,
                vector=vector,
                payload=payload
            )

            # Store the point in Qdrant
            self.client.upsert(
                collection_name=collection_name,
                points=[point]
            )

            logger.debug(f"Stored embedding in Qdrant with ID: {valid_point_id}")
            return True

        except Exception as e:
            logger.error(f"Error storing embedding in Qdrant: {e}")
            return False

qdrant_service = QdrantService()

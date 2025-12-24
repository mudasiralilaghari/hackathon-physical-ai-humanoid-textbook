import asyncio
import os
import sys
from pathlib import Path

# Add the backend/src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.document_processor import DocumentProcessor
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def main():
    """
    Main function to process all textbook content and store in Qdrant
    """
    # Initialize the document processor
    processor = DocumentProcessor()
    
    # Define the path to the textbook content
    docs_path = os.path.join(os.path.dirname(__file__), '..', 'docs')
    
    # Verify the path exists
    if not os.path.exists(docs_path):
        logger.error(f"Docs path does not exist: {docs_path}")
        return
    
    logger.info(f"Starting to process textbook content from: {docs_path}")
    
    # Process all documents
    success_count, total_count = await processor.process_all_documents(
        docs_path=docs_path,
        collection_name="textbook_content"
    )
    
    logger.info(f"Processing complete. Successfully processed {success_count}/{total_count} documents.")
    
    if success_count == total_count:
        logger.info("All documents processed successfully!")
    else:
        logger.warning(f"Only {success_count}/{total_count} documents were processed successfully.")


if __name__ == "__main__":
    # Set environment variables from .env file if it exists
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the async main function
    asyncio.run(main())
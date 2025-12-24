import os
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import tiktoken
from src.services.cohere_service import get_cohere_service
from src.services.qdrant_service import qdrant_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DocumentProcessor:
    """
    Service to process textbook content (Markdown files) and prepare them for RAG indexing
    """
    
    def __init__(self):
        self.cohere_service = get_cohere_service()
        self.qdrant_service = qdrant_service
        self.enc = tiktoken.get_encoding("cl100k_base")  # Using the same encoding as GPT models
    
    def read_markdown_files(self, docs_path: str) -> List[Dict[str, Any]]:
        """
        Read all markdown files from the textbook directory
        """
        markdown_files = []
        docs_dir = Path(docs_path)
        
        for md_file in docs_dir.rglob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                markdown_files.append({
                    'filename': md_file.name,
                    'filepath': str(md_file),
                    'content': content,
                    'relative_path': str(md_file.relative_to(docs_dir))
                })
        
        logger.info(f"Found {len(markdown_files)} markdown files to process")
        return markdown_files
    
    def extract_text_from_markdown(self, markdown_content: str) -> str:
        """
        Extract clean text from markdown content
        """
        # Convert markdown to HTML
        html = markdown.markdown(markdown_content)
        # Extract text from HTML
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        # Clean up extra whitespace
        text = ' '.join(text.split())
        return text
    
    def chunk_text(self, text: str, max_tokens: int = 512) -> List[str]:
        """
        Split text into chunks of approximately max_tokens
        """
        # Split text into sentences to create more meaningful chunks
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Estimate token count (rough approximation: 1 token ~ 4 chars)
            # Using tiktoken for accurate tokenization
            sentence_tokens = len(self.enc.encode(sentence + ". "))
            current_tokens = len(self.enc.encode(current_chunk))
            
            if current_tokens + sentence_tokens > max_tokens and current_chunk:
                # If adding the sentence would exceed the limit, save the current chunk
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
            else:
                # Otherwise, add the sentence to the current chunk
                if current_chunk:
                    current_chunk += sentence + ". "
                else:
                    current_chunk = sentence + ". "
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def process_and_store_document(self, file_info: Dict[str, Any], collection_name: str = "textbook_content"):
        """
        Process a single document and store its chunks in Qdrant
        """
        logger.info(f"Processing document: {file_info['filepath']}")
        
        try:
            # Extract clean text from markdown
            clean_text = self.extract_text_from_markdown(file_info['content'])
            
            # Chunk the text
            chunks = self.chunk_text(clean_text)
            
            logger.info(f"Document {file_info['filename']} split into {len(chunks)} chunks")
            
            # Process each chunk and store in Qdrant
            for i, chunk in enumerate(chunks):
                # Create embedding for the chunk
                embedding = self.cohere_service.embed_document(chunk)
                
                # Prepare metadata
                metadata = {
                    'source_file': file_info['filename'],
                    'relative_path': file_info['relative_path'],
                    'chunk_number': i,
                    'original_file_path': file_info['filepath']
                }
                
                # Store in Qdrant
                point_id = f"{file_info['filename']}_{i}_{hash(chunk) % 1000000}"
                self.qdrant_service.store_embedding(
                    collection_name=collection_name,
                    point_id=point_id,
                    vector=embedding,
                    payload={
                        'text': chunk,
                        'metadata': metadata
                    }
                )
                
                logger.debug(f"Stored chunk {i} of {file_info['filename']} in Qdrant")
            
            logger.info(f"Successfully processed and stored document: {file_info['filename']}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing document {file_info['filepath']}: {str(e)}")
            return False
    
    async def process_all_documents(self, docs_path: str, collection_name: str = "textbook_content"):
        """
        Process all documents in the specified path and store in Qdrant
        """
        logger.info(f"Starting to process all documents in {docs_path}")
        
        # Read all markdown files
        markdown_files = self.read_markdown_files(docs_path)
        
        # Process each file
        success_count = 0
        for file_info in markdown_files:
            success = await self.process_and_store_document(file_info, collection_name)
            if success:
                success_count += 1
        
        logger.info(f"Completed processing. Successfully processed {success_count}/{len(markdown_files)} documents")
        return success_count, len(markdown_files)
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text using tiktoken
        """
        return len(self.enc.encode(text))
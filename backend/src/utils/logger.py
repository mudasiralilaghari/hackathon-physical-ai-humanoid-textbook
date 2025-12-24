import logging
import sys
from datetime import datetime
from typing import Optional

def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger with the given name.
    
    Args:
        name: Name of the logger (typically __name__ of the module)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False
    
    return logger

def log_query_event(query_id: str, question: str, response: str, retrieval_score: Optional[float] = None):
    """Log a query event with relevant information"""
    logger = get_logger("query_logger")
    logger.info(f"Query {query_id}: '{question}' -> Score: {retrieval_score}, Response length: {len(response)}")

def log_retrieval_event(query: str, chunks_count: int, avg_score: float):
    """Log a retrieval event with relevant information"""
    logger = get_logger("retrieval_logger")
    logger.info(f"Retrieved {chunks_count} chunks for query '{query[:50]}...', avg score: {avg_score}")

def log_error_event(error_type: str, error_message: str, query_id: Optional[str] = None):
    """Log an error event with relevant information"""
    logger = get_logger("error_logger")
    logger.error(f"Error {error_type} - Query ID: {query_id}, Message: {error_message}")
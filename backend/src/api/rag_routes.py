from fastapi import APIRouter, HTTPException, Body
from src.models.rag_models import QueryRequest, QueryResponse, APIErrorResponse
from src.services.rag_service import rag_service
from src.utils.logger import get_logger
from datetime import datetime
import uuid

router = APIRouter()
logger = get_logger(__name__)

@router.post("/query", response_model=QueryResponse, responses={500: {"model": APIErrorResponse}})
async def query(request: QueryRequest = Body(...)):
    """
    Accepts a user question and optional selected text, retrieves relevant content,
    and generates an answer.
    """
    try:
        if not request.query_id:
            request.query_id = str(uuid.uuid4())

        logger.info(f"Received query with ID: {request.query_id}")

        # Use the rag_service which handles both backends
        response = rag_service.query(request)

        return response

    except Exception as e:
        logger.error(f"Failed to process query {request.query_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=APIErrorResponse(
                error="Failed to process query.",
                error_code="RAG_001",
                timestamp=datetime.now(),
                query_id=request.query_id
            ).dict()
        )

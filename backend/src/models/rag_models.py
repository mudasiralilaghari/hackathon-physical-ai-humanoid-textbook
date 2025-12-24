from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class QueryRequest(BaseModel):
    question: str = Field(..., max_length=1000)
    selected_text: Optional[str] = Field(None, max_length=5000)
    query_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    query_id: str
    retrieval_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    chunks_count: Optional[int] = Field(None, ge=0)
    timestamp: datetime = Field(default_factory=datetime.now)

class RetrievedChunk(BaseModel):
    content: str
    score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[dict] = None

class APIErrorResponse(BaseModel):
    error: str
    error_code: str
    timestamp: datetime = Field(default_factory=datetime.now)
    query_id: Optional[str] = None

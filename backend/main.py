from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from src.services.postgres_service import get_postgres_service

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot Backend",
    description="Retrieval-Augmented Generation chatbot backend service",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    # Create database tables
    try:
        postgres_service = get_postgres_service()
        await postgres_service.create_tables()
    except Exception as e:
        logger.warning(f"Could not create database tables: {e}. Database functionality will be disabled.")

# Import API routes
from src.api.rag_routes import router as rag_router

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://localhost:3001",  # Alternative local port
        "https://mudasiralilaghari.github.io",  # Your deployed GitHub Pages site
        "https://*.hf.space"  # Hugging Face Spaces (for testing)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(rag_router, prefix="/rag", tags=["rag"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rag-chatbot-backend"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=True)
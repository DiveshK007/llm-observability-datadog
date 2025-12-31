"""
LLM Observability API - Main Application
FastAPI backend for Gemini-powered LLM with Datadog observability.
"""

import os
import time
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import structlog

from telemetry.datadog_setup import init_datadog
from gemini_client import call_gemini, GeminiResponse

# Load environment variables
load_dotenv()

logger = structlog.get_logger()


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for LLM query."""
    prompt: str = Field(..., min_length=1, max_length=10000, description="User prompt")
    max_tokens: int = Field(default=1024, ge=1, le=4096, description="Max response tokens")


class QueryResponse(BaseModel):
    """Response model for LLM query."""
    response: str
    latency_ms: float
    tokens_used: int
    estimated_cost_usd: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    init_datadog()
    logger.info("application_started", service="llm-observability-app")
    yield
    # Shutdown
    logger.info("application_shutdown")


# Create FastAPI app
app = FastAPI(
    title="LLM Observability API",
    description="Production-grade observability for Gemini-powered LLM applications",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def root():
    """Serve the frontend UI."""
    if FRONTEND_DIR.exists():
        return FileResponse(FRONTEND_DIR / "index.html")
    return {
        "message": "Welcome to the LLM Observability App!",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring.
    Used by Datadog and Cloud Run for availability checks.
    """
    return HealthResponse(
        status="healthy",
        service=os.getenv("DD_SERVICE", "llm-observability-app"),
        version=os.getenv("DD_VERSION", "1.0.0")
    )


@app.post("/query", response_model=QueryResponse)
async def query_llm(request: QueryRequest):
    """
    Query the Gemini LLM model.
    
    This endpoint:
    - Sends prompt to Gemini via Vertex AI
    - Measures latency
    - Tracks token usage
    - Estimates cost
    - Emits all metrics to Datadog
    """
    try:
        # Call Gemini model
        result: GeminiResponse = call_gemini(
            prompt=request.prompt,
            max_tokens=request.max_tokens
        )
        
        return QueryResponse(
            response=result.text,
            latency_ms=round(result.latency_ms, 2),
            tokens_used=result.total_tokens,
            estimated_cost_usd=round(result.estimated_cost_usd, 6)
        )
        
    except ValueError as e:
        logger.error("validation_error", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            "llm_request_failed",
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail="LLM processing failed. Please try again."
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        error_type=type(exc).__name__,
        error_message=str(exc)
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8000")),
        reload=True
    )

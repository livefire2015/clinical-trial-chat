"""
Clinical Trial Analysis Chat - FastAPI Backend
"""
import os
from contextlib import asynccontextmanager

# Load environment variables FIRST (before other imports that need them)
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    print("Starting Clinical Trial Analysis Chat Backend...")
    yield
    print("Shutting down...")


app = FastAPI(
    title="Clinical Trial Analysis Chat API",
    description="AI-powered pharmaceutical clinical trial analysis using Pydantic-AI and MCP",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Svelte dev server
        "http://localhost:4173",  # Svelte preview
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Clinical Trial Analysis Chat API",
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )

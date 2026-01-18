"""
FastAPI application with agent pipeline for GenAI-powered BI analysis.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, schema_routes, analyze
from app.core.cache import get_redis, close_redis
from app.core.database import close_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle (startup and shutdown)."""
    # Startup
    logger.info("Starting BI-Copilot API...")
    
    # Initialize Redis connection
    try:
        redis = await get_redis()
        await redis.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down BI-Copilot API...")
    await close_redis()
    await close_engine()
    logger.info("Connections closed")


# Create FastAPI app
app = FastAPI(
    title="BI-Copilot API",
    description="GenAI-powered data analysis with multi-agent pipeline",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(schema_routes.router)
app.include_router(analyze.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "BI-Copilot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

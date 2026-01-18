"""
Health check endpoints for monitoring system status.
"""

from fastapi import APIRouter, HTTPException
from app.core.cache import get_redis
from app.core.database import get_db_connection

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "service": "BI-Copilot API"}


@router.get("/redis")
async def redis_health():
    """Check Redis connection."""
    try:
        redis = await get_redis()
        await redis.ping()
        return {"status": "healthy", "service": "redis"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis unhealthy: {str(e)}")


@router.get("/database")
async def database_health():
    """Check database connection."""
    try:
        async with get_db_connection() as conn:
            result = await conn.execute("SELECT 1")
            result.close()
        return {"status": "healthy", "service": "database"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {str(e)}")

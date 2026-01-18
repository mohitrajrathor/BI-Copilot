"""
Redis cache management with async support.
Provides caching utilities for schema, query plans, SQL results, and LLM responses.
"""

import json
import hashlib
from typing import Any, Optional
from redis.asyncio import Redis
from app.core.config import get_settings

settings = get_settings()

# Global Redis client instance
_redis_client: Optional[Redis] = None


async def get_redis() -> Redis:
    """Get async Redis client instance."""
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
    return _redis_client


async def close_redis():
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


def generate_cache_key(prefix: str, *args: Any) -> str:
    """
    Generate a consistent cache key from prefix and arguments.
    
    Args:
        prefix: Key prefix (e.g., 'schema', 'query_plan', 'sql_result')
        *args: Values to hash into the key
        
    Returns:
        Cache key string
    """
    content = ":".join(str(arg) for arg in args)
    hash_digest = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"{prefix}:{hash_digest}"


async def get_cached(key: str) -> Optional[Any]:
    """
    Retrieve value from cache.
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None if not found
    """
    redis = await get_redis()
    value = await redis.get(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return None


async def set_cached(
    key: str,
    value: Any,
    ttl: Optional[int] = None
) -> bool:
    """
    Store value in cache.
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (None for permanent)
        
    Returns:
        True if successful
    """
    redis = await get_redis()
    
    # Serialize value
    if isinstance(value, (dict, list)):
        serialized = json.dumps(value)
    else:
        serialized = str(value)
    
    if ttl:
        await redis.setex(key, ttl, serialized)
    else:
        await redis.set(key, serialized)
    
    return True


async def delete_cached(key: str) -> bool:
    """
    Delete value from cache.
    
    Args:
        key: Cache key
        
    Returns:
        True if key existed and was deleted
    """
    redis = await get_redis()
    result = await redis.delete(key)
    return result > 0


async def invalidate_pattern(pattern: str) -> int:
    """
    Delete all keys matching a pattern.
    
    Args:
        pattern: Redis key pattern (e.g., 'schema:*')
        
    Returns:
        Number of keys deleted
    """
    redis = await get_redis()
    keys = []
    async for key in redis.scan_iter(match=pattern):
        keys.append(key)
    
    if keys:
        return await redis.delete(*keys)
    return 0


async def cache_exists(key: str) -> bool:
    """
    Check if cache key exists.
    
    Args:
        key: Cache key
        
    Returns:
        True if key exists
    """
    redis = await get_redis()
    return await redis.exists(key) > 0

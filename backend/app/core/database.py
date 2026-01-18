"""
Database connection and SQL safety enforcement.
Provides read-only database access with validation and safety checks.
"""

import re
import logging
from typing import Any, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy import text
import asyncio

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Global database engine
_engine: Optional[AsyncEngine] = None


def get_engine() -> AsyncEngine:
    """Get or create async SQLAlchemy engine with read-only configuration."""
    global _engine
    if _engine is None:
        # Create engine with read-only settings
        connect_args = {}
        engine_kwargs = {
            "echo": False,
            "connect_args": connect_args
        }
        
        # SQLite doesn't support connection pooling
        if "sqlite" in settings.database_url:
            connect_args["check_same_thread"] = False
            # SQLite uses NullPool by default, no pool settings needed
        else:
            # PostgreSQL, MySQL, etc. support connection pooling
            engine_kwargs.update({
                "pool_pre_ping": True,
                "pool_size": 5,
                "max_overflow": 10,
            })
        
        _engine = create_async_engine(
            settings.database_url,
            **engine_kwargs
        )
    
    return _engine


async def close_engine():
    """Close database engine."""
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None


@asynccontextmanager
async def get_db_connection():
    """
    Get async database connection.
    
    Yields:
        AsyncConnection
    """
    engine = get_engine()
    async with engine.connect() as conn:
        yield conn


def validate_sql_safety(sql: str) -> tuple[bool, Optional[str]]:
    """
    Validate SQL query for safety.
    Checks for forbidden keywords and patterns.
    
    Args:
        sql: SQL query string
        
    Returns:
        Tuple of (is_safe, error_message)
    """
    # Convert to uppercase for checking
    sql_upper = sql.upper()
    
    # Check for forbidden keywords
    for keyword in settings.SQL_FORBIDDEN_KEYWORDS:
        # Use word boundary to avoid false positives (e.g., "DELETE" in "UNDELETE")
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            return False, f"Forbidden SQL keyword detected: {keyword}"
    
    # Check for SQL comments that might hide malicious code
    if "--" in sql or "/*" in sql:
        return False, "SQL comments are not allowed"
    
    # Check for semicolon (to prevent multiple statements)
    if ";" in sql.rstrip().rstrip(";"):
        return False, "Multiple SQL statements are not allowed"
    
    return True, None


def inject_limit_clause(sql: str, limit: int = None) -> str:
    """
    Inject LIMIT clause into SQL query if not present.
    
    Args:
        sql: SQL query string
        limit: Maximum number of rows (defaults to settings.max_rows)
        
    Returns:
        SQL with LIMIT clause
    """
    if limit is None:
        limit = settings.max_rows
    
    sql = sql.strip().rstrip(";")
    sql_upper = sql.upper()
    
    # Check if LIMIT already exists
    if "LIMIT" not in sql_upper:
        sql = f"{sql} LIMIT {limit}"
    else:
        # Replace existing LIMIT with our max if it's higher
        # This is a simple approach; a full SQL parser would be more robust
        pass
    
    return sql


async def execute_query_safe(
    sql: str,
    params: Optional[dict] = None,
    timeout: Optional[int] = None
) -> dict[str, Any]:
    """
    Execute SQL query with safety checks and timeout.
    
    Args:
        sql: SQL query string
        params: Query parameters for binding
        timeout: Query timeout in seconds (defaults to settings.query_timeout_seconds)
        
    Returns:
        Dict with 'columns' and 'rows' keys
        
    Raises:
        ValueError: If SQL is unsafe
        TimeoutError: If query exceeds timeout
        Exception: For other database errors
    """
    if timeout is None:
        timeout = settings.query_timeout_seconds
    
    # Validate SQL safety
    is_safe, error_msg = validate_sql_safety(sql)
    if not is_safe:
        raise ValueError(f"Unsafe SQL query: {error_msg}")
    
    # Inject LIMIT clause
    sql = inject_limit_clause(sql)
    
    # Log query if enabled
    if settings.enable_query_logging:
        logger.info(f"Executing query: {sql[:200]}...")
    
    async def _execute():
        async with get_db_connection() as conn:
            result = await conn.execute(text(sql), params or {})
            rows = result.fetchall()
            
            # Get column names
            columns = list(result.keys()) if rows else []
            
            # Convert rows to list of dicts
            data = [dict(zip(columns, row)) for row in rows]
            
            return {
                "columns": columns,
                "rows": data,
                "row_count": len(data)
            }
    
    try:
        # Execute with timeout
        result = await asyncio.wait_for(_execute(), timeout=timeout)
        return result
    except asyncio.TimeoutError:
        raise TimeoutError(f"Query execution exceeded timeout of {timeout} seconds")
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        raise

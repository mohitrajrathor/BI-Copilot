"""
Schema extraction and intelligence with embedding generation.
Handles schema caching and semantic search for schema elements.
"""

import logging
from typing import Any, Optional
from sqlalchemy import inspect
import hashlib

from app.core.database import get_engine
from app.core.cache import get_cached, set_cached, generate_cache_key
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


def get_database_hash(database_url: str) -> str:
    """Generate a consistent hash for a database URL."""
    return hashlib.sha256(database_url.encode()).hexdigest()[:16]


async def extract_schema() -> dict[str, Any]:
    """
    Extract schema metadata from connected database.
    
    Returns:
        Dict with tables, columns, and data types
    """
    engine = get_engine()
    
    schema_info = {
        "tables": [],
        "database_hash": get_database_hash(settings.database_url)
    }
    
    async with engine.connect() as conn:
        # Run inspection in a separate thread since it's sync
        def _inspect(sync_conn):
            inspector = inspect(sync_conn)
            tables = []
            
            for table_name in inspector.get_table_names():
                columns = []
                for column in inspector.get_columns(table_name):
                    columns.append({
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column.get("nullable", True),
                        "default": str(column.get("default")) if column.get("default") else None
                    })
                
                # Extract foreign key relationships
                foreign_keys = []
                for fk in inspector.get_foreign_keys(table_name):
                    foreign_keys.append({
                        "constrained_columns": fk["constrained_columns"],
                        "referred_table": fk["referred_table"],
                        "referred_columns": fk["referred_columns"]
                    })
                
                tables.append({
                    "name": table_name,
                    "columns": columns,
                    "foreign_keys": foreign_keys
                })
            
            return tables
        
        schema_info["tables"] = await conn.run_sync(_inspect)
    
    logger.info(f"Extracted schema: {len(schema_info['tables'])} tables")
    return schema_info


async def get_cached_schema(database_url: str) -> Optional[dict[str, Any]]:
    """
    Retrieve cached schema for a database.
    
    Args:
        database_url: Database connection URL
        
    Returns:
        Cached schema or None
    """
    db_hash = get_database_hash(database_url)
    cache_key = generate_cache_key("schema", db_hash)
    return await get_cached(cache_key)


async def cache_schema(database_url: str, schema: dict[str, Any]) -> bool:
    """
    Cache schema permanently (or until DB URL changes).
    
    Args:
        database_url: Database connection URL
        schema: Schema metadata
        
    Returns:
        True if cached successfully
    """
    db_hash = get_database_hash(database_url)
    cache_key = generate_cache_key("schema", db_hash)
    
    # Cache permanently if setting is enabled (no TTL)
    ttl = None if settings.schema_cache_permanent else settings.cache_ttl_seconds
    return await set_cached(cache_key, schema, ttl)


async def get_or_extract_schema() -> dict[str, Any]:
    """
    Get schema from cache or extract if not cached.
    
    Returns:
        Schema metadata
    """
    # Check cache first
    cached = await get_cached_schema(settings.database_url)
    if cached:
        logger.info("Using cached schema")
        return cached
    
    # Extract and cache
    logger.info("Extracting schema from database")
    schema = await extract_schema()
    await cache_schema(settings.database_url, schema)
    
    return schema


def format_schema_for_llm(schema: dict[str, Any]) -> str:
    """
    Format schema metadata into a readable string for LLM.
    
    Args:
        schema: Schema metadata dict
        
    Returns:
        Formatted schema string
    """
    lines = ["Database Schema:\n"]
    
    for table in schema["tables"]:
        lines.append(f"\nTable: {table['name']}")
        lines.append("Columns:")
        for col in table["columns"]:
            nullable = "NULL" if col["nullable"] else "NOT NULL"
            lines.append(f"  - {col['name']} ({col['type']}) {nullable}")
        
        # Add foreign key relationships
        if table.get("foreign_keys"):
            lines.append("Relationships:")
            for fk in table["foreign_keys"]:
                constrained = ", ".join(fk["constrained_columns"])
                referred = ", ".join(fk["referred_columns"])
                lines.append(f"  - {constrained} -> {fk['referred_table']}.{referred}")
    
    return "\n".join(lines)


def get_table_names(schema: dict[str, Any]) -> list[str]:
    """Extract list of table names from schema."""
    return [table["name"] for table in schema["tables"]]


def get_column_names(schema: dict[str, Any], table_name: str) -> list[str]:
    """
    Get column names for a specific table.
    
    Args:
        schema: Schema metadata
        table_name: Name of the table
        
    Returns:
        List of column names
    """
    for table in schema["tables"]:
        if table["name"] == table_name:
            return [col["name"] for col in table["columns"]]
    return []


def validate_table_exists(schema: dict[str, Any], table_name: str) -> bool:
    """Check if a table exists in the schema."""
    return table_name in get_table_names(schema)


def validate_column_exists(
    schema: dict[str, Any],
    table_name: str,
    column_name: str
) -> bool:
    """Check if a column exists in a table."""
    column_names = get_column_names(schema, table_name)
    return column_name in column_names

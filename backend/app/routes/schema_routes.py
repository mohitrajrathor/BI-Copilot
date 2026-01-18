"""
Schema management endpoints.
Handles database connection and schema caching.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.schema import get_or_extract_schema, format_schema_for_llm

router = APIRouter(prefix="/api/schema", tags=["schema"])


class SchemaResponse(BaseModel):
    """Schema information response."""
    tables: list[dict]
    database_hash: str
    table_count: int


@router.get("/info", response_model=SchemaResponse)
async def get_schema_info():
    """
    Get cached schema information.
    Automatically extracts and caches if not present.
    """
    try:
        schema = await get_or_extract_schema()
        
        return SchemaResponse(
            tables=schema["tables"],
            database_hash=schema["database_hash"],
            table_count=len(schema["tables"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schema extraction failed: {str(e)}")


@router.get("/formatted")
async def get_formatted_schema():
    """Get schema formatted for LLM."""
    try:
        schema = await get_or_extract_schema()
        formatted = format_schema_for_llm(schema)
        
        return {"schema": formatted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schema formatting failed: {str(e)}")

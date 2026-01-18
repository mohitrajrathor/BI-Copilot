"""
Agent 3: SQL Generator & Executor
Converts analysis plan into SQL and executes safely.
Uses templates, validates SQL, and enforces safety limits.
"""

import logging
import hashlib
from typing import Any

from app.core.database import execute_query_safe
from app.core.cache import get_cached, set_cached, generate_cache_key
from app.core.config import get_settings
from app.utils.sql_templates import build_select_query, build_simple_select

settings = get_settings()
logger = logging.getLogger(__name__)


class SQLGenerator:
    """
    SQL Generator that converts analysis plans to SQL and executes them safely.
    NEVER accepts raw SQL from users.
    """
    
    async def generate_sql(self, plan: dict) -> str:
        """
        Generate SQL from structured analysis plan.
        
        Args:
            plan: Analysis plan from planner agent
            
        Returns:
            SQL query string
        """
        table = plan["table"]
        metrics = plan.get("metrics", [])
        dimensions = plan.get("dimensions", [])
        filters = plan.get("filters", [])
        joins = plan.get("joins", [])  # Extract joins from plan
        
        # Build aggregations dict
        aggregations = {
            metric["column"]: metric.get("aggregation", "SUM")
            for metric in metrics
        }
        
        # Decide if we need aggregation query or simple select
        if metrics and any(m.get("aggregation") for m in metrics):
            sql = build_select_query(
                table=table,
                metrics=metrics,
                dimensions=dimensions,
                filters=filters,
                aggregations=aggregations,
                limit=settings.max_rows,
                joins=joins  # Pass joins to template builder
            )
        else:
            # Simple select
            columns = dimensions if dimensions else None
            sql = build_simple_select(
                table=table,
                columns=columns,
                filters=filters,
                limit=settings.max_rows
            )
        
        logger.info(f"Generated SQL: {sql[:100]}...")
        return sql
    
    async def execute_sql(self, sql: str) -> dict[str, Any]:
        """
        Execute SQL query with safety checks and caching.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results with columns and rows
        """
        # Check cache first
        sql_hash = hashlib.sha256(sql.encode()).hexdigest()[:16]
        cache_key = generate_cache_key("sql_result", sql_hash)
        
        cached_result = await get_cached(cache_key)
        if cached_result:
            logger.info("Using cached SQL result")
            return cached_result
        
        # Execute query with safety checks
        try:
            result = await execute_query_safe(sql)
            
            # Cache the result
            await set_cached(cache_key, result, settings.cache_ttl_seconds)
            
            logger.info(f"Query executed: {result['row_count']} rows returned")
            return result
            
        except Exception as e:
            logger.error(f"SQL execution failed: {str(e)}")
            raise
    
    async def generate_and_execute(self, plan: dict) -> dict:
        """
        Main method: Generate SQL from plan and execute it.
        
        Args:
            plan: Analysis plan
            
        Returns:
            Dict with SQL, results, and status
        """
        try:
            # Generate SQL from plan
            sql = await self.generate_sql(plan)
            
            # Execute SQL
            result = await self.execute_sql(sql)
            
            return {
                "sql": sql,
                "data": result,
                "status": "query_executed"
            }
            
        except Exception as e:
            logger.error(f"SQL generation/execution failed: {str(e)}")
            raise ValueError(f"Failed to execute query: {str(e)}")

"""
SQL template builder for converting analysis plans to SQL queries.
Uses template-based generation for safety and consistency.
"""

from typing import Any


def build_select_query(
    table: str,
    metrics: list[dict[str, str]],
    dimensions: list[str],
    filters: list[dict[str, Any]],
    aggregations: dict[str, str],
    limit: int = 10000,
    joins: list[dict[str, str]] = None
) -> str:
    """
    Build a SELECT query from structured analysis plan.
    
    Args:
        table: Table name
        metrics: List of metric specifications [{"column": "revenue", "aggregation": "SUM", "table": "sales"}]
        dimensions: List of dimension columns (for GROUP BY) - can include table prefix
        filters: List of filter specs [{"column": "date", "operator": ">=", "value": "2024-01-01"}]
        aggregations: Dict mapping metrics to aggregation functions
        limit: Row limit
        joins: List of join specifications [{"table": "customers", "on_column": "customer_id", "from_column": "customer_id", "join_from": "sales"}]
        
    Returns:
        SQL query string
    """
    # Determine if we need table prefixes (when joins are present)
    use_prefixes = joins and len(joins) > 0
    
    # SELECT clause
    select_parts = []
    
    # Add dimensions (with table prefix if joins exist)
    for dim in dimensions:
        # Dimension may already have table prefix (e.g., "regions.region_name")
        select_parts.append(dim)
    
    # Add aggregated metrics
    for metric in metrics:
        col = metric["column"]
        agg = metric.get("aggregation", "SUM")
        metric_table = metric.get("table", table)
        
        # Use table prefix if joins exist and not already prefixed
        if use_prefixes and "." not in col:
            col_ref = f"{metric_table}.{col}"
        else:
            col_ref = col
        
        select_parts.append(f"{agg}({col_ref}) AS {col.split('.')[-1]}_{agg.lower()}")
    
    select_clause = ", ".join(select_parts) if select_parts else "*"
    
    # FROM clause
    from_clause = f"FROM {table}"
    
    # JOIN clauses
    join_clauses = []
    if joins:
        for join in joins:
            join_table = join["table"]
            on_column = join["on_column"]
            from_column = join["from_column"]
            join_from_table = join.get("join_from", table)
            
            join_clauses.append(
                f"JOIN {join_table} ON {join_from_table}.{from_column} = {join_table}.{on_column}"
            )
    
    # WHERE clause
    where_parts = []
    for filter_spec in filters:
        col = filter_spec["column"]
        op = filter_spec["operator"]
        val = filter_spec["value"]
        
        # Handle string values with quotes
        if isinstance(val, str):
            val = f"'{val}'"
        
        where_parts.append(f"{col} {op} {val}")
    
    where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
    
    # GROUP BY clause
    group_by_clause = ""
    if dimensions and metrics:
        group_by_clause = f"GROUP BY {', '.join(dimensions)}"
    
    # ORDER BY clause (optional, order by first metric)
    order_by_clause = ""
    if metrics:
        first_metric = metrics[0]
        col = first_metric["column"]
        agg = first_metric.get("aggregation", "SUM")
        order_by_clause = f"ORDER BY {col.split('.')[-1]}_{agg.lower()} DESC"
    
    # LIMIT clause
    limit_clause = f"LIMIT {limit}"
    
    # Combine all parts
    query_parts = [
        f"SELECT {select_clause}",
        from_clause
    ]
    
    # Add join clauses
    query_parts.extend(join_clauses)
    
    # Add remaining clauses
    query_parts.extend([
        where_clause,
        group_by_clause,
        order_by_clause,
        limit_clause
    ])
    
    # Filter out empty parts and join
    query = "\n".join(part for part in query_parts if part)
    
    return query


def build_simple_select(
    table: str,
    columns: list[str] = None,
    filters: list[dict[str, Any]] = None,
    limit: int = 10000
) -> str:
    """
    Build a simple SELECT query without aggregations.
    
    Args:
        table: Table name
        columns: List of column names (None for SELECT *)
        filters: List of filter specifications
        limit: Row limit
        
    Returns:
        SQL query string
    """
    # SELECT clause
    select_clause = ", ".join(columns) if columns else "*"
    
    # FROM clause
    from_clause = f"FROM {table}"
    
    # WHERE clause
    where_parts = []
    if filters:
        for filter_spec in filters:
            col = filter_spec["column"]
            op = filter_spec["operator"]
            val = filter_spec["value"]
            
            if isinstance(val, str):
                val = f"'{val}'"
            
            where_parts.append(f"{col} {op} {val}")
    
    where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
    
    # LIMIT clause
    limit_clause = f"LIMIT {limit}"
    
    # Combine
    query_parts = [
        f"SELECT {select_clause}",
        from_clause,
        where_clause,
        limit_clause
    ]
    
    query = "\n".join(part for part in query_parts if part)
    
    return query

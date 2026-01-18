"""
Deterministic chart type mapping based on data shape.
Maps dataset characteristics to appropriate visualization types.
"""

from typing import Any, Literal


ChartType = Literal["kpi", "line", "bar", "pie", "scatter", "table"]


def analyze_data_shape(data: dict[str, Any]) -> dict[str, Any]:
    """
    Analyze the shape and characteristics of query results.
    
    Args:
        data: Query results with 'columns' and 'rows'
        
    Returns:
        Dict with data characteristics
    """
    columns = data.get("columns", [])
    rows = data.get("rows", [])
    
    if not rows:
        return {
            "num_columns": len(columns),
            "num_rows": 0,
            "has_time_series": False,
            "numeric_columns": [],
            "text_columns": [],
            "is_aggregated": False
        }
    
    # Analyze column types from first row
    first_row = rows[0]
    numeric_columns = []
    text_columns = []
    date_columns = []
    
    for col in columns:
        value = first_row.get(col)
        if value is None:
            continue
        
        if isinstance(value, (int, float)):
            numeric_columns.append(col)
        elif isinstance(value, str):
            # Simple heuristic for date detection
            if any(keyword in col.lower() for keyword in ["date", "time", "year", "month", "day"]):
                date_columns.append(col)
            else:
                text_columns.append(col)
    
    # Detect if data is aggregated (has aggregation functions in column names)
    is_aggregated = any(
        any(agg in col.lower() for agg in ["sum", "avg", "count", "min", "max"])
        for col in columns
    )
    
    # Detect time series (has date column and numeric metric)
    has_time_series = len(date_columns) > 0 and len(numeric_columns) > 0
    
    return {
        "num_columns": len(columns),
        "num_rows": len(rows),
        "has_time_series": has_time_series,
        "numeric_columns": numeric_columns,
        "text_columns": text_columns,
        "date_columns": date_columns,
        "is_aggregated": is_aggregated
    }


def select_chart_type(data_shape: dict[str, Any]) -> ChartType:
    """
    Deterministically select chart type based on data shape.
    
    Rules:
    - Single metric (1 column, 1 row) → KPI card
    - Time series (date + metric) → Line chart
    - Categories + metric (text + numeric) → Bar chart
    - Two numeric columns → Scatter plot
    - Single column with percentages → Pie chart
    - Default → Table
    
    Args:
        data_shape: Data characteristics from analyze_data_shape
        
    Returns:
        Chart type
    """
    num_cols = data_shape["num_columns"]
    num_rows = data_shape["num_rows"]
    has_time = data_shape["has_time_series"]
    num_numeric = len(data_shape["numeric_columns"])
    num_text = len(data_shape["text_columns"])
    
    # Single value → KPI
    if num_cols == 1 and num_rows == 1:
        return "kpi"
    
    # Time series → Line chart
    if has_time and num_numeric >= 1:
        return "line"
    
    # Categories + metric → Bar chart
    if num_text >= 1 and num_numeric >= 1:
        return "bar"
    
    # Two numeric columns → Scatter
    if num_numeric >= 2 and num_text == 0:
        return "scatter"
    
    # Fewer rows with text → Pie chart (for percentage breakdowns)
    if num_rows <= 10 and num_text == 1 and num_numeric == 1:
        return "pie"
    
    # Default to table
    return "table"


def build_chart_config(
    chart_type: ChartType,
    data: dict[str, Any],
    data_shape: dict[str, Any]
) -> dict[str, Any]:
    """
    Build chart configuration based on chart type and data.
    
    Args:
        chart_type: Selected chart type
        data: Query results
        data_shape: Data characteristics
        
    Returns:
        Chart configuration dict
    """
    columns = data.get("columns", [])
    rows = data.get("rows", [])
    
    config = {
        "type": chart_type,
        "data": rows,
        "columns": columns
    }
    
    if chart_type == "kpi":
        # Single metric display
        if rows and columns:
            config["metric"] = {
                "label": columns[0],
                "value": rows[0][columns[0]]
            }
    
    elif chart_type == "line":
        # X-axis: date column, Y-axis: numeric columns
        config["xAxis"] = data_shape["date_columns"][0] if data_shape["date_columns"] else columns[0]
        config["yAxis"] = data_shape["numeric_columns"]
    
    elif chart_type == "bar":
        # X-axis: text column, Y-axis: numeric column
        config["xAxis"] = data_shape["text_columns"][0] if data_shape["text_columns"] else columns[0]
        config["yAxis"] = data_shape["numeric_columns"][0] if data_shape["numeric_columns"] else columns[-1]
    
    elif chart_type == "pie":
        # Label: text column, Value: numeric column
        config["labelColumn"] = data_shape["text_columns"][0] if data_shape["text_columns"] else columns[0]
        config["valueColumn"] = data_shape["numeric_columns"][0] if data_shape["numeric_columns"] else columns[-1]
    
    elif chart_type == "scatter":
        # X and Y: first two numeric columns
        numeric_cols = data_shape["numeric_columns"]
        config["xAxis"] = numeric_cols[0] if len(numeric_cols) > 0 else columns[0]
        config["yAxis"] = numeric_cols[1] if len(numeric_cols) > 1 else columns[1] if len(columns) > 1 else columns[0]
    
    return config

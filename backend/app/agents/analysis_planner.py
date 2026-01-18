"""
Agent 2: Analysis Planner
Converts user intent + schema into structured analysis plan.
Output is STRICT JSON, no SQL, no prose.
"""

import logging
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import get_settings
from app.core.schema import format_schema_for_llm
from app.core.cache import get_cached, set_cached, generate_cache_key

settings = get_settings()
logger = logging.getLogger(__name__)


class AnalysisPlanner:
    """
    Analysis Planner agent that converts intent into structured plan.
    Uses a larger model for better reasoning.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.planning_model,
            api_key=settings.gemini_api_key,
            temperature=0
        )
    
    async def create_plan(
        self,
        user_query: str,
        intent: str,
        schema: dict
    ) -> dict:
        """
        Create structured analysis plan from user query and schema.
        
        Args:
            user_query: User's natural language query
            intent: Classified intent type
            schema: Database schema metadata
            
        Returns:
            Structured analysis plan as dict
        """
        # Check cache first
        cache_key = generate_cache_key("analysis_plan", user_query, intent)
        cached_plan = await get_cached(cache_key)
        if cached_plan:
            logger.info("Using cached analysis plan")
            return cached_plan
        
        schema_str = format_schema_for_llm(schema)
        
        system_prompt = """You are a data analysis planner. 

Your job is to convert a user's natural language query into a STRUCTURED analysis plan.

You MUST respond with ONLY a JSON object in this EXACT format:
{
  "table": "table_name",
  "joins": [
    {
      "table": "joined_table_name",
      "on_column": "column_in_joined_table",
      "from_column": "column_in_source_table",
      "join_from": "source_table_name"
    }
  ],
  "metrics": [
    {"column": "column_name", "aggregation": "SUM|AVG|COUNT|MIN|MAX", "table": "table_name"}
  ],
  "dimensions": ["table.column_name"],
  "filters": [
    {"column": "column_name", "operator": "=|>|<|>=|<=|!=", "value": "value"}
  ],
  "recommended_chart": "line|bar|pie|scatter|kpi|table"
}

RULES:
- Output ONLY JSON, no explanations
- NO SQL queries
- NO prose or markdown
- Use ONLY tables and columns from the provided schema
- Pay attention to the "Relationships" section showing foreign keys
- If a query needs data from related tables, specify the joins needed
- Table relationships are shown as: column -> related_table.column
- Always prefix dimension columns with their table name (e.g., "regions.region_name")
- For metrics, specify the table in the metric object
- If comparing categories, use dimensions
- Recommended chart should be ONE of: line, bar, pie, scatter, kpi, table

EXAMPLES:
- Query: "sales by region" requires joining sales → customers → regions
  Main table: "sales"
  Joins: [{"table": "customers", "on_column": "customer_id", "from_column": "customer_id", "join_from": "sales"},
          {"table": "regions", "on_column": "region_id", "from_column": "region_id", "join_from": "customers"}]
  Dimensions: ["regions.region_name"]
  Metrics: [{"column": "total_amount", "aggregation": "SUM", "table": "sales"}]
"""

        user_prompt = f"""Query: {user_query}

Intent: {intent}

{schema_str}

Generate the analysis plan JSON:"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            plan = json.loads(content.strip())
            
            # Validate plan structure (joins is optional)
            required_keys = ["table", "metrics", "dimensions", "filters"]
            if not all(key in plan for key in required_keys):
                raise ValueError(f"Plan missing required keys. Got: {plan.keys()}")
            
            # Cache the plan
            await set_cached(cache_key, plan, settings.cache_ttl_seconds)
            
            logger.info(f"Created analysis plan for table: {plan.get('table')}")
            return plan
            
        except Exception as e:
            logger.error(f"Analysis planning failed: {str(e)}")
            raise ValueError(f"Failed to create analysis plan: {str(e)}")
    
    async def plan(
        self,
        user_query: str,
        intent: str,
        schema: dict
    ) -> dict:
        """
        Main planning method.
        
        Args:
            user_query: User's query
            intent: Classified intent
            schema: Database schema
            
        Returns:
            Analysis plan dict
        """
        plan = await self.create_plan(user_query, intent, schema)
        
        return {
            "plan": plan,
            "status": "plan_created"
        }

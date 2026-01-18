"""
Agent 4: Dashboard Generator
Creates dashboard specifications from query results.
Uses deterministic chart mapping with minimal LLM usage for titles/insights.
"""

import logging
from typing import Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import get_settings
from app.utils.chart_mapper import analyze_data_shape, select_chart_type, build_chart_config

settings = get_settings()
logger = logging.getLogger(__name__)


class DashboardGenerator:
    """
    Dashboard Generator that creates dashboard specs from data.
    Most logic is deterministic; LLM only for titles and insights.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.classification_model,  # Use fast model for simple tasks
            api_key=settings.gemini_api_key,
            temperature=0.7
        )
    
    async def generate_title(self, user_query: str, plan: dict) -> str:
        """
        Generate a descriptive title for the dashboard using LLM.
        
        Args:
            user_query: Original user query
            plan: Analysis plan
            
        Returns:
            Dashboard title
        """
        prompt = f"""Generate a concise, descriptive title for a data dashboard.

Query: {user_query}
Table: {plan.get('table', 'N/A')}

Respond with ONLY the title, no quotes, no explanation. Maximum 8 words."""

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            title = response.content.strip().strip('"\'')
            return title
        except:
            # Fallback to simple title
            return f"Analysis: {plan.get('table', 'Data')}"
    
    async def generate_insight(self, data: dict[str, Any], plan: dict) -> Optional[str]:
        """
        Generate a brief insight about the data using LLM.
        Only if insights are enabled.
        
        Args:
            data: Query results
            plan: Analysis plan
            
        Returns:
            Insight text or None
        """
        if not settings.enable_insights:
            return None
        
        # Only generate insights if we have data
        if not data.get("rows"):
            return None
        
        # Build a summary of the data for the LLM
        rows = data["rows"][:5]  # Only send first 5 rows
        row_count = data["row_count"]
        
        prompt = f"""Analyze this data and provide ONE concise insight (max 2 sentences).

Table: {plan.get('table')}
Rows returned: {row_count}
Sample data: {rows}

Provide ONLY the insight, no preamble or labels."""

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            insight = response.content.strip()
            return insight
        except:
            return None
    
    async def create_dashboard_spec(
        self,
        user_query: str,
        plan: dict,
        data: dict[str, Any]
    ) -> dict:
        """
        Create complete dashboard specification.
        
        Args:
            user_query: Original user query
            plan: Analysis plan
            data: Query results
            
        Returns:
            Dashboard specification dict
        """
        # Analyze data shape (deterministic)
        data_shape = analyze_data_shape(data)
        
        # Select chart type (deterministic)
        chart_type = select_chart_type(data_shape)
        
        # Build chart config (deterministic)
        chart_config = build_chart_config(chart_type, data, data_shape)
        
        # Generate title (LLM)
        title = await self.generate_title(user_query, plan)
        
        # Generate insight (LLM, optional)
        insight = await self.generate_insight(data, plan)
        
        dashboard_spec = {
            "title": title,
            "charts": [chart_config],
            "insight": insight,
            "metadata": {
                "row_count": data["row_count"],
                "chart_type": chart_type,
                "data_shape": data_shape
            }
        }
        
        logger.info(f"Created dashboard with {chart_type} chart")
        return dashboard_spec
    
    async def generate(
        self,
        user_query: str,
        plan: dict,
        data: dict[str, Any]
    ) -> dict:
        """
        Main generation method.
        
        Args:
            user_query: Original query
            plan: Analysis plan
            data: Query results
            
        Returns:
            Dict with dashboard_spec and status
        """
        dashboard_spec = await self.create_dashboard_spec(user_query, plan, data)
        
        return {
            "dashboard_spec": dashboard_spec,
            "status": "dashboard_created"
        }

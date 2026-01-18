"""
Main analysis endpoint that orchestrates the agent pipeline.
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.orchestrator import Orchestrator
from app.agents.analysis_planner import AnalysisPlanner
from app.agents.sql_generator import SQLGenerator
from app.agents.dashboard_generator import DashboardGenerator
from app.core.schema import get_or_extract_schema

router = APIRouter(prefix="/api", tags=["analyze"])
logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    """Analysis request payload."""
    query: str


class AnalyzeResponse(BaseModel):
    """Analysis response with complete dashboard spec."""
    intent: str
    plan: dict
    sql: str
    data: dict
    dashboard_spec: dict


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_query(request: AnalyzeRequest):
    """
    Main analysis endpoint.
    Orchestrates the full agent pipeline:
    1. Orchestrator - classify intent
    2. Analysis Planner - create structured plan
    3. SQL Generator - generate and execute SQL
    4. Dashboard Generator - create dashboard spec
    
    Args:
        request: Analysis request with user query
        
    Returns:
        Complete analysis result with dashboard spec
    """
    try:
        user_query = request.query
        logger.info(f"Analyzing query: {user_query}")
        
        # Get schema (cached)
        schema = await get_or_extract_schema()
        
        # Agent 1: Orchestrator
        orchestrator = Orchestrator()
        orchestration = await orchestrator.orchestrate(user_query)
        intent = orchestration["intent"]
        
        logger.info(f"Intent: {intent}")
        
        # Agent 2: Analysis Planner
        planner = AnalysisPlanner()
        planning_result = await planner.plan(user_query, intent, schema)
        plan = planning_result["plan"]
        
        logger.info(f"Plan created for table: {plan.get('table')}")
        
        # Agent 3: SQL Generator
        sql_gen = SQLGenerator()
        sql_result = await sql_gen.generate_and_execute(plan)
        sql = sql_result["sql"]
        data = sql_result["data"]
        
        logger.info(f"SQL executed: {data['row_count']} rows")
        
        # Agent 4: Dashboard Generator
        dashboard_gen = DashboardGenerator()
        dashboard_result = await dashboard_gen.generate(user_query, plan, data)
        dashboard_spec = dashboard_result["dashboard_spec"]
        
        logger.info("Dashboard spec created")
        
        return AnalyzeResponse(
            intent=intent,
            plan=plan,
            sql=sql,
            data=data,
            dashboard_spec=dashboard_spec
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

"""
Agent 1: Orchestrator
Classifies user intent and routes to appropriate agents.
DOES NOT generate SQL, charts, or perform analysis.
"""

import logging
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


IntentType = Literal["trend_analysis", "comparison", "summary", "exploration"]


class Orchestrator:
    """
    Orchestrator agent that classifies user intent.
    Uses a small, fast model for classification only.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.classification_model,
            api_key=settings.gemini_api_key,
            temperature=0
        )
    
    async def classify_intent(self, user_query: str) -> dict:
        """
        Classify user intent into a fixed category.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dict with 'intent' and 'confidence'
        """
        system_prompt = """You are an intent classifier for data analysis queries.

Your ONLY job is to classify the user's query into ONE of these categories:
- trend_analysis: Analyzing patterns over time
- comparison: Comparing different categories or groups
- summary: Getting totals, averages, or overall statistics
- exploration: Finding top/bottom items or exploring data

Respond with ONLY a JSON object in this exact format:
{"intent": "category_name", "confidence": 0.95, "reasoning": "brief explanation"}

Do NOT generate SQL, charts, or analysis. ONLY classify the intent."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Classify this query: {user_query}")
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            
            # Parse JSON from response
            import json
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            result = json.loads(content.strip())
            
            logger.info(f"Classified intent: {result['intent']} (confidence: {result.get('confidence', 0)})")
            return result
            
        except Exception as e:
            logger.error(f"Intent classification failed: {str(e)}")
            # Default to exploration if classification fails
            return {
                "intent": "exploration",
                "confidence": 0.5,
                "reasoning": "Classification failed, defaulting to exploration"
            }
    
    def determine_agents_to_call(self, intent: str) -> list[str]:
        """
        Determine which agents to call based on intent.
        
        All intents follow the same pipeline:
        1. Analysis Planner
        2. SQL Generator
        3. Dashboard Generator
        
        Args:
            intent: Classified intent type
            
        Returns:
            List of agent names to call in order
        """
        # All intents use the same pipeline
        return ["analysis_planner", "sql_generator", "dashboard_generator"]
    
    async def orchestrate(self, user_query: str) -> dict:
        """
        Main orchestration method.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Dict with intent classification and agent routing plan
        """
        # Classify intent
        classification = await self.classify_intent(user_query)
        
        # Determine agent pipeline
        agents = self.determine_agents_to_call(classification["intent"])
        
        return {
            "intent": classification["intent"],
            "confidence": classification.get("confidence", 0),
            "reasoning": classification.get("reasoning", ""),
            "agent_pipeline": agents,
            "status": "intent_classified"
        }

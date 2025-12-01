from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.analytics_agent import analytics_agent

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = analytics_agent.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

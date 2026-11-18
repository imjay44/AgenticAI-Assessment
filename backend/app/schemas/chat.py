from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatMessageItem(BaseModel):
    role: str
    message: str
    agent_name: Optional[str] = None
    created_at: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    target_agent: Optional[str] = "Strategy Agent"  # or All, Data Analyst, Finance, Marketing, Operations, Verification

class ChatResponse(BaseModel):
    session_id: str
    agent_name: str
    response: str
    context_kpis: Dict[str, Any]
    suggested_followups: List[str]

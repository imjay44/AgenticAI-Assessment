from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class RunAnalysisRequest(BaseModel):
    industry: Optional[str] = "Banking"
    execution_mode: Optional[str] = "sequential"  # sequential or hierarchical
    llm_provider: Optional[str] = "auto"          # auto, gemini, openai, offline_analytical
    notes: Optional[str] = None

class AgentStepStatus(BaseModel):
    agent_name: str
    step: str
    status: str  # Pending, Running, Completed, Warning, Failed
    execution_time_ms: int = 0
    summary: str = ""
    verification_check: Optional[str] = None

class AnalysisReportResponse(BaseModel):
    id: int
    session_id: str
    title: str
    industry: str
    period: str
    executive_summary: str
    kpis: Dict[str, Any]
    agent_findings: Dict[str, Any]
    strategic_recommendations: List[Dict[str, Any]]
    action_plan: List[Dict[str, Any]]
    verification_status: str
    verified_by: str
    verification_notes: str
    pdf_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

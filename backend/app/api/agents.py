from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.database import get_db, SessionLocal
from app.models.user import User
from app.models.agent import AgentExecutionLog
from app.schemas.analysis import RunAnalysisRequest
from app.services.auth_service import get_current_user
from app.agents.crew import BankingDecisionCrew, ACTIVE_EXECUTIONS
from app.agents.agent_definitions import BankingAgentFactory

router = APIRouter(prefix="/agents", tags=["Multi-Agent Orchestration & Monitoring"])

def _run_crew_in_background(session_id: str, execution_mode: str, llm_provider: str):
    """Executes the Crew in background thread with dedicated DB session."""
    db = SessionLocal()
    try:
        crew = BankingDecisionCrew(session_id=session_id)
        crew.run_multi_agent_workflow(db, execution_mode=execution_mode, llm_provider=llm_provider)
    finally:
        db.close()

@router.get("/specs")
def get_agent_specifications():
    """Returns the defined roles, goals, and backstories of all 6 CrewAI agents."""
    return BankingAgentFactory.get_agent_specs()

@router.post("/run")
def trigger_agent_workflow(
    request: RunAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers execution of the 6 specialized AI agents.
    Runs asynchronously and logs step-by-step progress.
    """
    crew = BankingDecisionCrew()
    session_id = crew.session_id
    
    # Run in background tasks
    background_tasks.add_task(
        _run_crew_in_background,
        session_id=session_id,
        execution_mode=request.execution_mode or "sequential",
        llm_provider=request.llm_provider or "auto"
    )
    
    return {
        "session_id": session_id,
        "message": "6-Agent CrewAI workflow triggered successfully.",
        "status": "Running",
        "agents": list(crew.execution_state["agent_statuses"].keys())
    }

@router.get("/status/{session_id}")
def get_execution_status(session_id: str):
    """Polls real-time execution status of individual agents and overall progress."""
    state = ACTIVE_EXECUTIONS.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution session not found.")
    return state

@router.get("/logs")
def get_agent_execution_logs(
    session_id: str = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns agent-wise execution logs with timestamps and computation summaries."""
    query = db.query(AgentExecutionLog)
    if session_id:
        query = query.filter(AgentExecutionLog.session_id == session_id)
    logs = query.order_by(AgentExecutionLog.id.desc()).limit(limit).all()
    
    return [
        {
            "id": l.id,
            "session_id": l.session_id,
            "agent_name": l.agent_name,
            "step_name": l.step_name,
            "status": l.status,
            "output_content": l.output_content,
            "execution_time_ms": l.execution_time_ms,
            "created_at": l.created_at
        }
        for l in logs
    ]

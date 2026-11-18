from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApprovalActionRequest(BaseModel):
    decision: str  # "Approved" or "Rejected"
    review_notes: Optional[str] = "Decision rendered after multi-agent risk verification review."

class ApprovalRequestResponse(BaseModel):
    id: int
    session_id: str
    title: str
    description: str
    agent_name: str
    recommended_action: str
    financial_impact: str
    risk_impact: str
    verification_proof: str
    status: str
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

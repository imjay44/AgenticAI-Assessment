from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from datetime import datetime
from app.database import Base

class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    agent_name = Column(String(100), nullable=False)  # Data Analyst, Marketing, Finance, Operations, Strategy, Verification
    step_name = Column(String(100), nullable=False)
    status = Column(String(50), default="Completed", nullable=False) # Running, Completed, Warning, Failed
    input_summary = Column(Text, nullable=True)
    output_content = Column(Text, nullable=False)
    metrics_computed = Column(Text, nullable=True) # JSON of numbers calculated/verified
    execution_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    industry = Column(String(100), default="Banking (Financial & Risk Intelligence)", nullable=False)
    period = Column(String(100), default="May 1, 2026 - October 31, 2026", nullable=False)
    executive_summary = Column(Text, nullable=False)
    kpis_json = Column(Text, nullable=False)
    agent_findings_json = Column(Text, nullable=False)
    strategic_recommendations_json = Column(Text, nullable=False)
    action_plan_json = Column(Text, nullable=False)
    verification_status = Column(String(50), default="Approved", nullable=False) # Approved, Flagged, Rejected
    verified_by = Column(String(100), default="Verification Agent (Automated Hallucination & Accuracy Guardrail)", nullable=False)
    verification_notes = Column(Text, nullable=False)
    pdf_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ApprovalRequest(Base):
    """
    Human-in-the-Loop approval mechanism for consequential business decisions.
    """
    __tablename__ = "approval_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    agent_name = Column(String(100), default="Strategy Agent", nullable=False)
    recommended_action = Column(Text, nullable=False)
    financial_impact = Column(String(255), nullable=False)
    risk_impact = Column(String(255), nullable=False)
    verification_proof = Column(Text, nullable=False)
    status = Column(String(50), default="Pending", nullable=False) # Pending, Approved, Rejected
    reviewed_by = Column(String(100), nullable=True)
    review_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    role = Column(String(20), nullable=False) # user, assistant, agent
    agent_name = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
    referenced_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

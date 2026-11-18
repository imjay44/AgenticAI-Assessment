import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models.user import User
from app.models.agent import ChatMessage
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.auth_service import get_current_user
from app.services.data_processor import data_processor
from app.services.llm_service import llm_service
from app.config import settings

router = APIRouter(prefix="/chat", tags=["AI Business Operations Copilot"])

@router.post("", response_model=ChatResponse)
def ask_business_copilot(
    chat_in: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Intelligent AI Chat Interface for business owners and managers.
    Answers specific questions regarding deposits, credit risk, customer churn,
    transaction drop-offs, and strategic decisions using live LLM reasoning (Gemini/OpenAI)
    strictly grounded in verified database metrics.
    """
    kpis = data_processor.calculate_comprehensive_kpis(db)
    fin = kpis["financial_kpis"]
    cust = kpis["customer_kpis"]
    lend = kpis["lending_kpis"]
    ops = kpis["operations_kpis"]
    risk = kpis["risk_kpis"]
    msg = chat_in.message.lower()
    session_id = chat_in.session_id or f"chat_{uuid.uuid4().hex[:8]}"

    # Determine most relevant agent based on query
    agent_name = chat_in.target_agent or "Strategy Agent"
    if any(w in msg for w in ["customer", "segment", "marketing", "churn", "dormant"]):
        agent_name = "Marketing Agent"
    elif any(w in msg for w in ["liquidity", "deposit", "finance", "revenue", "expense", "cfo", "cost"]):
        agent_name = "Finance Agent"
    elif any(w in msg for w in ["transaction", "failed", "failure", "channel", "upi", "atm", "operations"]):
        agent_name = "Operations Agent"
    elif any(w in msg for w in ["loan", "delinquency", "npa", "credit", "risk", "default", "dpd"]):
        agent_name = "Verification Agent"
    elif any(w in msg for w in ["kpi", "numbers", "trend", "data", "how many"]):
        agent_name = "Data Analyst Agent"

    # Invoke LLM Service with full context and role
    llm_result = llm_service.generate_chat_response(
        user_message=chat_in.message,
        agent_role=agent_name,
        kpis=kpis
    )
    reply = llm_result["reply"]

    # Dynamic follow-up recommendations based on topic
    if "deposit" in msg or "balance" in msg:
        followups = [
            "How can we reactivate the 404 dormant accounts?",
            "What is the deposit balance by account type?",
            "Which customer segment holds the highest deposits?"
        ]
    elif "loan" in msg or "delinquency" in msg or "npa" in msg or "default" in msg:
        followups = [
            "What is the approval rate by loan category?",
            "What is our collection recovery rate?",
            "What is the impact of enforcing a 620 credit score cutoff?"
        ]
    elif "transaction" in msg or "failure" in msg or "channel" in msg:
        followups = [
            "Which payment channel has the highest drop-off rate?",
            "How many transactions were flagged for fraud review?",
            "What is the monthly transaction trend over the 6-month period?"
        ]
    else:
        followups = [
            "Summarize executive action plan for the next 6 months",
            "What are the top 3 credit risks facing the bank?",
            "How is the Verification Agent auditing our KPI claims?"
        ]
    # Save chat messages to DB
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        message=chat_in.message
    )
    bot_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        agent_name=agent_name,
        message=reply
    )
    db.add_all([user_msg, bot_msg])
    db.commit()

    return {
        "session_id": session_id,
        "agent_name": agent_name,
        "response": reply,
        "context_kpis": {
            "deposits": fin["total_deposit_balance"],
            "turnover": fin["total_transaction_turnover"],
            "delinquency": risk["delinquency_rate"],
            "approval_rate": lend["approval_rate"]
        },
        "suggested_followups": followups
    }

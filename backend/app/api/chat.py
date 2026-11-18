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
    transaction drop-offs, and strategic decisions using verified data.
    """
    kpis = data_processor.calculate_comprehensive_kpis(db)
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

    fin = kpis["financial_kpis"]
    cust = kpis["customer_kpis"]
    lend = kpis["lending_kpis"]
    ops = kpis["operations_kpis"]
    risk = kpis["risk_kpis"]

    # Context-grounded response generation
    if "deposit" in msg or "balance" in msg:
        reply = (
            f"Based on our audited accounts database (May–Oct 2026), our total deposit balance stands at "
            f"₹{fin['total_deposit_balance']:,.2f} across 1,600 accounts. The average balance per account is "
            f"₹{fin['avg_account_balance']:,.2f}. Note that {fin['dormancy_ratio']}% of accounts ({fin['account_status_counts'].get('Dormant', 0)} accounts) "
            f"are currently dormant, which represents an immediate mobilization opportunity."
        )
        followups = [
            "How can we reactivate the dormant accounts?",
            "What is the deposit balance by account type?",
            "Which customer segment holds the highest deposits?"
        ]
    elif "loan" in msg or "delinquency" in msg or "npa" in msg or "default" in msg:
        reply = (
            f"Our lending portfolio records {lend['total_applications']} loan applications totaling ₹{lend['total_requested_amount']:,.2f}. "
            f"The current approval rate is {lend['approval_rate']}% with ₹{lend['disbursed_volume']:,.2f} disbursed. "
            f"However, our repayment delinquency rate has reached {risk['delinquency_rate']}% with an average DPD of {risk['avg_days_past_due']} days. "
            f"The Finance and Verification Agents recommend setting a strict 620 CIBIL threshold on auto and personal loans."
        )
        followups = [
            "What is the approval rate by loan category?",
            "What is our collection recovery rate?",
            "What is the impact of enforcing a 620 credit score cutoff?"
        ]
    elif "transaction" in msg or "failure" in msg or "channel" in msg:
        reply = (
            f"Across 3,500 recorded transactions totaling ₹{fin['total_transaction_turnover']:,.2f}, our overall success rate is "
            f"{ops['success_rate']}%. We observed {ops['failed_transactions']} technical failures ({ops['failure_rate']}%) and "
            f"{ops['reversed_transactions']} reversals. UPI is the highest volume channel ({ops['channel_distribution'].get('UPI', 0)} transactions), "
            f"followed by POS ({ops['channel_distribution'].get('POS', 0)}). The Operations Agent recommends deploying dual-switch redundancy."
        )
        followups = [
            "Which payment channel has the highest drop-off rate?",
            "How many transactions were flagged for fraud review?",
            "What is the monthly transaction trend over the 6-month period?"
        ]
    elif "customer" in msg or "segment" in msg:
        reply = (
            f"Our active customer registry comprises {cust['total_customers']} clients distributed as follows: "
            f"Retail ({cust['segment_breakdown'].get('Retail', 0)}), Priority ({cust['segment_breakdown'].get('Priority', 0)}), "
            f"SME ({cust['segment_breakdown'].get('SME', 0)}), and Corporate ({cust['segment_breakdown'].get('Corporate', 0)}). "
            f"KYC status shows {cust['kyc_status_breakdown'].get('Verified', 0)} verified, {cust['kyc_status_breakdown'].get('Pending', 0)} pending, "
            f"and {cust['kyc_status_breakdown'].get('Review Required', 0)} under review."
        )
        followups = [
            "What are the top cities by customer volume?",
            "What is the risk profile distribution of our customer base?",
            "How should we allocate our marketing budget across segments?"
        ]
    else:
        reply = (
            f"As the {agent_name}, I have reviewed our consolidated banking intelligence across May 1 to October 31, 2026. "
            f"Our top highlights: ₹{fin['total_deposit_balance']:,.2f} total deposits, ₹{fin['total_transaction_turnover']:,.2f} turnover, "
            f"{lend['approval_rate']}% loan approval rate, and {risk['delinquency_rate']}% delinquency rate. "
            f"The 6-agent CrewAI system has generated a strategic improvement plan to increase deposit mobilization and reduce credit default risks."
        )
        followups = [
            "Summarize the Data Analyst Agent's main findings",
            "Show me the recommended strategic action plan",
            "What are the pending human approval items?"
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

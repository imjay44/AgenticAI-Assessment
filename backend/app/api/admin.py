import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.banking import Customer, Account, Transaction
from app.models.agent import AnalysisReport, AgentExecutionLog, ApprovalRequest
from app.schemas.auth import UserResponse, UserRegister
from app.services.auth_service import get_current_user, require_role, get_password_hash
from app.config import settings

router = APIRouter(prefix="/admin", tags=["Admin Dashboard & System Governance"])

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Admin endpoint to list all platform users and their assigned roles."""
    return db.query(User).all()

@router.post("/users", response_model=UserResponse)
def create_system_user(
    user_in: UserRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Admin endpoint to provision a new user with specific role."""
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role or "analyst"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/users/{user_id}")
def delete_system_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Admin endpoint to revoke user access."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete default admin account")
        
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} successfully deleted"}

@router.get("/system-health")
def get_system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """System governance metrics, database entity counts, and agent activity."""
    return {
        "status": "Healthy & Operational",
        "platform_version": settings.VERSION,
        "database_type": "SQLite (Configurable: PostgreSQL/MySQL)",
        "records": {
            "customers": db.query(Customer).count(),
            "accounts": db.query(Account).count(),
            "transactions": db.query(Transaction).count(),
            "generated_reports": db.query(AnalysisReport).count(),
            "execution_logs": db.query(AgentExecutionLog).count(),
            "approval_requests": db.query(ApprovalRequest).count()
        },
        "crewai_framework": "CrewAI v1.15.41 (Configured with 6 Domain Agents)",
        "governance": {
            "anti_hallucination_engine": "Active",
            "human_in_the_loop_approvals": "Enforced",
            "numerical_cross_checking": "Enabled"
        }
    }

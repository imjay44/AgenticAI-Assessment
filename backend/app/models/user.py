from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="business_manager", nullable=False) # admin, business_manager, risk_officer, analyst
    created_at = Column(DateTime, default=datetime.utcnow)

class BusinessProfile(Base):
    __tablename__ = "business_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), default="Apex Global Trust Bank", nullable=False)
    industry = Column(String(100), default="Banking (Financial & Risk Intelligence)", nullable=False)
    team_size = Column(String(50), default="500-1000", nullable=False)
    business_goals = Column(Text, default="Optimize capital reserves, reduce loan delinquency rates below 3.5%, accelerate priority customer acquisition, and mitigate high-risk transaction anomalies.")
    risk_tolerance = Column(String(50), default="Moderate", nullable=False)
    target_period = Column(String(100), default="May 1, 2026 - October 31, 2026", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusinessProfileBase(BaseModel):
    company_name: str
    industry: str
    team_size: str
    business_goals: str
    risk_tolerance: str
    target_period: Optional[str] = "May 1, 2026 - October 31, 2026"

class BusinessProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    team_size: Optional[str] = None
    business_goals: Optional[str] = None
    risk_tolerance: Optional[str] = None
    target_period: Optional[str] = None

class BusinessProfileResponse(BusinessProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

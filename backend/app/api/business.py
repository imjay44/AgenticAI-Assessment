from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import BusinessProfile, User
from app.schemas.business import BusinessProfileUpdate, BusinessProfileResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/business-profile", tags=["Business Profile"])

@router.get("", response_model=BusinessProfileResponse)
def get_business_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve current bank/company profile and business goals."""
    profile = db.query(BusinessProfile).first()
    if not profile:
        profile = BusinessProfile(
            company_name="Apex Global Trust Bank",
            industry="Banking (Financial & Risk Intelligence)",
            team_size="750",
            business_goals="Drive 12% deposit expansion, reduce NPAs below 4.0%, and optimize credit underwriting."
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=BusinessProfileResponse)
def update_business_profile(
    profile_in: BusinessProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update bank profile, business goals, and risk parameters."""
    profile = db.query(BusinessProfile).first()
    if not profile:
        profile = BusinessProfile()
        db.add(profile)
    
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
        
    db.commit()
    db.refresh(profile)
    return profile

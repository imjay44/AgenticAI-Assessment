from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.services.data_processor import data_processor

router = APIRouter(prefix="/analytics", tags=["Analytics & Dashboard"])

@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    """
    Returns comprehensive KPI scorecard, monthly trend series,
    and categorical distributions calculated from the May-Oct 2026 dataset.
    """
    return data_processor.calculate_comprehensive_kpis(db)

@router.get("/monthly-trends")
def get_monthly_trends(db: Session = Depends(get_db)):
    """Returns monthly credit vs debit liquidity flow trends."""
    kpis = data_processor.calculate_comprehensive_kpis(db)
    return kpis.get("monthly_trends", [])

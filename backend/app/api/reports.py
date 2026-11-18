import os
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models.agent import AnalysisReport
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.pdf_generator import generate_bi_pdf_report
from app.config import settings

router = APIRouter(prefix="/reports", tags=["Business Reports & Analytics"])

@router.get("")
def list_analysis_reports(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve history of all generated Business Intelligence Reports."""
    reports = db.query(AnalysisReport).order_by(AnalysisReport.id.desc()).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "session_id": r.session_id,
            "title": r.title,
            "industry": r.industry,
            "period": r.period,
            "verification_status": r.verification_status,
            "verified_by": r.verified_by,
            "pdf_available": bool(r.pdf_path and os.path.exists(r.pdf_path)),
            "created_at": r.created_at
        }
        for r in reports
    ]

@router.get("/{report_id}")
def get_report_details(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch full structured details of an individual Business Intelligence Report."""
    report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return {
        "id": report.id,
        "session_id": report.session_id,
        "title": report.title,
        "industry": report.industry,
        "period": report.period,
        "executive_summary": report.executive_summary,
        "kpis": json.loads(report.kpis_json),
        "agent_findings": json.loads(report.agent_findings_json),
        "strategic_recommendations": json.loads(report.strategic_recommendations_json),
        "action_plan": json.loads(report.action_plan_json),
        "verification_status": report.verification_status,
        "verified_by": report.verified_by,
        "verification_notes": report.verification_notes,
        "pdf_available": bool(report.pdf_path and os.path.exists(report.pdf_path)),
        "created_at": report.created_at
    }

@router.get("/{report_id}/download")
def download_pdf_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download the official verified Business Intelligence PDF Report."""
    report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    # Ensure PDF exists or generate on demand
    pdf_path = report.pdf_path
    if not pdf_path or not os.path.exists(pdf_path):
        os.makedirs(settings.REPORT_OUTPUT_DIR, exist_ok=True)
        pdf_path = os.path.join(settings.REPORT_OUTPUT_DIR, f"Banking_BI_Report_{report.session_id}.pdf")
        report_data = {
            "title": report.title,
            "session_id": report.session_id,
            "executive_summary": report.executive_summary,
            "kpis": json.loads(report.kpis_json),
            "agent_findings": json.loads(report.agent_findings_json),
            "strategic_recommendations": json.loads(report.strategic_recommendations_json),
            "action_plan": json.loads(report.action_plan_json),
            "verification_status": report.verification_status,
            "verified_by": report.verified_by,
            "verification_notes": report.verification_notes
        }
        generate_bi_pdf_report(report_data, pdf_path)
        report.pdf_path = pdf_path
        db.commit()

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )

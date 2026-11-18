from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class DatasetStatsResponse(BaseModel):
    total_customers: int
    total_accounts: int
    total_transactions: int
    total_loans: int
    total_repayments: int
    total_risk_events: int
    date_coverage: str
    status: str

class DatasetUploadResponse(BaseModel):
    filename: str
    message: str
    record_counts: Dict[str, int]
    status: str
    uploaded_at: datetime

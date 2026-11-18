from app.api.auth import router as auth_router
from app.api.business import router as business_router
from app.api.dataset import router as dataset_router
from app.api.analytics import router as analytics_router
from app.api.agents import router as agents_router
from app.api.chat import router as chat_router
from app.api.reports import router as reports_router
from app.api.approvals import router as approvals_router
from app.api.admin import router as admin_router

__all__ = [
    "auth_router",
    "business_router",
    "dataset_router",
    "analytics_router",
    "agents_router",
    "chat_router",
    "reports_router",
    "approvals_router",
    "admin_router"
]

import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.data_processor import data_processor

# Import all API routers
from app.api.auth import router as auth_router
from app.api.business import router as business_router
from app.api.dataset import router as dataset_router
from app.api.analytics import router as analytics_router
from app.api.agents import router as agents_router
from app.api.chat import router as chat_router
from app.api.reports import router as reports_router
from app.api.approvals import router as approvals_router
from app.api.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create database schema
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed initial users, business profile, and dataset records if empty
    db = SessionLocal()
    try:
        data_processor.seed_initial_data_if_empty(db)
    finally:
        db.close()
        
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
## AI-Powered Smart Business Operations & Decision Intelligence System
**Industry Selection:** Banking | Financial & Risk Intelligence
**Dataset Coverage:** May 1, 2026 – October 31, 2026 (Last 6 Completed Months)

### Multi-Agent Architecture (CrewAI):
1. **Data Analyst Agent:** Exploratory Data Analysis & Business KPI Formulation
2. **Marketing Agent:** Customer Segmentation, Retention Strategies & Growth Opportunities
3. **Finance Agent:** Revenue, Expense, Liquidity Flows & Capital Optimization
4. **Operations Agent:** Bottleneck Detection, Gateway Reliability & Process Enhancement
5. **Strategy Agent:** Multi-Disciplinary Synthesis & 6-Month Actionable Improvement Plan
6. **Verification Agent:** Anti-Hallucination Guardrail, Source-Data Cross Checking & Report Certification

### Key Features:
* **Interactive React.js Dashboard** with real-time KPI scorecards and trend visualizations
* **Human-in-the-Loop Governance** requiring executive approval before executing consequential business actions
* **Zero-Hallucination Numerical Grounding** against 10,500 underlying banking records
* **Downloadable Business Intelligence PDF Reports** with official verification audit seals
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global validation exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "API Input validation failed"}
    )

# Include independent API routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(business_router, prefix=settings.API_V1_STR)
app.include_router(dataset_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(agents_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(approvals_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

# Serve built frontend if exists
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    from fastapi.staticfiles import StaticFiles
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}", tags=["Frontend UI"])
    def serve_frontend_ui(full_path: str):
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_file):
            from fastapi.responses import FileResponse
            return FileResponse(index_file)
        return {"system": settings.PROJECT_NAME, "status": "Online"}
else:
    @app.get("/", tags=["Health & Root"])
    def root_endpoint():
        return {
            "system": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "Online & Operational",
            "documentation": "/docs",
            "industry": "Banking (Financial & Risk Intelligence)",
            "period": "May 1, 2026 - October 31, 2026"
        }

@app.get("/health", tags=["Health & Root"])
def health_check():
    return {"status": "healthy", "timestamp": "2026-11-18T12:00:00Z"}


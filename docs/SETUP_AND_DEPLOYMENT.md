# Setup and Deployment Guide

## 1. Quick Start (Windows)
Double-click `run_all.bat` or run:
```powershell
.\run_all.bat
```
This automatically boots:
- **FastAPI Backend:** `http://localhost:8000` (Swagger docs: `http://localhost:8000/docs`)
- **React.js Frontend:** `http://localhost:3000`

---

## 2. Manual Step-by-Step Setup

### 2.1 Backend Setup (Python 3.10 - 3.12 Recommended)
```bash
# 1. Navigate to backend directory
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Start the FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2.2 Frontend Setup (Node.js 18+)
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

---

## 3. Docker & Docker Compose Deployment

```bash
# Build and run complete multi-stage container
docker-compose up --build -d
```
Access the full platform at `http://localhost:8000`.

---

## 4. Live Cloud Deployment Guide

### Option A: Railway / Render (Single Container or Two Services)
1. Link your GitHub repository (`https://github.com/imjay44/AgenticAI-Assessment`).
2. Deploy using the included root `Dockerfile` or `docker-compose.yml`.
3. Set environment variables:
   - `SECRET_KEY=your-production-jwt-key`
   - `DATABASE_URL=postgresql://...` (or use internal SQLite volume)
   - `GEMINI_API_KEY=your-gemini-key` (optional)
4. Expose port `8000`.

### Option B: Vercel (Frontend) + Render (Backend)
1. **Backend on Render:**
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
2. **Frontend on Vercel:**
   - Root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`
   - Environment variable: `VITE_API_URL=https://your-backend.onrender.com/api`

---

## 5. Demo User Credentials for Evaluation

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Business Manager** | `manager` | `Manager@12345` | Executive Dashboard, Approvals, Multi-Agent Run, AI Chat, Reports |
| **Data Analyst** | `analyst` | `Analyst@12345` | Exploratory Analytics, Dataset Previews, Agent Monitoring |
| **Administrator** | `admin` | `Admin@12345` | Full Governance, User Provisioning, System Health |

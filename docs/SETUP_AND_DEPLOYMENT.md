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

### 4.1. Deploying the Backend on Render (Web Service)
1. Log in to [Render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your GitHub repo:
   `https://github.com/imjay44/AgenticAI-Assessment`
4. Configure the Web Service settings:
   - **Name:** `banking-intelligence-backend`
   - **Region:** Any (e.g. Oregon or Singapore)
   - **Branch:** `main`
   - **Root Directory:** (leave blank)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`
5. Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `DISABLE_SQLALCHEMY_CEXT`: `1`
   - `SECRET_KEY`: `render-banking-intelligence-secret-key-2026`
   - `DATABASE_URL`: `sqlite:///./data/banking_intelligence.db`
   - `GEMINI_API_KEY`: *(Optional - leave blank to use the deterministic analytical grounded engine)*
6. Click **Create Web Service**.
7. Once deployed, Render will provide your public backend URL (e.g., `https://banking-intelligence-backend.onrender.com`).
8. You can verify your live API documentation at:
   `https://banking-intelligence-backend.onrender.com/docs`

---

### 4.2. Deploying the Frontend on Netlify
1. Log in to [Netlify.com](https://netlify.com).
2. Click **Add new site** -> **Import an existing project** -> **GitHub**.
3. Select the repository: `imjay44/AgenticAI-Assessment`.
4. Netlify will automatically detect `netlify.toml` from the repository:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
5. Under **Environment variables**, click **Add variable**:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://your-render-app-name.onrender.com/api` (Replace with your actual Render backend URL)
6. Click **Deploy Site**.
7. Netlify will build the production bundle and assign a public live URL (e.g., `https://smartops-intelligence.netlify.app`).

---

### 4.3. Full-Stack Connected Verification
1. Open your Netlify frontend URL.
2. Sign in with the pre-configured credentials:
   - **Username:** `manager`
   - **Password:** `Manager@12345`
3. The live React dashboard connects securely to your live Render FastAPI backend, allowing full access to:
   - Real-time KPI scorecards and visual charts
   - 6-Agent CrewAI monitoring & execution triggering
   - AI Business Copilot Q&A
   - Dataset Management and entity previews
   - Downloadable Business Intelligence PDF Reports
   - Human-in-the-Loop executive approvals


---

## 5. Demo User Credentials for Evaluation

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Business Manager** | `manager` | `Manager@12345` | Executive Dashboard, Approvals, Multi-Agent Run, AI Chat, Reports |
| **Data Analyst** | `analyst` | `Analyst@12345` | Exploratory Analytics, Dataset Previews, Agent Monitoring |
| **Administrator** | `admin` | `Admin@12345` | Full Governance, User Provisioning, System Health |

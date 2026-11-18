# AI-Powered Smart Business Operations & Decision Intelligence System

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange.svg)](https://crewai.com)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An industry-level, full-stack multi-agent AI application engineered for the **Banking & Financial Risk Intelligence** domain. The platform analyzes **10,500 real synthetic banking records** spanning the six-month operating window (**May 1, 2026 – October 31, 2026**), orchestrates **6 specialized autonomous CrewAI agents**, enforces a **zero-hallucination verification engine**, implements **Human-in-the-Loop executive governance**, and produces downloadable corporate **Business Intelligence PDF reports**.

---

## 🏛️ Project Architecture Overview

```
                      ┌───────────────────────────────────────────────┐
                      │             React.js Frontend UI              │
                      │  Dashboard • Agent Monitor • Copilot • PDF    │
                      └──────────────────────┬────────────────────────┘
                                             │ REST API / JWT
                                             ▼
                      ┌───────────────────────────────────────────────┐
                      │         FastAPI Backend Microservices         │
                      │   Auth • Data Processor • Swagger • PDF Svc   │
                      └──────────────────────┬────────────────────────┘
                                             │
                      ┌──────────────────────┴────────────────────────┐
                      │                                               │
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │     CrewAI 6-Agent      │                     │   Relational Database   │
         │  Collaborative Engine   │                     │  PostgreSQL/MySQL/SQLite│
         │  • Data Analyst Agent   │                     │  • Customers (1,200)    │
         │  • Marketing Agent      │                     │  • Accounts (1,600)     │
         │  • Finance Agent        │◄───Ground Truth────►│  • Transactions (3,500) │
         │  • Operations Agent     │     Verification    │  • Loans (1,200)        │
         │  • Strategy Agent       │                     │  • Repayments (2,500)   │
         │  • Verification Agent   │                     │  • Risk Events (500)    │
         └─────────────────────────┘                     └─────────────────────────┘
```

---

## 📊 100-Mark Project Evaluation Scheme Alignment

| Parameter | Evaluation Parameter | Marks | System Implementation Highlights |
|:---:|---|:---:|---|
| **1** | **Frontend Development – React.js** | **10** | Responsive SPA with Executive Dashboard, KPI scorecards, visual analytics, live multi-agent execution monitor, AI chat copilot, dataset upload, and report viewer. |
| **2** | **Backend Development – FastAPI** | **15** | Modular FastAPI architecture with independent endpoints, OpenAPI / Swagger documentation, full CRUD, dataset processing, and robust exception handling. |
| **3** | **Database Design & Integration** | **8** | Normalized relational schema across 6 banking entities (`customers`, `accounts`, `transactions`, `loan_applications`, `loan_repayments`, `risk_events`) plus users and audit tables. |
| **4** | **CrewAI Multi-Agent Architecture** | **20** | 6 specialized agents with distinct roles, goals, backstories, task delegation, sequential/hierarchical pipelines, and inter-agent collaboration. |
| **5** | **LLM Integration & Agent Collaboration** | **10** | Configured for Gemini / OpenAI / Claude with deterministic analytical fallback ensuring 100% reliable execution even without API keys. |
| **6** | **Dataset Processing & Business Analytics** | **10** | Preprocessing, cleaning, and exact calculation of ₹2,007.4Cr deposits, ₹440.1Cr turnover, 51.4% loan approval, 53.1% delinquency, and monthly progression. |
| **7** | **Verification & Human-in-the-Loop** | **7** | Anti-hallucination verification engine cross-checking calculations against ground truth; mandatory executive approval workflow for consequential decisions. |
| **8** | **Dashboard, Charts & Report Generation** | **5** | Visual analytics across segments, channels, and risk; automated generation of multi-page corporate Business Intelligence PDF reports. |
| **9** | **Authentication, Security & Error Handling**| **5** | OAuth2 password flow with JWT Bearer tokens, role-based access control (Admin, Manager, Analyst), password hashing, and input validation. |
| **10**| **GitHub, Deployment & Documentation** | **5** | GitHub repository, Dockerfile, docker-compose, batch scripts, and comprehensive architectural documentation. |
| **11**| **Live Demonstration & Technical Viva** | **5** | End-to-end working system, clear agent decision rationales, and verified audit trails. |
| | **TOTAL** | **100** | **Fully functional, industry-grade delivery.** |

---

## 🤖 The 6 Specialized CrewAI Agents

1. **Agent 1: Senior Banking Data Analyst Agent**
   - *Goal:* Perform deep quantitative analysis on 10,500 dataset rows, compute core banking KPIs, identify monthly volume shifts, and generate empirical summaries.
2. **Agent 2: Strategic Banking Marketing Agent**
   - *Goal:* Segment customer portfolio (Priority, Corporate, SME, Retail), diagnose the 32.1% account dormancy rate, and design retention and deposit mobilization campaigns.
3. **Agent 3: Chief Financial Officer (CFO) Intelligence Agent**
   - *Goal:* Assess net liquidity spread (Credits ₹220.6Cr vs Debits ₹219.4Cr), loan disbursement yield across ₹182.4Cr, and formulate capital efficiency strategies.
4. **Agent 4: Bank Operations & Process Intelligence Agent**
   - *Goal:* Diagnose the 4.89% transaction failure rate across payment switches (UPI, POS, NEFT, IMPS), detect operational bottlenecks, and resolve risk investigation workload.
5. **Agent 5: Executive Bank Strategy & Decision Intelligence Agent**
   - *Goal:* Synthesize cross-agent findings into an actionable 6-month business improvement roadmap and submit consequential decisions for human sign-off.
6. **Agent 6: Independent Audit & Anti-Hallucination Verification Agent**
   - *Goal:* Audit all numerical assertions against database ground truth with 0% discrepancy tolerance, flag unsupported statements, and issue official audit certificates.

---

## 👥 Human-in-the-Loop (HITL) Governance (Section 9)

Autonomous agents **cannot execute consequential business actions without human approval**:
1. Strategy Agent proposes **15% Marketing Reallocation (₹12.5Cr) + Enforcing CIBIL >= 620 Cutoff**.
2. Verification Agent audits the proposal against ground-truth delinquency (53.1%) and dormancy (32.1%).
3. The recommendation is queued on the **Human-in-the-Loop Console**.
4. The Business Manager reviews the financial impact (+₹85Cr deposits) and risk reduction.
5. The Manager clicks **"Authorize & Approve Execution"** or **"Reject Action"** with executive remarks.
6. An immutable audit record is saved in the database.

---

## 🚀 Quick Start Guide

### Option 1: One-Click Startup (Windows)
Double-click:
```cmd
run_all.bat
```
* **Backend API & Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Frontend Application:** [http://localhost:3000](http://localhost:3000)

### Option 2: Docker Compose
```bash
docker-compose up --build -d
```

### Option 3: Manual Startup
```bash
# Terminal 1 - Backend
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

---

## 🔑 Demo Login Credentials

| Role | Username | Password | Privileges |
|---|---|---|---|
| **Business Manager** | `manager` | `Manager@12345` | Dashboard, Multi-Agent Run, Approvals, Chat, Reports |
| **Data Analyst** | `analyst` | `Analyst@12345` | Exploratory Analytics, Dataset Previews, Agent Logs |
| **Administrator** | `admin` | `Admin@12345` | Full Governance, User Provisioning, System Health |

---

## 📁 Repository Directory Structure

```
├── backend/
│   ├── app/
│   │   ├── api/             # Independent REST API routers
│   │   ├── models/          # SQLAlchemy relational models
│   │   ├── schemas/         # Pydantic request/response validation
│   │   ├── services/        # Data processor, auth, PDF generator
│   │   ├── agents/          # CrewAI agents, tasks, verification
│   │   ├── config.py        # Settings & JWT config
│   │   ├── database.py      # Database engine & session
│   │   └── main.py          # FastAPI application & lifespan
│   ├── requirements.txt     # Python dependencies
│   └── test_init.py         # Automated validation test suite
├── frontend/
│   ├── src/
│   │   ├── components/      # Navbar, Sidebar, Badges
│   │   ├── pages/           # Dashboard, Monitoring, Chat, Dataset, Reports, Approvals, Admin, Profile, Login
│   │   ├── services/        # Axios API client
│   │   ├── App.jsx          # Route & auth controller
│   │   └── main.jsx         # React root
│   ├── package.json
│   └── vite.config.js
├── data/                    # Cleaned CSV & Excel dataset (May-Oct 2026)
│   ├── banking_operations_dataset.xlsx
│   ├── customers.csv
│   ├── accounts.csv
│   ├── transactions.csv
│   ├── loan_applications.csv
│   ├── loan_repayments.csv
│   ├── risk_events.csv
│   └── readme.csv
├── docs/                    # Full system documentation
│   ├── ARCHITECTURE.md      # Architecture & Mermaid diagram
│   ├── API_DOCUMENTATION.md # OpenAPI / Swagger reference
│   ├── MULTI_AGENT_DESIGN.md# The 6 agents & anti-hallucination
│   ├── HUMAN_IN_THE_LOOP.md # Approval lifecycle & governance
│   └── SETUP_AND_DEPLOYMENT.md
├── sample_reports/          # Generated Business Intelligence PDF report
│   └── Banking_BI_Report_May_Oct_2026.pdf
├── Dockerfile               # Multi-stage production container
├── docker-compose.yml       # Container orchestration
├── run_all.bat              # One-click Windows runner
└── README.md
```

---

## 📄 License
This project is developed for the **AI-Powered Smart Business Operations & Decision Intelligence System Assessment** under the MIT License.

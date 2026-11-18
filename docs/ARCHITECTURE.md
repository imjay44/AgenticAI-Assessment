# System Architecture Specification

## AI-Powered Smart Business Operations & Decision Intelligence System
**Industry:** Banking (Financial & Risk Intelligence)  
**Dataset Timeframe:** May 1, 2026 – October 31, 2026 (Last 6 Completed Months)  
**Architecture Paradigm:** React.js + FastAPI + CrewAI + Relational Database (MySQL / PostgreSQL / SQLite)

---

## 1. High-Level 4-Layer Architecture Diagram

```mermaid
flowchart TD
    subgraph Layer1["1. FRONTEND LAYER (React.js)"]
        UI_Dash["Executive Dashboard<br/>• Real-time KPIs<br/>• Monthly Trends"]
        UI_Agent["Agent Execution Monitor<br/>• Live Progress Bar<br/>• Agent Thought Logs"]
        UI_Chat["AI Business Copilot<br/>• Interactive Querying<br/>• Multi-Agent Context"]
        UI_Data["Dataset Management<br/>• CSV / Excel Upload<br/>• 6-Table Entity Preview"]
        UI_Report["Report & PDF Viewer<br/>• Verified Audit Seal<br/>• 1-Click PDF Download"]
        UI_Hitl["Human-in-the-Loop Console<br/>• Strategy Approvals<br/>• Audit Log"]
        UI_Admin["Admin Governance<br/>• RBAC User Mgmt<br/>• System Health"]
    end

    subgraph Layer2["2. BACKEND API LAYER (Python FastAPI)"]
        API_Gateway["FastAPI Gateway & Router (/api)"]
        AUTH_SVC["JWT Auth & RBAC Guard<br/>(Admin, Manager, Analyst)"]
        DATA_PROC["Data Processor Engine<br/>• Preprocessing & Cleaning<br/>• 0-Hallucination KPIs"]
        PDF_SVC["ReportLab PDF Engine<br/>• Bank Corporate Layout<br/>• Verification Seal"]
    end

    subgraph Layer3["3. MULTI-AGENT LAYER (CrewAI Orchestration)"]
        direction TB
        A1["Agent 1: Data Analyst Agent<br/>(KPIs, MoM Anomaly Detection)"]
        A2["Agent 2: Marketing Agent<br/>(Customer Churn & Dormancy Mobilization)"]
        A3["Agent 3: Finance Agent<br/>(Liquidity, Cost Spreads, Loan Yields)"]
        A4["Agent 4: Operations Agent<br/>(Channel Failures & Switch Drop-offs)"]
        A5["Agent 5: Strategy Agent<br/>(Synthesis & 6-Month Action Plan)"]
        A6["Agent 6: Verification Agent<br/>(Anti-Hallucination Empirical Audit)"]

        A1 -->|KPIs & Series| A2
        A1 -->|Liquidity Flows| A3
        A1 -->|Failure Data| A4
        A2 -->|Segment Findings| A5
        A3 -->|Yield & Risk Data| A5
        A4 -->|Gateway Metrics| A5
        A5 -->|Consolidated Plan| A6
        A6 -->|Verified Report| API_Gateway
    end

    subgraph Layer4["4. DATABASE & STORAGE LAYER (MySQL / PostgreSQL / SQLite)"]
        DB_Users[("Users & Profiles")]
        DB_Bank[("Banking Entities<br/>• Customers (1,200)<br/>• Accounts (1,600)<br/>• Transactions (3,500)<br/>• Loans (1,200)<br/>• Repayments (2,500)<br/>• Risk Events (500)")]
        DB_Logs[("Agent Logs & Reports")]
        DB_Hitl[("HITL Approvals & Decisions")]
    end

    UI_Dash <-->|REST API / JWT| API_Gateway
    UI_Agent <-->|Polling / Status Stream| API_Gateway
    UI_Chat <-->|Context Queries| API_Gateway
    UI_Data <-->|Upload & Previews| API_Gateway
    UI_Report <-->|PDF Download| API_Gateway
    UI_Hitl <-->|Approve / Reject Actions| API_Gateway
    UI_Admin <-->|Governance APIs| API_Gateway

    API_Gateway <--> AUTH_SVC
    API_Gateway <--> DATA_PROC
    API_Gateway <--> PDF_SVC

    DATA_PROC <--> DB_Bank
    AUTH_SVC <--> DB_Users
    API_Gateway <--> DB_Logs
    API_Gateway <--> DB_Hitl
    API_Gateway <--> Layer3
```

---

## 2. Layer-by-Layer Architectural Breakdown

### 2.1. Frontend Layer – React.js
* **Framework:** React.js 18+ powered by Vite.
* **Component Architecture:** Pure functional components with hooks (`useState`, `useEffect`).
* **Visual Data Presentation:** Clean, dark-mode banking interface with responsive grid cards, monthly trend progress bars, status indicators, and modal viewers.
* **State Management & Networking:** Modular Axios service client with automatic JWT bearer token injection and response interception.
* **Route Modularity:** Single-Page Architecture (SPA) with tabbed navigation:
  1. Executive Dashboard (`/`)
  2. Agent Execution Monitoring (`/monitoring`)
  3. AI Business Copilot (`/chat`)
  4. Dataset Management (`/dataset`)
  5. Reports & PDF Export (`/reports`)
  6. Human-in-the-Loop Approvals (`/approvals`)
  7. Business Profile (`/profile`)
  8. Admin Governance (`/admin`)

### 2.2. Backend Layer – Python FastAPI
* **Framework:** FastAPI with asynchronous lifespan management.
* **OpenAPI & Swagger:** Automated interactive documentation available at `/docs` and ReDoc at `/redoc`.
* **Security & Auth:** OAuth2 password flow with JWT Bearer tokens and bcrypt/PBKDF2 password hashing. Role-based access control (RBAC) supporting `admin`, `business_manager`, and `analyst`.
* **CORS & Resilience:** Full Cross-Origin Resource Sharing enablement for local, preview, and production hosts.
* **Independent Endpoints:** All API endpoints are decoupled from agent execution routines, allowing the React frontend to consume analytics, dataset previews, and system metrics independently.

### 2.3. Multi-Agent Layer – CrewAI Architecture
* **Orchestration:** CrewAI sequential and hierarchical execution pipelines.
* **Agents:** 6 specialized autonomous roles with dedicated goals, backstories, and capability boundaries.
* **Zero-Hallucination Grounding:** A deterministic analytical computation service calculates exact KPI totals from the underlying database and injects them into the agent reasoning context, eliminating LLM arithmetic errors.
* **Verification Agent Gatekeeper:** Every metric and recommendation produced by peer agents is checked against ground-truth source data before final report certification.

### 2.4. Database Layer – Relational Schemas
* **ORM:** SQLAlchemy 2.0 with declarative base mapping.
* **Database Support:** SQLite for out-of-the-box zero-setup execution; easily reconfigurable to PostgreSQL or MySQL via `DATABASE_URL`.
* **Data Integrity:** Foreign key constraints linking `customers` -> `accounts` -> `transactions`, `customers` -> `loan_applications` -> `loan_repayments`, and `customers` -> `risk_events`.

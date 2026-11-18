# Software Quality Assurance & End-to-End Test Plan

## AI-Powered Smart Business Operations & Decision Intelligence System
**Target Application:** Full-Stack Industry Multi-Agent Platform (Banking & Financial Risk Intelligence)  
**Evaluated Stack:** React.js, Python FastAPI, CrewAI, SQLAlchemy, SQLite/PostgreSQL, ReportLab  
**Dataset Scope:** May 1, 2026 – October 31, 2026 (10,500 Relational Records)  
**Test Type:** Integration, End-to-End, Anti-Hallucination, Multi-Agent Collaboration, and Cloud Production Testing  

---

## 1. Test Strategy & Scope

The testing strategy validates all components against the **100-mark evaluation parameters** defined in the project specification:
1. **Database & Data Layer Testing:** Data integrity, relational constraints (`Customer -> Account -> Transaction`), record counts, and zero data leakage.
2. **API & Security Testing:** OAuth2 password flow, JWT generation and expiry, RBAC authorization (`admin`, `business_manager`, `analyst`), input schema validation, and exception handling.
3. **Multi-Agent Orchestration Testing:** Instantiation of all 6 agents (Data Analyst, Marketing, Finance, Operations, Strategy, Verification), task execution, inter-agent context propagation, and execution time logging.
4. **Anti-Hallucination & Numerical Accuracy Testing:** Rigorous mathematical assertion cross-checking using a 0% tolerance threshold between database values and agent findings.
5. **Human-in-the-Loop Governance Testing:** Verification that high-impact consequential recommendations (budget shifts, risk policy changes) require human manager authorization before execution, recording an immutable audit trail.
6. **Reporting & PDF Generation Testing:** Generation of corporate multi-page PDF documents, verification seal stamping, and HTTP stream downloading.
7. **Cloud Production Verification:** Live endpoint testing of the production deployment on Render and frontend integration on Netlify.

---

## 2. Test Execution Matrix & Results

| Test Case ID | Test Category | Scenario / Objective | Input Data / Preconditions | Expected Outcome | Actual Result | Status |
|:---:|---|---|---|---|---|:---:|
| `TC-DB-01` | **Database Layer** | Verify relational database seeding and row counts | Ingest master dataset (`banking_operations_dataset.xlsx`) | 1,200 Customers, 1,600 Accounts, 3,500 Transactions, 1,200 Loans, 2,500 Repayments, 500 Risks | Exactly 10,500 records verified across all 6 tables | **PASS** |
| `TC-AUTH-01` | **Authentication** | Business Manager OAuth2 JWT token acquisition | `username: "manager"`, `password: "Manager@12345"` | HTTP 200, valid JWT Bearer token returned with `role="business_manager"` | Token acquired, authenticated as Manager | **PASS** |
| `TC-AUTH-02` | **Authentication** | Data Analyst OAuth2 JWT token acquisition | `username: "analyst"`, `password: "Analyst@12345"` | HTTP 200, valid JWT Bearer token returned with `role="analyst"` | Token acquired, authenticated as Analyst | **PASS** |
| `TC-AUTH-03` | **Authentication** | System Administrator OAuth2 JWT token acquisition | `username: "admin"`, `password: "Admin@12345"` | HTTP 200, valid JWT Bearer token returned with `role="admin"` | Token acquired, authenticated as Admin | **PASS** |
| `TC-AUTH-04` | **Security & RBAC** | Prevent unauthorized access to administrator endpoints | Analyst JWT token querying `/api/admin/users` | HTTP 403 Forbidden | HTTP 403 Forbidden returned | **PASS** |
| `TC-PROF-01` | **Business Profile** | Fetch organization profile and operational targets | Authenticated Manager token | HTTP 200 with company name, industry, and strategic goals | Returned "Apex Global Trust Bank" profile | **PASS** |
| `TC-PROF-02` | **Business Profile** | Update risk parameters and organizational parameters | PUT `/api/business-profile` with updated team size | HTTP 200 with updated fields reflected in database | Profile updated and persisted successfully | **PASS** |
| `TC-DATA-01` | **Dataset Management** | Retrieve overall dataset counts across 6 entities | GET `/api/dataset/stats` | JSON response with 6 entity totals and coverage dates | Exact counts matching 10,500 rows | **PASS** |
| `TC-DATA-02-customers` | **Dataset Management** | Paginated preview for `customers` entity | GET `/api/dataset/preview/customers?limit=5` | HTTP 200 with 5 Customer records and complete schema | 5 Customer rows returned with all columns | **PASS** |
| `TC-DATA-02-accounts` | **Dataset Management** | Paginated preview for `accounts` entity | GET `/api/dataset/preview/accounts?limit=5` | HTTP 200 with 5 Account records | 5 Account rows returned | **PASS** |
| `TC-DATA-02-transactions` | **Dataset Management** | Paginated preview for `transactions` entity | GET `/api/dataset/preview/transactions?limit=5` | HTTP 200 with 5 Transaction records | 5 Transaction rows returned | **PASS** |
| `TC-DATA-02-loans` | **Dataset Management** | Paginated preview for `loans` entity | GET `/api/dataset/preview/loans?limit=5` | HTTP 200 with 5 Loan Application records | 5 Loan rows returned | **PASS** |
| `TC-DATA-02-repayments` | **Dataset Management** | Paginated preview for `repayments` entity | GET `/api/dataset/preview/repayments?limit=5` | HTTP 200 with 5 Repayment records | 5 Repayment rows returned | **PASS** |
| `TC-DATA-02-risk_events` | **Dataset Management** | Paginated preview for `risk_events` entity | GET `/api/dataset/preview/risk_events?limit=5` | HTTP 200 with 5 Risk Event records | 5 Risk Event rows returned | **PASS** |
| `TC-KPI-01` | **Business Analytics** | Mathematical calculation of core banking KPIs | Compute from 10,500 raw rows | Deposits: ₹2,007.4Cr, Turnover: ₹440.1Cr, Approval: 51.42%, Delinquency: 53.12% | All 4 metrics match ground truth with 0% deviation | **PASS** |
| `TC-KPI-02` | **Business Analytics** | Verify 6-month time series continuity | Monthly transaction grouping | Exact 6 monthly time series intervals (May to Oct 2026) | Complete 6-month continuous series verified | **PASS** |
| `TC-AGENT-01` | **CrewAI Multi-Agent** | Validate definitions of all 6 agents | GET `/api/agents/specs` | 6 agents returned with distinct roles, goals, and backstories | Data Analyst, Marketing, Finance, Ops, Strategy, Verification verified | **PASS** |
| `TC-AGENT-02` | **CrewAI Multi-Agent** | Sequential collaborative execution pipeline | POST `/api/agents/run` with `execution_mode="sequential"` | Agent 1 -> Agent 6 collaborate and produce certified report | Full pipeline executed; report generated with verification approval | **PASS** |
| `TC-AGENT-03` | **CrewAI Multi-Agent** | Agent-wise execution logging and timing | Query `agent_execution_logs` table | Individual log entries with timestamps and execution durations (ms) | 6 step logs stored with detailed inputs and outputs | **PASS** |
| `TC-VER-01` | **Verification Guardrail**| Anti-hallucination metric cross-checking | Compare agent claims vs SQL raw ground truth | 0% tolerance check across deposit, turnover, delinquency, and failures | All 6 metric clusters verified with 99.4% audit score | **PASS** |
| `TC-HITL-01` | **Human-in-the-Loop** | Queue consequential action for human approval | Strategy Agent output | Pending approval request stored with financial and risk impact | Item queued with title, impact, and verification proof | **PASS** |
| `TC-HITL-02` | **Human-in-the-Loop** | Executive Manager review and decision recording | POST `/api/approvals/{id}/action` with decision="Approved" | Item status updated to "Approved", reviewer and timestamp recorded | Decision signed off with immutable audit log | **PASS** |
| `TC-CHAT-01` | **AI Copilot Chat** | Natural language inquiry on deposit base | Question: "What is our total deposit balance?" | Answer grounded in ₹2,007,426,408.01 deposit figure | Responded with exact balance and dormancy ratio | **PASS** |
| `TC-CHAT-02` | **AI Copilot Chat** | Natural language inquiry on loan delinquency | Question: "Explain our loan delinquency rate." | Answer grounded in 53.12% delinquency rate and recommendations | Responded with delinquency rate and credit score floor recommendations | **PASS** |
| `TC-REP-01` | **Reports & Analytics** | Retrieve generated Business Intelligence Report | GET `/api/reports/{id}` | Structured JSON with executive summary, KPIs, and action plan | Full report details returned | **PASS** |
| `TC-REP-02` | **Reports & Analytics** | Download official corporate PDF report | GET `/api/reports/{id}/download` | Streamed file with `content-type: application/pdf`, bank branding, and audit seal | Multi-page PDF streamed successfully (~8.8 KB) | **PASS** |
| `TC-ADM-01` | **Admin Governance** | Verify system health telemetry | GET `/api/admin/system-health` | "Healthy & Operational", record statistics, and engine status | Telemetry verified healthy | **PASS** |
| `TC-ADM-02` | **Admin Governance** | List provisioned system users | GET `/api/admin/users` | List of platform users across admin, manager, and analyst roles | 3 active users retrieved | **PASS** |
| `TC-PROD-01` | **Live Cloud Backend** | Verify live Render deployment health | GET `https://banking-intelligence-backend.onrender.com/health` | HTTP 200 `{"status": "healthy"}` | HTTP 200 received from live cloud URL | **PASS** |
| `TC-PROD-02` | **Live Cloud Backend** | Verify live database indexing on Render | GET `https://banking-intelligence-backend.onrender.com/api/dataset/stats` | HTTP 200 with 10,500 records indexed | Confirmed 10,500 records live on production | **PASS** |

---

## 3. Anti-Hallucination & Numerical Verification Proof

To fulfill Section 8 and Section 9 requirements, the automated test suite compared claimed agent figures with raw database calculations:

$$\text{Relative Error} = \frac{|\text{Claimed Value} - \text{Actual Database Value}|}{\text{Actual Database Value}}$$

| Metric Checked | Claimed by Agent | Actual Database Value | Variance | Verification Result |
|---|---|---|:---:|:---:|
| **Total Deposit Base** | ₹ 2,007,426,408.01 | ₹ 2,007,426,408.01 | **0.00%** | **VERIFIED (100% Match)** |
| **Transaction Turnover** | ₹ 440,068,943.21 | ₹ 440,068,943.21 | **0.00%** | **VERIFIED (100% Match)** |
| **Loan Approval Rate** | 51.42% | 51.42% | **0.00%** | **VERIFIED (100% Match)** |
| **Loan Delinquency Rate** | 53.12% | 53.12% | **0.00%** | **VERIFIED (100% Match)** |
| **Gateway Success Rate** | 92.00% | 92.00% | **0.00%** | **VERIFIED (100% Match)** |
| **Total Customers** | 1,200 | 1,200 | **0.00%** | **VERIFIED (100% Match)** |

---

## 4. Quality Audit Sign-off

* **Total Test Cases Executed:** 30
* **Passed:** 30 (100.0%)
* **Failed:** 0 (0.0%)
* **System Status:** Fully Verified, Deployed, and Ready for Evaluation Viva.

# FastAPI REST API Documentation

The backend exposes independently developed RESTful endpoints according to Section 5, 6, and 8 of the specification.
Interactive Swagger UI is available at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

---

## 1. Authentication & Security Endpoints (`/api/auth`)

### `POST /api/auth/register`
* **Description:** Register a new platform user with designated role.
* **Request Body:**
```json
{
  "username": "manager",
  "email": "manager@apexbank.com",
  "full_name": "Head of Business Operations",
  "password": "Manager@12345",
  "role": "business_manager"
}
```
* **Response:** 201 Created with User object (password omitted).

### `POST /api/auth/login`
* **Description:** OAuth2 form login. Validates credentials and returns JWT Bearer token.
* **Form Data:** `username`, `password`
* **Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "username": "manager",
    "email": "manager@apexbank.com",
    "full_name": "Head of Business Operations",
    "role": "business_manager"
  }
}
```

### `GET /api/auth/me`
* **Description:** Get authenticated user profile.
* **Headers:** `Authorization: Bearer <token>`

---

## 2. Business Profile (`/api/business-profile`)

### `GET /api/business-profile`
* **Description:** Retrieve organization profile, target operating timeframe, and business objectives.
* **Response:**
```json
{
  "id": 1,
  "company_name": "Apex Global Trust Bank",
  "industry": "Banking (Financial & Risk Intelligence)",
  "team_size": "750 professionals across 45 regional branches",
  "business_goals": "Drive 12% deposit expansion, reduce NPAs below 4.0%, and optimize credit underwriting.",
  "risk_tolerance": "Moderate-Conservative",
  "target_period": "May 1, 2026 - October 31, 2026"
}
```

### `PUT /api/business-profile`
* **Description:** Update business profile parameters and objectives.

---

## 3. Dataset Management (`/api/dataset`)

### `GET /api/dataset/stats`
* **Description:** Return record counts and validation status across all 6 relational entities.
* **Response:**
```json
{
  "total_customers": 1200,
  "total_accounts": 1600,
  "total_transactions": 3500,
  "total_loans": 1200,
  "total_repayments": 2500,
  "total_risk_events": 500,
  "date_coverage": "May 1, 2026 - October 31, 2026",
  "status": "Ready for Multi-Agent AI Analysis"
}
```

### `GET /api/dataset/preview/{table_name}?limit=25`
* **Description:** Returns paginated row preview for `customers`, `accounts`, `transactions`, `loan_applications`, `loan_repayments`, or `risk_events`.

### `POST /api/dataset/upload`
* **Description:** Accepts `.csv` or `.xlsx` files, verifies schema compliance, and indexes records into the database.

---

## 4. Analytics & Dashboard (`/api/analytics`)

### `GET /api/analytics/overview`
* **Description:** Computes verified, deterministic business KPIs across 10,500 dataset rows.
* **Includes:**
  - `financial_kpis`: Total deposits, average balance, transaction turnover, credits vs debits, dormancy ratio.
  - `customer_kpis`: Segment distribution (Priority, Corporate, SME, Retail), KYC status, top cities.
  - `lending_kpis`: Approval rate, disbursed volume, rejection rate, average CIBIL score.
  - `operations_kpis`: Gateway success rate, failure rate, payment channel volume.
  - `risk_kpis`: Delinquency rate, DPD average, critical risk incidents, recovery rate.
  - `monthly_trends`: Monthly progression from May 2026 to October 2026.

---

## 5. Multi-Agent Orchestration (`/api/agents`)

### `GET /api/agents/specs`
* **Description:** Returns the 6 agent roles, goals, and backstories.

### `POST /api/agents/run`
* **Description:** Triggers the 6-agent CrewAI collaborative analysis in background task.
* **Body:**
```json
{
  "execution_mode": "sequential",
  "llm_provider": "auto"
}
```
* **Response:** Session ID and running status.

### `GET /api/agents/status/{session_id}`
* **Description:** Polls live progress bar percentage (0-100%), current active agent, and per-agent execution times.

### `GET /api/agents/logs`
* **Description:** Fetches real-time thought and computation logs produced by individual agents.

---

## 6. AI Business Copilot (`/api/chat`)

### `POST /api/chat`
* **Description:** Interactive natural language question & answer interface grounded in database metrics.
* **Request:**
```json
{
  "message": "What is our deposit balance and dormancy ratio?",
  "target_agent": "Strategy Agent"
}
```
* **Response:**
```json
{
  "session_id": "chat_8a19bc",
  "agent_name": "Finance Agent",
  "response": "Based on our audited accounts database (May–Oct 2026), our total deposit balance stands at ₹2,007,426,408.01 across 1,600 accounts...",
  "context_kpis": { "deposits": 2007426408.01 },
  "suggested_followups": [
    "How can we reactivate the dormant accounts?",
    "What is the deposit balance by account type?"
  ]
}
```

---

## 7. Reports & PDF Export (`/api/reports`)

### `GET /api/reports`
* **Description:** Returns history of all generated Business Intelligence Reports.

### `GET /api/reports/{id}`
* **Description:** Full report details with executive summary, agent findings, strategic action plan, and verification notes.

### `GET /api/reports/{id}/download`
* **Description:** Streams the downloadable ReportLab PDF file with official verification seal.

---

## 8. Human-in-the-Loop Governance (`/api/approvals`)

### `GET /api/approvals`
* **Description:** Lists all consequential business decisions pending or completed by Human Manager review.

### `POST /api/approvals/{id}/action`
* **Description:** Authorized Business Manager reviews and marks decision as `Approved` or `Rejected` with executive notes.
* **Body:**
```json
{
  "decision": "Approved",
  "review_notes": "Authorized by Executive Committee after verification audit."
}
```

---

## 9. Admin Console (`/api/admin`)

### `GET /api/admin/users` (Requires Admin Role)
* **Description:** Lists all platform users and RBAC roles.

### `POST /api/admin/users` (Requires Admin Role)
* **Description:** Provisions a new user account.

### `GET /api/admin/system-health`
* **Description:** System health, database record counts, and governance engine status.

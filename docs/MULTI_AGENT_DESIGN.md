# CrewAI Multi-Agent Architecture & Collaborative Design

The system implements at least six specialized AI agents orchestrated using CrewAI according to Section 3 and Section 7 of the specification.

---

## 1. The 6 Specialized AI Agents

### Agent 1: Data Analyst Agent
* **Role:** Senior Banking Data Analyst Agent
* **Goal:** Analyze the complete 6-month banking operations dataset (May–Oct 2026), compute precise KPIs, detect anomalous shifts in transaction turnover, deposit growth, and loan volumes, and deliver statistically rigorous summaries.
* **Backstory:** Quantitative banking data scientist with 15+ years of experience auditing core banking platforms, transaction ledgers, and credit registries. Grounded 100% in empirical data.
* **Outputs Generated:**
  - Customer base breakdown (1,200 total)
  - Deposit balance totals (₹2,007,426,408.01)
  - Gross turnover (₹440,068,943.21 across 3,500 transactions)
  - Monthly liquidity progression from May to October 2026

---

### Agent 2: Marketing Agent
* **Role:** Strategic Banking Marketing Agent
* **Goal:** Evaluate customer segmentation (Priority, Corporate, SME, Retail), identify demographic growth drivers, diagnose dormant customer profiles, and design targeted cross-sell and customer retention strategies.
* **Backstory:** Elite retail banking marketing director specializing in high-net-worth client engagement, SME relationship expansion, and customer lifetime value optimization.
* **Outputs Generated:**
  - Customer segment distribution: Priority (295), Corporate (304), SME (297), Retail (304)
  - Dormancy diagnostics: 32.1% account dormancy rate representing ₹560Cr in stagnant funds
  - Geographic hub mapping: Ahmedabad, Surat, Vadodara, Pune, Rajkot
  - Targeted retention campaign with 15% budget reallocation recommendation

---

### Agent 3: Finance Agent
* **Role:** Chief Financial Officer (CFO) Intelligence Agent
* **Goal:** Examine bank liquidity, deposit liabilities, interest rate spreads, net cash inflows/outflows, financial risks, and formulate cost-optimization and revenue maximization frameworks.
* **Backstory:** Seasoned bank treasury and financial operations veteran specializing in net interest margins, cost of funds, and capital allocation efficiency.
* **Outputs Generated:**
  - Net liquidity velocity: Credits (₹220.6Cr) vs Debits (₹219.4Cr), generating +₹1.2Cr net inflow
  - Loan portfolio yield: ₹182.4Cr disbursed across 617 approved loans at 13.1% average coupon
  - Repayment recovery efficiency: ₹7.8Cr collected against ₹9.1Cr due (85.7% recovery rate)
  - Frozen asset analysis: 22.8% of accounts frozen, creating capital drag

---

### Agent 4: Operations Agent
* **Role:** Bank Operations & Process Intelligence Agent
* **Goal:** Detect operational bottlenecks, analyze channel performance across UPI, ATM, NEFT, IMPS, and POS, quantify transaction failure rates, and propose process automation and digital throughput improvements.
* **Backstory:** Chief Operations Officer in digital banking infrastructure, responsible for switch uptime, payment settlement reliability, and reducing transaction drop-offs.
* **Outputs Generated:**
  - Gateway success rate: 92.0%
  - Technical failure diagnosis: 4.89% failure rate (171 failed transactions) and 3.11% reversals
  - Channel throughput: UPI leads in volume (842 txns), NEFT leads in ticket size
  - Risk investigation workload: 120 Critical risk events requiring switch routing updates

---

### Agent 5: Strategy Agent
* **Role:** Executive Bank Strategy & Decision Intelligence Agent
* **Goal:** Synthesize outputs from Data Analyst, Marketing, Finance, and Operations Agents to formulate high-impact strategic business recommendations, prioritize growth initiatives, and generate an actionable 6-month business improvement roadmap.
* **Backstory:** Former McKinsey/BCG Senior Partner and banking executive advisor skilled at turning multi-disciplinary data into executive roadmaps.
* **Outputs Generated:**
  - 4 Prioritized Strategic Recommendations (Rec 01 through Rec 04)
  - Actionable 3-Phase Business Improvement Plan (Immediate, Medium Term, Strategic)
  - Consequential Human-in-the-Loop decision submission

---

### Agent 6: Verification Agent
* **Role:** Independent Audit, Verification & Anti-Hallucination Agent
* **Goal:** Rigorously validate all findings from peer agents against ground-truth source data, recalculate numerical metrics, flag unsupported claims or conflicting recommendations, and officially approve or reject the final Business Intelligence Report.
* **Backstory:** Uncompromising Lead Bank Regulator and Chief Internal Auditor. Enforces 0% discrepancy tolerance against source ledgers.
* **Outputs Generated:**
  - Metric verification cross-check table (Deposits, Turnover, Approval Rate, Delinquency, Failures)
  - Contradiction check: verifies loan risk recommendations align with 53.1% delinquency rate
  - Official Verification Audit Seal and Approval Verdict

---

## 2. Inter-Agent Communication & Data Flow

```
[Uploaded Dataset: 10,500 rows]
         │
         ▼
[Step 1: Data Analyst Agent]
         │  (Emits KPIs & Monthly Time Series)
         ├───────────────────────────┬───────────────────────────┐
         ▼                           ▼                           ▼
[Step 2: Marketing Agent]   [Step 3: Finance Agent]   [Step 4: Operations Agent]
         │ (Segments & Churn)        │ (Yields & Liquidity)      │ (Drop-offs & Switches)
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                        [Step 5: Strategy Agent]
                                     │ (Synthesized Business Improvement Plan)
                                     ▼
                       [Step 6: Verification Agent]
                                     │ (Checks calculations against database)
                                     ▼
                   [Verified Report + HITL Approval Queue]
```

## 3. Anti-Hallucination & Numerical Accuracy Guardrails
To prevent LLMs from inventing metrics, the system implements:
1. **Deterministic Database Grounding:** Raw SQL counts and sums are computed in Python and injected into the execution context.
2. **Tolerance Checking:** The Verification Agent calculates `relative_error = |actual - claimed| / actual`. If `relative_error > 0.05`, the metric is flagged.
3. **Audit Trail Signing:** The generated PDF and database report store the auditor hash, passing metrics count, and audit summary.

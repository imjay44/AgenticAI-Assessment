# Human-in-the-Loop (HITL) Governance Implementation

## 1. Overview
In compliance with **Section 8 and Section 9** of the project specification, autonomous AI agents are **prohibited from executing consequential business actions automatically without authorized human approval**.

Consequential business actions include:
* Reallocating marketing budgets (> 10%)
* Modifying credit underwriting cutoffs (e.g. CIBIL score floors)
* Adjusting capital reserve allocations or liquidity provisioning
* Re-routing core payment switch partner gateways

---

## 2. The 6-Stage Approval Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Strategy as Strategy Agent
    actor Verifier as Verification Agent
    actor System as Backend System
    actor Manager as Business Manager (Human)
    actor DB as Database Audit Log

    Strategy->>Verifier: Submits Recommendation (e.g. 15% Budget Shift + CIBIL >= 620)
    Verifier->>Verifier: Audits Empirical Feasibility & Risk Alignment
    Verifier->>System: Attests Verified Evidence (0% Deviation)
    System->>DB: Queues Approval Request (Status: Pending)
    System->>Manager: Displays Alert on Human-in-the-Loop Dashboard
    Manager->>System: Reviews Proposal, Financial ROI & Risk Proof
    alt Manager Approves
        Manager->>System: Signs off with Remarks ("Approved by Executive Committee")
        System->>DB: Records Decision (Status: Approved, Reviewed_At, Reviewer_Name)
        System-->>Manager: Confirms Policy Update Registered
    else Manager Rejects
        Manager->>System: Rejects with Reason ("Capital reserved for Q3 bond redemption")
        System->>DB: Records Decision (Status: Rejected, Reviewed_At, Reviewer_Name)
        System-->>Manager: Confirms Action Blocked
    end
```

---

## 3. Real Example Implemented in the System

* **Title:** Strategic Capital & Credit Policy Realignment (15% Marketing Reallocation & CIBIL Cutoff)
* **Initiated By:** Strategy Agent (collaboration with Marketing & Finance)
* **Recommended Action:** Reallocate 15% of annual marketing expenditure (₹12.5Cr) toward Priority & SME reactivation, and enforce a mandatory 620 CIBIL floor on personal and auto loan underwriting.
* **Financial Impact:** Projected deposit recovery of ₹85Cr with default reduction of ₹14.8Cr in Q1.
* **Risk Impact:** Compresses current delinquency rate from 53.1% below 4.0% ceiling.
* **Verification Proof:** Verification Agent verified 32.1% dormancy rate across 1,600 accounts and 53.1% repayment default rate across 2,500 repayment records.
* **Human Action:** Accessible via the `/approvals` console where the manager clicks **"Authorize & Approve Execution"** or **"Reject Action"**.

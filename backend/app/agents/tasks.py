from typing import Dict, Any, List

class BankingTasksFactory:
    """
    Defines the 6 CrewAI tasks corresponding to the mandatory workflow in Section 7:
    Step 1: Data Analyst Agent (Analyzes uploaded dataset, KPIs, monthly trends & anomalies)
    Step 2: Marketing Agent (Analyzes customer segments & retention/marketing opportunities)
    Step 3: Finance Agent (Analyzes revenue, expenses, profitability, financial risk, cost optimization)
    Step 4: Operations Agent (Analyzes operational efficiency, bottlenecks, failure rates)
    Step 5: Strategy Agent (Consolidates business insights into strategic recommendations & plan)
    Step 6: Verification Agent (Cross-checks calculations against source data, flags hallucinations, issues verdict)
    """

    @staticmethod
    def create_task_definitions(kpis: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "task_id": "data_analysis",
                "name": "Exploratory & Quantitative Business Data Analysis",
                "agent": "Data Analyst Agent",
                "description": (
                    f"Perform deep quantitative analysis on the 6-month banking operations dataset (May 1 - Oct 31, 2026). "
                    f"Compute essential KPIs: Customer base ({kpis['customer_kpis']['total_customers']}), total deposit liabilities "
                    f"(₹{kpis['financial_kpis']['total_deposit_balance']:,.2f}), transaction turnover "
                    f"(₹{kpis['financial_kpis']['total_transaction_turnover']:,.2f}), and monthly trends. "
                    f"Highlight significant month-over-month shifts and anomalies."
                ),
                "expected_output": "Comprehensive quantitative report with verified KPI values and monthly trend breakdown."
            },
            {
                "task_id": "marketing_intelligence",
                "name": "Customer Segmentation & Growth Opportunity Evaluation",
                "agent": "Marketing Agent",
                "description": (
                    f"Analyze customer segments (Priority: {kpis['customer_kpis']['segment_breakdown'].get('Priority', 0)}, "
                    f"Corporate: {kpis['customer_kpis']['segment_breakdown'].get('Corporate', 0)}, "
                    f"SME: {kpis['customer_kpis']['segment_breakdown'].get('SME', 0)}, "
                    f"Retail: {kpis['customer_kpis']['segment_breakdown'].get('Retail', 0)}). "
                    f"Evaluate dormancy rates ({kpis['financial_kpis']['dormancy_ratio']}%) and recommend data-driven retention "
                    f"and acquisition initiatives."
                ),
                "expected_output": "Customer behavior analysis, segment monetization strategies, and retention recommendations."
            },
            {
                "task_id": "finance_intelligence",
                "name": "Revenue, Expense & Liquidity Optimization Analysis",
                "agent": "Finance Agent",
                "description": (
                    f"Assess bank liquidity flows (Credits: ₹{kpis['financial_kpis']['total_credits']:,.2f} vs Debits: ₹{kpis['financial_kpis']['total_debits']:,.2f}). "
                    f"Analyze capital tied in frozen accounts ({kpis['financial_kpis']['frozen_ratio']}%), loan disbursement efficiency "
                    f"(Disbursed: ₹{kpis['lending_kpis']['disbursed_volume']:,.2f}), and recovery rate ({kpis['risk_kpis']['repayment_recovery_rate']}%). "
                    f"Formulate cost-optimization strategies."
                ),
                "expected_output": "Financial risk analysis, net liquidity spread evaluation, and cost-efficiency recommendations."
            },
            {
                "task_id": "operations_intelligence",
                "name": "Operational Bottlenecks & Channel Reliability Diagnosis",
                "agent": "Operations Agent",
                "description": (
                    f"Analyze transaction execution across channels (Total transactions: {kpis['operations_kpis']['total_transactions']}). "
                    f"Examine failure rates ({kpis['operations_kpis']['failure_rate']}%), reversed transactions ({kpis['operations_kpis']['reversed_transactions']}), "
                    f"and critical risk workload ({kpis['risk_kpis']['critical_risk_events']} critical events). "
                    f"Recommend process improvements for core banking gateways and branch workload."
                ),
                "expected_output": "Operational efficiency diagnosis with channel reliability recommendations and automation opportunities."
            },
            {
                "task_id": "strategic_synthesis",
                "name": "Consolidated Strategic Plan & Business Improvement Roadmap",
                "agent": "Strategy Agent",
                "description": (
                    "Receive and synthesize analytical findings from Data Analyst, Marketing, Finance, and Operations Agents. "
                    "Synthesize insights into an actionable 6-month business improvement roadmap with prioritized strategic initiatives, "
                    "measurable impact projections, and key executive actions."
                ),
                "expected_output": "Consolidated strategic roadmap with prioritized initiatives, revenue upside projections, and risk mitigation safeguards."
            },
            {
                "task_id": "audit_verification",
                "name": "Independent Source-Data Verification & Hallucination Audit",
                "agent": "Verification Agent",
                "description": (
                    "Rigorously audit all claims, figures, and recommendations in the consolidated report against exact source database values. "
                    "Verify deposit balance, turnover, approval rates, delinquency, and failure metrics. Flag any hallucinated numbers, "
                    "unsupported assertions, or policy contradictions. Grant formal audit certification."
                ),
                "expected_output": "Comprehensive audit verification seal with cross-check matrices and formal approval/rejection declaration."
            }
        ]

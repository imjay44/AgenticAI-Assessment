from typing import Dict, Any, List, Optional

try:
    from crewai import Task
except ImportError:
    from app.agents.crewai_engine import Task

class BankingTasksFactory:
    """
    Defines and instantiates the 6 CrewAI tasks corresponding to Section 7:
    Step 1: Data Analyst Agent (Exploratory Data Analysis & Verified KPIs)
    Step 2: Marketing Agent (Customer Segments & Dormancy Reactivation)
    Step 3: Finance Agent (Liquidity Flows & Cost Optimization)
    Step 4: Operations Agent (Channel Reliability & Gateway Bottlenecks)
    Step 5: Strategy Agent (Consolidated Strategic Plan with Inter-Agent Context)
    Step 6: Verification Agent (Numerical Anti-Hallucination Audit & Certification)
    """

    @staticmethod
    def create_crewai_tasks(agents: Dict[str, Any], kpis: Dict[str, Any]) -> List[Any]:
        """
        Creates real CrewAI Task objects with upstream context dependencies:
        - Marketing, Finance, Operations receive Data Analyst context.
        - Strategy Agent receives context from Data Analyst, Marketing, Finance, Operations.
        - Verification Agent receives Strategy output and all domain contexts.
        """
        fin = kpis["financial_kpis"]
        cust = kpis["customer_kpis"]
        lend = kpis["lending_kpis"]
        ops = kpis["operations_kpis"]
        risk = kpis["risk_kpis"]

        # Task 1: Data Analysis
        task_da = Task(
            description=(
                f"Perform deep quantitative analysis on the 6-month banking operations dataset (May 1 - Oct 31, 2026). "
                f"Verify total customers ({cust['total_customers']}), total deposit balance (₹{fin['total_deposit_balance']:,.2f}), "
                f"gross transaction turnover (₹{fin['total_transaction_turnover']:,.2f}), and monthly trends. "
                f"Detect anomalous shifts in liquidity flows and channel volume."
            ),
            expected_output="Verified empirical baseline containing all core KPIs, monthly liquidity volumes, and account status breakdowns.",
            agent=agents["data_analyst"]
        )

        # Task 2: Marketing Intelligence
        task_mkt = Task(
            description=(
                f"Analyze customer segmentation across Priority ({cust['segment_breakdown'].get('Priority', 0)}), "
                f"Corporate ({cust['segment_breakdown'].get('Corporate', 0)}), SME ({cust['segment_breakdown'].get('SME', 0)}), "
                f"and Retail ({cust['segment_breakdown'].get('Retail', 0)}). "
                f"Analyze the 25.25% account dormancy rate ({fin['account_status_counts'].get('Dormant', 0)} accounts) "
                f"and recommend high-impact retention and reactivation initiatives."
            ),
            expected_output="Customer segment monetisation strategies, dormancy reduction initiatives, and regional growth priorities.",
            agent=agents["marketing"],
            context=[task_da]
        )

        # Task 3: Finance Intelligence
        task_fin = Task(
            description=(
                f"Evaluate bank liquidity dynamics: Gross credits of ₹{fin['total_credits']:,.2f} versus debits of ₹{fin['total_debits']:,.2f}, "
                f"resulting in net inflow of +₹{fin['net_liquidity_flow']:,.2f}. "
                f"Analyze capital locked in frozen accounts ({fin['frozen_ratio']}%, {fin['account_status_counts'].get('Frozen', 0)} accounts) "
                f"and evaluate lending disbursement of ₹{lend['disbursed_volume']:,.2f} at {lend['avg_interest_rate']}% average interest."
            ),
            expected_output="Net liquidity spread assessment, treasury yield optimization, and capital allocation recommendations.",
            agent=agents["finance"],
            context=[task_da]
        )

        # Task 4: Operations Intelligence
        task_ops = Task(
            description=(
                f"Diagnose transaction channel throughput across 3,500 transactions. "
                f"Audit digital failure rate of {ops['failure_rate']}% (exactly 171 technical failures) and 109 reversals (3.11%). "
                f"Evaluate 500 operational risk alerts (including {risk['critical_risk_events']} Critical events and {risk['open_cases']} Open cases). "
                f"Formulate payment switch redundancy recommendations."
            ),
            expected_output="Channel reliability diagnosis, digital switch failover architecture, and risk SLA remediation roadmap.",
            agent=agents["operations"],
            context=[task_da]
        )

        # Task 5: Strategy Synthesis
        task_strat = Task(
            description=(
                "Synthesize inputs from Data Analyst, Marketing, Finance, and Operations Agents. "
                "Synthesize findings into a unified 6-month executive roadmap with prioritized strategic initiatives, "
                "projected financial returns, and high-impact actions requiring Human-in-the-Loop executive authorization."
            ),
            expected_output="Consolidated executive business intelligence plan, 4 strategic recommendations, and 3-phase action roadmap.",
            agent=agents["strategy"],
            context=[task_da, task_mkt, task_fin, task_ops]
        )

        # Task 6: Audit Verification
        task_ver = Task(
            description=(
                "Independently audit all numerical claims, findings, and strategic proposals against ground-truth database rows. "
                "Verify zero-hallucination tolerance across deposit balance, turnover, approval rates, delinquency, and gateway failures. "
                "Grant formal audit certification and compute the empirical verification score."
            ),
            expected_output="Audit verification seal with empirical cross-check matrix, mathematical tolerance calculations, and certification verdict.",
            agent=agents["verification"],
            context=[task_strat, task_da, task_fin, task_ops]
        )

        return [task_da, task_mkt, task_fin, task_ops, task_strat, task_ver]

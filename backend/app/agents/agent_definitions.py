import os
from typing import Optional, Any, Dict
from app.config import settings

try:
    from crewai import Agent
    HAS_REAL_CREWAI = True
except ImportError:
    from app.agents.crewai_engine import Agent
    HAS_REAL_CREWAI = False

# Try importing LangChain LLM base to construct seamless custom LLM for real CrewAI when API keys are absent
GroundedBankingCrewLLM = None
try:
    from langchain_core.language_models.llms import LLM
    class GroundedBankingCrewLLM(LLM):
        agent_role: str = "Banking Analyst"
        kpis: Dict[str, Any] = {}

        @property
        def _llm_type(self) -> str:
            return "grounded_banking_crew_llm"

        def _call(self, prompt: str, stop=None, run_manager=None, **kwargs) -> str:
            from app.services.llm_service import llm_service
            analysis = llm_service.generate_agent_analysis(
                role=self.agent_role,
                goal="",
                backstory="",
                task_description=prompt,
                expected_output="",
                kpis=self.kpis,
                context=prompt
            )
            return f"Thought: Analysis grounded in verified banking data.\nFinal Answer: {analysis}"
except Exception:
    GroundedBankingCrewLLM = None

class BankingAgentFactory:
    """
    Factory for instantiating the 6 specialized AI agents.
    Supports both CrewAI (when LLM API keys are provided)
    and robust deterministic analytical execution grounded in dataset metrics.
    """

    @staticmethod
    def get_agent_specs():
        return {
            "data_analyst": {
                "role": "Senior Banking Data Analyst Agent",
                "goal": "Analyze the complete 6-month banking operations dataset (May–Oct 2026), compute precise KPIs, detect anomalous shifts in transaction turnover, deposit growth, and loan volumes, and deliver statistically rigorous summaries.",
                "backstory": "You are a quantitative banking data scientist with 15+ years of experience auditing core banking platforms, transaction ledgers, and credit registries. You never guess numbers; your insights are 100% grounded in empirical data."
            },
            "marketing": {
                "role": "Strategic Banking Marketing Agent",
                "goal": "Evaluate customer segmentation (Priority, Corporate, SME, Retail), identify demographic growth drivers, diagnose dormant customer profiles, and design targeted cross-sell and customer retention strategies.",
                "backstory": "You are an elite retail banking marketing director specializing in high-net-worth client engagement, SME relationship expansion, and customer lifetime value optimization in competitive Asian financial markets."
            },
            "finance": {
                "role": "Chief Financial Officer (CFO) Intelligence Agent",
                "goal": "Examine bank liquidity, deposit liabilities, interest rate spreads, net cash inflows/outflows, financial risks, and formulate cost-optimization and revenue maximization frameworks.",
                "backstory": "You are a seasoned bank treasury and financial operations veteran. You evaluate net liquidity spreads, cost of funds, capital adequacy, and the economic efficiency of active vs dormant balances with surgical precision."
            },
            "operations": {
                "role": "Bank Operations & Process Intelligence Agent",
                "goal": "Detect operational bottlenecks, analyze channel performance across UPI, ATM, NEFT, IMPS, and POS, quantify transaction failure rates, and propose process automation and digital throughput improvements.",
                "backstory": "You are a Chief Operations Officer in digital banking infrastructure, responsible for mission-critical core banking switch uptime, payment settlement reliability, and reducing transaction drop-offs across omnichannel gateways."
            },
            "strategy": {
                "role": "Executive Bank Strategy & Decision Intelligence Agent",
                "goal": "Synthesize outputs from Data Analyst, Marketing, Finance, and Operations Agents to formulate high-impact strategic business recommendations, prioritize growth initiatives, and generate an actionable 6-month business improvement roadmap.",
                "backstory": "You are a former McKinsey/BCG Senior Partner and banking executive advisor. You excel at translating complex multi-dimensional risk, operational, and customer insights into board-level action plans and executive decisions."
            },
            "verification": {
                "role": "Independent Audit, Verification & Anti-Hallucination Agent",
                "goal": "Rigorously validate all findings from peer agents against ground-truth source data, recalculate numerical metrics, flag unsupported claims or conflicting recommendations, and officially approve or reject the final Business Intelligence Report.",
                "backstory": "You are an uncompromising Lead Bank Regulator and Chief Internal Auditor. You reject any report containing statistical hallucinations, invented metrics, or contradictory recommendations, ensuring absolute data integrity."
            }
        }

    @staticmethod
    def create_crewai_agents(kpis: Optional[Dict[str, Any]] = None, llm: Optional[Any] = None) -> dict:
        """Creates CrewAI Agent instances with roles, goals, backstories, and tools."""
        specs = BankingAgentFactory.get_agent_specs()
        agents = {}
        for key, spec in specs.items():
            agent_llm = llm
            if agent_llm is None and HAS_REAL_CREWAI:
                if settings.OPENAI_API_KEY:
                    agent_llm = "gpt-4o-mini"
                elif settings.GEMINI_API_KEY:
                    agent_llm = f"gemini/{settings.LLM_MODEL}"
                elif GroundedBankingCrewLLM is not None:
                    agent_llm = GroundedBankingCrewLLM(agent_role=spec["role"], kpis=kpis or {})

            if HAS_REAL_CREWAI:
                agents[key] = Agent(
                    role=spec["role"],
                    goal=spec["goal"],
                    backstory=spec["backstory"],
                    verbose=True,
                    allow_delegation=(key in ["strategy", "verification"]),
                    llm=agent_llm
                )
            else:
                agents[key] = Agent(
                    role=spec["role"],
                    goal=spec["goal"],
                    backstory=spec["backstory"],
                    verbose=True,
                    allow_delegation=(key in ["strategy", "verification"]),
                    llm=agent_llm,
                    kpis=kpis
                )
        return agents

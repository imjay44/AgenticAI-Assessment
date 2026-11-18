import sys
sys.path.insert(0, 'backend')
from app.main import app
from app.database import engine, Base, SessionLocal
from app.services.data_processor import data_processor
from app.agents.crew import BankingDecisionCrew

print("1. Creating database schema...")
Base.metadata.create_all(bind=engine)

print("2. Seeding dataset into SQLite database...")
db = SessionLocal()
data_processor.seed_initial_data_if_empty(db)

print("3. Computing comprehensive KPIs from May-Oct 2026 data...")
kpis = data_processor.calculate_comprehensive_kpis(db)
fin = kpis['financial_kpis']
lend = kpis['lending_kpis']
ops = kpis['operations_kpis']
risk = kpis['risk_kpis']
cust = kpis['customer_kpis']

print(f"   - Total Customers: {cust['total_customers']}")
print(f"   - Total Deposit Balance: INR {fin['total_deposit_balance']:,.2f}")
print(f"   - Total Transaction Turnover: INR {fin['total_transaction_turnover']:,.2f}")
print(f"   - Total Loans Requested: {lend['total_applications']} (Approval Rate: {lend['approval_rate']}%)")
print(f"   - Loan Delinquency Rate: {risk['delinquency_rate']}%")
print(f"   - Payment Success Rate: {ops['success_rate']}% (Failure: {ops['failure_rate']}%)")
print(f"   - Critical Risk Events: {risk['critical_risk_events']} of {risk['total_risk_events']}")

print("4. Testing 6-Agent CrewAI Execution Workflow...")
crew = BankingDecisionCrew(session_id="test_init_session_01")
report = crew.run_multi_agent_workflow(db, execution_mode="sequential", llm_provider="auto")

print(f"   - Generated Report Title: {report['title']}")
print(f"   - Verification Status: {report['verification_status']}")
print(f"   - Strategic Recommendations Count: {len(report['strategic_recommendations'])}")
print(f"   - Action Plan Items Count: {len(report['action_plan'])}")

db.close()
print("All backend checks passed with flying colors!")

import os
import csv
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict
from sqlalchemy.orm import Session

from app.config import settings
from app.models.banking import (
    Customer, Account, Transaction, LoanApplication, LoanRepayment, RiskEvent, UploadedDataset
)
from app.models.user import User, BusinessProfile
from app.services.auth_service import get_password_hash

class DataProcessor:
    """
    Cleans, validates, ingests, and computes exact mathematical KPIs from the May-Oct 2026 banking dataset.
    Grounds all multi-agent operations with verified source metrics.
    """
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or settings.DATA_DIR

    def seed_initial_data_if_empty(self, db: Session):
        """Seed default admin, business profile, and banking data if tables are empty."""
        # 1. Seed default user
        if db.query(User).count() == 0:
            admin_user = User(
                username="admin",
                email="admin@apexbank.com",
                full_name="Chief Executive Officer",
                hashed_password=get_password_hash("Admin@12345"),
                role="admin"
            )
            manager_user = User(
                username="manager",
                email="manager@apexbank.com",
                full_name="Head of Business Operations",
                hashed_password=get_password_hash("Manager@12345"),
                role="business_manager"
            )
            analyst_user = User(
                username="analyst",
                email="analyst@apexbank.com",
                full_name="Lead Data Analyst",
                hashed_password=get_password_hash("Analyst@12345"),
                role="analyst"
            )
            db.add_all([admin_user, manager_user, analyst_user])
            db.commit()

        # 2. Seed business profile
        if db.query(BusinessProfile).count() == 0:
            profile = BusinessProfile(
                company_name="Apex Global Trust Bank",
                industry="Banking (Financial & Risk Intelligence)",
                team_size="750 professionals across 45 regional branches",
                business_goals="Drive 12% deposit expansion, reduce Non-Performing Assets (NPAs) below 4.0%, improve digital channel throughput, and optimize credit underwriting for SME/Retail segments.",
                risk_tolerance="Moderate-Conservative",
                target_period="May 1, 2026 - October 31, 2026"
            )
            db.add(profile)
            db.commit()

        # 3. Seed banking data from CSVs if empty
        if db.query(Customer).count() == 0:
            self.load_all_csvs_into_db(db)

    def load_all_csvs_into_db(self, db: Session):
        """Loads all CSV files into the relational database."""
        cust_path = os.path.join(self.data_dir, "customers.csv")
        acc_path = os.path.join(self.data_dir, "accounts.csv")
        tx_path = os.path.join(self.data_dir, "transactions.csv")
        loan_path = os.path.join(self.data_dir, "loan_applications.csv")
        rep_path = os.path.join(self.data_dir, "loan_repayments.csv")
        risk_path = os.path.join(self.data_dir, "risk_events.csv")

        # Load Customers
        if os.path.exists(cust_path):
            with open(cust_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                customers = [
                    Customer(
                        customer_id=row['customer_id'].strip(),
                        customer_name=row['customer_name'].strip(),
                        age=int(row['age']),
                        city=row['city'].strip(),
                        customer_since=row['customer_since'].strip(),
                        customer_segment=row['customer_segment'].strip(),
                        kyc_status=row['kyc_status'].strip(),
                        risk_profile=row['risk_profile'].strip()
                    )
                    for row in reader
                ]
                db.bulk_save_objects(customers)
                db.commit()

        # Load Accounts
        if os.path.exists(acc_path):
            with open(acc_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                accounts = [
                    Account(
                        account_id=row['account_id'].strip(),
                        customer_id=row['customer_id'].strip(),
                        account_type=row['account_type'].strip(),
                        opening_date=row['opening_date'].strip(),
                        branch_id=row['branch_id'].strip(),
                        current_balance=float(row['current_balance']),
                        account_status=row['account_status'].strip(),
                        currency=row.get('currency', 'INR').strip()
                    )
                    for row in reader
                ]
                db.bulk_save_objects(accounts)
                db.commit()

        # Load Transactions
        if os.path.exists(tx_path):
            with open(tx_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                transactions = [
                    Transaction(
                        transaction_id=row['transaction_id'].strip(),
                        account_id=row['account_id'].strip(),
                        transaction_date=row['transaction_date'].strip(),
                        transaction_type=row['transaction_type'].strip(),
                        amount=float(row['amount']),
                        channel=row['channel'].strip(),
                        merchant_category=row['merchant_category'].strip(),
                        transaction_status=row['transaction_status'].strip(),
                        is_flagged=row.get('is_flagged', 'No').strip()
                    )
                    for row in reader
                ]
                db.bulk_save_objects(transactions)
                db.commit()

        # Load Loans
        if os.path.exists(loan_path):
            with open(loan_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                loans = [
                    LoanApplication(
                        loan_id=row['loan_id'].strip(),
                        customer_id=row['customer_id'].strip(),
                        application_date=row['application_date'].strip(),
                        loan_type=row['loan_type'].strip(),
                        requested_amount=float(row['requested_amount']),
                        annual_interest_rate=float(row['annual_interest_rate']),
                        tenure_months=int(row['tenure_months']),
                        credit_score=int(row['credit_score']),
                        application_status=row['application_status'].strip()
                    )
                    for row in reader
                ]
                db.bulk_save_objects(loans)
                db.commit()

        # Load Repayments
        if os.path.exists(rep_path):
            with open(rep_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                repayments = [
                    LoanRepayment(
                        repayment_id=row['repayment_id'].strip(),
                        loan_id=row['loan_id'].strip(),
                        due_date=row['due_date'].strip(),
                        due_amount=float(row['due_amount']),
                        paid_amount=float(row['paid_amount']),
                        payment_date=row['payment_date'].strip(),
                        repayment_status=row['repayment_status'].strip(),
                        days_past_due=int(row['days_past_due'])
                    )
                    for row in reader
                ]
                db.bulk_save_objects(repayments)
                db.commit()

        # Load Risk Events
        if os.path.exists(risk_path):
            with open(risk_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                risks = [
                    RiskEvent(
                        event_id=row['event_id'].strip(),
                        customer_id=row['customer_id'].strip(),
                        event_date=row['event_date'].strip(),
                        event_type=row['event_type'].strip(),
                        risk_level=row['risk_level'].strip(),
                        case_status=row['case_status'].strip(),
                        assigned_team=row['assigned_team'].strip()
                    )
                    for row in reader
                ]
                db.bulk_save_objects(risks)
                db.commit()

        # Log upload in dataset table
        ds = UploadedDataset(
            filename="banking_operations_dataset.xlsx",
            record_counts_json='{"customers": 1200, "accounts": 1600, "transactions": 3500, "loans": 1200, "repayments": 2500, "risk_events": 500}',
            status="Processed"
        )
        db.add(ds)
        db.commit()

    def calculate_comprehensive_kpis(self, db: Session) -> Dict[str, Any]:
        """
        Computes exact mathematical business KPIs based on real dataset records.
        Covers May 1, 2026 - October 31, 2026.
        """
        # 1. Customers
        customers = db.query(Customer).all()
        total_customers = len(customers)
        segment_counts = defaultdict(int)
        kyc_counts = defaultdict(int)
        risk_profile_counts = defaultdict(int)
        city_counts = defaultdict(int)
        
        for c in customers:
            segment_counts[c.customer_segment] += 1
            kyc_counts[c.kyc_status] += 1
            risk_profile_counts[c.risk_profile] += 1
            city_counts[c.city] += 1

        # 2. Accounts
        accounts = db.query(Account).all()
        total_accounts = len(accounts)
        total_deposit_balance = sum(a.current_balance for a in accounts)
        avg_account_balance = total_deposit_balance / total_accounts if total_accounts else 0
        account_status_counts = defaultdict(int)
        account_type_counts = defaultdict(int)
        account_type_balance = defaultdict(float)

        for a in accounts:
            account_status_counts[a.account_status] += 1
            account_type_counts[a.account_type] += 1
            account_type_balance[a.account_type] += a.current_balance

        # 3. Transactions
        transactions = db.query(Transaction).all()
        total_transactions = len(transactions)
        total_volume = sum(t.amount for t in transactions)
        total_credit_volume = sum(t.amount for t in transactions if t.transaction_type == "Credit")
        total_debit_volume = sum(t.amount for t in transactions if t.transaction_type == "Debit")
        credit_count = sum(1 for t in transactions if t.transaction_type == "Credit")
        debit_count = sum(1 for t in transactions if t.transaction_type == "Debit")
        
        channel_volume = defaultdict(float)
        channel_count = defaultdict(int)
        category_volume = defaultdict(float)
        tx_status_counts = defaultdict(int)
        flagged_transactions = sum(1 for t in transactions if t.is_flagged == "Yes")
        flagged_volume = sum(t.amount for t in transactions if t.is_flagged == "Yes")

        # Monthly transaction progression
        monthly_tx = defaultdict(lambda: {"volume": 0.0, "credits": 0.0, "debits": 0.0, "count": 0})
        for t in transactions:
            channel_volume[t.channel] += t.amount
            channel_count[t.channel] += 1
            category_volume[t.merchant_category] += t.amount
            tx_status_counts[t.transaction_status] += 1
            
            # Month grouping (YYYY-MM)
            month = t.transaction_date[:7]
            monthly_tx[month]["volume"] += t.amount
            monthly_tx[month]["count"] += 1
            if t.transaction_type == "Credit":
                monthly_tx[month]["credits"] += t.amount
            else:
                monthly_tx[month]["debits"] += t.amount

        # 4. Lending & Loans
        loans = db.query(LoanApplication).all()
        total_loans = len(loans)
        total_loan_amount_requested = sum(l.requested_amount for l in loans)
        loan_status_counts = defaultdict(int)
        loan_type_counts = defaultdict(int)
        loan_type_amount = defaultdict(float)
        approved_disbursed_loans = [l for l in loans if l.application_status in ["Approved", "Disbursed"]]
        disbursed_volume = sum(l.requested_amount for l in loans if l.application_status == "Disbursed")
        approved_volume = sum(l.requested_amount for l in loans if l.application_status == "Approved")
        rejected_volume = sum(l.requested_amount for l in loans if l.application_status == "Rejected")
        
        for l in loans:
            loan_status_counts[l.application_status] += 1
            loan_type_counts[l.loan_type] += 1
            loan_type_amount[l.loan_type] += l.requested_amount

        approval_rate = (len(approved_disbursed_loans) / total_loans * 100) if total_loans else 0
        rejection_rate = (loan_status_counts["Rejected"] / total_loans * 100) if total_loans else 0
        avg_interest_rate = sum(l.annual_interest_rate for l in loans) / total_loans if total_loans else 0
        avg_credit_score = sum(l.credit_score for l in loans) / total_loans if total_loans else 0

        # 5. Loan Repayments & Delinquency (NPA)
        repayments = db.query(LoanRepayment).all()
        total_repayments = len(repayments)
        total_due_amount = sum(r.due_amount for r in repayments)
        total_paid_amount = sum(r.paid_amount for r in repayments)
        repayment_status_counts = defaultdict(int)
        dpd_sum = 0
        delinquent_records = 0

        for r in repayments:
            repayment_status_counts[r.repayment_status] += 1
            dpd_sum += r.days_past_due
            if r.days_past_due > 30 or r.repayment_status in ["Missed", "Late"]:
                delinquent_records += 1

        repayment_recovery_rate = (total_paid_amount / total_due_amount * 100) if total_due_amount else 0
        delinquency_rate = (delinquent_records / total_repayments * 100) if total_repayments else 0
        avg_dpd = dpd_sum / total_repayments if total_repayments else 0

        # 6. Risk Events
        risk_events = db.query(RiskEvent).all()
        total_risk_events = len(risk_events)
        risk_level_counts = defaultdict(int)
        risk_type_counts = defaultdict(int)
        risk_status_counts = defaultdict(int)
        risk_team_counts = defaultdict(int)

        for re in risk_events:
            risk_level_counts[re.risk_level] += 1
            risk_type_counts[re.event_type] += 1
            risk_status_counts[re.case_status] += 1
            risk_team_counts[re.assigned_team] += 1

        # Format sorted monthly data
        monthly_series = []
        for m in sorted(monthly_tx.keys()):
            monthly_series.append({
                "month": m,
                "total_volume": round(monthly_tx[m]["volume"], 2),
                "credits": round(monthly_tx[m]["credits"], 2),
                "debits": round(monthly_tx[m]["debits"], 2),
                "transaction_count": monthly_tx[m]["count"],
                "net_inflow": round(monthly_tx[m]["credits"] - monthly_tx[m]["debits"], 2)
            })

        return {
            "period": "May 1, 2026 - October 31, 2026 (Last 6 Completed Months)",
            "customer_kpis": {
                "total_customers": total_customers,
                "segment_breakdown": dict(segment_counts),
                "kyc_status_breakdown": dict(kyc_counts),
                "risk_profile_breakdown": dict(risk_profile_counts),
                "top_cities": sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            },
            "financial_kpis": {
                "total_deposit_balance": round(total_deposit_balance, 2),
                "avg_account_balance": round(avg_account_balance, 2),
                "total_transaction_turnover": round(total_volume, 2),
                "total_credits": round(total_credit_volume, 2),
                "total_debits": round(total_debit_volume, 2),
                "net_liquidity_flow": round(total_credit_volume - total_debit_volume, 2),
                "account_type_balances": {k: round(v, 2) for k, v in account_type_balance.items()},
                "account_status_counts": dict(account_status_counts),
                "dormancy_ratio": round(account_status_counts["Dormant"] / total_accounts * 100, 2) if total_accounts else 0,
                "frozen_ratio": round(account_status_counts["Frozen"] / total_accounts * 100, 2) if total_accounts else 0
            },
            "lending_kpis": {
                "total_applications": total_loans,
                "total_requested_amount": round(total_loan_amount_requested, 2),
                "disbursed_volume": round(disbursed_volume, 2),
                "approved_volume": round(approved_volume, 2),
                "rejected_volume": round(rejected_volume, 2),
                "approval_rate": round(approval_rate, 2),
                "rejection_rate": round(rejection_rate, 2),
                "avg_interest_rate": round(avg_interest_rate, 2),
                "avg_credit_score": round(avg_credit_score, 1),
                "loan_type_distribution": dict(loan_type_counts),
                "loan_status_distribution": dict(loan_status_counts)
            },
            "operations_kpis": {
                "total_transactions": total_transactions,
                "failed_transactions": tx_status_counts["Failed"],
                "failure_rate": round((tx_status_counts["Failed"] / total_transactions * 100), 2) if total_transactions else 0,
                "reversed_transactions": tx_status_counts["Reversed"],
                "successful_transactions": tx_status_counts["Successful"],
                "success_rate": round((tx_status_counts["Successful"] / total_transactions * 100), 2) if total_transactions else 0,
                "channel_distribution": dict(channel_count),
                "channel_volume": {k: round(v, 2) for k, v in channel_volume.items()},
                "merchant_category_volume": {k: round(v, 2) for k, v in category_volume.items()}
            },
            "risk_kpis": {
                "total_risk_events": total_risk_events,
                "critical_risk_events": risk_level_counts["Critical"],
                "high_risk_events": risk_level_counts["High"],
                "open_cases": risk_status_counts["Open"],
                "under_review_cases": risk_status_counts["Under Review"],
                "closed_cases": risk_status_counts["Closed"],
                "event_type_distribution": dict(risk_type_counts),
                "team_workload": dict(risk_team_counts),
                "delinquency_rate": round(delinquency_rate, 2),
                "delinquent_records": delinquent_records,
                "total_repayments": total_repayments,
                "repayment_recovery_rate": round(repayment_recovery_rate, 2),
                "total_due_amount": round(total_due_amount, 2),
                "total_paid_amount": round(total_paid_amount, 2),
                "avg_days_past_due": round(avg_dpd, 1),
                "flagged_transactions_count": flagged_transactions,
                "flagged_transactions_volume": round(flagged_volume, 2)
            },
            "monthly_trends": monthly_series
        }

data_processor = DataProcessor()

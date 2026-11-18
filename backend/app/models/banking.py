from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String(50), primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String(100), nullable=False)
    customer_since = Column(String(20), nullable=False)
    customer_segment = Column(String(50), nullable=False) # Priority, Corporate, SME, Retail
    kyc_status = Column(String(50), nullable=False)       # Verified, Pending, Review Required
    risk_profile = Column(String(50), nullable=False)     # Low, Medium, High

    # Relationships
    accounts = relationship("Account", back_populates="customer", cascade="all, delete-orphan")
    loans = relationship("LoanApplication", back_populates="customer", cascade="all, delete-orphan")
    risk_events = relationship("RiskEvent", back_populates="customer", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"
    
    account_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    account_type = Column(String(50), nullable=False)     # Business, Salary, Current, Savings
    opening_date = Column(String(20), nullable=False)
    branch_id = Column(String(50), nullable=False)
    current_balance = Column(Float, nullable=False, default=0.0)
    account_status = Column(String(50), nullable=False)   # Active, Dormant, Frozen
    currency = Column(String(10), default="INR", nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(String(50), primary_key=True, index=True)
    account_id = Column(String(50), ForeignKey("accounts.account_id"), nullable=False, index=True)
    transaction_date = Column(String(20), nullable=False, index=True)
    transaction_type = Column(String(20), nullable=False) # Credit, Debit
    amount = Column(Float, nullable=False)
    channel = Column(String(50), nullable=False)          # UPI, NEFT, IMPS, ATM, POS, Internet Banking
    merchant_category = Column(String(50), nullable=False)# Retail, Food, Travel, Utilities, Salary, Healthcare, Transfer
    transaction_status = Column(String(50), nullable=False)# Successful, Failed, Reversed
    is_flagged = Column(String(10), default="No", nullable=False) # Yes, No

    # Relationships
    account = relationship("Account", back_populates="transactions")


class LoanApplication(Base):
    __tablename__ = "loan_applications"
    
    loan_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    application_date = Column(String(20), nullable=False, index=True)
    loan_type = Column(String(50), nullable=False)        # Home, Personal, Business, Education, Auto
    requested_amount = Column(Float, nullable=False)
    annual_interest_rate = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    credit_score = Column(Integer, nullable=False)
    application_status = Column(String(50), nullable=False)# Approved, Disbursed, Rejected, Under Review

    # Relationships
    customer = relationship("Customer", back_populates="loans")
    repayments = relationship("LoanRepayment", back_populates="loan", cascade="all, delete-orphan")


class LoanRepayment(Base):
    __tablename__ = "loan_repayments"
    
    repayment_id = Column(String(50), primary_key=True, index=True)
    loan_id = Column(String(50), ForeignKey("loan_applications.loan_id"), nullable=False, index=True)
    due_date = Column(String(20), nullable=False, index=True)
    due_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    payment_date = Column(String(20), nullable=False)
    repayment_status = Column(String(50), nullable=False)  # On Time, Late, Missed, Partial
    days_past_due = Column(Integer, default=0, nullable=False)

    # Relationships
    loan = relationship("LoanApplication", back_populates="repayments")


class RiskEvent(Base):
    __tablename__ = "risk_events"
    
    event_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    event_date = Column(String(20), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)       # High Value Transfer, KYC Review, Overdue Loan, Repeated Failed Login, Unusual Transaction
    risk_level = Column(String(50), nullable=False)        # Low, Medium, High, Critical
    case_status = Column(String(50), nullable=False)       # Open, Under Review, Closed
    assigned_team = Column(String(50), nullable=False)     # Fraud, Compliance, Operations, Credit Risk

    # Relationships
    customer = relationship("Customer", back_populates="risk_events")


class UploadedDataset(Base):
    __tablename__ = "uploaded_datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    record_counts_json = Column(Text, nullable=False)
    status = Column(String(50), default="Processed", nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

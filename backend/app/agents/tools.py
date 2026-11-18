import json
from typing import Dict, Any

class BankingAnalyticsTools:
    """
    Dedicated toolset providing deterministic, data-grounded metrics
    to eliminate hallucinations during agent reasoning.
    """
    
    @staticmethod
    def get_ground_truth_metrics(kpis: Dict[str, Any]) -> str:
        """Returns structured JSON of all verified dataset KPIs."""
        return json.dumps(kpis, indent=2)

    @staticmethod
    def cross_check_numerical_claim(claim_key: str, claimed_value: float, ground_truth_kpis: Dict[str, Any], tolerance: float = 0.05) -> Dict[str, Any]:
        """
        Cross-checks a numerical value against the ground truth KPI dictionary.
        Returns whether the claim is verified, tolerance error, and reference value.
        """
        fin = ground_truth_kpis.get("financial_kpis", {})
        lending = ground_truth_kpis.get("lending_kpis", {})
        ops = ground_truth_kpis.get("operations_kpis", {})
        risk = ground_truth_kpis.get("risk_kpis", {})

        lookup = {
            "total_deposit_balance": fin.get("total_deposit_balance"),
            "total_transaction_turnover": fin.get("total_transaction_turnover"),
            "approval_rate": lending.get("approval_rate"),
            "disbursed_volume": lending.get("disbursed_volume"),
            "delinquency_rate": risk.get("delinquency_rate"),
            "failure_rate": ops.get("failure_rate"),
            "critical_risk_events": risk.get("critical_risk_events")
        }

        actual = lookup.get(claim_key)
        if actual is None:
            return {"status": "Unknown Key", "verified": False, "key": claim_key}

        diff = abs(actual - claimed_value)
        relative_error = diff / actual if actual != 0 else 0
        is_valid = relative_error <= tolerance

        return {
            "key": claim_key,
            "claimed_value": claimed_value,
            "actual_value": actual,
            "relative_error": round(relative_error * 100, 2),
            "verified": is_valid,
            "status": "APPROVED" if is_valid else "DISCREPANCY FLAGGED"
        }

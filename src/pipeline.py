import pandas as pd

from src.approval import predict_approval
from src.fraud import predict_fraud
from src.premium import predict_premium
from src.risk import predict_risk


def _fraud_response(reason: str):
    return {
        "fraud": "Fraud Detected",
        "risk_cluster": None,
        "predicted_premium": None,
        "claim_status": "Rejected",
        "reason": reason,
    }


def run_pipeline(transaction_data: dict, customer_data: dict):
    # ---------------- FRAUD CHECK ----------------
    txn_df = pd.DataFrame([transaction_data])
    fraud = predict_fraud(txn_df)

    # Rule-based high-risk transaction block
    if (
        transaction_data["amount"] >= 150000
        and transaction_data["type"] in [1, 4]  # CASH_OUT or TRANSFER
    ):
        return _fraud_response("Fraudulent Transaction (Rule-Based)")

    # ML-based fraud signal
    if fraud == 1:
        return _fraud_response("Fraudulent Transaction (ML-Based)")

    # ---------------- CUSTOMER SCORING ----------------
    cust_df = pd.DataFrame([customer_data])

    risk_cluster = predict_risk(cust_df[["age", "bmi", "smoker"]])

    premium = predict_premium(
        cust_df[["age", "sex", "bmi", "children", "smoker", "region"]]
    )

    # Business-rule fast approval
    if premium <= 4700 and risk_cluster in [0, 1]:
        return {
            "fraud": "No Fraud",
            "risk_cluster": risk_cluster,
            "predicted_premium": premium,
            "claim_status": "Approved (Business Rule)",
        }

    approval_df = cust_df[
        ["age", "sex", "bmi", "children", "smoker", "region"]
    ].copy()
    approval_df["charges"] = premium

    approval = predict_approval(approval_df)

    return {
        "fraud": "No Fraud",
        "risk_cluster": risk_cluster,
        "predicted_premium": premium,
        "claim_status": "Approved" if approval == 1 else "Rejected",
    }

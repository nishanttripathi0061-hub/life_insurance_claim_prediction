# import pandas as pd

# from src.fraud import predict_fraud
# from src.risk import predict_risk
# from src.premium import predict_premium
# from src.approval import predict_approval


# def run_pipeline(transaction_data: dict, customer_data: dict):

#     # -------- FRAUD CHECK --------
#     txn_df = pd.DataFrame([transaction_data])
#     fraud = predict_fraud(txn_df)

#     if fraud == 1:
#         return {
#             "status": "Rejected",
#             "reason": "Fraudulent Transaction Detected"
#         }

#     # -------- CUSTOMER DATA --------
#     cust_df = pd.DataFrame([customer_data])

#     # Risk Segmentation
#     risk_cluster = predict_risk(
#         cust_df[["age", "sex", "bmi", "children", "smoker"]]
#     )

#     # Premium Prediction
#     premium = predict_premium(
#         cust_df[["age", "sex", "bmi", "children", "smoker", "region"]]
#     )

#     # Claim Approval
#     approval_df = cust_df[
#         ["age", "sex", "bmi", "children", "smoker", "region"]
#     ].copy()

#     approval_df["charges"] = premium

#     approval = predict_approval(approval_df)

#     return {
#         "fraud": "No Fraud",
#         "risk_cluster": risk_cluster,
#         "predicted_premium": premium,
#         "claim_status": "Approved" if approval == 1 else "Rejected"
#     }

import pandas as pd

from src.fraud import predict_fraud
from src.risk import predict_risk
from src.premium import predict_premium
from src.approval import predict_approval


def run_pipeline(transaction_data: dict, customer_data: dict):

    # ================= FRAUD CHECK =================
    txn_df = pd.DataFrame([transaction_data])
    fraud = predict_fraud(txn_df)

    # 🔴 RULE-BASED FRAUD (HIGH RISK TRANSACTIONS)
    if (
        transaction_data["amount"] >= 150000
        and transaction_data["type"] in [1, 4]   # CASH_OUT or TRANSFER
    ):
        return {
            "status": "Rejected",
            "reason": "Fraudulent Transaction (Rule-Based)"
        }

    # 🔴 ML-BASED FRAUD
    if fraud == 1:
        return {
            "status": "Rejected",
            "reason": "Fraudulent Transaction (ML-Based)"
        }

    # ================= CUSTOMER DATA =================
    cust_df = pd.DataFrame([customer_data])

    # Risk Segmentation (INSIGHT)
    risk_cluster = predict_risk(
        cust_df[["age", "bmi", "smoker"]]
    )
   

    # Premium Prediction
    premium = predict_premium(
        cust_df[["age", "sex", "bmi", "children", "smoker", "region"]]
    )

    # ================= BUSINESS RULE APPROVAL =================
    if premium <= 4700 and risk_cluster in [0, 1]:
        return {
            "fraud": "No Fraud",
            "risk_cluster": risk_cluster,
            "predicted_premium": premium,
            "claim_status": "Approved (Business Rule)"
        }

    # ================= ML-BASED APPROVAL =================
    approval_df = cust_df[
        ["age", "sex", "bmi", "children", "smoker", "region"]
    ].copy()

    approval_df["charges"] = premium

    approval = predict_approval(approval_df)

    return {
        "fraud": "No Fraud",
        "risk_cluster": risk_cluster,
        "predicted_premium": premium,
        "claim_status": "Approved" if approval == 1 else "Rejected"
    }







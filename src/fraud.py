import joblib
import pandas as pd

# Load trained fraud detection model
fraud_detection = joblib.load("models/fraud_model.pkl")
fraud_detection.n_jobs = 1

FRAUD_FEATURES = list(getattr(fraud_detection, "feature_names_in_", [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "orig_diff",
    "dest_diff",
    "orig_zero",
    "dest_unchanged",
]))


def predict_fraud(df: pd.DataFrame):
    """
    Input columns:
    step, type, amount, oldbalanceOrg, newbalanceOrig,
    oldbalanceDest, newbalanceDest,
    orig_diff, dest_diff, orig_zero, dest_unchanged
    """
    # Keep feature names and order exactly same as training.
    df_ordered = df.reindex(columns=FRAUD_FEATURES, fill_value=0)
    prediction = fraud_detection.predict(df_ordered)
    return int(prediction[0])


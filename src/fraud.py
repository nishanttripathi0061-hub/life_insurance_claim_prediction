import joblib
import pandas as pd

# Load trained fraud detection model
fraud_detection = joblib.load("models/fraud_model.pkl")


def predict_fraud(df: pd.DataFrame):
    """
    Input columns:
    amount, oldbalanceOrg, newbalanceOrig,
    oldbalanceDest, newbalanceDest,
    orig_diff, dest_diff, orig_zero, dest_unchanged
    """
    prediction = fraud_detection.predict(df)
    return int(prediction[0])


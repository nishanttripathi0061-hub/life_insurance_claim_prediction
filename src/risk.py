import joblib
import pandas as pd

# Load trained model and scaler
kmeans = joblib.load("models/risk_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# EXACT feature order used during training
RISK_FEATURES = ["age", "bmi", "smoker"]


def predict_risk(df: pd.DataFrame):
    """
    Input columns:
    age, bmi, smoker
    """

    # 1️⃣ Enforce column order
    df_ordered = df[RISK_FEATURES]

    # 2️⃣ DROP FEATURE NAMES (CRITICAL FIX)
    X = df_ordered.to_numpy()

    # 3️⃣ Scale + Predict
    X_scaled = scaler.transform(X)
    cluster = kmeans.predict(X_scaled)

    return int(cluster[0])

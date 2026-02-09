import joblib
import pandas as pd

# Load trained claim approval model
claim_approval = joblib.load("models/approval_model.pkl")


def predict_approval(df: pd.DataFrame):
    """
    Input columns:
    age, sex, bmi, children, smoker, region, charges
    """
    prediction = claim_approval.predict(df)
    return int(prediction[0])

import joblib
import pandas as pd

# Load trained premium prediction model
premium_prediction = joblib.load("models/premium_model.pkl")


def predict_premium(df: pd.DataFrame):
    """
    Input columns:
    age, sex, bmi, children, smoker, region
    """
    prediction = premium_prediction.predict(df)
    return float(prediction[0])

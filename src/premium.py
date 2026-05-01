import joblib
import pandas as pd

# Load trained premium prediction model
premium_prediction = joblib.load("models/premium_model.pkl")
premium_prediction.n_jobs = 1
PREMIUM_FEATURES = list(getattr(premium_prediction, "feature_names_in_", [
    "age",
    "sex",
    "bmi",
    "children",
    "smoker",
    "region",
]))


def predict_premium(df: pd.DataFrame):
    """
    Input columns:
    age, sex, bmi, children, smoker, region
    """
    df_ordered = df.reindex(columns=PREMIUM_FEATURES, fill_value=0)
    prediction = premium_prediction.predict(df_ordered)
    return float(prediction[0])

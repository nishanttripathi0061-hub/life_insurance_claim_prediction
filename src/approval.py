import joblib
import pandas as pd

# Load trained claim approval model
claim_approval = joblib.load("models/approval_model.pkl")
claim_approval.n_jobs = 1
APPROVAL_FEATURES = list(getattr(claim_approval, "feature_names_in_", [
    "age",
    "sex",
    "bmi",
    "children",
    "smoker",
    "region",
    "charges",
]))


def predict_approval(df: pd.DataFrame):
    """
    Input columns:
    age, sex, bmi, children, smoker, region, charges
    """
    df_ordered = df.reindex(columns=APPROVAL_FEATURES, fill_value=0)
    prediction = claim_approval.predict(df_ordered)
    return int(prediction[0])

# from src.pipeline import run_pipeline

# # ---------------- TRANSACTION INPUT (Fraud Detection) ----------------
# transaction_input = {
#     "step": 5,
#     "type": 3,              # PAYMENT (safe)
#     "amount": 2000,

#     "oldbalanceOrg": 100000,
#     "newbalanceOrig": 98000,

#     "oldbalanceDest": 50000,
#     "newbalanceDest": 52000,

#     "orig_diff": 2000,
#     "dest_diff": 2000,

#     "orig_zero": 0,
#     "dest_unchanged": 0
# }

# # ---------------- CUSTOMER INPUT (Risk, Premium, Approval) ----------------
# customer_input = {
#     "age": 18,        # thoda kam
#     "sex": 1,         # female (dataset me avg premium kam hota hai)
#     "bmi": 18.0,      # ideal BMI
#     "children": 1,    # IMPORTANT
#     "smoker": 0,       # smoker (high risk)
#     "region": 3       # lowest encoded region
# }


# # ---------------- RUN PIPELINE ----------------
# result = run_pipeline(transaction_input, customer_input)

# print("\n========== CLAIM PREDICTION RESULT ==========")
# print()
# for key, value in result.items():
#     print(f"{key} : {value}")

from flask import Flask, request, jsonify
from flask_cors import CORS

from src.pipeline import run_pipeline

app = Flask(__name__)
CORS(app)   # frontend (HTML file) se request allow karne ke liye

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "Life Insurance Claim Prediction API is running"

# ---------------- PREDICTION ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # basic validation
    if not data:
        return jsonify({"error": "No data received"}), 400

    if "transaction" not in data or "customer" not in data:
        return jsonify({"error": "Invalid input format"}), 400

    try:
        result = run_pipeline(
            transaction_data=data["transaction"],
            customer_data=data["customer"]
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)


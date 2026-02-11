function getRiskBadge(risk) {
    if (risk == 0) return '<span class="badge low">Low Risk 🟢</span>';
    if (risk == 1) return '<span class="badge medium">Medium Risk 🟡</span>';
    return '<span class="badge high">High Risk 🔴</span>';
}

function predict() {

    const resultDiv = document.getElementById("result");

    // Show loading
    resultDiv.innerHTML = '<div class="loading">Predicting...</div>';

    const amount = Number(document.getElementById("amount").value);

    const data = {
        transaction: {
            step: 1,
            type: Number(document.getElementById("type").value),
            amount: amount,

            oldbalanceOrg: 100000,
            newbalanceOrig: 100000 - amount,

            oldbalanceDest: 50000,
            newbalanceDest: 50000 + amount,

            orig_diff: amount,
            dest_diff: amount,

            orig_zero: 0,
            dest_unchanged: 0
        },

        customer: {
            age: Number(document.getElementById("age").value),
            sex: Number(document.getElementById("sex").value),
            bmi: Number(document.getElementById("bmi").value),
            children: Number(document.getElementById("children").value),
            smoker: Number(document.getElementById("smoker").value),
            region: Number(document.getElementById("region").value)
        }
    };

    fetch("https://life-insurance-claim-prediction.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {

        const risk = result.risk || result.risk_cluster;
        const claim = result.claim_status || result.claim;

        resultDiv.innerHTML = `
            <p><b>Fraud:</b> ${result.fraud || "N/A"}</p>
            <p><b>Risk:</b> ${getRiskBadge(risk)}</p>
            <p><b>Premium:</b> ₹${result.predicted_premium || result.premium}</p>
            <p><b>Claim:</b> 
                <span class="${claim.includes("Approved") ? "approved" : "rejected"}">
                    ${claim}
                </span>
            </p>
        `;
    })
    .catch(() => {
        resultDiv.innerHTML = "Server Error ⚠️";
    });
}

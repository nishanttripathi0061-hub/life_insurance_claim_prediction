function predict() {

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

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById("result").innerHTML = `
            <b>Fraud:</b> ${result.fraud || "N/A"}<br>
            <b>Risk:</b> ${result.risk || result.risk_cluster}<br>
            <b>Premium:</b> ₹${result.predicted_premium || result.premium}<br>
            <b>Claim:</b> ${result.claim_status || result.claim}
        `;
    })
    .catch(() => {
        document.getElementById("result").innerText =
            "Error connecting to backend";
    });
}

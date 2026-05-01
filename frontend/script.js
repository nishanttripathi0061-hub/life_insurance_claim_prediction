function getRiskBadge(risk) {
    if (risk === 0) return '<span class="badge low">Low Risk</span>';
    if (risk === 1) return '<span class="badge medium">Medium Risk</span>';
    if (risk === 2) return '<span class="badge high">High Risk</span>';
    return '<span class="badge neutral">N/A</span>';
}

function formatAmount(value) {
    const amount = Number(value);
    if (!Number.isFinite(amount)) return "N/A";
    return `Rs ${amount.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
}

function showResult(html, isError = false) {
    const resultDiv = document.getElementById("result");
    resultDiv.classList.remove("has-content", "error");
    resultDiv.innerHTML = html;

    if (isError) {
        resultDiv.classList.add("error");
    }

    requestAnimationFrame(() => {
        resultDiv.classList.add("has-content");
    });
}

function buildTransaction(amount, type) {
    const oldbalanceOrg = Math.max(100000, amount + 5000);
    const newbalanceOrig = oldbalanceOrg - amount;
    const oldbalanceDest = 50000;
    const newbalanceDest = oldbalanceDest + amount;

    return {
        step: 1,
        type,
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        orig_diff: amount,
        dest_diff: amount,
        orig_zero: oldbalanceOrg === 0 ? 1 : 0,
        dest_unchanged: oldbalanceDest === newbalanceDest ? 1 : 0,
    };
}

async function predict() {
    const amount = Number(document.getElementById("amount").value);

    if (!Number.isFinite(amount) || amount <= 0) {
        showResult("Please enter a valid transaction amount greater than 0.", true);
        return;
    }

    showResult('<div class="loading">Predicting...</div>');

    const transactionType = Number(document.getElementById("type").value);

    const data = {
        transaction: buildTransaction(amount, transactionType),
        customer: {
            age: Number(document.getElementById("age").value),
            sex: Number(document.getElementById("sex").value),
            bmi: Number(document.getElementById("bmi").value),
            children: Number(document.getElementById("children").value),
            smoker: Number(document.getElementById("smoker").value),
            region: Number(document.getElementById("region").value),
        },
    };

    try {
        const res = await fetch("https://life-insurance-claim-prediction.onrender.com/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await res.json().catch(() => ({}));

        if (!res.ok || result.error) {
            throw new Error(result.details || result.error || `Request failed with status ${res.status}`);
        }

        const risk = result.risk ?? result.risk_cluster;
        const claimText = result.claim_status ?? result.claim ?? result.status ?? "N/A";

        let claimClass = "neutral";
        if (typeof claimText === "string") {
            const lower = claimText.toLowerCase();
            if (lower.includes("approved")) {
                claimClass = "approved";
            } else if (lower.includes("rejected")) {
                claimClass = "rejected";
            }
        }

        const reasonBlock = result.reason ? `<p><b>Reason:</b> ${result.reason}</p>` : "";

        showResult(`
            <p><b>Fraud:</b> ${result.fraud ?? "N/A"}</p>
            <p><b>Risk:</b> ${getRiskBadge(risk)}</p>
            <p><b>Premium:</b> ${formatAmount(result.predicted_premium ?? result.premium)}</p>
            <p><b>Claim:</b> <span class="${claimClass}">${claimText}</span></p>
            ${reasonBlock}
        `);
    } catch (error) {
        showResult(`Unable to predict: ${error.message}`, true);
    }
}

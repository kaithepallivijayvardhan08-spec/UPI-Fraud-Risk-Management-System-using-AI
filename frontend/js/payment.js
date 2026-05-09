// Payment Module for SafePay

let currentPayment = null;

async function initiatePayment(to, amount, note) {
    currentPayment = { to, amount, note };
    
    const risk = await riskEngine.calculateRisk({
        amount: amount,
        to: to,
        category: 'grocery'
    });
    
    if (risk.risk_score >= 70) {
        showRiskWarning(to, amount, note, risk);
    } else {
        showPinVerification(to, amount, note, risk);
    }
}

function retryPayment() {
    if (currentPayment) {
        initiatePayment(currentPayment.to, currentPayment.amount, currentPayment.note);
    }
}

function saveAsDraft() {
    if (currentPayment) {
        const drafts = JSON.parse(localStorage.getItem('safepay_drafts') || '[]');
        drafts.push({
            ...currentPayment,
            id: generateId(),
            savedAt: new Date().toISOString()
        });
        localStorage.setItem('safepay_drafts', JSON.stringify(drafts));
        showToast('Payment saved as draft', 'success');
    }
}
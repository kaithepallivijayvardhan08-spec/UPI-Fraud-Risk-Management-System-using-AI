// Risk Engine for SafePay

class RiskEngine {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
    }
    
    async calculateRisk(transactionData) {
        const user = getCurrentUser();
        
        const payload = {
            user_id: user?.email || 'default_user',
            amount: transactionData.amount,
            trans_hours: new Date().getHours(),
            category: transactionData.category || 'grocery',
            state: transactionData.state || 'KA',
            age: user?.age || 30
        };
        
        try {
            const response = await fetch(`${this.apiBase}/calculate-risk`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            
            if (result.success) {
                return result.risk;
            } else {
                return this.fallbackRiskCalculation(transactionData);
            }
        } catch (error) {
            console.error('Risk API error:', error);
            return this.fallbackRiskCalculation(transactionData);
        }
    }
    
    fallbackRiskCalculation(transactionData) {
        let riskScore = 0;
        const factors = [];
        
        // Amount factor
        const amount = transactionData.amount;
        if (amount > 10000) {
            riskScore += 30;
            factors.push("💰 Amount is very high (₹" + amount.toLocaleString() + ")");
        } else if (amount > 5000) {
            riskScore += 20;
            factors.push("💰 Amount is higher than average");
        } else if (amount > 2000) {
            riskScore += 10;
        }
        
        // Time factor
        const hour = new Date().getHours();
        if (hour < 6 || hour > 22) {
            riskScore += 25;
            factors.push("⏰ Unusual transaction time (" + hour + ":00)");
        }
        
        // Check if receiver is new
        const payees = JSON.parse(localStorage.getItem(STORAGE_KEYS.PAYEES) || '[]');
        const isNewReceiver = !payees.some(p => p.upi === transactionData.to);
        if (isNewReceiver) {
            riskScore += 15;
            factors.push("🆕 First time sending to this receiver");
        }
        
        // Check transaction count
        const transactions = JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS) || '[]');
        if (transactions.length < 5) {
            riskScore += 10;
            factors.push("🆕 New user - limited transaction history");
        }
        
        riskScore = Math.min(riskScore, 100);
        
        let riskLevel = 'Low';
        if (riskScore >= 70) riskLevel = 'High';
        else if (riskScore >= 30) riskLevel = 'Medium';
        
        return {
            risk_score: riskScore,
            risk_level: riskLevel,
            color: riskLevel === 'High' ? '🔴' : riskLevel === 'Medium' ? '🟡' : '🟢',
            risk_factors: factors.slice(0, 3),
            recommendation: this.getRecommendation(riskScore)
        };
    }
    
    getRecommendation(riskScore) {
        if (riskScore < 30) {
            return "Transaction appears safe. You can proceed.";
        } else if (riskScore < 70) {
            return "Medium risk detected. Verify receiver details before paying.";
        } else {
            return "HIGH RISK! This transaction may be fraudulent. Consider canceling.";
        }
    }
    
    updateRiskMeter(riskScore, elementId = 'risk-gauge') {
        const container = document.getElementById(elementId);
        if (!container) return;
        
        const percentage = riskScore;
        const circumference = 2 * Math.PI * 80;
        const dashArray = (percentage / 100) * circumference;
        
        let color;
        if (riskScore < 30) color = '#00C853';
        else if (riskScore < 70) color = '#FFC107';
        else color = '#FF3B30';
        
        container.innerHTML = `
            <svg width="180" height="180" viewBox="0 0 180 180">
                <circle class="bg-circle" cx="90" cy="90" r="80" stroke="#E9ECEF" stroke-width="12" fill="none"/>
                <circle class="fill-circle" cx="90" cy="90" r="80" stroke="${color}" stroke-width="12" fill="none"
                        stroke-dasharray="${dashArray} ${circumference}" stroke-linecap="round"/>
            </svg>
            <div class="risk-text">
                <div class="risk-score" style="color: ${color}">${riskScore}%</div>
                <div class="risk-label" style="background: ${color}20; color: ${color}">
                    ${riskScore < 30 ? 'LOW RISK' : riskScore < 70 ? 'MEDIUM RISK' : 'HIGH RISK'}
                </div>
            </div>
        `;
    }
}

// Create global instance
const riskEngine = new RiskEngine();
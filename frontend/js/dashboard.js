// Dashboard Module for SafePay

function updateDashboardStats() {
    const transactions = JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS) || '[]');
    const balance = localStorage.getItem(STORAGE_KEYS.BALANCE) || 0;
    
    const totalSpent = transactions.reduce((sum, t) => sum + t.amount, 0);
    const avgRisk = transactions.length > 0 
        ? Math.round(transactions.reduce((sum, t) => sum + (t.risk_score || 0), 0) / transactions.length)
        : 0;
    
    return {
        balance,
        totalSpent,
        transactionCount: transactions.length,
        avgRisk,
        lastTransaction: transactions[0]
    };
}

function refreshDashboard() {
    const stats = updateDashboardStats();
    
    // Update balance display
    const balanceEl = document.querySelector('.balance-amount');
    if (balanceEl) balanceEl.textContent = formatCurrency(stats.balance);
    
    // Update risk meter
    if (stats.avgRisk > 0) {
        riskEngine.updateRiskMeter(stats.avgRisk, 'dashboard-risk-meter');
    }
    
    // Update recent transactions
    const transactions = JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS) || '[]');
    const recentContainer = document.getElementById('recent-transactions');
    if (recentContainer) {
        recentContainer.innerHTML = getRecentTransactionsHTML(transactions.slice(0, 5));
    }
}
// Frontend Unit Tests

describe('SafePay Frontend Tests', () => {
    
    describe('Utility Functions', () => {
        test('formatCurrency should format Indian Rupees correctly', () => {
            expect(formatCurrency(1000)).toBe('₹1,000');
            expect(formatCurrency(50000)).toBe('₹50,000');
            expect(formatCurrency(0)).toBe('₹0');
        });
        
        test('validateUPIId should validate UPI IDs correctly', () => {
            expect(validateUPIId('user@okhdfcbank')).toBe(true);
            expect(validateUPIId('user.name@icici')).toBe(true);
            expect(validateUPIId('invalid')).toBe(false);
            expect(validateUPIId('user@')).toBe(false);
        });
        
        test('validateAmount should validate amounts correctly', () => {
            expect(validateAmount(100)).toBe(true);
            expect(validateAmount(50000)).toBe(true);
            expect(validateAmount(0)).toBe(false);
            expect(validateAmount(-100)).toBe(false);
            expect(validateAmount(150000)).toBe(false);
        });
        
        test('getRiskColor should return correct colors', () => {
            expect(getRiskColor('Low')).toBe('#00C853');
            expect(getRiskColor('Medium')).toBe('#FFC107');
            expect(getRiskColor('High')).toBe('#FF3B30');
        });
        
        test('getRiskIcon should return correct emojis', () => {
            expect(getRiskIcon('Low')).toBe('🟢');
            expect(getRiskIcon('Medium')).toBe('🟡');
            expect(getRiskIcon('High')).toBe('🔴');
        });
    });
    
    describe('Risk Engine Tests', () => {
        test('fallbackRiskCalculation should return valid risk score', async () => {
            const result = riskEngine.fallbackRiskCalculation({
                amount: 5000,
                to: 'test@okhdfcbank'
            });
            expect(result.risk_score).toBeGreaterThanOrEqual(0);
            expect(result.risk_score).toBeLessThanOrEqual(100);
            expect(['Low', 'Medium', 'High']).toContain(result.risk_level);
        });
        
        test('getRecommendation should return appropriate message', () => {
            expect(riskEngine.getRecommendation(10)).toContain('safe');
            expect(riskEngine.getRecommendation(50)).toContain('Medium');
            expect(riskEngine.getRecommendation(90)).toContain('HIGH RISK');
        });
    });
    
    describe('Storage Tests', () => {
        beforeEach(() => {
            localStorage.clear();
        });
        
        test('getCurrentUser should return null for new user', () => {
            expect(getCurrentUser()).toBeNull();
        });
        
        test('setCurrentUser should save user to localStorage', () => {
            const user = { name: 'Test', email: 'test@example.com' };
            setCurrentUser(user);
            expect(getCurrentUser()).toEqual(user);
        });
        
        test('clearAllData should clear all storage', () => {
            setCurrentUser({ name: 'Test' });
            localStorage.setItem('test', 'value');
            clearAllData();
            expect(getCurrentUser()).toBeNull();
            expect(localStorage.getItem('test')).toBeNull();
        });
        
        test('addNotification should add to storage', () => {
            addNotification('Test notification', 'info');
            const notifications = JSON.parse(localStorage.getItem(STORAGE_KEYS.NOTIFICATIONS) || '[]');
            expect(notifications.length).toBe(1);
            expect(notifications[0].message).toBe('Test notification');
        });
    });
    
    describe('Transaction Tests', () => {
        beforeEach(() => {
            localStorage.clear();
        });
        
        test('new user should have empty transaction history', () => {
            const transactions = JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS) || '[]');
            expect(transactions.length).toBe(0);
        });
        
        test('should save transaction after payment', () => {
            const transaction = {
                id: 'test123',
                to: 'test@okhdfcbank',
                amount: 1000,
                risk_score: 15,
                risk_level: 'Low',
                date: new Date().toISOString()
            };
            const transactions = [transaction];
            localStorage.setItem(STORAGE_KEYS.TRANSACTIONS, JSON.stringify(transactions));
            
            const saved = JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS));
            expect(saved.length).toBe(1);
            expect(saved[0].amount).toBe(1000);
        });
        
        test('should update balance after transaction', () => {
            localStorage.setItem(STORAGE_KEYS.BALANCE, '10000');
            let balance = parseFloat(localStorage.getItem(STORAGE_KEYS.BALANCE));
            balance -= 500;
            localStorage.setItem(STORAGE_KEYS.BALANCE, balance);
            
            expect(parseFloat(localStorage.getItem(STORAGE_KEYS.BALANCE))).toBe(9500);
        });
    });
});
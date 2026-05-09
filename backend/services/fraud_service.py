import re
from datetime import datetime

class FraudDetectionService:
    
    @staticmethod
    def detect_suspicious_patterns(transaction, user_history):
        """Detect suspicious patterns in transaction"""
        risk_score = 0
        reasons = []
        
        # Check amount patterns
        avg_amount = user_history.get('avg_amount', 0)
        if avg_amount > 0 and transaction['amount'] > avg_amount * 3:
            risk_score += 25
            reasons.append(f"Amount {transaction['amount']} is 3x higher than average")
        
        # Check time patterns
        hour = datetime.now().hour
        if hour < 6 or hour > 22:
            risk_score += 15
            reasons.append(f"Unusual transaction time: {hour}:00")
        
        # Check frequency
        recent_txns = user_history.get('recent_transactions', [])
        if len(recent_txns) > 5:
            last_5_min = []
            for t in recent_txns:
                try:
                    txn_time = datetime.fromisoformat(t.get('date', ''))
                    if (datetime.now() - txn_time).seconds < 300:
                        last_5_min.append(t)
                except (ValueError, TypeError):
                    pass
            
            if len(last_5_min) > 3:
                risk_score += 20
                reasons.append("Multiple transactions in short period")
        
        # Check UPI ID pattern
        upi_id = transaction.get('receiver_upi', '')
        if FraudDetectionService._is_suspicious_upi(upi_id):
            risk_score += 30
            reasons.append("Suspicious UPI ID pattern detected")
        
        return min(risk_score, 100), reasons
    
    @staticmethod
    def _is_suspicious_upi(upi_id):
        """Check if UPI ID looks suspicious"""
        suspicious_patterns = [
            'free', 'cashback', 'prize', 'winner', 'lucky',
            'unknown', 'random', 'temp', 'test', 'scam', 'fraud'
        ]
        upi_lower = upi_id.lower()
        for pattern in suspicious_patterns:
            if pattern in upi_lower:
                return True
        return False
    
    @staticmethod
    def get_risk_level(risk_score):
        """Get risk level based on score"""
        if risk_score < 30:
            return 'Low', '🟢'
        elif risk_score < 70:
            return 'Medium', '🟡'
        else:
            return 'High', '🔴'
    
    @staticmethod
    def should_block_transaction(risk_score, user_settings):
        """Determine if transaction should be blocked"""
        threshold = user_settings.get('risk_threshold', 70)
        return risk_score >= threshold
    
    @staticmethod
    def calculate_risk_score(amount, hour, is_new_receiver, transaction_count):
        """Calculate risk score based on multiple factors"""
        risk = 0
        
        # Amount factor
        if amount > 10000:
            risk += 30
        elif amount > 5000:
            risk += 20
        elif amount > 2000:
            risk += 10
        
        # Time factor
        if hour < 6 or hour > 22:
            risk += 25
        
        # New receiver factor
        if is_new_receiver:
            risk += 15
        
        # New user factor
        if transaction_count < 5:
            risk += 10
        
        return min(risk, 100)

# Create singleton instance
fraud_service = FraudDetectionService()
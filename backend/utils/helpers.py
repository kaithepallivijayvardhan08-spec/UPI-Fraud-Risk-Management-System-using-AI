import re
import uuid
from datetime import datetime

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"TXN{uuid.uuid4().hex[:12].upper()}"

def validate_upi_id(upi_id):
    """Validate UPI ID format"""
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+$'
    return bool(re.match(pattern, upi_id))

def validate_amount(amount):
    """Validate transaction amount"""
    try:
        amount = float(amount)
        return amount > 0 and amount <= 100000
    except (ValueError, TypeError):
        return False

def format_currency(amount):
    """Format amount in Indian currency format"""
    try:
        amount = float(amount)
        return f"₹{amount:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

def calculate_risk_color(risk_score):
    """Get color based on risk score"""
    if risk_score < 30:
        return '#00C853'  # Green
    elif risk_score < 70:
        return '#FFC107'  # Yellow
    else:
        return '#FF3B30'  # Red

def get_time_of_day():
    """Get time of day category"""
    hour = datetime.now().hour
    if hour < 12:
        return 'morning'
    elif hour < 17:
        return 'afternoon'
    elif hour < 21:
        return 'evening'
    else:
        return 'night'

def mask_upi_id(upi_id):
    """Mask UPI ID for privacy"""
    if '@' in upi_id:
        prefix, suffix = upi_id.split('@')
        if len(prefix) > 3:
            masked_prefix = prefix[:2] + '***' + prefix[-2:]
        else:
            masked_prefix = '***'
        return f"{masked_prefix}@{suffix}"
    return upi_id

def calculate_average_amount(transactions):
    """Calculate average transaction amount"""
    if not transactions:
        return 0
    total = sum(t.get('amount', 0) for t in transactions)
    return total / len(transactions)

def get_risk_level(risk_score):
    """Get risk level string"""
    if risk_score < 30:
        return 'Low'
    elif risk_score < 70:
        return 'Medium'
    else:
        return 'High'
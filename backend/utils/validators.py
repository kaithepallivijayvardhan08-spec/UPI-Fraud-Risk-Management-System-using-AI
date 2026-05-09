import re
from datetime import datetime

class Validators:
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_mobile(mobile):
        pattern = r'^[6-9]\d{9}$'
        return bool(re.match(pattern, str(mobile)))
    
    @staticmethod
    def validate_pin(pin):
        pin_str = str(pin)
        return pin_str.isdigit() and 4 <= len(pin_str) <= 6
    
    @staticmethod
    def validate_name(name):
        return bool(name and len(name.strip()) >= 2)
    
    @staticmethod
    def validate_date(date_string):
        try:
            datetime.fromisoformat(date_string)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_transaction(transaction):
        required_fields = ['receiver_upi', 'amount']
        for field in required_fields:
            if field not in transaction:
                return False, f"Missing field: {field}"
        
        if not validate_upi_id(transaction['receiver_upi']):
            return False, "Invalid UPI ID format"
        
        if not validate_amount(transaction['amount']):
            return False, "Invalid amount"
        
        return True, "Valid"
    
    @staticmethod
    def sanitize_input(input_string):
        if not input_string:
            return ""
        # Remove potentially dangerous characters
        return re.sub(r'[<>{}]', '', input_string)

# Import from helpers for validation functions
from .helpers import validate_upi_id, validate_amount
from datetime import datetime
import json

class Transaction:
    def __init__(self, user_id, receiver_upi, amount, risk_score, risk_level, note=None, status='completed'):
        self.user_id = user_id
        self.receiver_upi = receiver_upi
        self.amount = amount
        self.risk_score = risk_score
        self.risk_level = risk_level
        self.note = note
        self.status = status
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': getattr(self, 'id', None),
            'user_id': self.user_id,
            'receiver_upi': self.receiver_upi,
            'amount': self.amount,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'note': self.note,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        txn = cls(
            user_id=data['user_id'],
            receiver_upi=data['receiver_upi'],
            amount=data['amount'],
            risk_score=data['risk_score'],
            risk_level=data['risk_level'],
            note=data.get('note'),
            status=data.get('status', 'completed')
        )
        txn.id = data.get('id')
        if data.get('created_at'):
            txn.created_at = datetime.fromisoformat(data['created_at'])
        return txn

class User:
    def __init__(self, email, name, mobile=None, upi_id=None, bank_name=None, balance=0):
        self.email = email
        self.name = name
        self.mobile = mobile
        self.upi_id = upi_id
        self.bank_name = bank_name
        self.balance = balance
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': getattr(self, 'id', None),
            'email': self.email,
            'name': self.name,
            'mobile': self.mobile,
            'upi_id': self.upi_id,
            'bank_name': self.bank_name,
            'balance': self.balance,
            'created_at': self.created_at.isoformat()
        }

class Alert:
    def __init__(self, user_id, title, message, alert_type='info'):
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = alert_type
        self.is_read = False
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': getattr(self, 'id', None),
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
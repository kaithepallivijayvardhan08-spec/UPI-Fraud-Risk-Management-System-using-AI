from .db_config import db_config
from .models import Transaction, User, Alert

class QueryManager:
    
    # User queries
    @staticmethod
    def create_user(user):
        query = '''
            INSERT INTO users (email, name, mobile, upi_id, bank_name, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        user_id = db_config.execute_query(query, (
            user.email, user.name, user.mobile, user.upi_id, user.bank_name, user.balance
        ))
        return user_id
    
    @staticmethod
    def get_user_by_email(email):
        query = 'SELECT * FROM users WHERE email = ?'
        result = db_config.fetch_one(query, (email,))
        if result:
            return {
                'id': result[0],
                'email': result[1],
                'name': result[2],
                'mobile': result[3],
                'upi_id': result[4],
                'bank_name': result[5],
                'balance': result[6],
                'created_at': result[7]
            }
        return None
    
    @staticmethod
    def update_balance(user_id, new_balance):
        query = 'UPDATE users SET balance = ? WHERE id = ?'
        db_config.execute_query(query, (new_balance, user_id))
    
    # Transaction queries
    @staticmethod
    def save_transaction(transaction):
        query = '''
            INSERT INTO transactions (user_id, transaction_id, receiver_upi, amount, note, risk_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        txn_id = db_config.execute_query(query, (
            transaction.user_id, transaction.id, transaction.receiver_upi,
            transaction.amount, transaction.note, transaction.risk_score,
            transaction.risk_level, transaction.status
        ))
        return txn_id
    
    @staticmethod
    def get_user_transactions(user_id, limit=50, offset=0):
        query = '''
            SELECT * FROM transactions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        '''
        results = db_config.fetch_all(query, (user_id, limit, offset))
        return [dict(zip(['id', 'user_id', 'transaction_id', 'receiver_upi', 'amount', 
                          'note', 'risk_score', 'risk_level', 'status', 'created_at'], r)) for r in results]
    
    @staticmethod
    def get_transaction_by_id(transaction_id):
        query = 'SELECT * FROM transactions WHERE transaction_id = ?'
        result = db_config.fetch_one(query, (transaction_id,))
        if result:
            return dict(zip(['id', 'user_id', 'transaction_id', 'receiver_upi', 'amount', 
                            'note', 'risk_score', 'risk_level', 'status', 'created_at'], result))
        return None
    
    # Alert queries
    @staticmethod
    def create_alert(alert):
        query = '''
            INSERT INTO alerts (user_id, title, message, type, is_read)
            VALUES (?, ?, ?, ?, ?)
        '''
        alert_id = db_config.execute_query(query, (
            alert.user_id, alert.title, alert.message, alert.type, 0
        ))
        return alert_id
    
    @staticmethod
    def get_user_alerts(user_id, unread_only=False):
        if unread_only:
            query = 'SELECT * FROM alerts WHERE user_id = ? AND is_read = 0 ORDER BY created_at DESC'
        else:
            query = 'SELECT * FROM alerts WHERE user_id = ? ORDER BY created_at DESC'
        results = db_config.fetch_all(query, (user_id,))
        return [dict(zip(['id', 'user_id', 'title', 'message', 'type', 'is_read', 'created_at'], r)) for r in results]
    
    @staticmethod
    def mark_alert_read(alert_id):
        query = 'UPDATE alerts SET is_read = 1 WHERE id = ?'
        db_config.execute_query(query, (alert_id,))
    
    # Payee queries
    @staticmethod
    def add_or_update_payee(user_id, upi_id, name):
        existing = db_config.fetch_one('SELECT * FROM payees WHERE user_id = ? AND upi_id = ?', (user_id, upi_id))
        if existing:
            query = '''
                UPDATE payees 
                SET count = count + 1, last_transaction = CURRENT_TIMESTAMP 
                WHERE user_id = ? AND upi_id = ?
            '''
            db_config.execute_query(query, (user_id, upi_id))
        else:
            query = '''
                INSERT INTO payees (user_id, upi_id, name, count, last_transaction)
                VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
            '''
            db_config.execute_query(query, (user_id, upi_id, name))
    
    @staticmethod
    def get_recent_payees(user_id, limit=5):
        query = '''
            SELECT upi_id, name, count, last_transaction 
            FROM payees 
            WHERE user_id = ? 
            ORDER BY last_transaction DESC 
            LIMIT ?
        '''
        results = db_config.fetch_all(query, (user_id, limit))
        return [{'upi_id': r[0], 'name': r[1], 'count': r[2], 'last_transaction': r[3]} for r in results]

query_manager = QueryManager()
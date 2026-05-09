from flask import Blueprint, request, jsonify
from models.fraud_detector import detector
import json
from datetime import datetime

api_bp = Blueprint('api', __name__)

# In-memory storage
user_transactions = {}
user_balances = {}
user_profiles = {}

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'SafePay API is running'})

@api_bp.route('/calculate-risk', methods=['POST'])
def calculate_risk():
    try:
        data = request.json
        transaction_data = {
            'trans_hours': data.get('trans_hours', datetime.now().hour),
            'trans_day': datetime.now().day,
            'trans_month': datetime.now().month,
            'trans_year': datetime.now().year,
            'age': data.get('age', 30),
            'transact_amount': data.get('amount', 0),
            'category': data.get('category', 'grocery'),
            'state': data.get('state', 'KA')
        }
        
        user_id = data.get('user_id', 'default_user')
        user_history = user_transactions.get(user_id, {})
        
        risk_result = detector.predict_risk(transaction_data, user_history)
        
        return jsonify({'success': True, 'risk': risk_result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/register-transaction', methods=['POST'])
def register_transaction():
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        
        transaction = {
            'id': len(user_transactions.get(user_id, {}).get('transactions', [])) + 1,
            'to': data.get('to'),
            'amount': data.get('amount'),
            'risk_score': data.get('risk_score'),
            'risk_level': data.get('risk_level'),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success'
        }
        
        if user_id not in user_transactions:
            user_transactions[user_id] = {
                'transactions': [],
                'avg_amount': 0,
                'total_transactions': 0
            }
        
        user_transactions[user_id]['transactions'].append(transaction)
        amounts = [t['amount'] for t in user_transactions[user_id]['transactions']]
        user_transactions[user_id]['avg_amount'] = sum(amounts) / len(amounts)
        user_transactions[user_id]['total_transactions'] = len(amounts)
        
        if user_id in user_balances:
            user_balances[user_id] -= data.get('amount', 0)
        
        return jsonify({'success': True, 'transaction': transaction, 'balance': user_balances.get(user_id, 0)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/get-history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id', 'default_user')
    if user_id in user_transactions:
        return jsonify({
            'success': True,
            'transactions': user_transactions[user_id]['transactions'],
            'stats': {
                'total_transactions': user_transactions[user_id]['total_transactions'],
                'avg_amount': user_transactions[user_id]['avg_amount']
            }
        })
    return jsonify({'success': True, 'transactions': [], 'stats': {'total_transactions': 0, 'avg_amount': 0}})

@api_bp.route('/set-balance', methods=['POST'])
def set_balance():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    balance = data.get('balance', 0)
    user_balances[user_id] = balance
    return jsonify({'success': True, 'balance': balance})

@api_bp.route('/get-balance', methods=['GET'])
def get_balance():
    user_id = request.args.get('user_id', 'default_user')
    return jsonify({'success': True, 'balance': user_balances.get(user_id, 0)})

@api_bp.route('/save-profile', methods=['POST'])
def save_profile():
    data = request.json
    user_id = data.get('email', 'default_user')
    user_profiles[user_id] = {
        'name': data.get('name'),
        'email': data.get('email'),
        'upi_id': data.get('upi_id'),
        'mobile': data.get('mobile'),
        'bank': data.get('bank'),
        'mpin': data.get('mpin')
    }
    return jsonify({'success': True, 'profile': user_profiles[user_id]})

@api_bp.route('/get-profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id', 'default_user')
    return jsonify({'success': True, 'profile': user_profiles.get(user_id, {})})
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'safepay_secret_key_2024'
CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000', 'http://localhost:3000'])

# Import fraud detector
from models.fraud_detector import detector

# In-memory storage for demo (replace with database in production)
user_transactions = {}
user_balances = {}
user_profiles = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'SafePay API is running'})

@app.route('/api/calculate-risk', methods=['POST'])
def calculate_risk():
    """Calculate fraud risk for a transaction"""
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
        
        # Get user history if available
        user_id = data.get('user_id', 'default_user')
        user_history = user_transactions.get(user_id, {})
        
        # Calculate risk
        risk_result = detector.predict_risk(transaction_data, user_history)
        
        return jsonify({
            'success': True,
            'risk': risk_result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/register-transaction', methods=['POST'])
def register_transaction():
    """Save completed transaction to user history"""
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
        
        # Update averages
        all_amounts = [t['amount'] for t in user_transactions[user_id]['transactions']]
        user_transactions[user_id]['avg_amount'] = sum(all_amounts) / len(all_amounts)
        user_transactions[user_id]['total_transactions'] = len(all_amounts)
        
        # Update balance if exists
        if user_id in user_balances:
            user_balances[user_id] -= data.get('amount', 0)
        
        return jsonify({
            'success': True,
            'transaction': transaction,
            'balance': user_balances.get(user_id, 0)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-history', methods=['GET'])
def get_history():
    """Get transaction history for user"""
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
    else:
        return jsonify({
            'success': True,
            'transactions': [],
            'stats': {
                'total_transactions': 0,
                'avg_amount': 0
            }
        })

@app.route('/api/set-balance', methods=['POST'])
def set_balance():
    """Set user's bank balance"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    balance = data.get('balance', 0)
    
    user_balances[user_id] = balance
    
    return jsonify({
        'success': True,
        'balance': balance
    })

@app.route('/api/get-balance', methods=['GET'])
def get_balance():
    """Get user's bank balance"""
    user_id = request.args.get('user_id', 'default_user')
    balance = user_balances.get(user_id, 0)
    
    return jsonify({
        'success': True,
        'balance': balance
    })

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    """Save user profile"""
    data = request.json
    user_id = data.get('email', 'default_user')
    
    user_profiles[user_id] = {
        'name': data.get('name'),
        'email': data.get('email'),
        'upi_id': data.get('upi_id'),
        'mobile': data.get('mobile'),
        'bank': data.get('bank'),
        'mpin': data.get('mpin')  # In production, hash this!
    }
    
    return jsonify({
        'success': True,
        'profile': user_profiles[user_id]
    })

@app.route('/api/get-profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    user_id = request.args.get('user_id', 'default_user')
    profile = user_profiles.get(user_id, {})
    
    return jsonify({
        'success': True,
        'profile': profile
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 SafePay Backend Server")
    print("=" * 50)
    print("📍 Running on: http://localhost:5000")
    print("📡 API endpoints:")
    print("   POST /api/calculate-risk")
    print("   POST /api/register-transaction")
    print("   GET  /api/get-history")
    print("   POST /api/set-balance")
    print("   GET  /api/get-balance")
    print("=" * 50)
    app.run(debug=True, port=5000)
from flask import Blueprint, request, jsonify
from models.fraud_detector import detector
from datetime import datetime

risk_bp = Blueprint('risk', __name__, url_prefix='/risk')

@risk_bp.route('/analyze', methods=['POST'])
def analyze_risk():
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
    
    user_history = data.get('user_history', {})
    result = detector.predict_risk(transaction_data, user_history)
    
    return jsonify({'success': True, 'risk': result})

@risk_bp.route('/batch', methods=['POST'])
def batch_analyze():
    data = request.json
    transactions = data.get('transactions', [])
    results = []
    
    for txn in transactions:
        transaction_data = {
            'trans_hours': txn.get('hour', 12),
            'trans_day': txn.get('day', 15),
            'trans_month': txn.get('month', 6),
            'trans_year': txn.get('year', 2024),
            'age': txn.get('age', 30),
            'transact_amount': txn.get('amount', 0),
            'category': txn.get('category', 'grocery'),
            'state': txn.get('state', 'KA')
        }
        result = detector.predict_risk(transaction_data, {})
        results.append(result)
    
    return jsonify({'success': True, 'results': results})

@risk_bp.route('/thresholds', methods=['GET'])
def get_thresholds():
    return jsonify({
        'success': True,
        'thresholds': {
            'low_risk_max': 30,
            'medium_risk_max': 70,
            'high_risk_min': 70
        }
    })

@risk_bp.route('/update-model', methods=['POST'])
def update_model():
    data = request.json
    new_transactions = data.get('transactions', [])
    
    # In production, this would retrain the model
    # For now, just acknowledge
    return jsonify({
        'success': True,
        'message': f'Received {len(new_transactions)} transactions for retraining'
    })
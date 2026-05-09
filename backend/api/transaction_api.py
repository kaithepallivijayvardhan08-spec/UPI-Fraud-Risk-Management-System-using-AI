from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transaction')

# In-memory transaction storage
transactions_db = {}

@transaction_bp.route('/add', methods=['POST'])
def add_transaction():
    data = request.json
    user_id = data.get('user_id')
    transaction = {
        'id': data.get('id'),
        'to': data.get('to'),
        'amount': data.get('amount'),
        'note': data.get('note'),
        'risk_score': data.get('risk_score'),
        'risk_level': data.get('risk_level'),
        'date': datetime.now().isoformat(),
        'status': data.get('status', 'completed')
    }
    
    if user_id not in transactions_db:
        transactions_db[user_id] = []
    
    transactions_db[user_id].append(transaction)
    return jsonify({'success': True, 'transaction': transaction})

@transaction_bp.route('/list', methods=['GET'])
def list_transactions():
    user_id = request.args.get('user_id')
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    user_transactions = transactions_db.get(user_id, [])
    user_transactions.reverse()  # Most recent first
    
    paginated = user_transactions[offset:offset + limit]
    
    return jsonify({
        'success': True,
        'transactions': paginated,
        'total': len(user_transactions)
    })

@transaction_bp.route('/filter', methods=['POST'])
def filter_transactions():
    data = request.json
    user_id = data.get('user_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    min_amount = data.get('min_amount')
    max_amount = data.get('max_amount')
    risk_level = data.get('risk_level')
    
    user_transactions = transactions_db.get(user_id, [])
    filtered = user_transactions
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        filtered = [t for t in filtered if datetime.fromisoformat(t['date']) >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        filtered = [t for t in filtered if datetime.fromisoformat(t['date']) <= end]
    
    if min_amount:
        filtered = [t for t in filtered if t['amount'] >= min_amount]
    
    if max_amount:
        filtered = [t for t in filtered if t['amount'] <= max_amount]
    
    if risk_level:
        filtered = [t for t in filtered if t['risk_level'] == risk_level]
    
    return jsonify({'success': True, 'transactions': filtered, 'count': len(filtered)})

@transaction_bp.route('/summary', methods=['GET'])
def transaction_summary():
    user_id = request.args.get('user_id')
    user_transactions = transactions_db.get(user_id, [])
    
    total_spent = sum(t['amount'] for t in user_transactions)
    total_transactions = len(user_transactions)
    avg_amount = total_spent / total_transactions if total_transactions > 0 else 0
    high_risk_count = len([t for t in user_transactions if t.get('risk_level') == 'High'])
    
    return jsonify({
        'success': True,
        'summary': {
            'total_spent': total_spent,
            'total_transactions': total_transactions,
            'avg_amount': avg_amount,
            'high_risk_count': high_risk_count
        }
    })
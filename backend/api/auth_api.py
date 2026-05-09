from flask import Blueprint, request, jsonify
import hashlib
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

SECRET_KEY = os.environ.get('SECRET_KEY', 'safepay_secret_key_2024')

# In-memory user storage
users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    mobile = data.get('mobile')
    
    if email in users:
        return jsonify({'success': False, 'error': 'User already exists'}), 400
    
    users[email] = {
        'email': email,
        'password': hash_password(password),
        'name': name,
        'mobile': mobile,
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({'success': True, 'message': 'User registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if email not in users:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    if not verify_password(password, users[email]['password']):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'email': email,
            'name': users[email]['name'],
            'mobile': users[email]['mobile']
        }
    })

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.json
    token = data.get('token')
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'success': True, 'email': payload['email']})
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'error': 'Invalid token'}), 401

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.json
    email = data.get('email')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if email not in users:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    if not verify_password(old_password, users[email]['password']):
        return jsonify({'success': False, 'error': 'Invalid old password'}), 401
    
    users[email]['password'] = hash_password(new_password)
    return jsonify({'success': True, 'message': 'Password changed successfully'})
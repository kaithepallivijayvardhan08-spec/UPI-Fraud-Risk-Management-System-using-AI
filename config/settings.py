import os
from pathlib import Path

class Settings:
    # Base directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # App settings
    APP_NAME = "SafePay"
    APP_VERSION = "1.0.0"
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'safepay_secret_key_2024')
    JWT_EXPIRATION_HOURS = 24
    
    # Risk thresholds
    LOW_RISK_THRESHOLD = 30
    MEDIUM_RISK_THRESHOLD = 70
    HIGH_RISK_THRESHOLD = 70
    
    # Transaction limits
    MAX_TRANSACTION_AMOUNT = 100000
    MIN_TRANSACTION_AMOUNT = 1
    DAILY_LIMIT = 50000
    
    # Database
    DATABASE_PATH = BASE_DIR / 'safepay.db'
    
    # Model paths
    MODEL_PATH = BASE_DIR / 'backend' / 'models' / 'fraud_model.pkl'
    FEATURES_PATH = BASE_DIR / 'backend' / 'models' / 'feature_columns.pkl'
    
    # API settings
    API_PREFIX = '/api'
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000', 'http://localhost:3000']
    
    # Feature columns for ML model
    FEATURE_COLUMNS = [
        'trans_hours', 'trans_day', 'trans_month', 'trans_year',
        'age', 'transact_amount', 'category_grocery', 'category_entertainment',
        'category_shopping', 'category_bills', 'state_KA', 'state_MH',
        'state_DL', 'state_TN'
    ]

settings = Settings()
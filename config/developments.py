from .settings import Settings

class DevelopmentConfig(Settings):
    DEBUG = True
    DATABASE_PATH = Settings.BASE_DIR / 'safepay_dev.db'
    
    # Development specific settings
    DEV_MODE = True
    MOCK_QR_SCANNER = True
    SKIP_PIN_VERIFICATION = False
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    # Test data
    LOAD_TEST_DATA = False
    
    # API endpoints for development
    API_BASE_URL = 'http://localhost:5000/api'

dev_config = DevelopmentConfig()
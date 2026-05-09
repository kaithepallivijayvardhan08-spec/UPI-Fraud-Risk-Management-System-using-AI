# Config package initializer

class Settings:
    """Base settings for SafePay"""
    APP_NAME = "SafePay"
    APP_VERSION = "1.0.0"
    DEBUG = True
    API_BASE_URL = 'http://localhost:5000/api'

class DevelopmentConfig(Settings):
    """Development specific settings"""
    DEBUG = True
    DEV_MODE = True
    MOCK_QR_SCANNER = True

__all__ = ['Settings', 'DevelopmentConfig']
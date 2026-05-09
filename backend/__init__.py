# Backend package initializer
from flask import Flask
from flask_cors import CORS

def create_app(config=None):
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])
    
    if config:
        app.config.update(config)
    
    # Register blueprints
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
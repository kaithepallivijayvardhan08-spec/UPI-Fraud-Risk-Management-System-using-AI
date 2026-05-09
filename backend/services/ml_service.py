import joblib
import pandas as pd
import numpy as np
import os

class MLService:
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'fraud_model.pkl')
        features_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'feature_columns.pkl')
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print("✅ ML Model loaded successfully")
        
        if os.path.exists(features_path):
            self.feature_columns = joblib.load(features_path)
    
    def predict(self, features):
        if self.model is None:
            return self._fallback_predict(features)
        
        df = pd.DataFrame([features])
        
        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        df = df[self.feature_columns]
        probability = self.model.predict_proba(df)[0][1]
        return probability
    
    def _fallback_predict(self, features):
        # Simple rule-based fallback
        risk = 0
        if features.get('transact_amount', 0) > 10000:
            risk += 0.3
        if features.get('trans_hours', 12) < 6 or features.get('trans_hours', 12) > 22:
            risk += 0.25
        return min(risk, 1.0)
    
    def predict_batch(self, features_list):
        return [self.predict(f) for f in features_list]
    
    def get_feature_importance(self):
        if self.model and hasattr(self.model, 'feature_importances_'):
            return dict(zip(self.feature_columns, self.model.feature_importances_))
        return {}

ml_service = MLService()
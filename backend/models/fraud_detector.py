import joblib
import pandas as pd
import numpy as np
import os

class FraudDetector:
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        """Load the trained Random Forest model"""
        model_path = os.path.join(os.path.dirname(__file__), 'fraud_model.pkl')
        features_path = os.path.join(os.path.dirname(__file__), 'feature_columns.pkl')
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print("✅ Fraud detection model loaded")
        else:
            print("⚠️ Model not found. Please run train_model.py first")
            self.model = None
        
        if os.path.exists(features_path):
            self.feature_columns = joblib.load(features_path)
            print("✅ Feature columns loaded")
    
    def predict_risk(self, transaction_data, user_history=None):
        """
        Predict fraud risk for a transaction
        
        transaction_data: dict with keys:
            - trans_hours: int (0-23)
            - trans_day: int (1-31)
            - trans_month: int (1-12)
            - trans_year: int
            - age: int
            - transact_amount: float
            - category: str
            - state: str
        
        Returns: risk_score (0-100), risk_level (Low/Medium/High), risk_factors
        """
        if self.model is None:
            return self._fallback_risk_calculation(transaction_data, user_history)
        
        # Prepare feature vector
        features = self._prepare_features(transaction_data)
        
        # Get probability of fraud
        fraud_probability = self.model.predict_proba(features)[0][1]
        risk_score = int(fraud_probability * 100)
        
        # Determine risk level
        if risk_score < 30:
            risk_level = "Low"
            color = "🟢"
        elif risk_score < 70:
            risk_level = "Medium"
            color = "🟡"
        else:
            risk_level = "High"
            color = "🔴"
        
        # Generate risk factors
        risk_factors = self._generate_risk_factors(transaction_data, user_history, risk_score)
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'color': color,
            'risk_factors': risk_factors,
            'recommendation': self._get_recommendation(risk_score)
        }
    
    def _prepare_features(self, data):
        """Convert transaction data to feature vector"""
        # Base features
        base_features = {
            'trans_hours': data.get('trans_hours', 12),
            'trans_day': data.get('trans_day', 15),
            'trans_month': data.get('trans_month', 6),
            'trans_year': data.get('trans_year', 2024),
            'age': data.get('age', 30),
            'transact_amount': data.get('transact_amount', 1000)
        }
        
        # Create DataFrame
        df = pd.DataFrame([base_features])
        
        # Add categorical columns (all possible categories from training)
        categories = ['category_entertainment', 'category_grocery', 'category_shopping', 'category_bills']
        states = ['state_KA', 'state_MH', 'state_DL', 'state_TN']
        
        for cat in categories:
            df[cat] = 0
        for st in states:
            df[st] = 0
        
        # Set actual category
        category = data.get('category', 'grocery')
        if category != 'grocery':
            df[f'category_{category}'] = 1
        else:
            df['category_grocery'] = 1
        
        # Set actual state
        state = data.get('state', 'KA')
        if state != 'KA':
            df[f'state_{state}'] = 1
        else:
            df['state_KA'] = 1
        
        # Ensure all training columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training
        df = df[self.feature_columns]
        
        return df
    
    def _generate_risk_factors(self, data, user_history, risk_score):
        """Generate human-readable risk factors"""
        factors = []
        
        # Amount based factor
        amount = data.get('transact_amount', 0)
        if amount > 10000:
            factors.append("💰 Amount is very high (₹{:,.0f})".format(amount))
            risk_score += 10
        elif amount > 5000:
            factors.append("💰 Amount is higher than average")
            risk_score += 5
        
        # Time based factor
        hour = data.get('trans_hours', 12)
        if hour < 6 or hour > 22:
            factors.append("⏰ Unusual transaction time ({}:00)".format(hour))
            risk_score += 15
        
        # User history based factors
        if user_history:
            avg_amount = user_history.get('avg_amount', 0)
            if avg_amount > 0 and amount > avg_amount * 3:
                factors.append("📈 Amount is 3x higher than your average")
                risk_score += 20
            
            if user_history.get('total_transactions', 0) < 5:
                factors.append("🆕 New user - limited transaction history")
                risk_score += 10
        
        # Default factors based on risk score
        if not factors:
            if risk_score > 70:
                factors.append("⚠️ Multiple suspicious patterns detected")
            elif risk_score > 30:
                factors.append("🔍 Some unusual patterns detected")
            else:
                factors.append("✅ Transaction looks normal")
        
        return factors[:3]  # Return top 3 factors
    
    def _get_recommendation(self, risk_score):
        """Get recommendation based on risk score"""
        if risk_score < 30:
            return "Transaction appears safe. You can proceed."
        elif risk_score < 70:
            return "Medium risk detected. Verify receiver details before paying."
        else:
            return "HIGH RISK! This transaction may be fraudulent. Consider canceling."
    
    def _fallback_risk_calculation(self, data, user_history):
        """Fallback risk calculation if ML model not available"""
        risk_score = 0
        
        # Amount factor
        amount = data.get('transact_amount', 0)
        if amount > 10000:
            risk_score += 30
        elif amount > 5000:
            risk_score += 20
        elif amount > 2000:
            risk_score += 10
        
        # Time factor
        hour = data.get('trans_hours', 12)
        if hour < 6 or hour > 22:
            risk_score += 25
        
        # User history factor
        if user_history:
            if user_history.get('total_transactions', 0) < 3:
                risk_score += 15
        
        risk_score = min(risk_score, 100)
        
        if risk_score < 30:
            risk_level = "Low"
            color = "🟢"
        elif risk_score < 70:
            risk_level = "Medium"
            color = "🟡"
        else:
            risk_level = "High"
            color = "🔴"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'color': color,
            'risk_factors': self._generate_risk_factors(data, user_history, risk_score),
            'recommendation': self._get_recommendation(risk_score)
        }

# Singleton instance
detector = FraudDetector()
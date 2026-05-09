import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import os

def train_model():
    print("=" * 50)
    print("🤖 SAFEPAY - FRAUD DETECTION MODEL TRAINING")
    print("=" * 50)
    
    # Load dataset
    print("\n📊 Loading dataset...")
    df = pd.read_csv('../backend/data/upi_fraud_data.csv')
    
    print(f"✅ Loaded {len(df)} transactions")
    print(f"📈 Columns: {list(df.columns)}")
    
    # Check fraud distribution
    fraud_count = df['fraud_risk'].sum()
    print(f"\n⚠️ Fraud cases: {fraud_count} ({fraud_count/len(df)*100:.1f}%)")
    print(f"✅ Safe cases: {len(df)-fraud_count} ({(len(df)-fraud_count)/len(df)*100:.1f}%)")
    
    # Feature columns for training (as requested - keeping fraud_risk)
    feature_cols = [
        "trans_hour",
        "trans_day",
        "trans_month",
        "trans_year",
        "category",
        "upi_number",
        "age",
        "trans_amount",
        "state",
        "zip",
        "fraud_risk"
    ]
    
    # Categorical features to encode
    categorical_cols = ['category', 'state']
    
    # Create feature matrix
    X = df[feature_cols].copy()
    
    # 🔧 FIX: Remove fraud_risk from features if it exists (since it's the target)
    if 'fraud_risk' in X.columns:
        X = X.drop('fraud_risk', axis=1)
        print("\n🔧 Removed 'fraud_risk' from features (it's the target variable)")
    
    # One-hot encode categorical variables
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    # Target variable
    y = df['fraud_risk']
    
    print(f"\n🔢 Feature matrix shape: {X.shape}")
    print(f"📊 Features: {list(X.columns)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📚 Training set: {len(X_train)} samples")
    print(f"🧪 Testing set: {len(X_test)} samples")
    
    # Train Random Forest model
    print("\n🤖 Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    
    print("\n" + "=" * 50)
    print("📊 MODEL EVALUATION RESULTS")
    print("=" * 50)
    print(f"🎯 Accuracy:  {accuracy_score(y_test, y_pred)*100:.2f}%")
    print(f"🎯 Precision: {precision_score(y_test, y_pred)*100:.2f}%")
    print(f"🎯 Recall:    {recall_score(y_test, y_pred)*100:.2f}%")
    print(f"🎯 F1 Score:  {f1_score(y_test, y_pred)*100:.2f}%")
    
    print("\n📋 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"   True Negatives:  {cm[0][0]}")
    print(f"   False Positives: {cm[0][1]}")
    print(f"   False Negatives: {cm[1][0]}")
    print(f"   True Positives:  {cm[1][1]}")
    
    # Feature importance
    print("\n📊 FEATURE IMPORTANCE:")
    importance = model.feature_importances_
    for name, imp in sorted(zip(X.columns, importance), key=lambda x: x[1], reverse=True):
        print(f"   {name}: {imp:.3f}")
    
    # Save model
    os.makedirs('../backend/models', exist_ok=True)
    joblib.dump(model, '../backend/models/fraud_model.pkl')
    print("\n💾 Model saved to: backend/models/fraud_model.pkl")
    
    # Save feature columns for reference
    feature_columns = list(X.columns)
    joblib.dump(feature_columns, '../backend/models/feature_columns.pkl')
    print("💾 Feature columns saved to: backend/models/feature_columns.pkl")
    
    print("\n✅ Training complete!")
    return model

if __name__ == '__main__':
    train_model()
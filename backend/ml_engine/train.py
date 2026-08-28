import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def generate_synthetic_data(samples=5000):
    np.random.seed(42)
    
    # Genuine transactions
    amount_genuine = np.random.exponential(scale=50, size=int(samples * 0.95))
    device_risk_genuine = np.random.choice([0, 1], size=int(samples * 0.95), p=[0.9, 0.1])
    location_risk_genuine = np.random.choice([0, 1], size=int(samples * 0.95), p=[0.95, 0.05])
    is_fraud_genuine = np.zeros(int(samples * 0.95))

    # Fraudulent transactions
    amount_fraud = np.random.normal(loc=1200, scale=300, size=int(samples * 0.05))
    device_risk_fraud = np.random.choice([0, 1], size=int(samples * 0.05), p=[0.2, 0.8])
    location_risk_fraud = np.random.choice([0, 1], size=int(samples * 0.05), p=[0.3, 0.7])
    is_fraud_fraud = np.ones(int(samples * 0.05))

    # Combine dataset
    amounts = np.concatenate([amount_genuine, amount_fraud])
    device_risks = np.concatenate([device_risk_genuine, device_risk_fraud])
    location_risks = np.concatenate([location_risk_genuine, location_risk_fraud])
    labels = np.concatenate([is_fraud_genuine, is_fraud_fraud])

    df = pd.DataFrame({
        'amount': amounts,
        'device_risk': device_risks,
        'location_risk': location_risks,
        'is_fraud': labels
    })
    return df

def train_and_save_models():
    df = generate_synthetic_data()
    X = df[['amount', 'device_risk', 'location_risk']]
    y = df['is_fraud']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 1. Unsupervised Anomaly Detection: Isolation Forest
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    iso_forest.fit(X_scaled)

    # 2. Supervised Classification: XGBoost
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    xgb_model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_train, y_train)

    # Model Storage Directory
    model_dir = os.path.dirname(__file__)
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(iso_forest, os.path.join(model_dir, 'isolation_forest.pkl'))
    joblib.dump(xgb_model, os.path.join(model_dir, 'xgboost.pkl'))
    
    print("[SUCCESS] Models trained and exported to backend/ml_engine/")

if __name__ == "__main__":
    train_and_save_models()
import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(__file__)
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))
iso_forest = joblib.load(os.path.join(BASE_DIR, 'isolation_forest.pkl'))
xgb_model = joblib.load(os.path.join(BASE_DIR, 'xgboost.pkl'))

def evaluate_transaction(amount, device_risk, location_risk):
    features = np.array([[float(amount), int(device_risk), int(location_risk)]])
    features_scaled = scaler.transform(features)

    # Isolation forest outputs -1 for anomaly, 1 for normal
    iso_score = iso_forest.decision_function(features_scaled)[0]
    iso_anomaly = 1 if iso_forest.predict(features_scaled)[0] == -1 else 0

    # XGBoost outputs probability [0, 1]
    xgb_prob = float(xgb_model.predict_proba(features_scaled)[0][1])

    # Hybrid Ensemble Score Calculation (Scaled 0 - 100)
    # 70% Supervised XGBoost + 30% Unsupervised Anomaly signal
    iso_component = 30 if iso_anomaly else 0
    xgb_component = xgb_prob * 70
    
    fraud_risk_score = round(iso_component + xgb_component, 2)
    is_fraudulent = fraud_risk_score > 60.0

    return {
        "fraud_risk_score": fraud_risk_score,
        "is_fraud": is_fraudulent,
        "xgb_prob": round(xgb_prob, 4),
        "iso_anomaly": bool(iso_anomaly)
    }
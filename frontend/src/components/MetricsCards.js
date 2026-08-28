import React from 'react';

export default function MetricsCards({ transactions }) {
  const total = transactions.length;
  const fraudCount = transactions.filter(t => t.is_fraud).length;
  const fraudPercentage = total > 0 ? ((fraudCount / total) * 100).toFixed(1) : 0;
  const avgRisk = total > 0 ? (transactions.reduce((acc, t) => acc + t.fraud_risk_score, 0) / total).toFixed(1) : 0;

  return (
    <div className="grid-cards">
      <div className="card">
        <h4>Total Processed</h4>
        <p className="card-value">{total}</p>
      </div>
      <div className="card alert">
        <h4>Flagged Fraud</h4>
        <p className="card-value">{fraudCount}</p>
      </div>
      <div className="card">
        <h4>Fraud Rate</h4>
        <p className="card-value">{fraudPercentage}%</p>
      </div>
      <div className="card">
        <h4>Avg Risk Score</h4>
        <p className="card-value">{avgRisk} / 100</p>
      </div>
    </div>
  );
}
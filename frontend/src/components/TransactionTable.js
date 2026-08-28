import React from 'react';

export default function TransactionTable({ transactions }) {
  return (
    <table className="tx-table">
      <thead>
        <tr>
          <th>Tx ID</th>
          <th>Sender</th>
          <th>Receiver</th>
          <th>Amount</th>
          <th>Risk Score</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((tx) => (
          <tr key={tx.transaction_id} className={tx.is_fraud ? 'row-fraud' : ''}>
            <td>{tx.transaction_id}</td>
            <td>{tx.sender_account}</td>
            <td>{tx.receiver_account}</td>
            <td>${tx.amount}</td>
            <td><strong>{tx.fraud_risk_score}</strong></td>
            <td>
              <span className={`badge ${tx.is_fraud ? 'badge-fraud' : 'badge-pass'}`}>
                {tx.is_fraud ? 'FRAUD' : 'CLEARED'}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
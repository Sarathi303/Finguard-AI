import React, { useState, useEffect } from 'react';
import MetricsCards from './components/MetricsCards';
import FraudChart from './components/FraudChart';
import TransactionTable from './components/TransactionTable';
import './App.css';

function App() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // 1. Initial REST API load
    fetch('http://127.0.0.1:8000/api/transactions/')
      .then(res => res.json())
      .then(data => setTransactions(data))
      .catch(err => console.error("API Fetch Error:", err));

    // 2. Real-Time WebSocket stream listener
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/alerts/');

    socket.onmessage = (event) => {
      const newTx = JSON.parse(event.data);
      setTransactions((prev) => [newTx, ...prev.slice(0, 49)]);
    };

    return () => socket.close();
  }, []);

  return (
    <div className="dashboard-container">
      <header className="header">
        <h2>FinGuard AI — Real-Time Fraud Operations Dashboard</h2>
      </header>
      <MetricsCards transactions={transactions} />
      <div className="content-grid">
        <div className="chart-box">
          <h3>Real-time Risk Trend</h3>
          <FraudChart transactions={transactions} />
        </div>
        <div className="table-box">
          <h3>Live Transaction Feed</h3>
          <TransactionTable transactions={transactions} />
        </div>
      </div>
    </div>
  );
}

export default App;
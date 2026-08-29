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
useEffect
import React, { useEffect, useState } from 'react';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [metrics, setMetrics] = useState({ total: 0, flagged: 0, fraudRate: 0, avgRisk: 0 });

  useEffect(() => {
    // WebSocket URL-ஐ அமைத்தல்
    const wsScheme = window.location.protocol === "https:" ? "wss://" : "ws://";
    const socket = new WebSocket(wsScheme + window.location.host + "/ws/fraud-feed/");

    socket.onmessage = function(event) {
      const data = JSON.parse(event.data);
      
      // புதிய பரிவர்த்தனையை டேபிளில் சேர்ப்பது
      setTransactions((prev) => [data, ...prev]);
      
      // கார்டு மதிப்புகளை அப்டேட் செய்வது
      // (உங்கள் தேவைக்கேற்ப இங்கு லாஜிக் மாற்றிக்கொள்ளலாம்)
    };

    socket.onclose = function() {
      console.error('WebSocket closed unexpectedly');
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    // உங்களுடைய டஷ்போர்டு UI கோடுகள் இங்கே இருக்கும்
    <div>
      {/* Live Transaction Feed டேபிள் மற்றும் கார்டுகள் */}
    </div>
  );
}

export default App;
const API_URL = "https://finguard-ai-h6d7.onrender.com/api/";
const WS_URL = "wss://finguard-ai-h6d7.onrender.com/ws/fraud-feed/";
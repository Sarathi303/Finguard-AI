import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function FraudChart({ transactions }) {
  const recent = [...transactions].reverse().slice(-15);

  const data = {
    labels: recent.map(t => t.timestamp ? t.timestamp.split(' ')[1] : ''),
    datasets: [
      {
        label: 'Fraud Risk Score',
        data: recent.map(t => t.fraud_risk_score),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
        tension: 0.3
      }
    ]
  };

  const options = {
    responsive: true,
    scales: {
      y: { min: 0, max: 100 }
    }
  };

  return <Line data={data} options={options} />;
}
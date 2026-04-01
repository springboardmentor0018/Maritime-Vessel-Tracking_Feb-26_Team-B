import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  Legend
} from "recharts";

import "../styles/dashboard.css";

const riskTrendData = [
  { date: "Mar 1", score: 7.2 },
  { date: "Mar 5", score: 7.5 },
  { date: "Mar 10", score: 7.1 },
  { date: "Mar 15", score: 7.3 },
  { date: "Mar 19", score: 7.2 }
];

const severityData = [
  { month: "Oct", high: 12, medium: 25, low: 45 },
  { month: "Nov", high: 15, medium: 28, low: 40 },
  { month: "Dec", high: 18, medium: 30, low: 38 },
  { month: "Jan", high: 14, medium: 27, low: 42 },
  { month: "Feb", high: 16, medium: 29, low: 39 },
  { month: "Mar", high: 13, medium: 26, low: 44 }
];

const RiskAnalysis = () => {
  return (
    <div className="dashboard">

      <h1 className="title">Risk Analysis</h1>

      {/* TOP CARDS */}
      <div className="card-container">
        <div className="card">
          <h3>Overall Risk Score</h3>
          <p>7.2</p>
        </div>

        <div className="card">
          <h3>High Risk Vessels</h3>
          <p>13</p>
        </div>

        <div className="card">
          <h3>Risk Trend</h3>
          <p>Improving</p>
        </div>

        <div className="card">
          <h3>Incidents</h3>
          <p>3</p>
        </div>
      </div>

      {/* CHARTS */}
      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>

        {/* BAR CHART */}
        <div className="card">
          <h3>Risk Trends by Severity</h3>

          <BarChart width={400} height={250} data={severityData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="high" fill="#ef4444" />
            <Bar dataKey="medium" fill="#f59e0b" />
            <Bar dataKey="low" fill="#10b981" />
          </BarChart>
        </div>

        {/* LINE CHART */}
        <div className="card">
          <h3>Overall Risk Score Trend</h3>

          <LineChart width={400} height={250} data={riskTrendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#2563eb" />
          </LineChart>
        </div>

      </div>

    </div>
  );
};

export default RiskAnalysis;
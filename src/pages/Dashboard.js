import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/dashboard.css";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/dashboard")
      .then((res) => setData(res.data))
      .catch((err) => {
        console.log(err);

        // fallback dummy data (so UI won't break)
        setData({
          vessels: 1247,
          alerts: 23,
          ports: 156,
          risk: 7.2,
          activities: [
            { name: "MSC Oscar", action: "Entered Port", time: "2 hours ago" },
            { name: "OOCL Germany", action: "Weather Warning", time: "4 hours ago" },
            { name: "Ever Given", action: "Route Updated", time: "6 hours ago" },
          ],
          status: [
            { name: "AIS Tracking", status: "Operational" },
            { name: "Weather Service", status: "Operational" },
            { name: "Port API", status: "Operational" },
            { name: "Alert System", status: "Operational" },
          ],
        });
      });
  }, []);

  if (!data) return <p>Loading dashboard...</p>;

  return (
    <div className="dashboard-page">
      <h2>Dashboard</h2>
      <p className="subtitle">
        Welcome to Maritime Risk Intelligence Platform
      </p>

      {/* TOP CARDS */}
      <div className="dashboard-cards">
        <div className="card">
          <h4>Active Vessels</h4>
          <h2>{data.vessels}</h2>
        </div>

        <div className="card">
          <h4>Active Alerts</h4>
          <h2>{data.alerts}</h2>
        </div>

        <div className="card">
          <h4>Ports Monitored</h4>
          <h2>{data.ports}</h2>
        </div>

        <div className="card">
          <h4>Risk Score</h4>
          <h2>{data.risk}</h2>
        </div>
      </div>

      {/* BOTTOM SECTION */}
      <div className="dashboard-bottom">
        {/* Activity */}
        <div className="card">
          <h3>Recent Activity</h3>

          {data.activities.map((item, index) => (
            <div key={index} className="activity-item">
              <div>
                <b>{item.name}</b>
                <p>{item.action}</p>
              </div>
              <span>{item.time}</span>
            </div>
          ))}
        </div>

        {/* System Status */}
        <div className="card">
          <h3>System Status</h3>

          {data.status.map((s, index) => (
            <div key={index} className="status-item">
              <span>{s.name}</span>
              <span className="status-badge">{s.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
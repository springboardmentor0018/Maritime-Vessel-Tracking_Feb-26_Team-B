import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/port.css";

function PortAuthority() {
  const [ports, setPorts] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/ports")
      .then((res) => setPorts(res.data))
      .catch((err) => {
        console.log(err);

        // fallback dummy data
        setPorts([
          {
            name: "Port of Singapore",
            vessels: 124,
            capacity: 95,
            wait_time: "2.5 hrs",
            status: "Operational",
          },
          {
            name: "Port of Shanghai",
            vessels: 98,
            capacity: 88,
            wait_time: "1.8 hrs",
            status: "Operational",
          },
          {
            name: "Port of Los Angeles",
            vessels: 67,
            capacity: 78,
            wait_time: "4.8 hrs",
            status: "Congested",
          },
        ]);
      });
  }, []);

  if (!ports.length) return <p>Loading ports...</p>;

  return (
    <div className="port-page">
      <h2>Port Authority</h2>
      <p className="subtitle">
        Monitor port operations and vessel traffic
      </p>

      <div className="port-grid">
        {ports.map((port, index) => (
          <div key={index} className="card">
            <h3>{port.name}</h3>

            <p>🚢 Active Vessels: {port.vessels}</p>
            <p>📊 Capacity: {port.capacity}%</p>
            <p>⏱ Avg Wait: {port.wait_time}</p>

            <div
              className={
                port.status === "Operational"
                  ? "status-ok"
                  : "status-bad"
              }
            >
              {port.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PortAuthority;
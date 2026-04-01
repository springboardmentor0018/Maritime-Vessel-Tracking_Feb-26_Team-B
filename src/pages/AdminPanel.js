import React, { useEffect, useState } from "react";
import "../styles/admin.css";

function AdminPanel() {

  const [apiStatus, setApiStatus] = useState([]);
  const [logs, setLogs] = useState([]);

  // ✅ Ready for backend (replace with API later)
  useEffect(() => {
    setApiStatus([
      { name: "AIS Tracking API", status: "Operational", time: "10:30 AM" },
      { name: "Replay API", status: "Operational", time: "10:32 AM" },
      { name: "Weather API", status: "Down", time: "10:35 AM" },
      { name: "Port API", status: "Operational", time: "10:40 AM" },
    ]);

    setLogs([
      { time: "10:30 AM", message: "Server Started", type: "INFO" },
      { time: "10:32 AM", message: "Replay API Called", type: "INFO" },
      { time: "10:35 AM", message: "Weather API Failed", type: "ERROR" },
      { time: "10:40 AM", message: "Port Data Updated", type: "INFO" },
    ]);
  }, []);

  const handleExport = (type) => {
    // 👉 backend ready
    alert(`${type} export started`);
  };

  return (
    <div className="admin-container">

      <h2>Admin Panel</h2>

      {/* ✅ STATS CARDS */}
      <div className="admin-cards">
        <div className="card">
          <h3>{apiStatus.length}</h3>
          <p>Total APIs</p>
        </div>

        <div className="card">
          <h3>{apiStatus.filter(a => a.status === "Operational").length}</h3>
          <p>Active APIs</p>
        </div>

        <div className="card">
          <h3>{apiStatus.filter(a => a.status === "Down").length}</h3>
          <p>Errors</p>
        </div>
      </div>

      {/* ✅ API STATUS */}
      <div className="admin-section">
        <h3>API Status Monitoring</h3>

        <table>
          <thead>
            <tr>
              <th>API Name</th>
              <th>Status</th>
              <th>Last Checked</th>
            </tr>
          </thead>

          <tbody>
            {apiStatus.map((api, index) => (
              <tr key={index}>
                <td>{api.name}</td>
                <td>
                  <span className={api.status === "Operational" ? "green" : "red"}>
                    {api.status}
                  </span>
                </td>
                <td>{api.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ✅ LOGS */}
      <div className="admin-section">
        <h3>System Logs</h3>

        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Message</th>
              <th>Type</th>
            </tr>
          </thead>

          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>{log.time}</td>
                <td>{log.message}</td>
                <td>{log.type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ✅ EXPORT */}
      <div className="admin-section">
        <h3>Export Data</h3>

        <button onClick={() => handleExport("Users")}>Export Users</button>
        <button onClick={() => handleExport("Vessels")}>Export Vessels</button>
        <button onClick={() => handleExport("Reports")}>Export Reports</button>
      </div>

    </div>
  );
}

export default AdminPanel;
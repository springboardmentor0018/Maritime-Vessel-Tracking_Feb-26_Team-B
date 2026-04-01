import React from "react";
import "../styles/notification.css";

function Notification({ alerts }) {
  return (
    <div className="notification-box">
      <h3>Alerts</h3>

      {alerts.length === 0 ? (
        <p>No alerts</p>
      ) : (
        alerts.map((a, i) => (
          <div key={i} className="alert">
            ⚠ {a.message}
          </div>
        ))
      )}
    </div>
  );
}

export default Notification;
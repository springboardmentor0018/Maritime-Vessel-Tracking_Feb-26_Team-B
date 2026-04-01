import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import "../styles/subscription.css"; // ✅ FIXED (capital S)

function Subscription() {
  const location = useLocation();
  const vessel = location.state;

  const [alertType, setAlertType] = useState("Speed Alert");
  const [email, setEmail] = useState(true);
  const [sms, setSms] = useState(true);
  const [showPopup, setShowPopup] = useState(false);

  const handleSave = () => {
    const data = {
      vesselId: vessel?.id,
      alertType,
      email,
      sms,
    };

    console.log("Send to backend:", data);
    setShowPopup(true);
  };

  return (
    <div className="subscription-container">
      <div className="card">
        <h2>Setup alerts for</h2>
        <h1>{vessel?.name}</h1>

        <div className="form-group">
          <label>Alert Type</label>
          <select
            value={alertType}
            onChange={(e) => setAlertType(e.target.value)}
          >
            <option>Speed Alert</option>
            <option>Arrival Alert</option>
            <option>Departure Alert</option>
          </select>
        </div>

        <div className="checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={email}
              onChange={() => setEmail(!email)}
            />
            Email Alerts
          </label>

          <label>
            <input
              type="checkbox"
              checked={sms}
              onChange={() => setSms(!sms)}
            />
            SMS Alerts
          </label>
        </div>

        <button className="save-btn" onClick={handleSave}>
          Save
        </button>

        {showPopup && (
          <div className="success-box">
            <p>Subscribed Successfully</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Subscription;
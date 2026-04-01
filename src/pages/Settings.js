import React, { useState, useEffect } from "react";
import "../styles/settings.css";

function Settings() {
  const [settings, setSettings] = useState({
    company: "",
    email: "",
    timezone: "",

    emailNotif: false,
    vesselAlerts: false,
    portUpdates: false,
    weatherWarnings: false,

    twoFactor: false,
    sessionTimeout: false,

    aisKey: "",
    weatherKey: "",
    portKey: ""
  });

  const [editApi, setEditApi] = useState(false);

  useEffect(() => {
    const data = {
      company: "Maritime Corp",
      email: "admin@maritime.com",
      timezone: "UTC +5:30",

      emailNotif: true,
      vesselAlerts: true,
      portUpdates: true,
      weatherWarnings: true,

      twoFactor: false,
      sessionTimeout: true,

      aisKey: "********",
      weatherKey: "********",
      portKey: "********"
    };

    setSettings(data);
  }, []);

  const handleChange = (e) => {
    setSettings({ ...settings, [e.target.name]: e.target.value });
  };

  const handleToggle = (key) => {
    setSettings({ ...settings, [key]: !settings[key] });
  };

  const handleSave = () => {
    console.log("Saving:", settings);
    alert("Settings saved successfully!");
  };

  const handleReset = () => {
    window.location.reload();
  };

  return (
    <div className="settings-page">

      <h2>Settings</h2>
      <p className="subtitle">Manage your system preferences and configuration</p>

      {/* GENERAL */}
      <div className="settings-card">
        <h3>General Settings</h3>

        <label>Company Name</label>
        <input name="company" value={settings.company} onChange={handleChange} />

        <label>Admin Email</label>
        <input name="email" value={settings.email} onChange={handleChange} />

        <label>Timezone</label>
        <select name="timezone" value={settings.timezone} onChange={handleChange}>
          <option value="">Select Timezone</option>
          <option>UTC +0:00</option>
          <option>UTC +5:30 (India)</option>
          <option>UTC -5:00 (EST)</option>
        </select>
      </div>

      {/* NOTIFICATIONS */}
      <div className="settings-card">
        <h3>Notifications</h3>

        {[
          ["emailNotif", "Email Notifications"],
          ["vesselAlerts", "Vessel Alerts"],
          ["portUpdates", "Port Updates"],
          ["weatherWarnings", "Weather Warnings"],
        ].map(([key, title]) => (
          <div className="toggle-row" key={key}>
            <b>{title}</b>
            <input
              type="checkbox"
              checked={settings[key]}
              onChange={() => handleToggle(key)}
            />
          </div>
        ))}
      </div>

      {/* API */}
      <div className="settings-card">
        <h3>API Configuration</h3>

        <button className="edit-btn" onClick={() => setEditApi(!editApi)}>
          {editApi ? "Lock API Keys" : "Edit API Keys"}
        </button>

        <label>AIS Key</label>
        <input
          type="password"
          name="aisKey"
          value={settings.aisKey}
          disabled={!editApi}
          onChange={handleChange}
        />

        <label>Weather Key</label>
        <input
          type="password"
          name="weatherKey"
          value={settings.weatherKey}
          disabled={!editApi}
          onChange={handleChange}
        />

        <label>Port Key</label>
        <input
          type="password"
          name="portKey"
          value={settings.portKey}
          disabled={!editApi}
          onChange={handleChange}
        />
      </div>

      {/* SECURITY */}
      <div className="settings-card">
        <h3>Security</h3>

        <div className="toggle-row">
          <b>Two-Factor Authentication</b>
          <input
            type="checkbox"
            checked={settings.twoFactor}
            onChange={() => handleToggle("twoFactor")}
          />
        </div>

        <div className="toggle-row">
          <b>Session Timeout</b>
          <input
            type="checkbox"
            checked={settings.sessionTimeout}
            onChange={() => handleToggle("sessionTimeout")}
          />
        </div>
      </div>

      {/* BUTTONS */}
      <div className="btn-group">
        <button className="save-btn" onClick={handleSave}>
          Save Changes
        </button>

        <button className="reset-btn" onClick={handleReset}>
          Reset to Defaults
        </button>
      </div>

    </div>
  );
}

export default Settings;
import React, { useState } from "react";
import { FaUser, FaEnvelope, FaLock } from "react-icons/fa";

const ProfileEdit = () => {
  const [open, setOpen] = useState(false);

  const [user, setUser] = useState({
    name: "John Doe",
    email: "john.doe@maritime.com",
    password: "123456"
  });

  // ✅ temp state for editing
  const [tempUser, setTempUser] = useState(user);

  // ✅ reset temp when opening
  const handleOpen = () => {
    setTempUser(user);
    setOpen(!open);
  };

  // ✅ save changes
  const handleSave = () => {
    setUser(tempUser);
    setOpen(false);
  };

  // initials
  const initials = user.name
    .split(" ")
    .map(n => n[0])
    .join("");

  return (
    <div style={{ position: "relative" }}>

      {/* 👤 Top Profile */}
      <div style={styles.profileTop} onClick={handleOpen}>
        <div style={styles.avatar}>{initials}</div>
        <span style={styles.username}>{user.name}</span>
      </div>

      {/* Panel */}
      {open && (
        <div style={styles.panel}>

          {/* Header */}
          <div style={styles.header}>
            <div style={styles.avatarLarge}>
              {tempUser.name.split(" ").map(n => n[0]).join("")}
            </div>
            <div>
              <h4 style={{ margin: 0 }}>{tempUser.name}</h4>
              <p style={styles.role}>Admin</p>
            </div>
          </div>

          <hr style={styles.hr} />

          {/* Name */}
          <div style={styles.field}>
            <label style={styles.label}>
              <FaUser /> Name
            </label>
            <input
              style={styles.input}
              value={tempUser.name}
              onChange={(e) =>
                setTempUser({ ...tempUser, name: e.target.value })
              }
            />
          </div>

          {/* Email */}
          <div style={styles.field}>
            <label style={styles.label}>
              <FaEnvelope /> Email
            </label>
            <input
              style={styles.input}
              value={tempUser.email}
              onChange={(e) =>
                setTempUser({ ...tempUser, email: e.target.value })
              }
            />
          </div>

          {/* Password */}
          <div style={styles.field}>
            <label style={styles.label}>
              <FaLock /> Change Password
            </label>
            <input
              type="password"
              style={styles.input}
              value={tempUser.password}
              onChange={(e) =>
                setTempUser({ ...tempUser, password: e.target.value })
              }
            />
          </div>

          {/* Button */}
          <button style={styles.button} onClick={handleSave}>
            Save Changes
          </button>
        </div>
      )}
    </div>
  );
};

const styles = {
  profileTop: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    cursor: "pointer"
  },

  avatar: {
    width: "35px",
    height: "35px",
    borderRadius: "50%",
    background: "#e5e7eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "600"
  },

  username: {
    fontSize: "14px",
    fontWeight: "500"
  },

  panel: {
    position: "absolute",
    top: "50px",
    right: 0,
    width: "340px",
    background: "#ffffff",
    borderRadius: "16px",
    padding: "20px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.08)"
  },

  header: {
    display: "flex",
    alignItems: "center",
    gap: "12px"
  },

  avatarLarge: {
    width: "45px",
    height: "45px",
    borderRadius: "50%",
    background: "#020617",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "600"
  },

  role: {
    margin: 0,
    fontSize: "13px",
    color: "#6b7280"
  },

  hr: {
    margin: "15px 0",
    border: "none",
    borderTop: "1px solid #e5e7eb"
  },

  field: {
    marginBottom: "12px"
  },

  label: {
    fontSize: "13px",
    fontWeight: "500",
    display: "flex",
    alignItems: "center",
    gap: "6px"
  },

  input: {
    width: "100%",
    padding: "10px",
    marginTop: "6px",
    borderRadius: "10px",
    border: "none",
    background: "#f1f5f9",
    outline: "none"
  },

  button: {
    marginTop: "15px",
    width: "100%",
    padding: "12px",
    background: "#020617",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    fontWeight: "600",
    cursor: "pointer"
  }
};

export default ProfileEdit;
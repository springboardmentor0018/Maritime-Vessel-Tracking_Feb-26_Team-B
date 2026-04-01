import React from "react";
import { FaBell, FaUserCircle } from "react-icons/fa";
import NotificationPanel from "./NotificationPanel";
import ProfileEdit from "./ProfileEdit";

const Header = () => {
  return (
    <div style={styles.header}>
      <h2 style={styles.title}>Dashboard</h2>

      <div style={styles.right}>
        <NotificationPanel />
        <ProfileEdit />
      </div>
    </div>
  );
};

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 25px",
    background: "#ffffff",
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
  },
  title: {
    fontWeight: "600"
  },
  right: {
    display: "flex",
    gap: "20px",
    alignItems: "center"
  }
};

export default Header;
import React, { useState } from "react";
import { FaBell } from "react-icons/fa";

const NotificationPanel = () => {
  const [open, setOpen] = useState(false);

  const [notifications, setNotifications] = useState([
    { title: "Vessel Alert", unread: true },
    { title: "Risk Warning", unread: true },
  ]);

  // count unread
  const unreadCount = notifications.filter(n => n.unread).length;

  const markAllRead = () => {
    const updated = notifications.map(n => ({ ...n, unread: false }));
    setNotifications(updated);
  };

  return (
    <div style={{ position: "relative" }}>
      
      {/* 🔔 Bell */}
      <div onClick={() => setOpen(!open)} style={{ position: "relative", cursor: "pointer" }}>
        <FaBell size={20} />

        {/* 🔴 Badge */}
        {unreadCount > 0 && (
          <span style={styles.badge}>{unreadCount}</span>
        )}
      </div>

      {/* Panel */}
      {open && (
        <div style={styles.panel}>
          
          <div style={styles.header}>
            <h4>Notifications</h4>
            <span onClick={markAllRead} style={styles.mark}>
              Mark all as read
            </span>
          </div>

          {notifications.map((n, i) => (
            <div key={i} style={styles.item}>
              <p>{n.title}</p>
              {n.unread && <div style={styles.dot}></div>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const styles = {
  badge: {
    position: "absolute",
    top: "-5px",
    right: "-8px",
    background: "black",
    color: "#fff",
    fontSize: "10px",
    padding: "2px 6px",
    borderRadius: "50%"
  },
  panel: {
    position: "absolute",
    top: "40px",
    right: 0,
    width: "280px",
    background: "#fff",
    borderRadius: "12px",
    boxShadow: "0 8px 25px rgba(0,0,0,0.1)"
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px",
    borderBottom: "1px solid #eee"
  },
  mark: {
    fontSize: "12px",
    cursor: "pointer"
  },
  item: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px"
  },
  dot: {
    width: "6px",
    height: "6px",
    background: "black",
    borderRadius: "50%"
  }
};

export default NotificationPanel;
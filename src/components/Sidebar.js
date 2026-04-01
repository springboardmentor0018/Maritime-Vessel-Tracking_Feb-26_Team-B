import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../styles/sidebar.css";

function Sidebar() {
  const location = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Live Track", path: "/map" },
    { name: "Replay", path: "/replay" },
    { name: "Vessel Tracker", path: "/vessels" },
    { name: "Port Authority", path: "/ports" },
    { name: "Admin Panel", path: "/admin" },
    { name: "Settings", path: "/settings" },
  ];

  return (
    <div className="sidebar">
      <h2>Maritime Platform</h2>

      {menuItems.map((item, index) => (
        <Link
          key={index}
          to={item.path}
          className={
            location.pathname.startsWith(item.path) ? "active" : ""
          }
        >
          {item.name}
        </Link>
      ))}
    </div>
  );
}

export default Sidebar;
import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

function Layout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>

      {/* Sidebar */}
      <Sidebar />

      {/* Page Content */}
      <div style={{ flex: 1, padding: "20px", background: "#f5f7fb" }}>
        <Outlet />
      </div>

    </div>
  );
}

export default Layout;
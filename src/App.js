import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

// Pages
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import MapPage from "./pages/MapPage";
import VesselTracker from "./pages/VesselTracker";
import VesselMap from "./pages/VesselMap";
import UserManagement from "./pages/UserManagement";
import Settings from "./pages/Settings";
import Reports from "./pages/Reports";
import ReplayPage from "./pages/ReplayPage";
import AdminPanel from "./pages/AdminPanel";
import PortAuthority from "./pages/PortAuthority";

// Components
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // ✅ SINGLE Layout (FIXED)
  const Layout = ({ children }) => {
    return (
      <div style={{ display: "flex" }}>

        {/* Sidebar */}
        <Sidebar />

        {/* Main Content Area */}
        <div style={{ flex: 1 }}>

          {/* Header (Top Bar) */}
          <Header />

          {/* Page Content */}
          <div style={{ padding: "20px" }}>
            {children}
          </div>

        </div>

      </div>
    );
  };

  return (
    <Router>
      <Routes>

        {/* Login */}
        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />

        {isLoggedIn ? (
          <>
            {/* Main Routes */}
            <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
            <Route path="/map" element={<Layout><MapPage /></Layout>} />
            <Route path="/replay" element={<Layout><ReplayPage /></Layout>} />
            <Route path="/vessels" element={<Layout><VesselTracker /></Layout>} />
            <Route path="/vessel/:id" element={<Layout><VesselMap /></Layout>} />
            <Route path="/users" element={<Layout><UserManagement /></Layout>} />
            <Route path="/admin" element={<Layout><AdminPanel /></Layout>} />
            <Route path="/settings" element={<Layout><Settings /></Layout>} />
            <Route path="/reports" element={<Layout><Reports /></Layout>} />
            <Route path="/ports" element={<Layout><PortAuthority /></Layout>} />

            {/* Default */}
            <Route path="*" element={<Navigate to="/dashboard" />} />
          </>
        ) : (
          <Route path="*" element={<Navigate to="/login" />} />
        )}

      </Routes>
    </Router>
  );
}

export default App;
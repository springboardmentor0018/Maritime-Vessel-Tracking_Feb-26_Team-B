const roleConfig = {
  admin: [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Live Track", path: "/map" },
    { name: "Vessel Tracker", path: "/vessels" },
    { name: "Port Authority", path: "/ports" },
    { name: "Insurer", path: "/insurer" },
    { name: "User Management", path: "/users" },
    { name: "Reports", path: "/reports" },
    { name: "Settings", path: "/settings" }
  ],
  analyst: [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Live Track", path: "/map" },
    { name: "Vessel Tracker", path: "/vessels" },
    { name: "Risk Analysis", path: "/risk-analysis" },
    { name: "Reports", path: "/reports" }
  ],
  operator: [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Live Track", path: "/map" },
    { name: "Vessel Tracker", path: "/vessels" },
    { name: "Alerts", path: "/alerts" },
    { name: "Port Updates", path: "/port-updates" }
  ]
};

export default roleConfig;
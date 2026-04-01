import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// ✅ Leaflet CSS (IMPORTANT for map)
import "leaflet/dist/leaflet.css";

// Optional global styles
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

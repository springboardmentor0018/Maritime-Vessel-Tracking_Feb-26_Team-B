import React, { useEffect, useState } from "react";
import MapComponent from "../components/MapComponent";

function MapPage() {
  const [vessels, setVessels] = useState([]);

  // ✅ SIMULATED BACKEND (for now)
  useEffect(() => {
    const data = [
      {
        name: "MSC Oscar",
        status: "In Port",
        speed: "0 kts",
        location: "Singapore",
        lat: 1.29,
        lng: 103.85,
      },
      {
        name: "OOCL Germany",
        status: "At Anchor",
        speed: "2 kts",
        location: "Hong Kong",
        lat: 22.3,
        lng: 114.2,
      },
    ];

    setVessels(data);
  }, []);

  return (
    <div>
      <h2>Live Tracking</h2>

      {/* ✅ PASS ALL VESSELS */}
      <MapComponent vessels={vessels} />
    </div>
  );
}

export default MapPage;
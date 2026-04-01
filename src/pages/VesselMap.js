import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import MapComponent from "../components/MapComponent";

function VesselMap() {
  const { id } = useParams();
  const [vessel, setVessel] = useState(null);

  useEffect(() => {
    // ✅ SAME DATA AS VesselTracker
    const vessels = [
      {
        imo: "IMO9321483",
        name: "MSC Oscar",
        lat: 1.29,
        lng: 103.85,
        speed: "0 kts",
        location: "Singapore",
      },
      {
        imo: "IMO9778856",
        name: "OOCL Germany",
        lat: 22.3,
        lng: 114.2,
        speed: "2 kts",
        location: "Hong Kong",
      },
    ];

    // ✅ FIND SELECTED VESSEL
    const selected = vessels.find((v) => v.imo === id);

    console.log("Selected vessel:", selected); // 🔍 DEBUG

    setVessel(selected);
  }, [id]);

  if (!vessel) return <p>Loading vessel...</p>;

  return (
    <div>
      <h2>Vessel Details</h2>
      <h3>{vessel.name}</h3>

      {/* ✅ PASS CORRECT DATA */}
      <MapComponent vessels={[vessel]} />
    </div>
  );
}

export default VesselMap;
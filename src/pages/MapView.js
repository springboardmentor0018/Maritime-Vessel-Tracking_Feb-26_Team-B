import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MapComponent from "../components/MapComponent";

function MapView() {
  const location = useLocation();
  const navigate = useNavigate();

  const defaultVessels = [
    {
      name: "MSC Oscar",
      lat: 1.3521,
      lng: 103.8198,
      status: "In Port",
      location: "Singapore",
    },
    {
      name: "OOCL Germany",
      lat: 22.3193,
      lng: 114.1694,
      status: "At Anchor",
      location: "Hong Kong",
    },
    {
      name: "Ever Given",
      lat: 30.0444,
      lng: 31.2357,
      status: "In Transit",
      location: "Suez Canal",
    },
    {
      name: "Maersk Essen",
      lat: 35.6762,
      lng: 139.6503,
      status: "In Transit",
      location: "Pacific Ocean",
    },
  ];

  const vessels = location.state?.vessels || defaultVessels;

  return (
    <div>
      <h2>Live Track</h2>

      <MapComponent vessels={vessels} />

      {/* Subscribe Button */}
      {vessels.length === 1 && (
        <button
          style={{ marginTop: "20px" }}
          onClick={() =>
            navigate("/subscription", {
              state: vessels[0],
            })
          }
        >
          Subscribe
        </button>
      )}
    </div>
  );
}

export default MapView;
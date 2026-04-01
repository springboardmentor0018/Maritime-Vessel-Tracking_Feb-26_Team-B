import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// ✅ FIX MARKER ICON ISSUE
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

function MapComponent({ vessels = [] }) {
  return (
    <MapContainer
      center={[10, 100]} // default center
      zoom={3}
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {/* ✅ MULTIPLE VESSELS */}
      {vessels.map((v, index) => (
        <Marker key={index} position={[v.lat, v.lng]}>
          <Popup>
            <b>{v.name}</b><br />
            Status: {v.status}<br />
            Speed: {v.speed}<br />
            Location: {v.location}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapComponent;
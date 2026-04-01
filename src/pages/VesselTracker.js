import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function VesselTracker() {
  const navigate = useNavigate();

  const vessels = [
    {
      imo: "IMO9321483",
      name: "MSC Oscar",
      type: "Container Ship",
      flag: "Panama",
      status: "In Port",
      location: "Singapore",
      speed: "0 kts",
      course: "N/A",
      lat: 1.29,
      lng: 103.85,
    },
    {
      imo: "IMO9778856",
      name: "OOCL Germany",
      type: "Container Ship",
      flag: "Hong Kong",
      status: "At Anchor",
      location: "Hong Kong",
      speed: "2 kts",
      course: "045°",
      lat: 22.3,
      lng: 114.2,
    },
  ];

  const [search, setSearch] = useState("");

  const filtered = vessels.filter((v) =>
    v.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h2>Vessel Tracker</h2>

      <input
        type="text"
        placeholder="Search vessel..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />

      <table width="100%">
        <thead>
          <tr>
            <th>IMO</th>
            <th>Name</th>
            <th>Type</th>
            <th>Flag</th>
            <th>Status</th>
            <th>Location</th>
            <th>Speed</th>
            <th>Course</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {filtered.map((v) => (
            <tr key={v.imo}>
              <td>{v.imo}</td>
              <td>{v.name}</td>
              <td>{v.type}</td>
              <td>{v.flag}</td>
              <td>{v.status}</td>
              <td>{v.location}</td>
              <td>{v.speed}</td>
              <td>{v.course}</td>
              <td>
                <button onClick={() => navigate(`/vessel/${v.imo}`)}>
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default VesselTracker;
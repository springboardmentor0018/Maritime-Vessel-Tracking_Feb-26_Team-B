import React from "react";

function StatsCards({ ports, alerts }) {
  const totalArrivals = ports.reduce((a, p) => a + (p.arrivals || 0), 0);
  const totalDepartures = ports.reduce((a, p) => a + (p.departures || 0), 0);

  return (
    <div className="stats">
      <div className="card">Arrivals: {totalArrivals}</div>
      <div className="card">Departures: {totalDepartures}</div>
      <div className="card">Alerts: {alerts.length}</div>
    </div>
  );
}

export default StatsCards;
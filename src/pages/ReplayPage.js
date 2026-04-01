import React, { useEffect, useState } from "react";
import MapComponent from "../components/MapComponent";

function ReplayPage() {
  const [replayData, setReplayData] = useState([]);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);

  // ✅ FETCH + SORT DATA (VERY IMPORTANT)
  useEffect(() => {
    fetch("http://localhost:8000/api/replay/IMO9321483")
      .then((res) => res.json())
      .then((data) => {
        // 🔥 SORT BY TIME
        const sorted = data.sort(
          (a, b) => new Date(a.time) - new Date(b.time)
        );
        setReplayData(sorted);
      })
      .catch(() => {
        console.log("Using fallback data");

        const fallback = [
          {
            lat: 10,
            lng: 80,
            speed: 12,
            time: "2026-03-10T10:00:00",
            name: "MSC Oscar",
          },
          {
            lat: 11,
            lng: 82,
            speed: 14,
            time: "2026-03-10T10:05:00",
            name: "MSC Oscar",
          },
          {
            lat: 12,
            lng: 85,
            speed: 13,
            time: "2026-03-10T10:10:00",
            name: "MSC Oscar",
          },
        ];

        setReplayData(fallback);
      });
  }, []);

  // ✅ REPLAY MOVEMENT (NO LOOP, NO BACKWARD)
  useEffect(() => {
    if (!playing || replayData.length === 0) return;

    const interval = setInterval(() => {
      setIndex((prev) => {
        if (prev < replayData.length - 1) {
          return prev + 1;
        } else {
          clearInterval(interval); // ✅ STOP at end
          return prev;
        }
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [playing, replayData]);

  // ✅ CURRENT POINT
  const current = replayData[index];

  return (
    <div>
      <h2>Replay</h2>

      {/* 🎮 CONTROLS */}
      <div style={{ marginBottom: "10px" }}>
        <button
          onClick={() => {
            setIndex(0);     // ✅ restart
            setPlaying(true);
          }}
        >
          ▶ Play
        </button>

        <button onClick={() => setPlaying(false)}>
          ⏸ Pause
        </button>
      </div>

      {/* 🗺️ MAP */}
      {current && (
        <MapComponent
          vessels={[
            {
              name: current.name,
              lat: current.lat,
              lng: current.lng,
              speed: current.speed,
              status: "Moving",
              location: `Lat ${current.lat}, Lng ${current.lng}`,
              time: current.time,
            },
          ]}
        />
      )}
    </div>
  );
}

export default ReplayPage;
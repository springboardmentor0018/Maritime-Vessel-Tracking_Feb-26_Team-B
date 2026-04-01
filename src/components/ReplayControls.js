import React from "react";
import "../styles/replay.css";

function ReplayControls({ current, max, onChange, onPlay, playing }) {
  return (
    <div className="controls">

      <button onClick={onPlay}>
        {playing ? "Pause" : "Play"}
      </button>

      <input
        type="range"
        min="0"
        max={max}
        value={current}
        onChange={(e) => onChange(Number(e.target.value))}
      />

      <span>{current} / {max}</span>

    </div>
  );
}

export default ReplayControls;
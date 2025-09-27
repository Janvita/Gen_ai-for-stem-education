import React from "react";
import "../styles/Zoom.css";

export default function ZoomControls({ zoom, zoomIn, zoomOut }) {
  return (
    <div className="zoom-controls">
      <button onClick={zoomIn} title="Zoom in" className="zoom-btn">+</button>
      <button onClick={zoomOut} title="Zoom out" className="zoom-btn">−</button>
    </div>
  );
}

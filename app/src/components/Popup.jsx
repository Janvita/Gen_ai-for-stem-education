
import { useState, useEffect } from "react";

function Popup({ selectedShape, onClose, zoom = 1 }) {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    if (!selectedShape || selectedShape.r) return;
    setInfo("Loading...");
    fetch("http://localhost:8001/llm/generate_info/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: selectedShape.text || "Unlabeled text" }),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => setInfo(data.info))
      .catch((error) => {
        console.error("LLM fetch error:", error);
        setInfo("Error generating info");
      });
  }, [selectedShape]);

  if (!selectedShape) return null;

  // ✅ Apply zoom only to coordinates, not to popup size
  const left =
    (selectedShape.r
      ? selectedShape.x + selectedShape.r + 10
      : selectedShape.x2 + 10) * zoom;

  const top =
    (selectedShape.r
      ? selectedShape.y - selectedShape.r / 2
      : selectedShape.y1) * zoom;

  // Redirect handler
  const handleRedirect = (e, pageNumber, circleText) => {
    e.preventDefault();
    e.stopPropagation();

    if (!pageNumber) {
      console.log("Missing navigation data:", { pageNumber });
      return;
    }

    const pageImageUrl = `/images/${pageNumber}.png`;
    let targetUrl = `/page?image=${encodeURIComponent(pageImageUrl)}`;
    if (circleText) {
      targetUrl += `&circle=${encodeURIComponent(circleText)}`;
    }

    window.open(targetUrl, "_blank", "noopener,noreferrer");
    onClose();
  };

  return (
    <div
      className="popup-box"
      onClick={(e) => e.stopPropagation()}
      style={{
        position: "absolute",
        left: `${left}px`,
        top: `${top}px`,
        zIndex: 1001,
        backgroundColor: "orange",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "10px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
        minWidth: "200px",
        transform: "scale(1)", 
      }}
    >
      {selectedShape.r ? (
        <div>
          <h4>Circle Information</h4>
          {selectedShape.page_number ? (
            <ul style={{ listStyle: "none", padding: 0 }}>
              <li style={{ marginBottom: "8px" }}>
                <strong>Page Number:</strong> {selectedShape.page_number}
              </li>
              {selectedShape.circle_text && (
                <li>
                  <strong>Circle Text:</strong> {selectedShape.circle_text}
                </li>
              )}
              <li style={{ marginTop: "5px" }}>
                <button
                  style={{
                    cursor: "pointer",
                    color: "white",
                    backgroundColor: "#007bff",
                    border: "none",
                    padding: "5px 10px",
                    borderRadius: "4px",
                  }}
                  onClick={(e) =>
                    handleRedirect(
                      e,
                      selectedShape.page_number,
                      selectedShape.circle_text
                    )
                  }
                >
                  Go to page {selectedShape.page_number}
                </button>
              </li>
            </ul>
          ) : (
            <p>No page number available for navigation.</p>
          )}
          <button
            onClick={onClose}
            style={{
              marginTop: "10px",
              padding: "5px 10px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Close
          </button>
        </div>
      ) : (
        <div>
          <h4>Detected Text</h4>
          <p>
            <strong>Text:</strong> {selectedShape.text || "Text"}
          </p>
          <p>
            <strong>Info:</strong> {info || "Click to generate info"}
          </p>
          <button
            onClick={onClose}
            style={{
              marginTop: "10px",
              padding: "5px 10px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
}

export default Popup;


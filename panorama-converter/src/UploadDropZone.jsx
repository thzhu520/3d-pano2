import React, { useState } from "react";
import "./UploadDropZone.css";

export default function UploadDropZone() {
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = async (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      const sceneName = await res.text(); // Expecting plain text like "abcd1234"
      if (sceneName.startsWith("Error")) {
        alert(sceneName);
      } else {
        // Redirect to the viewer with the generated scene
        window.location.href = `/renderer.html?scene=${sceneName}`;
      }
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`upload-zone ${dragOver ? "drag-over" : ""}`}
      onDrop={handleDrop}
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
    >
      {loading
        ? "Processing..."
        : dragOver
        ? "Release to upload"
        : "Drop your panorama here"}
    </div>
  );
}

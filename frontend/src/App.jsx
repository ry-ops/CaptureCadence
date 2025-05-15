import React, { useState, useEffect } from "react";
import ScheduleManager from "./ScheduleManager";
import axios from "axios";

export default function App() {
  const [cameras, setCameras] = useState([]);
  const [selectedCameras, setSelectedCameras] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/cameras")
      .then((res) => setCameras(res.data))
      .catch(() => alert("Failed to fetch cameras"));
  }, []);

  const toggleCamera = (id) => {
    setSelectedCameras((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Camera Manager</h1>
      <ul>
        {cameras.map((cam) => (
          <li key={cam.id}>
            <label>
              <input
                type="checkbox"
                checked={selectedCameras.includes(cam.id)}
                onChange={() => toggleCamera(cam.id)}
              />
              {cam.name || cam.id}
            </label>
          </li>
        ))}
      </ul>

      {selectedCameras.length > 0 && <ScheduleManager selectedCameras={selectedCameras} />}
    </div>
  );
}

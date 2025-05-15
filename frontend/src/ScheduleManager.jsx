import React, { useState, useEffect } from "react";
import axios from "axios";

export default function ScheduleManager({ selectedCameras }) {
  const [stillInterval, setStillInterval] = useState(10);
  const [videoCron, setVideoCron] = useState("0 * * * *");
  const [videoLength, setVideoLength] = useState(30);
  const [schedules, setSchedules] = useState([]);

  const fetchSchedules = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/schedule/list");
      setSchedules(Object.entries(res.data));
    } catch (err) {
      alert("Failed to fetch schedules");
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  const addStillSchedule = async () => {
    try {
      for (const camId of selectedCameras) {
        await axios.post("http://localhost:8000/api/schedule/still", {
          camera_id: camId,
          interval_minutes: stillInterval,
        });
      }
      fetchSchedules();
    } catch (err) {
      alert("Failed to add still schedule");
    }
  };

  const addVideoSchedule = async () => {
    try {
      for (const camId of selectedCameras) {
        await axios.post("http://localhost:8000/api/schedule/video", {
          camera_id: camId,
          cron: videoCron,
          length_sec: videoLength,
        });
      }
      fetchSchedules();
    } catch (err) {
      alert("Failed to add video schedule");
    }
  };

  const removeSchedule = async (jobId) => {
    try {
      await axios.delete(`http://localhost:8000/api/schedule/remove?job_id=${jobId}`);
      fetchSchedules();
    } catch (err) {
      alert("Failed to remove schedule");
    }
  };

  return (
    <div style={{ marginTop: 20 }}>
      <h2>Schedule Still Captures</h2>
      <label>
        Interval (minutes):
        <input
          type="number"
          value={stillInterval}
          onChange={(e) => setStillInterval(Number(e.target.value))}
          min={1}
          style={{ width: 80, marginLeft: 10 }}
        />
      </label>
      <button
        onClick={addStillSchedule}
        disabled={selectedCameras.length === 0}
        style={{ marginLeft: 10 }}
      >
        Schedule Still Capture
      </button>

      <h2 style={{ marginTop: 20 }}>Schedule Video Recordings</h2>
      <label>
        Cron Expression:
        <input
          type="text"
          value={videoCron}
          onChange={(e) => setVideoCron(e.target.value)}
          placeholder="e.g. 0 * * * *"
          style={{ width: 150, marginLeft: 10 }}
        />
      </label>
      <br />
      <label>
        Length (seconds):
        <input
          type="number"
          value={videoLength}
          onChange={(e) => setVideoLength(Number(e.target.value))}
          min={1}
          max={300}
          style={{ width: 80, marginLeft: 10 }}
        />
      </label>
      <button
        onClick={addVideoSchedule}
        disabled={selectedCameras.length === 0}
        style={{ marginLeft: 10 }}
      >
        Schedule Video Recording
      </button>

      <h2 style={{ marginTop: 20 }}>Active Schedules</h2>
      <ul>
        {schedules.length === 0 && <li>No schedules</li>}
        {schedules.map(([jobId, sched]) => (
          <li key={jobId} style={{ marginBottom: 5 }}>
            [{sched.type}] Camera: {sched.camera_id}{" "}
            {sched.type === "still"
              ? `every ${sched.interval_minutes} min`
              : `cron: ${sched.cron}, length: ${sched.length_sec}s`}{" "}
            <button onClick={() => removeSchedule(jobId)} style={{ marginLeft: 10 }}>
              Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
